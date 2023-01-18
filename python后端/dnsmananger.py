import requests
import hashlib, hmac, json, os, sys, time
from datetime import datetime

secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")

def createRecord(domain, record, type, value, line="默认"):
    service = "dnspod"
    host = "dnspod.tencentcloudapi.com"
    endpoint = "https://" + host
    action = "CreateRecord"
    version = "2021-03-23"
    algorithm = "TC3-HMAC-SHA256"
    timestamp = int(time.time())
    date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
    params = {"Domain": f"{domain}", "SubDomain": f"{record}", "RecordType": f"{type}", "RecordLine": f"{line}",
              "Value": f"{value}"}

    http_request_method = "POST"
    canonical_uri = "/"
    canonical_querystring = ""
    ct = "application/json; charset=utf-8"
    payload = json.dumps(params)
    canonical_headers = "content-type:%s\nhost:%s\n" % (ct, host)
    signed_headers = "content-type;host"
    hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    canonical_request = (http_request_method + "\n" +
                         canonical_uri + "\n" +
                         canonical_querystring + "\n" +
                         canonical_headers + "\n" +
                         signed_headers + "\n" +
                         hashed_request_payload)

    # ************* 步骤 2：拼接待签名字符串 *************
    credential_scope = date + "/" + service + "/" + "tc3_request"
    hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    string_to_sign = (algorithm + "\n" +
                      str(timestamp) + "\n" +
                      credential_scope + "\n" +
                      hashed_canonical_request)

    # ************* 步骤 3：计算签名 *************
    # 计算签名摘要函数
    def sign(key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    secret_date = sign(("TC3" + secret_key).encode("utf-8"), date)
    secret_service = sign(secret_date, service)
    secret_signing = sign(secret_service, "tc3_request")
    signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

    # ************* 步骤 4：拼接 Authorization *************
    authorization = (algorithm + " " +
                     "Credential=" + secret_id + "/" + credential_scope + ", " +
                     "SignedHeaders=" + signed_headers + ", " +
                     "Signature=" + signature)

    # print('curl -X POST ' + endpoint
    #       + ' -H "Authorization: ' + authorization + '"'
    #       + ' -H "Content-Type: application/json; charset=utf-8"'
    #       + ' -H "Host: ' + host + '"'
    #       + ' -H "X-TC-Action: ' + action + '"'
    #       + ' -H "X-TC-Timestamp: ' + str(timestamp) + '"'
    #       + ' -H "X-TC-Version: ' + version + '"'
    #       + " -d '" + payload + "'")
    headers = {"Authorization": authorization, "Content-Type": "application/json; charset=utf-8", "Host": host,
               "X-TC-Action": action, "X-TC-Timestamp": str(timestamp), "X-TC-Version": version}

    req = requests.post(url=endpoint, data=payload, headers=headers).text
    print(req)



def queryRecord(domain, record, type):
    service = "dnspod"
    host = "dnspod.tencentcloudapi.com"
    endpoint = "https://" + host
    action = "DescribeRecordList"
    version = "2021-03-23"
    algorithm = "TC3-HMAC-SHA256"
    timestamp = int(time.time())
    date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
    params = {"Domain": f"{domain}", "SubDomain": f"{record}", "RecordType": f"{type}"}

    http_request_method = "POST"
    canonical_uri = "/"
    canonical_querystring = ""
    ct = "application/json; charset=utf-8"
    payload = json.dumps(params)
    canonical_headers = "content-type:%s\nhost:%s\n" % (ct, host)
    signed_headers = "content-type;host"
    hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    canonical_request = (http_request_method + "\n" +
                         canonical_uri + "\n" +
                         canonical_querystring + "\n" +
                         canonical_headers + "\n" +
                         signed_headers + "\n" +
                         hashed_request_payload)

    # ************* 步骤 2：拼接待签名字符串 *************
    credential_scope = date + "/" + service + "/" + "tc3_request"
    hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    string_to_sign = (algorithm + "\n" +
                      str(timestamp) + "\n" +
                      credential_scope + "\n" +
                      hashed_canonical_request)

    # ************* 步骤 3：计算签名 *************
    # 计算签名摘要函数
    def sign(key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    secret_date = sign(("TC3" + secret_key).encode("utf-8"), date)
    secret_service = sign(secret_date, service)
    secret_signing = sign(secret_service, "tc3_request")
    signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

    # ************* 步骤 4：拼接 Authorization *************
    authorization = (algorithm + " " +
                     "Credential=" + secret_id + "/" + credential_scope + ", " +
                     "SignedHeaders=" + signed_headers + ", " +
                     "Signature=" + signature)

    # print('curl -X POST ' + endpoint
    #       + ' -H "Authorization: ' + authorization + '"'
    #       + ' -H "Content-Type: application/json; charset=utf-8"'
    #       + ' -H "Host: ' + host + '"'
    #       + ' -H "X-TC-Action: ' + action + '"'
    #       + ' -H "X-TC-Timestamp: ' + str(timestamp) + '"'
    #       + ' -H "X-TC-Version: ' + version + '"'
    #       + " -d '" + payload + "'")
    headers = {"Authorization": authorization, "Content-Type": "application/json; charset=utf-8", "Host": host,
               "X-TC-Action": action, "X-TC-Timestamp": str(timestamp), "X-TC-Version": version}

    return requests.post(url=endpoint, data=payload, headers=headers).json()


def deleteRecord(domain, record, type):
    service = "dnspod"
    host = "dnspod.tencentcloudapi.com"
    endpoint = "https://" + host
    action = "DeleteRecord"
    version = "2021-03-23"
    algorithm = "TC3-HMAC-SHA256"
    timestamp = int(time.time())
    date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
    arr = queryRecord(domain, record, type)
    recordId = arr["Response"]["RecordList"][0]["RecordId"]

    params = {"Domain": f"{domain}", "RecordId": recordId}

    http_request_method = "POST"
    canonical_uri = "/"
    canonical_querystring = ""
    ct = "application/json; charset=utf-8"
    payload = json.dumps(params)
    canonical_headers = "content-type:%s\nhost:%s\n" % (ct, host)
    signed_headers = "content-type;host"
    hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    canonical_request = (http_request_method + "\n" +
                         canonical_uri + "\n" +
                         canonical_querystring + "\n" +
                         canonical_headers + "\n" +
                         signed_headers + "\n" +
                         hashed_request_payload)

    # ************* 步骤 2：拼接待签名字符串 *************
    credential_scope = date + "/" + service + "/" + "tc3_request"
    hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    string_to_sign = (algorithm + "\n" +
                      str(timestamp) + "\n" +
                      credential_scope + "\n" +
                      hashed_canonical_request)

    # ************* 步骤 3：计算签名 *************
    # 计算签名摘要函数
    def sign(key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    secret_date = sign(("TC3" + secret_key).encode("utf-8"), date)
    secret_service = sign(secret_date, service)
    secret_signing = sign(secret_service, "tc3_request")
    signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

    # ************* 步骤 4：拼接 Authorization *************
    authorization = (algorithm + " " +
                     "Credential=" + secret_id + "/" + credential_scope + ", " +
                     "SignedHeaders=" + signed_headers + ", " +
                     "Signature=" + signature)

    # print('curl -X POST ' + endpoint
    #       + ' -H "Authorization: ' + authorization + '"'
    #       + ' -H "Content-Type: application/json; charset=utf-8"'
    #       + ' -H "Host: ' + host + '"'
    #       + ' -H "X-TC-Action: ' + action + '"'
    #       + ' -H "X-TC-Timestamp: ' + str(timestamp) + '"'
    #       + ' -H "X-TC-Version: ' + version + '"'
    #       + " -d '" + payload + "'")
    headers = {"Authorization": authorization, "Content-Type": "application/json; charset=utf-8", "Host": host,
               "X-TC-Action": action, "X-TC-Timestamp": str(timestamp), "X-TC-Version": version}

    req = requests.post(url=endpoint, data=payload, headers=headers).text
    print(req)
