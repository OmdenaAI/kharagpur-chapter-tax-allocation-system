from flask import Flask
from flask import render_template
from flask import request
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
        data = request.form.to_dict()
        helper = HelperFunction()
        status, msg = helper.add_data(data)
        if status:
            return f"Hi {data.get('name')}! Thanks for your response!"
        else:
            return msg

    return render_template("ui.html")



if __name__ == '__main__':
    app.run()