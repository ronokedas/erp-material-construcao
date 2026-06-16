import psycopg2

try:
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        dbname='erp_material',
        user='erp_user',
        password='erp_pass_123'
    )
    cur = conn.cursor()
    
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name")
    tables = cur.fetchall()
    
    print(f'✅ Conectado com sucesso!')
    print(f'📊 Total de tabelas: {len(tables)}')
    print('')
    
    for t in tables:
        cur.execute(f"SELECT COUNT(*) FROM {t[0]}")
        count = cur.fetchone()[0]
        print(f'   ✔ {t[0]:30s} ({count} registros)')
    
    cur.close()
    conn.close()
    print('')
    print('🎯 FASE 3 - Banco de Dados CONCLUÍDA COM SUCESSO!')
    
except Exception as e:
    print(f'❌ Erro: {e}')