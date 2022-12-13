from flask import Flask
from flask import render_template
from flask import request
import pandas as pd

app = Flask(__name__)


# main method renders the Tax form
@app.route('/')
def main():
    return render_template("tax-form.html")


# tax_direction method takes input from the form submit and shows the results page
@app.route('/tax-direction/', methods=['POST', 'GET'])
def tax_direction(name=None):
    if request.method == 'POST':
        result = request.form
        json_result = result.to_dict(flat=False)
        print(json_result)

        # save in csv file
        exists = False
        # step 1 - open csv file
        data_frame = pd.read_csv("./static/data.csv")

        print("###")
        print(data_frame)
        # we can add code to check data before saving
        input = {"consent": [json_result["consent"]],
                 "email": [json_result["email"]],
                 "percent": [json_result["percent"]],
                 "domain": [json_result["domainText"]],
                 "problem": [json_result["problemText"]],
                 "location": [json_result["locationText"]],
                 "suggestion": [json_result["suggestionText"]],
                 "coordinates": [json_result["locationText"]],
                 "addr": [json_result["addr"]]
                 }
        new_data_frame = pd.DataFrame.from_dict(input, orient='columns')
        if data_frame.empty:
            final_data_frame = data_frame.append(new_data_frame)
            final_data_frame.to_csv(r'./static/data.csv', index=False)
            print("Added")
            # return "added"
        else:
            for index, row in data_frame.iterrows():
                print("$$$")
                print(row["email"])
                if str(row["email"]) == str(json_result["email"]):
                    exists = True  # Creating the Second Dataframe using dictionary

                if not exists:
                    final_data_frame = data_frame.append(new_data_frame)
                    final_data_frame.to_csv(r'./static/data.csv', index=False)
                    print("Added")
                    # return "added"
                else:
                    # data_frame.to_csv(r'./static/data.csv', index=False)
                    # return "updated"
                    result = "Given email has already entered form details!"
        return render_template("results.html", result=json_result)


if __name__ == '__main__':
    app.run()
