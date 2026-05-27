import oracledb
from config import DB_USER, DB_PASS, DB_DSN

conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
cur = conn.cursor()

print("Starting blocked update...", flush=True)
cur.execute("""
update aiops_lock_test
set status = 'BLOCKED_BY_B',
    updated_at = systimestamp
where id = 1
""")

conn.commit()
print("Blocked update finished", flush=True)
