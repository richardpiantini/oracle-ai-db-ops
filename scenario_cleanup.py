import oracledb
from config import DB_USER, DB_PASS, DB_DSN

def safe_exec(cur, sql):
    try:
        cur.execute(sql)
        print(f"OK: {sql.strip()}")
    except oracledb.DatabaseError as exc:
        err = str(exc)
        if "ORA-00942" in err:
            print(f"SKIP (not found): {sql.strip()}")
        elif "ORA-00054" in err:
            print(f"SKIP (locked): {sql.strip()}")
        else:
            raise

def main():
    conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
    cur = conn.cursor()

    safe_exec(cur, "delete from aiops_lock_test")
    safe_exec(cur, """
        insert into aiops_lock_test (id, status, updated_at)
        values (1, 'READY', systimestamp)
    """)
    safe_exec(cur, "truncate table aiops_big_table")

    conn.commit()
    cur.close()
    conn.close()
    print("Cleanup complete.")

if __name__ == "__main__":
    raise SystemExit(main())
