import oracledb
from config import DB_USER, DB_PASS, DB_DSN

conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
cur = conn.cursor()

cur.execute("""
begin
    execute immediate '
        create table aiops_big_table (
            id number,
            group_id number,
            payload varchar2(200)
        )';
exception
    when others then
        if sqlcode != -955 then raise; end if;
end;
""")

cur.execute("select count(*) from aiops_big_table")
row_count = cur.fetchone()[0]

if row_count < 50000:
    cur.execute("truncate table aiops_big_table")
    rows = [(i, i % 100, "X" * 180) for i in range(1, 50001)]
    cur.executemany(
        "insert into aiops_big_table (id, group_id, payload) values (:1, :2, :3)",
        rows,
    )
    conn.commit()
    print("Loaded aiops_big_table with 50,000 rows.")
else:
    print(f"aiops_big_table already has {row_count} rows.")

print("Running repeated full-scan style queries...")
for i in range(10):
    cur.execute("""
        select count(*)
        from aiops_big_table
        where payload like '%XXXX%'
    """)
    count_val = cur.fetchone()[0]
    print(f"Run {i + 1}: count={count_val}")

cur.close()
conn.close()
print("Bad query scenario complete. Now run tools 6, 2, and 8.")
