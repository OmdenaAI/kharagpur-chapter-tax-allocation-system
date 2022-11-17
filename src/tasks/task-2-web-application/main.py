from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

# main method renders the Tax form
@app.route('/')
def main():
    return render_template("tax-form.html")

#tax_direction method takes input from the form submit and shows the results page
@app.route('/tax-direction/', methods=['POST', 'GET'])
def tax_direction(name=None):
    if request.method == 'POST':
        result = request.form
        json_result = dict(result)
        print(json_result)
        return render_template("results.html", result=result)


if __name__ == '__main__':
    app.run()
