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

def save_to_db(file_name, mig_suc, mig_err, lkd_src_dst, src_path, dst_path):
    conn = get_conn()
    with conn:
        time_stamp = datetime.now()
        mig = (file_name, time_stamp, mig_suc, mig_err, lkd_src_dst,
               src_path, dst_path)
        _sql = ''' INSERT INTO MIGRATION(FILE_NAME,TIMESTAMP,SUCCESS,\
        ERROR,LINKED_SRC_DST,SRC_FULL_PATH,DST_FULL_PATH)\
        VALUES(?,?,?,?,?,?,?) '''
        try:
            cur = conn.cursor()
            cur.execute(_sql, mig)
            conn.commit()
        except Exception as ex:
            print ex
    conn.close()
