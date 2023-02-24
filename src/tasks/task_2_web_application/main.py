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
        temp_dict = request.form.to_dict(flat=False)
        data = request.form.to_dict()
        data["contribution"] = temp_dict['contribution']
        data["problem-statement"] = temp_dict['problem-statement']
        print(data)
        helper = HelperFunction()
        status, msg = helper.add_data(data)
        if status:
            msg= f'''Thanks {data["name"]} for sharing your Tax Details and suggesting how this should be utilized. <br>We would be sharing batch-wise results monthly for you to review our Result Dashboard.<br>
                    Meanwhile, please do share this form <a href="https://omdena-tax-evaluation.el.r.appspot.com/">TAX-Evaluation Form</a> with your Colleagues, Friends, Relatives and Loved Ones. 
                    <br> Your Outreach is the first step towards development of this Suggestive Soft Power to citizens ensuring Effective Directives reach the right people in Time.
                    To help decision makers incorporate this novel #TaxDirection within their Decision Support Systems, please share this on: <br><br> 
                    <a href="https://www.linkedin.com/"> Linkedin</a>
                    <a href="https://www.facebook.com/"> Facebook</a>
                    '''
            return render_template("user-response.html",userinput=msg)
        else:
            return render_template("user-response.html", userinput=msg)

    return render_template("ui.html")


@app.route('/admin/tax-data',methods=["GET"])
def display_tax_evaluation_data():
    if request.method == 'GET':
        helper = HelperFunction()
        status, response = helper.save_tax_data()
        if status:
            status1, html_response = helper.get_html_data(response, os.getenv("TAX_DATA_HTML_PATH"))
            if status1:

                return render_template(os.getenv("TAX_DATA_RESPONSE_FORMAT"), data=html_response)
            else:
                return render_template("user-response.html", userinput="Error in fetching data!")
        else:
            return render_template("user-response.html", userinput=response)

    return render_template("ui.html")


@app.route('/admin/user-data',methods=["GET"])
def display_user_data():
    if request.method == 'GET':
        helper = HelperFunction()
        status, response = helper.save_user_data()
        if status:
            status1, html_response = helper.get_html_data(response, os.getenv("USER_DATA_HTML_PATH"))
            if status1:

                return render_template(os.getenv("TAX_DATA_RESPONSE_FORMAT"), data=html_response)
            else:
                return "Error in fetching data!"
        else:
            return response

    return render_template("ui.html")


if __name__ == '__main__':
    app.run(debug=True)