import sqlite3
from datetime import datetime

def create_db():
    conn = sqlite3.connect('/tmp/mig.db')
    conn.execute('''CREATE TABLE MIGRATION
           (ID        INTEGER PRIMARY KEY,
           FILE_NAME  TEXT,
           TIMESTAMP  TIMESTAMP,
           SUCCESS    INT,
           ERROR      INT,
           LINKED_SRC_DST TEXT);''')
    conn.close()

def get_conn():
    try:
        conn = sqlite3.connect('/tmp/mig.db')
        return conn
    except IOError as ex:
        print ex
    return None

def save_to_db(file_name, mig_success, mig_error, linked_src_dst):
    conn = get_conn()
    with conn:
        time_stamp = datetime.now()
        mig = (file_name, time_stamp, mig_success, mig_error, linked_src_dst)
        _sql = ''' INSERT INTO MIGRATION(FILE_NAME,TIMESTAMP,SUCCESS,ERROR,LINKED_SRC_DST) VALUES(?,?,?,?,?) '''
        try:
            cur = conn.cursor()
            cur.execute(_sql, mig)
            conn.commit()
        except Exception as ex:
            print ex
    conn.close()

if __name__ == '__main__':
    create_db()
    save_to_db()
