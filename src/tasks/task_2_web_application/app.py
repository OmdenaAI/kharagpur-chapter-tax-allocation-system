from flask import Flask
from flask import render_template
from flask import request
from helper_module.helper import HelperFunction
import os

app = Flask(__name__)


# main method renders the Tax form
@app.route('/')
def main():
    return render_template("ui.html")

@app.route('/tax-from-data/',methods=["GET","POST"])
def tax_direction():
    if request.method == 'POST':
        print(request.form.to_dict())
        data = request.form.to_dict()
        helper = HelperFunction()
        status, msg = helper.add_data(data)
        if status:
            return f"Hi {data.get('name')}! Thanks for your response!"
        else:
            return msg

    return render_template("ui.html")


@app.route('/admin/tax-data',methods=["GET"])
def display_tax_evaluation_data():
    if request.method == 'GET':
        helper = HelperFunction()
        status, response = helper.save_tax_data()
        if status:
            status1, html_response = helper.get_html_data(response, os.getenv("TAX_DATA_HTML_PATH"))
            if status1:
                res_data = html_response.split("/")[-1]

                return render_template(res_data)
            else:
                return "Error in fetching data!"
        else:
            return response

    return render_template("ui.html")


@app.route('/admin/user-data',methods=["GET"])
def display_user_data():
    if request.method == 'GET':
        helper = HelperFunction()
        status, response = helper.save_user_data()
        if status:
            status1, html_response = helper.get_html_data(response, os.getenv("USER_DATA_HTML_PATH"))
            if status1:
                res_data = html_response.split("/")[-1]

                return render_template(res_data)
            else:
                return "Error in fetching data!"
        else:
            return response

    return render_template("ui.html")


if __name__ == '__main__':
    app.run()