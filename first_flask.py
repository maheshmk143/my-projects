from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/mahesh")
def mahesh():
    name="mahesh"
    return render_template("about.html",name1=name)

app.run(debug=True)