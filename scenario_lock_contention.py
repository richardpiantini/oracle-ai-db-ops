import time
import oracledb
from config import DB_USER, DB_PASS, DB_DSN

conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
cur = conn.cursor()

cur.execute("""
begin
    execute immediate '
        create table aiops_lock_test (
            id number primary key,
            status varchar2(30),
            updated_at timestamp
        )';
exception
    when others then
        if sqlcode != -955 then raise; end if;
end;
""")

cur.execute("select count(*) from aiops_lock_test where id = 1")
exists = cur.fetchone()[0]
if exists == 0:
    cur.execute("""
        insert into aiops_lock_test (id, status, updated_at)
        values (1, 'READY', systimestamp)
    """)
    conn.commit()

cur.execute("""
update aiops_lock_test
set status = 'LOCKED_BY_A',
    updated_at = systimestamp
where id = 1
""")

print("Lock holder is running", flush=True)
conn.ping()

try:
    while True:
        time.sleep(5)
        conn.ping()
except KeyboardInterrupt:
    pass
finally:
    conn.rollback()
    cur.close()
    conn.close()
