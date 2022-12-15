import psycopg2
from conf import config


def db_init():
    conn = None
    try:
        params = config()
        print("Connecting to the postgreSQL database ...")
        with psycopg2.connect(**params) as conn:

            with conn.cursor() as cursor:
                cursor.execute("SELECT version();")
                print("[INFO] PostgreSQL version : {0} ".format(cursor.fetchone()))
                conn.commit()

            with conn.cursor() as cursor:
                cursor.execute("CREATE TABLE IF NOT EXISTS t (id bigserial PRIMARY KEY, name varchar(50));")
                cursor.execute("INSERT INTO t (name) VALUES ('vasja'),('piter'),('masha');")
                conn.commit()

            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM t;")
                print(cursor.fetchall())
                conn.commit()

    except (Exception, psycopg2.DatabaseError) as _ex:
        if conn is not None:
            conn.rollback()
        print("[ERROR] {0}".format(_ex))
    finally:
        if conn is not None:
            conn.commit()
        print("[INFO] PostgreSQL connection terminated.")


if __name__ == '__main__':
    db_init()

