

from .database_nsql import DBHelper
import pandas as pd
import datetime, os
from dotenv import load_dotenv

class HelperFunction:
    def __init__(self):
        load_dotenv()

    def add_data(self, data):
        db = DBHelper()
        client, connection = db.connect()
        try:
            status, msg = db.insert_data(connection, data)
            print(status,msg)
            return status, msg

        except Exception as e:
            print("UserAdd error: ",e)
            return False, "Exception occurred while adding user data"


    def save_tax_data(self):
        db = DBHelper()
        client, connection = db.connect()
        try:
            tax_data = []

            for entry in connection.find():
                for tax_info in entry["tax_information"]:
                    for tax_entry in tax_info["tax_breakup_details"]:

                        tax_entry["username"] = entry["user_name"]
                        tax_entry["email"] = entry["email"]
                        tax_entry["financial_year"] = tax_info["financial_year"]
                        tax_entry["tax_amount"] = tax_info["tax_amount"]

                        tax_data.append(tax_entry)

            dataframe = pd.DataFrame.from_dict(tax_data)
            csv_file = "/tmp/tax-eval-data.csv"#os.path.join(os.getcwd()+"/tax-eval-data.csv")
            dataframe.to_csv(csv_file)
            print("Data saved!")

            return True, csv_file

        except Exception as e:
            print("Error: ", e)
            return False, "Error in getting tax data!"

        finally:
            client.close()

    def save_user_data(self):
        db = DBHelper()
        client, connection = db.connect()
        try:
            data = connection.find()
            dataframe = pd.DataFrame(data)
            if "tax_information" in list(dataframe.columns):
                dataframe.pop("tax_information")
            filename = "/tmp/user_data.csv"#os.path.join(os.getcwd()+"/user_data.csv")
            dataframe.to_csv(filename)
            return True, filename

        except Exception as e:
            print("Error: ", e)
            return False, "Error in getting user data!"

        finally:
            client.close()

    def get_html_data(self, csv_file, path):
        html_filename = os.path.join(os.getcwd()+path)
        # html_filename = os.path.join(os.getcwd() + path)
        print(html_filename)
        csv_data = pd.read_csv(csv_file)
        html_text = csv_data.to_html()

        with open(html_filename, 'w') as f:
            f.writelines(open(os.path.join(os.getcwd()+os.getenv("TAX_DATA_RESPONSE_FORMAT"))).readlines())
            f.write(html_text)

        #os.removedirs(os.path.join(os.getcwd() + '/tmp'))
        return True, html_filename

