import psycopg2
import psycopg2.extras

def connect_db():
    login_info = open('/var/lib/postgresql/dev/Client/database-dsn', 'r').readlines()[0]
    try:
        conn = psycopg2.connect(login_info)
    except Exception as e:
        raise e
    else:
        return conn
    return None

def close_db(conn):
    conn.commit()
    conn.close()