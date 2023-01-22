
from .database import DB
from .database_nsql import DBHelper
import pandas as pd
import datetime, os
from dotenv import load_dotenv

class HelperFunction:
    def __init__(self):
        load_dotenv()


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
            return False, "Exception occurred while adding user data"


    def get_data(self):
        db = DBHelper()
        connection = db.connect()
        try:
            status, response = self.save_tax_data(connection)
            return status, response

        except Exception as e:
            print("SaveData error: ",e)
            return False, "Exception occurred while getting user data"

    def save_tax_data(self, db):
        try:
            tax_data = []

            for entry in db.find():
                for tax_info in entry["tax_information"]:
                    for tax_entry in tax_info["tax_breakup_details"]:
                        tax_entry["username"] = entry["user_name"]
                        tax_entry["email"] = entry["email"]
                        tax_entry["financial_year"] = tax_info["financial_year"]
                        tax_entry["tax_amount"] = tax_info["tax_amount"]
                        tax_data.append(tax_entry)

            dataframe = pd.DataFrame.from_dict(tax_data)
            curdate = datetime.datetime.today()
            today = curdate.strftime("%m-%d-%Y")
            csv_file = f"tax_data-{today}.csv"
            dataframe.to_csv(csv_file)
            print("Data saved!")

            return True, csv_file

        except Exception as e:
            print("Error: ", e)
            return False, "Error in getting user data!"

    def save_user_data(self, db):
        data = db.find()
        dataframe = pd.DataFrame(data)

        dataframe.pop("tax_information")
        filename = "user_data.csv"
        dataframe.to_csv(filename)
        return True, filename



    def get_html_data(self, csv_file):
        html_filename = os.path.join(os.getcwd() + os.getenv("RESPONSE_HTML_PATH"))
        csv_data = pd.read_csv(csv_file)
        html_text = csv_data.to_html()

        with open(html_filename,'w') as f:
            f.writelines(open(os.path.join(os.getcwd()+os.getenv("TAX_DATA_RESPONSE_FORMAT"))).readlines())
            f.write(html_text)
        # csv_data.to_html(html_filename)

        return True, html_filename