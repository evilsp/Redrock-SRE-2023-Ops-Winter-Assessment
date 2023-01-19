import time

import requests.utils
from flask import *
from dnsmananger import *

app = Flask(__name__)
app.secret_key = "ebb0371f3caf5a0f8e71ecee0336e5fc5f7c65a7ae1973721ef5b0e30c326cea"

@app.route('/createRecord',methods=["POST"])
def create():
    domain = request.form["domain"]
    record = request.form["record"]
    type = request.form["type"]
    value = request.form["value"]
    createRecord(domain,record,type,value)
    return "调用创建记录API成功！<br>"

@app.route('/deleteRecord',methods=["POST"])
def delete():
    domain = request.form["domain"]
    record = request.form["record"]
    type = request.form["type"]
    deleteRecord(domain,record,type)
    return "调用删除记录API成功！<br>"

if __name__== "__main__":
    app.run(port=1432)