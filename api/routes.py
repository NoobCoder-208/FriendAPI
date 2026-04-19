from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import jwt
from datetime import datetime
import config
from src.crypto import encrypt_api_payload, encrypt_payload
from src.proto import RemoveFriend_Req_pb2
from src.byte import Encrypt_ID

router = APIRouter()

class FriendRequest(BaseModel):
    uid: str
    password: str
    friend_uid: str

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

@router.post("/add")
async def add_friend(req: FriendRequest):
    token, err = get_token(req.uid, req.password)
    if not token: raise HTTPException(status_code=400, detail=err)

    encrypted_id = Encrypt_ID(req.friend_uid)
    payload_hex = f"08a7c4839f1e10{encrypted_id}1801"
    encrypted_data = encrypt_api_payload(payload_hex)

    res = requests.post("https://clientbp.ggblueshark.com/RequestAddingFriend", 
                        data=bytes.fromhex(encrypted_data), headers=get_headers(token), verify=False)
    
    if res.status_code == 200:
        return {"status": "success", "target": req.friend_uid, "time": datetime.now().strftime("%H:%M:%S")}
    raise HTTPException(status_code=500, detail="Server Free Fire từ chối")

@router.post("/remove")
async def remove_friend(req: FriendRequest):
    token, err = get_token(req.uid, req.password)
    if not token: raise HTTPException(status_code=400, detail=err)
    
    author_uid = jwt.decode(token, options={"verify_signature": False}).get("account_id")
    
    msg = RemoveFriend_Req_pb2.RemoveFriend()
    msg.AuthorUid = int(author_uid)
    msg.TargetUid = int(req.friend_uid)
    encrypted_data = encrypt_payload(msg.SerializeToString())

    res = requests.post("https://clientbp.ggblueshark.com/RemoveFriend", 
                        data=encrypted_data, headers=get_headers(token), verify=False)
    
    if res.status_code == 200:
        return {"status": "success", "target": req.friend_uid, "time": datetime.now().strftime("%H:%M:%S")}
    raise HTTPException(status_code=500, detail="Server Free Fire từ chối")
