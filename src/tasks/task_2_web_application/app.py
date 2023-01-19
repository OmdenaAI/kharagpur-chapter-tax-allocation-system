from flask import Flask
from flask import render_template
from flask import request
from helper_module.database import DB
from helper_module.helper import HelperFunction
app = Flask(__name__)


# main method renders the Tax form
@app.route('/')
def main():
    return render_template("ui.html")

@app.route('/tax-from-data/',methods=["GET","POST"])
def tax_direction():
    if request.method == 'POST':
        print(request.form.to_dict())
        dbobj = DB()
        data = request.form.to_dict()
        helper = HelperFunction()
        status, msg = helper.add_data(dbobj, data)
        if status:
            return "Your name is " + request.form.get("name") + request.form.get("email")
        else:
            return msg

    return render_template("ui.html")



if __name__ == '__main__':
    app.run()