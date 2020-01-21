from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

@app.route('/welcome')
def welcome():
    personalmessage = "Hello World"
    return render_template('welcome.html',message=personalmessage)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug="True")
