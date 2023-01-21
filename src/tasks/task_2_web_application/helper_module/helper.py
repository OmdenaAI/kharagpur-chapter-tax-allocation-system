
from .database import DB
from .database_nsql import DBHelper

class HelperFunction:

    def add_data_sql(self, data):
        db = DB()
        connection = db.connect()
        try:
            if not db.find_user(data['email']):
                status, msg = db.insert_user_data(data, connection)

            return status, msg
        except Exception as e:
            print("UserAdd error: ",e)
            return False, "Error while adding user entry"
        finally:
            connection.close()

    def add_data(self, data):
        db = DBHelper()
        connection = db.connect()
        try:
            status, msg = db.insert_data(connection, data)
            print(status,msg)
            return status, msg

        except Exception as e:
            print("UserAdd error: ",e)
            return False, "Error while adding user entry"
        finally:
            connection.close()


