
class HelperFunction:
    def add_data(self, db, data):
        try:
            connection = db.connect()
            status, msg = db.insert_data(data, connection)
            return status, msg
        except Exception as e:
            print("UserAdd error: ",e)
            return False, "Error while adding user entry"
