import sqlite3
from datetime import datetime

def get_conn():
    try:
        conn = sqlite3.connect('mig.db')
        return conn
    except IOError as ex:
        print(ex)

    return None


def create():
    conn = sqlite3.connect('mig.db')
    print "Opened database successfully";

    conn.execute('''CREATE TABLE MIGRATION
           (ID        INTEGER PRIMARY KEY,
           FILE_NAME  TEXT,
           TIMESTAMP  TIMESTAMP,
           SUCCESS    INT,
           ERROR      INT,
           LINKED_SRC_DST TEXT);''')
    print "Table created successfully";

    conn.close()


def insert():
    conn = get_conn()

    with conn:
        for idx in range(1,10):
            file_name = 'test%s.js' % idx
            time_stamp = datetime.now()
            success = 1
            error = 0
            linked_src_dst = 'test%s.js.link' % idx
            mig = (file_name, time_stamp, success, error, linked_src_dst)

            sql = ''' INSERT INTO MIGRATION(FILE_NAME,TIMESTAMP,SUCCESS,ERROR,LINKED_SRC_DST) VALUES(?,?,?,?,?) '''

            try:
                cur = conn.cursor()
                cur.execute(sql, mig)
                conn.commit()
            except Exception as ex:
                print ex
    conn.close()

if __name__ == '__main__':
    #create()
    insert()

