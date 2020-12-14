# project: p4
# submitter: rrgeorge
# partner: none

#My data is on police shootings in the USA. It was sourced from https://corgis-edu.github.io/corgis/csv/police_shootings/
#An interesting graph could compare whether the body camera was recording the shooting if the shooting was recorded as threat level "attack" or the victim was armed 

import pandas as pd
from flask import Flask, request, jsonify
import re
import bs4

app = Flask(__name__)
# df = pd.read_csv("main.csv")
n = 0
visits = 0
a_count = 0
b_count = 0
new_html = ""

@app.route('/')
def home():
    global visits
    with open("index.html") as f:
        html = f.read()
        if visits < 10 and visits%2 == 1:
            new = re.sub(r"donate\.html\?from=A", "donate.html?from=B\" style = \"color: #8ebf42", html)
            global new_html
            new_html = new
            visits+=1
            return new
        elif visits < 10:
            visits+=1
            return html
        else:
            if a_count > b_count:
                return html
            if b_count > a_count:
                return new_html
            else:
                return html

    return

@app.route('/browse.html')
def browse():
    df = pd.read_csv("main.csv", nrows = 1000)
    cols = df.loc[:1000, ["Person.Name", "Person.Age", "Person.Gender", "Person.Race", "Incident.Date.Full", "Factors.Armed", "Factors.Threat-Level", "Factors.Fleeing", "Shooting.Body-Camera"]]
    cols.to_html("browse.html")
    html = cols.to_html()
    return "<html><h1>Browse</h1>{}<html>".format(html)

@app.route('/donate.html', methods = ['GET', 'POST'])
def donate():
    html = """
    <html>
      <body>
        <h1>We Need Your Help!</h1>

        <p>We here, at Enjoy Your Data, are ever thankful for the support that we receive from the community. However, we cannot continue to display this single data frame and collect signup emails without your help! Please donate if you appreciate our data set.</p>
      </body>
    </html>
    
    """
    ab = request.args.get('from')
    global a_count
    global b_count
    if ab == "A":
        a_count +=1
    if ab == "B":
        b_count +=1
    return html

@app.route('/email', methods = ["POST"])
def email():
    global n
    email = str(request.data, "utf-8")
    if re.match(r"^[^@]+@[^@]+\.[^@]{3}$", email): #1
        with open("emails.txt", "a+") as f: # open file in append mode
            f.write(email + "\n") # 2
            n += 1
        return jsonify("thanks, you're subscriber number {}!".format(n))
    return jsonify("Invalid email, silly! Please try again in the following format \n abcd@abcd.abc") # 3

@app.route('/api.html')
def api():
    with open("api.html") as f:
        html = f.read()
    return html

@app.route('/policecols.json')
def return_cols():
    df = pd.read_csv("main.csv", nrows = 1000)
    cols = df.loc[:1000, ["Person.Name", "Person.Age", "Person.Gender", "Person.Race", "Incident.Date.Full", "Factors.Armed", "Factors.Threat-Level", "Factors.Fleeing", "Shooting.Body-Camera"]]
    c = cols.dtypes.apply(lambda x: x.name).to_dict()
    c["Person.Age"] = "int"
    return c
    
@app.route('/police.json', methods = ['GET', 'POST'])
def police_json():
    dic = {}
    df = pd.read_csv("main.csv", nrows = 1000)
    cols = df.loc[:1000, ["Person.Name", "Person.Age", "Person.Gender", "Person.Race", "Incident.Date.Full", "Factors.Armed", "Factors.Threat-Level", "Factors.Fleeing", "Shooting.Body-Camera"]]
    req =request.args.get('Person.Gender')
    if req != None:
        cols = cols[cols['Person.Gender'] == str(req)]
        d = []
        for key, val in cols.iterrows():
            l = []
            l.append(key)
            l.append(val.to_dict())
            d.append(l)
        return jsonify(d)
            
    else:
        d = []
        for key, val in cols.iterrows():
            d.append(val.to_dict())
        return jsonify(d)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug = True) # don't change this line!