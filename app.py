from flask import Flask, request, jsonify
import requests
import jwt
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

AES_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
AES_IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
RELEASE_VERSION = "OB53"
USER_AGENT = "Dalvik/2.1.0 (Linux; U; Android 12; Pixel 6 Build/SD1A.210817.036)"
TOKEN_API = "https://jwt.chuong.qzz.io/token"

dec = ['80','81','82','83','84','85','86','87','88','89','8a','8b','8c','8d','8e','8f','90','91','92','93','94','95','96','97','98','99','9a','9b','9c','9d','9e','9f','a0','a1','a2','a3','a4','a5','a6','a7','a8','a9','aa','ab','ac','ad','ae','af','b0','b1','b2','b3','b4','b5','b6','b7','b8','b9','ba','bb','bc','bd','be','bf','c0','c1','c2','c3','c4','c5','c6','c7','c8','c9','ca','cb','cc','cd','ce','cf','d0','d1','d2','d3','d4','d5','d6','d7','d8','d9','da','db','dc','dd','de','df','e0','e1','e2','e3','e4','e5','e6','e7','e8','e9','ea','eb','ec','ed','ee','ef','f0','f1','f2','f3','f4','f5','f6','f7','f8','f9','fa','fb','fc','fd','fe','ff']
xxx = ['1','01','02','03','04','05','06','07','08','09','0a','0b','0c','0d','0e','0f','10','11','12','13','14','15','16','17','18','19','1a','1b','1c','1d','1e','1f','20','21','22','23','24','25','26','27','28','29','2a','2b','2c','2d','2e','2f','30','31','32','33','34','35','36','37','38','39','3a','3b','3c','3d','3e','3f','40','41','42','43','44','45','46','47','48','49','4a','4b','4c','4d','4e','4f','50','51','52','53','54','55','56','57','58','59','5a','5b','5c','5d','5e','5f','60','61','62','63','64','65','66','67','68','69','6a','6b','6c','6d','6e','6f','70','71','72','73','74','75','76','77','78','79','7a','7b','7c','7d','7e','7f']

_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16RemoveFriend_Req.proto\"4\n\x0cRemoveFriend\x12\x11\n\tAuthorUid\x18\x01 \x01(\x03\x12\x11\n\tTargetUid\x18\x02 \x01(\x03\x62\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'RemoveFriend_Req_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    _globals['_REMOVEFRIEND']._serialized_start = 26
    _globals['_REMOVEFRIEND']._serialized_end = 78
RemoveFriend = _globals['RemoveFriend']

def encrypt_payload(data_bytes):
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    return cipher.encrypt(pad(data_bytes, AES.block_size))

def encrypt_api_payload(hex_str):
    raw = bytes.fromhex(hex_str)
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    return cipher.encrypt(pad(raw, AES.block_size))

def Encrypt_ID(x):
    x = int(x)
    x = x / 128
    if x > 128:
        x = x / 128
        if x > 128:
            x = x / 128
            if x > 128:
                x = x / 128
                strx = int(x)
                y = (x - int(strx)) * 128
                stry = str(int(y))
                z = (y - int(stry)) * 128
                strz = str(int(z))
                n = (z - int(strz)) * 128
                strn = str(int(n))
                m = (n - int(strn)) * 128
                return dec[int(m)] + dec[int(n)] + dec[int(z)] + dec[int(y)] + xxx[int(x)]
            else:
                strx = int(x)
                y = (x - int(strx)) * 128
                stry = str(int(y))
                z = (y - int(stry)) * 128
                strz = str(int(z))
                n = (z - int(strz)) * 128
                strn = str(int(n))
                return dec[int(n)] + dec[int(z)] + dec[int(y)] + xxx[int(x)]

app = Flask(__name__)

def get_token(uid, password):
    try:
        r = requests.get(f"{TOKEN_API}?uid={uid}&password={password}", timeout=10, verify=False)
        data = r.json()
        return data.get('token'), data.get('message')
    except:
        return None, "Token API Error"

def get_headers(token):
    return {
        'Authorization': f"Bearer {token}",
        'User-Agent': USER_AGENT,
        'Content-Type': "application/x-www-form-urlencoded",
        'X-Unity-Version': "2018.4.11f1",
        'X-GA': "v1 1",
        'ReleaseVersion': RELEASE_VERSION
    }

@app.route('/add', methods=['GET'])
def add_friend():
    uid = request.args.get('uid')
    password = request.args.get('password')
    friend_uid = request.args.get('friend_uid')
    if not all([uid, password, friend_uid]):
        return jsonify({"status": "failed", "message": "Missing parameters"}), 400
    token, err = get_token(uid, password)
    if not token:
        return jsonify({"status": "failed", "message": err}), 400
    encrypted_id = Encrypt_ID(friend_uid)
    payload_hex = f"08a7c4839f1e10{encrypted_id}1801"
    encrypted_data = encrypt_api_payload(payload_hex)
    res = requests.post("https://clientbp.ggpolarbear.com/RequestAddingFriend",
                        data=encrypted_data, headers=get_headers(token), verify=False)
    return jsonify({"status": "success" if res.status_code == 200 else "failed", "code": res.status_code})

@app.route('/remove', methods=['GET'])
def remove_friend():
    uid = request.args.get('uid')
    password = request.args.get('password')
    friend_uid = request.args.get('friend_uid')
    if not all([uid, password, friend_uid]):
        return jsonify({"status": "failed", "message": "Missing parameters"}), 400
    token, err = get_token(uid, password)
    if not token:
        return jsonify({"status": "failed", "message": err}), 400
    author_uid = jwt.decode(token, options={"verify_signature": False}).get("account_id")
    msg = RemoveFriend()
    msg.AuthorUid = int(author_uid)
    msg.TargetUid = int(friend_uid)
    encrypted_data = encrypt_payload(msg.SerializeToString())
    res = requests.post("https://clientbp.ggpolarbear.com/RemoveFriend",
                        data=encrypted_data, headers=get_headers(token), verify=False)
    return jsonify({"status": "success" if res.status_code == 200 else "failed", "code": res.status_code})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
