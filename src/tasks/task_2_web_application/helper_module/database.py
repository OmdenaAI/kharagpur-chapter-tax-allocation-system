import pymysql


class DB:
    def __init__(self):
        self._host = "localhost"
        self._user = "root"
        self._password = "Conceptum@12a"
        self._database = "tax_db"

    def connect(self):
        myDB = pymysql.connect(
            host=self._host,
            user=self._user,
            password=self._password,
            database=self._database
        )
        return myDB

    def insert_data(self, data, db):
        try:
            cursor = db.cursor()
            sql = '''insert ignore into Users (name, email, gender, agegroup) values(%s, %s ,%s, %s);'''
            value = (data['name'], data['email'], data['gender'], data['age-group'])
            cursor.execute(sql, value)
            db.commit()
            cursor.close()
            print("Record saved successfully!")
            return True, "Successful"
        except Exception as e:
            print("DB ERROR: ",e)
            return False, e
