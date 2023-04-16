

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
            csv_file = "/tmp/tax-eval-data.csv"
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
            filename = "/tmp/user_data.csv"
            dataframe.to_csv(filename)
            return True, filename

        except Exception as e:
            print("Error: ", e)
            return False, "Error in getting user data!"

        finally:
            client.close()

    def get_html_data(self, csv_file, path):
        html_filename = path

        print(html_filename)
        csv_data = pd.read_csv(csv_file)
        html_text = csv_data.to_html()

        return True, html_text

    def get_cities(self):
        try:
            data = pd.read_json(os.getcwd() + "/helper_module/cities.json")
            india = data[data["iso2"]=="IN"]
            indiancities = list(india["cities"])
            citynames = [i['name'].lower() for i in indiancities[0]]
            return citynames
        except Exception as e:
            print("Exception in fetching indian cities: ",e)
            return ["others"]

    def get_domains(self):
        domainlist = ["Atmosphere",
         "Biodiversity and Ecosystems",
         "Capacity Development",
         "Chemicals and Waste",
         "Climate Action and Synergies",
         "Defense and Security",
         "Desertification, Land Degradation and Drought",
         "Disaster Risk Reduction",
         "Education",
         "Employment, Decent Work for All and Social Protection",
         "Energy",
         "Finance",
         "Financial Inclusion",
         "Food Security and Nutrition",
         "Forests and Grasslands",
         "Gender equality and women’s empowerment",
         "Green Economy",
         "Health and Population",
         "Hills and Mountains",
         "Human Rights",
         "Indicators and Bio-Markers",
         "Industry or Innovation",
         "Information for Integrated Decision-Making and Participation",
         "Institutional Frameworks and International Co-operation for Sustainable Development",
         "Longevity and Reversing Aging",
         "Multi-Stakeholder Partnerships and Voluntary Commitments",
         "National Strategies and SDG Integration",
         "Oceans and Seas",
         "Orbit Shift and Space Travel",
         "Poverty Eradication",
         "Preserving Consciousness and Preventing Cognitive Warfare",
         "Rural Development",
         "Sanitation",
         "Science",
         "Small Island Developing States",
         "Sustainable Agriculture",
         "Sustainable Cities and Human Settlements",
         "Sustainable Consumption and Production",
         "Sustainable Tourism",
         "Sustainable Transport",
         "Technical Cooperation",
         "Technology",
         "Trade & Comerce",
         "Violence and War",
         "Water",
         "Wildlife Protection"]
        domainlist.sort()
        return domainlist