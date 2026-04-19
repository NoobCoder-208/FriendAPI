from flask import Flask, request, jsonify
import requests
import jwt
import config
from src.crypto import encrypt_api_payload, encrypt_payload
from src.proto import RemoveFriend_Req_pb2
from src.byte import Encrypt_ID

app = Flask(__name__)

def get_token(uid, password):
    try:
        r = requests.get(f"{config.TOKEN_API}?uid={uid}&password={password}", timeout=10, verify=False)
        data = r.json()
        return data.get('token'), data.get('message')
    except:
        return None, "Token API Error"

def get_headers(token):
    return {
        'Authorization': f"Bearer {token}",
        'User-Agent': config.USER_AGENT,
        'Content-Type': "application/x-www-form-urlencoded",
        'X-Unity-Version': "2018.4.11f1",
        'X-GA': "v1 1",
        'ReleaseVersion': config.RELEASE_VERSION
    }

@app.route('/add', methods=['GET'])
def add_friend():
    uid = request.args.get('uid')
    password = request.args.get('password')
    friend_uid = request.args.get('friend_uid')

    if not all([uid, password, friend_uid]):
        return jsonify({"status": "failed", "message": "Missing parameters"}), 400

    token, err = get_token(uid, password)
    if not token: return jsonify({"status": "failed", "message": err}), 400

    encrypted_id = Encrypt_ID(friend_uid)
    payload_hex = f"08a7c4839f1e10{encrypted_id}1801"
    encrypted_data = encrypt_api_payload(payload_hex)

    res = requests.post("https://clientbp.ggblueshark.com/RequestAddingFriend", 
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
    if not token: return jsonify({"status": "failed", "message": err}), 400
    
    author_uid = jwt.decode(token, options={"verify_signature": False}).get("account_id")
    
    msg = RemoveFriend_Req_pb2.RemoveFriend()
    msg.AuthorUid = int(author_uid)
    msg.TargetUid = int(friend_uid)
    encrypted_data = encrypt_payload(msg.SerializeToString())

    res = requests.post("https://clientbp.ggblueshark.com/RemoveFriend", 
                        data=encrypted_data, headers=get_headers(token), verify=False)
    
    return jsonify({"status": "success" if res.status_code == 200 else "failed", "code": res.status_code})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
