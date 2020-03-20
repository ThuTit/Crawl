import pymysql.cursors
import psycopg2



class DbConnect:
    def __init__(self, db_connection):
        self.host = db_connection["host"]
        self.dbname = db_connection["dbname"]
        self.username = db_connection["user"]
        self.password = db_connection["password"]
        self.port = int(db_connection["port"])
        self.engine = db_connection["engine"]

    def get_connection(self):
        if self.engine == "mysql":
            connection = pymysql.connect(database=self.dbname,
                                         user=self.username,
                                         password=self.password,
                                         host=self.host,
                                         port=self.port,
                                         cursorclass=pymysql.cursors.DictCursor
                                         )
        elif self.engine == "postgres":
            connection = psycopg2.connect(database=self.dbname,
                                          user=self.username,
                                          password=self.password,
                                          host=self.host,
                                          port=self.port)
        connection.commit()
        return connection

    def get_one_data(self, sql):
        db = self.get_connection()
        cursor = db.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        return row

    def get_all_data(self, sql):
        db = self.get_connection()
        cursor = db.cursor()
        cursor.execute(sql)
        row = cursor.fetchall()
        return row

    # def get_all_in_list(self, sql):
    #     db = self.get_connection()
    #     cursor = db.cursor()
    #     cursor.execute(sql)
    #     row = cursor.fetchall()
    #     return [list(i[0]) for i in row]

    def execute_query(self, sql):
        db = self.get_connection()
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        return

    def close_db(self):
        db = self.get_connection()
        cursor = db.cursor()
        cursor.close()

if __name__ == '__main__':
    from settings import db_connection_test1
    db = DbConnect(db_connection_test1)
    data = db.get_one_data('select * from shops;')
    print(data)
