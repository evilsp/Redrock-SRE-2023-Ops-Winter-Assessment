import time

import requests.utils
from flask import *
from dnsmananger import *

app = Flask(__name__)
app.secret_key = "y4589rhweoifsn98yheowifansd8y5423rwiejf4805y23rwpeijfa93u20rpqwjo532u90rw"

@app.route('/createRecord',methods=["POST"])
def create():
    domain = request.form["domain"]
    record = request.form["record"]
    type = request.form["type"]
    value = request.form["value"]
    createRecord(domain,record,type,value)
    return "调用API成功！<br>"

@app.route('/deleteRecord',methods=["POST"])
def delete():
    domain = request.form["domain"]
    record = request.form["record"]
    type = request.form["type"]
    deleteRecord(domain,record,type)
    return "调用API成功！<br>"

if __name__== "__main__":
    app.run(port=1432)