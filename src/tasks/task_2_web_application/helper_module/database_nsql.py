import pymongo,pprint, time
import json


class DBHelper:
    def __init__(self):

        self.username = "root"
        self.password = "omdena@project"

    def getDB(self):
        client = pymongo.MongoClient(
            "mongodb+srv://{}:{}@omdena-kc.r4ako8u.mongodb.net/?retryWrites=true&w=majority".format(self.username, self.password))
        db = client["TaxEvaluation"]
        collection = db["TaxEvaluationData"]
        return collection

    def insert_data(self, db, data):
        try:
            status, msg, input_data = self.find_user(db, data['email'])
            if not status:
                input_data = json.load(open("structure.json"))
                input_data["user_name"] = data["name"]
                input_data["email"] = data["email"]
                input_data["age_group"] = data["age-group"]
                input_data["gender"] = data["gender"]
                input_data["tax_information"][0]["financial_year"] =data["tax-year"]
                input_data["tax_information"][0]["tax_amount"] =data["tax-amount"]
                input_data["tax_information"][0]["tax_breakup_details"][0]["percentage_distribution"] = data["contribution"]
                input_data["tax_information"][0]["tax_breakup_details"][0]["problem_statement"] = data["problem-statement"]

                temp = db.insert_one(input_data)
                print("UserAdded: ", {data["name"]})

                if temp.inserted_id:
                    return True, "User Added Successfully"
                else:
                    return False, "Error: while adding user!"

            else:
                financial_yr_data = db.find({},{"email":data["email"],"financial_year":data["tax-year"]})
                if financial_yr_data:
                    return False, "UserData for given financial year is already present!"
                else:
                    tax_data_node = {
                        "financial_year":data["tax-year"],
                        "tax_amount":data["tax-amount"],
                        "tax_breakup_details":data["problem-statement"],
                        "percentage_contribution":data["contribution"]
                    }

                    new_tax_data = input_data["tax_information"].append(tax_data_node)
                    res = db.update_one({"email":data["email"]}, {"$set":new_tax_data})
                    if res.modified_count:
                        return True, "User Added updated successfully"
                    else:
                        return False, "Error: while updating user!"

        except Exception as e:
            print("AddUserError: ",e)
            return False, "Encountered error while adding user!"


    def find_user(self, db, user_mail):

        try:
            temp = db.find_one({"email": user_mail})
            # pprint.pprint(temp)
            if temp:
                return True, "User Found", temp
            else:
                return False, "User not found", {}

        except Exception as e:
            print("SearchUserError: ", e)
            return False, "Error Occured!", {}







