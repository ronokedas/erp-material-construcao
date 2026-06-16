"""
Serviço de geração de PDF profissional para Orçamentos
Usa ReportLab para gerar PDF de alta qualidade sem dependências externas
"""
from io import BytesIO
from datetime import datetime
from decimal import Decimal
from typing import Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.units import mm

from app.models.movimento_models import Orcamento
from app.models.auth_models import Usuario
from app.models.sistema_models import Empresa


def _fmt_currency(value: Decimal) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _fmt_date(dt) -> str:
    if dt is None:
        return ""
    if hasattr(dt, "strftime"):
        return dt.strftime("%d/%m/%Y")
    return str(dt)


def _fmt_datetime(dt) -> str:
    if dt is None:
        return ""
    if hasattr(dt, "strftime"):
        return dt.strftime("%d/%m/%Y %H:%M")
    return str(dt)


def _build_endereco(obj) -> str:
    if not obj:
        return ""
    parts = []
    if getattr(obj, "endereco", None):
        addr = obj.endereco
        if getattr(obj, "numero", None):
            addr += f", {obj.numero}"
        parts.append(addr)
    if getattr(obj, "bairro", None):
        parts.append(obj.bairro)
    if getattr(obj, "cidade", None):
        city = obj.cidade
        if getattr(obj, "estado", None):
            city += f" - {obj.estado}"
        parts.append(city)
    return " - ".join(parts)


def gerar_pdf_orcamento(
    orcamento: Orcamento,
    empresa: Optional[Empresa],
    usuario: Usuario,
) -> bytes:
    """Gera PDF profissional do orçamento usando ReportLab."""
    import os
    os.environ['RENDER_HOURGLASS'] = 'false'

    buf = BytesIO()

    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
    )

    styles = getSampleStyleSheet()
    story = []

    # Styles customizados
    style_title = ParagraphStyle(
        'Title', parent=styles['Title'],
        fontSize=22, textColor=colors.HexColor('#1e293b'),
        spaceAfter=2, spaceBefore=0
    )
    style_subtitle = ParagraphStyle(
        'Subtitle', parent=styles['Normal'],
        fontSize=10, textColor=colors.HexColor('#64748b'),
        spaceAfter=0, spaceBefore=0
    )
    style_normal = ParagraphStyle(
        'NormalP', parent=styles['Normal'],
        fontSize=9, leading=12, spaceAfter=2, spaceBefore=0
    )
    style_small = ParagraphStyle(
        'SmallP', parent=styles['Normal'],
        fontSize=8, leading=10, textColor=colors.HexColor('#64748b'),
        spaceAfter=1, spaceBefore=0
    )
    style_header_table = ParagraphStyle(
        'HeaderTable', parent=styles['Normal'],
        fontSize=7, textColor=colors.white, alignment=TA_CENTER
    )
    style_cell = ParagraphStyle(
        'Cell', parent=styles['Normal'],
        fontSize=8, leading=11, spaceAfter=0, spaceBefore=0
    )
    style_cell_right = ParagraphStyle(
        'CellRight', parent=style_cell,
        alignment=TA_RIGHT
    )
    style_cell_center = ParagraphStyle(
        'CellCenter', parent=style_cell,
        alignment=TA_CENTER
    )
    style_footer = ParagraphStyle(
        'Footer', parent=styles['Normal'],
        fontSize=7, textColor=colors.HexColor('#94a3b8'),
        alignment=TA_CENTER, spaceBefore=10
    )

    # Dados
    cliente = orcamento.cliente
    itens = orcamento.itens

    empresa_nome = empresa.nome if empresa else "Empresa"
    empresa_cnpj = empresa.cnpj if empresa else ""
    empresa_endereco = _build_endereco(empresa)
    empresa_telefone = empresa.telefone if empresa else ""
    empresa_email = empresa.email if empresa else ""

    cliente_nome = cliente.nome if cliente else "Cliente não informado"
    cliente_cpf_cnpj = cliente.cpf_cnpj if cliente else ""
    cliente_endereco = _build_endereco(cliente)
    cliente_telefone = cliente.telefone if cliente else ""
    cliente_email = cliente.email if cliente else ""

    status_map = {
        "ativo": "Ativo",
        "convertido": "Convertido em Venda",
        "vencido": "Vencido",
        "cancelado": "Cancelado",
    }
    status_texto = status_map.get(orcamento.status, orcamento.status)

    # ---- HEADER ----
    header_data = [[
        Paragraph(f"<b>{empresa_nome}</b>", style_title),
        Paragraph(
            f"<b>ORÇAMENTO</b><br/>"
            f"<font size='10' color='#475569'>Nº {orcamento.numero_orcamento}</font>",
            ParagraphStyle('RightHeader', parent=style_normal, alignment=TA_RIGHT, fontSize=14)
        )
    ]]
    header_table = Table(header_data, colWidths=[330, 200])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 2))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1e293b')))
    story.append(Spacer(1, 8))

    # ---- INFO SECTIONS ----
    info_style = TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ])

    info_data = [[
        # Empresa
        Paragraph(
            f"<b>EMPRESA</b><br/>"
            f"<font size='9'>{empresa_nome}</font><br/>"
            f"<font size='8' color='#64748b'>CNPJ: {empresa_cnpj}</font><br/>"
            f"<font size='8' color='#64748b'>{empresa_endereco}</font><br/>"
            f"<font size='8' color='#64748b'>Tel: {empresa_telefone}</font>",
            style_small
        ),
        # Cliente
        Paragraph(
            f"<b>CLIENTE</b><br/>"
            f"<font size='9'>{cliente_nome}</font><br/>"
            f"<font size='8' color='#64748b'>CPF/CNPJ: {cliente_cpf_cnpj}</font><br/>"
            f"<font size='8' color='#64748b'>{cliente_endereco}</font><br/>"
            f"<font size='8' color='#64748b'>Tel: {cliente_telefone}</font>",
            style_small
        ),
        # Detalhes
        Paragraph(
            f"<b>DETALHES</b><br/>"
            f"<font size='9'><b>Status:</b> {status_texto}</font><br/>"
            f"<font size='8' color='#64748b'>Data: {_fmt_datetime(orcamento.data_orcamento)}</font><br/>"
            f"<font size='8' color='#64748b'>Validade: {_fmt_date(orcamento.data_validade)}</font><br/>"
            f"<font size='8' color='#64748b'>Resp: {usuario.nome}</font>",
            style_small
        ),
    ]]
    info_table = Table(info_data, colWidths=[180, 180, 170])
    info_table.setStyle(info_style)
    story.append(info_table)
    story.append(Spacer(1, 10))

    # ---- TABELA DE ITENS ----
    header_color = colors.HexColor('#1e293b')
    border_color = colors.HexColor('#e2e8f0')
    alt_color = colors.HexColor('#f8fafc')

    table_data = [
        [
            Paragraph("<b>#</b>", style_header_table),
            Paragraph("<b>PRODUTO</b>", style_header_table),
            Paragraph("<b>QTD</b>", style_header_table),
            Paragraph("<b>PREÇO UNIT.</b>", style_header_table),
            Paragraph("<b>DESCONTO</b>", style_header_table),
            Paragraph("<b>SUBTOTAL</b>", style_header_table),
        ]
    ]

    for i, item in enumerate(itens, 1):
        table_data.append([
            Paragraph(str(i), style_cell_center),
            Paragraph(f"Produto #{item.produto_id}", style_cell),
            Paragraph(f"{item.quantidade:,.3f}", style_cell_center),
            Paragraph(_fmt_currency(item.preco_unitario), style_cell_right),
            Paragraph(_fmt_currency(item.desconto_item), style_cell_right),
            Paragraph(_fmt_currency(item.subtotal_item), style_cell_right),
        ])

    # Definir larguras das colunas
    col_widths = [25, 230, 55, 80, 70, 80]
    items_table = Table(table_data, colWidths=col_widths, repeatRows=1)

    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), header_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]

    # Alternar cores das linhas
    for i in range(1, len(table_data)):
        if i % 2 == 0:
            table_style.append(('BACKGROUND', (0, i), (-1, i), alt_color))

    items_table.setStyle(TableStyle(table_style))
    story.append(items_table)
    story.append(Spacer(1, 10))

    # ---- TOTAIS ----
    total_style = TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 0.5, border_color),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, border_color),
    ])

    total_data = [
        [Paragraph("Subtotal", style_cell), Paragraph(_fmt_currency(orcamento.subtotal), style_cell_right)],
        [Paragraph("Desconto", style_cell), Paragraph(_fmt_currency(orcamento.desconto), style_cell_right)],
        [
            Paragraph("<b>Total</b>", ParagraphStyle('TotalLabel', parent=style_cell, fontSize=11, textColor=colors.white)),
            Paragraph(f"<b>{_fmt_currency(orcamento.total)}</b>", ParagraphStyle('TotalVal', parent=style_cell_right, fontSize=11, textColor=colors.white))
        ],
    ]

    totals_table = Table(total_data, colWidths=[160, 120])
    totals_table.setStyle(total_style)
    totals_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 2), (-1, 2), header_color),
        ('LINEABOVE', (0, 2), (-1, 2), 1, header_color),
    ]))

    # Alinhar à direita
    totals_wrapper = Table([[totals_table]], colWidths=[540])
    totals_wrapper.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
    ]))
    story.append(totals_wrapper)

    # ---- OBSERVAÇÃO ----
    if orcamento.observacao:
        story.append(Spacer(1, 8))
        obs_data = [[
            Paragraph(
                f"<b>Observação:</b> {orcamento.observacao}",
                ParagraphStyle('Obs', parent=style_normal, fontSize=8, textColor=colors.HexColor('#475569'))
            )
        ]]
        obs_table = Table(obs_data, colWidths=[540])
        obs_table.setStyle(TableStyle([
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
            ('LINELEFT', (0, 0), (-1, -1), 3, header_color),
            ('BOX', (0, 0), (-1, -1), 0.5, border_color),
        ]))
        story.append(obs_table)

    # ---- FOOTER ----
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5, color=border_color))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        f"Documento gerado em {_fmt_datetime(datetime.now())} por {usuario.nome} | "
        f"Este é um orçamento informativo. Os preços e condições são válidos até a data de validade indicada.",
        style_footer
    ))

    # Gerar PDF
    doc.build(story)
    buf.seek(0)
    return buf.getvalue()