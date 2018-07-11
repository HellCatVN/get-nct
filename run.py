from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():  
    return render_template('index.html')

@app.route("/hello")
def hello():  
    return "Hello World!"

@app.route("/hello/<string:name>/")
def hello_user(name):  
    return render_template('hello.html', name=name)

if __name__ == "__main__":  
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()