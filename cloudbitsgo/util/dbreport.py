import sqlite3
from datetime import datetime
from os.path import exists


def create_db():
    if not exists('/tmp/mig.db'):
        conn = sqlite3.connect('/tmp/mig.db')
        conn.execute('''CREATE TABLE MIGRATION
               (ID            INTEGER PRIMARY KEY,
               FILE_NAME      TEXT,
               TIMESTAMP      TIMESTAMP,
               MIG_SUCCESS    INT,
               MIG_ERROR      INT,
               LINKED_SRC_DST TEXT,
               SRC_FULL_PATH  TEXT,
               DST_FULL_PATH  TEXT,
               ERROR_MSG      TEXT);''')
        conn.close()


def get_conn():
    try:
        conn = sqlite3.connect('/tmp/mig.db')
        return conn
    except IOError as ex:
        print ex
    return None


def save_to_db(file_name, mig_suc, mig_err, lkd_src_dst,
               src_path, dst_path, err_msg):
    conn = get_conn()
    with conn:
        time_stamp = datetime.now()
        mig = (file_name, time_stamp, mig_suc, mig_err, lkd_src_dst,
               src_path, dst_path, str(err_msg))
        _sql = ''' INSERT INTO MIGRATION(FILE_NAME,TIMESTAMP,MIG_SUCCESS,\
        MIG_ERROR,LINKED_SRC_DST,SRC_FULL_PATH,DST_FULL_PATH,ERROR_MSG)\
        VALUES(?,?,?,?,?,?,?,?) '''
        try:
            cur = conn.cursor()
            cur.execute(_sql, mig)
            conn.commit()
        except Exception as ex:
            print ex
    conn.close()
