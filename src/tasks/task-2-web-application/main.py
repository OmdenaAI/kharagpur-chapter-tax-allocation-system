from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/tax-direction/')
@app.route('/tax-direction/<name>')
def tax_direction(name=None):
    return render_template('tax-form.html', name=name)


if __name__ == '__main__':
    app.run()
