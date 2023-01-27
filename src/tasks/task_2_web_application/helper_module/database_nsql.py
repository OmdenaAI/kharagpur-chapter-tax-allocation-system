import pymongo,pprint
import json, urllib, os
from dotenv import load_dotenv
import pandas as pd


class DBHelper:
    def __init__(self):
        load_dotenv()

        print( os.getenv("DB_USERNAME"))
        self.username = os.getenv("DB_USERNAME")
        self.password = os.getenv("DB_PASSWORD")

    def connect(self):
        client = pymongo.MongoClient(
            os.getenv("MONGO_CLIENT").format(self.username, urllib.parse.quote(self.password)))
        db = client["TaxEvaluation"]
        collection = db["TaxEvaluationData"]
        return client, collection

    def insert_data(self, db, data):
        try:
            status, msg, input_data = self.find_user(db, data['email'])
            if not status:
                #print(os.path.join(os.getcwd()+ "structure.json"))
                input_data = json.load(open(os.path.join(os.getcwd()+ os.getenv("JSON_STRUCTURE_PATH"))))
                input_data["user_name"] = data["name"]
                input_data["email"] = data["email"]
                input_data["age_group"] = data["age-group"]
                input_data["gender"] = data["gender"]
                input_data["tax_information"][0]["financial_year"] =data["tax-year"]
                input_data["tax_information"][0]["tax_amount"] =data["tax-amount"]


                tax_entry_data = {"percentage_contribution":data["contribution"],
                 "problem_statement": data["problem-statement"]}

                input_data["tax_information"][0]["tax_breakup_details"].append(tax_entry_data)

                temp = db.insert_one(input_data)
                print("UserAdded: ", {data["name"]})

                if temp.inserted_id:
                    return True, "User Added Successfully"
                else:
                    return False, "Error: while adding user!"

            else:
                financial_yr_data = list(db.aggregate([{"$unwind":"$tax_information"},{"$match":{"email":data["email"],"tax_information.financial_year":data["tax-year"]}}]))
                if len(financial_yr_data)>0:
                    return False, "UserData for given financial year is already present!"
                else:

                    tax_entry_data = {"percentage_contribution":data["contribution"],
                            "problem_statement": data["problem-statement"]}
                    tax_data_node = {
                        "financial_year": data["tax-year"],
                        "tax_amount": data["tax-amount"],
                        "tax_breakup_details": [tax_entry_data]
                    }


                    new_tax_data = list(input_data["tax_information"])
                    new_tax_data.append(tax_data_node)
                    res = db.update_one({"email":data["email"]}, {"$set":{"tax_information":new_tax_data}})
                    if res.modified_count:
                        return True, "User updated successfully"
                    else:
                        return False, "Error: while updating user!"

        except Exception as e:
            print("AddUserError: ",e)
            return False, "Encountered error while adding user!"


    def find_user(self, db, user_mail):

        try:
            temp = db.find_one({"email": user_mail})
            if temp:
                pprint.PrettyPrinter(indent=3).pprint(temp)
                return True, "User Found", temp
            else:
                return False, "User not found", {}

        except Exception as e:
            print("SearchUserError: ", e)
            return False, "Error Occured!", {}



#
# if __name__ == '__main__':
#     db = DBHelper()
#     conn = db.connect()
#     i=1
#     for k in conn.find():
#         if i>10:
#             conn.remove()
#         i+=1
#     data = conn.find({})
# #
# #     # data = list(conn.aggregate([{"$unwind":"$tax_information"},{"$match":{"email":"neelam@gmail.com","tax_information.financial_year":"2020-2022"}}]))
# #     # print(data)
# #     # if len(data)>0:
# #     #     print("yes")
#     for i in data:
#         pprint.PrettyPrinter(indent=3).pprint(i)
    #db.save_user_data(conn)
