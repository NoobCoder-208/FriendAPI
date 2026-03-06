# JOIN @VAIBHAVAPI, VAIBHAVAPIS

from flask import Flask, request, jsonify
import sys
import jwt
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import RemoveFriend_Req_pb2
from byte import Encrypt_ID, encrypt_api
import binascii
import data_pb2
import uid_generator_pb2
import my_pb2
import output_pb2
from datetime import datetime
import json
import time
import urllib3
import warnings

# -----------------------------
# Security Warnings Disable
# -----------------------------
# HTTPS warnings disable karo
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore", category=UserWarning, message="Unverified HTTPS request")

app = Flask(__name__)

# -----------------------------
# AES Configuration
# -----------------------------
AES_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
AES_IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

def encrypt_message(data_bytes):
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    return cipher.encrypt(pad(data_bytes, AES.block_size))

def encrypt_message_hex(data_bytes):
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    encrypted = cipher.encrypt(pad(data_bytes, AES.block_size))
    return binascii.hexlify(encrypted).decode('utf-8')

# -----------------------------
# Region-based URL Configuration
# -----------------------------
def get_base_url(server_name):
    server_name = server_name.upper()
    if server_name == "IND":
        return "https://client.ind.freefiremobile.com/"
    elif server_name in {"BR", "US", "SAC", "NA"}:
        return "https://client.us.freefiremobile.com/"
    else:
        return "https://clientbp.ggblueshark.com/"

def get_server_from_token(token):
    """Extract server region from JWT token"""
    try:
        decoded = jwt.decode(token, options={"verify_signature": False})
        lock_region = decoded.get("lock_region", "IND")
        return lock_region.upper()
    except:
        return "IND"

# -----------------------------
# Retry Decorator - 10 baar try karega
# -----------------------------
def retry_operation(max_retries=10, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    result = func(*args, **kwargs)
                    if result and result.get('status') in ['success', 'failed']:
                        return result
                    # Agar result nahi aaya toh retry karo
                    print(f"Attempt {attempt + 1}/{max_retries} failed, retrying...")
                except Exception as e:
                    last_exception = e
                    print(f"Attempt {attempt + 1}/{max_retries} failed with error: {str(e)}")
                
                if attempt < max_retries - 1:
                    time.sleep(delay)
            
            # Agar 10 baar mein bhi fail hua toh last error return karo
            if last_exception:
                return {
                    "status": "error",
                    "message": f"All {max_retries} attempts failed",
                    "error": str(last_exception)
                }
            return {
                "status": "error", 
                "message": f"All {max_retries} attempts failed"
            }
        return wrapper
    return decorator

# -----------------------------
# JWT Token Generation - Using External API
# -----------------------------
def get_token_from_uid_password(uid, password):
    """Get JWT token using external API"""
    try:
        url = f"https://jwt-genall.vercel.app/token?uid={uid}&password={password}"
        response = requests.get(url, timeout=10, verify=False)
        response.raise_for_status()
        
        data = response.json()
        
        # Check status_code or error field
        if data.get('status_code') == 200 and not data.get('error') and 'token' in data:
            return data['token'], None
        else:
            return None, data.get('message', 'Failed to generate token')
            
    except requests.RequestException as e:
        return None, f"Token API request failed: {str(e)}"
    except ValueError:
        return None, "Invalid JSON response from token API"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

# -----------------------------
# Player Info Functions
# -----------------------------
def create_info_protobuf(uid):
    message = uid_generator_pb2.uid_generator()
    message.saturn_ = int(uid)
    message.garena = 1
    return message.SerializeToString()

def get_player_info(target_uid, token, server_name=None):
    """Get detailed player information"""
    try:
        if not server_name:
            server_name = get_server_from_token(token)
            
        protobuf_data = create_info_protobuf(target_uid)
        encrypted_data = encrypt_message_hex(protobuf_data)
        endpoint = get_base_url(server_name) + "GetPlayerPersonalShow"

        headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Authorization': f"Bearer {token}",
            'Content-Type': "application/x-www-form-urlencoded",
            'Expect': "100-continue",
            'X-Unity-Version': "2018.4.11f1",
            'X-GA': "v1 1",
            'ReleaseVersion': "OB52"
        }

        response = requests.post(endpoint, data=bytes.fromhex(encrypted_data), headers=headers, verify=False)
        
        if response.status_code != 200:
            return None

        hex_response = response.content.hex()
        binary = bytes.fromhex(hex_response)
        
        info = data_pb2.AccountPersonalShowInfo()
        info.ParseFromString(binary)
        
        return info
    except Exception as e:
        print(f"Error getting player info: {e}")
        return None

def extract_player_info(info_data):
    """Extract player information from protobuf response including friends count"""
    if not info_data:
        return None

    basic_info = info_data.basic_info
    
    # Friends count extract karo
    friends_count = 0
    try:
        # Check if friends field exists in protobuf
        if hasattr(info_data, 'friends'):
            friends_count = len(info_data.friends)
        elif hasattr(info_data, 'friend_list'):
            friends_count = len(info_data.friend_list)
        elif hasattr(info_data, 'social_info') and hasattr(info_data.social_info, 'friend_count'):
            friends_count = info_data.social_info.friend_count
    except:
        friends_count = 0
    
    return {
        'uid': basic_info.account_id,
        'nickname': basic_info.nickname,
        'level': basic_info.level,
        'region': basic_info.region,
        'likes': basic_info.liked,
        'release_version': basic_info.release_version,
        'friends_count': friends_count  # Friends count added
    }

# -----------------------------
# Authentication Helper Functions
# -----------------------------
def decode_author_uid(token):
    try:
        decoded = jwt.decode(token, options={"verify_signature": False})
        return decoded.get("account_id") or decoded.get("sub")
    except:
        return None

# -----------------------------
# Get Friends List Function (New)
# -----------------------------

def get_friends_list(target_uid, token, server_name=None):
    """Get friends list using GetPlayerSocialNetwork endpoint"""
    try:
        if not server_name:
            server_name = get_server_from_token(token)
            
        # Create protobuf for social network request
        msg = uid_generator_pb2.uid_generator()
        msg.saturn_ = int(target_uid)
        msg.garena = 1
        
        protobuf_data = msg.SerializeToString()
        encrypted_data = encrypt_message_hex(protobuf_data)
        
        endpoint = get_base_url(server_name) + "GetPlayerSocialNetwork"

        headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Authorization': f"Bearer {token}",
            'Content-Type': "application/x-www-form-urlencoded",
            'Expect': "100-continue",
            'X-Unity-Version': "2018.4.11f1",
            'X-GA': "v1 1",
            'ReleaseVersion': "OB52"
        }

        response = requests.post(endpoint, data=bytes.fromhex(encrypted_data), headers=headers, verify=False)
        
        if response.status_code != 200:
            return [], 0

        # Parse response - assuming social network protobuf exists
        try:
            # Try to parse with data_pb2 or create new protobuf
            hex_response = response.content.hex()
            binary = bytes.fromhex(hex_response)
            
            # Check if SocialNetwork proto exists in data_pb2
            if hasattr(data_pb2, 'SocialNetwork') or hasattr(data_pb2, 'PlayerSocialNetwork'):
                social_info = data_pb2.SocialNetwork() if hasattr(data_pb2, 'SocialNetwork') else data_pb2.PlayerSocialNetwork()
                social_info.ParseFromString(binary)
                
                friends_list = []
                friends_count = 0
                
                # Extract friends based on proto structure
                if hasattr(social_info, 'friends'):
                    friends_count = len(social_info.friends)
                    for friend in social_info.friends:
                        name = getattr(friend, 'nickname', None) or getattr(friend, 'name', 'Unknown')
                        friends_list.append(name)
                elif hasattr(social_info, 'friend_list'):
                    friends_count = len(social_info.friend_list)
                    for friend in social_info.friend_list:
                        name = getattr(friend, 'nickname', None) or getattr(friend, 'name', 'Unknown')
                        friends_list.append(name)
                
                return friends_list, friends_count
            else:
                # If no proto, return empty
                return [], 0
                
        except Exception as e:
            print(f"Error parsing friends list: {e}")
            return [], 0

    except Exception as e:
        print(f"Error getting friends list: {e}")
        return [], 0

# -----------------------------
# Updated Friend Management Functions
# -----------------------------

@retry_operation(max_retries=10, delay=1)
def remove_friend_with_retry(author_uid, target_uid, token, server_name=None):
    """Remove friend with retry mechanism"""
    try:
        if not server_name:
            server_name = get_server_from_token(token)
            
        # Get player info
        player_info = get_player_info(target_uid, token, server_name)
        
        # Get friends list separately
        friends_names, friends_count = get_friends_list(target_uid, token, server_name)
        
        msg = RemoveFriend_Req_pb2.RemoveFriend()
        msg.AuthorUid = int(author_uid)
        msg.TargetUid = int(target_uid)
        encrypted_bytes = encrypt_message(msg.SerializeToString())

        url = get_base_url(server_name) + "RemoveFriend"
        headers = {
            'Authorization': f"Bearer {token}",
            'User-Agent': "Dalvik/2.1.0 (Linux; Android 9)",
            'Content-Type': "application/x-www-form-urlencoded",
            'X-Unity-Version': "2018.4.11f1",
            'X-GA': "v1 1",
            'ReleaseVersion': "OB52"
        }

        res = requests.post(url, data=encrypted_bytes, headers=headers, verify=False)
        
        # Extract player info
        player_data = None
        if player_info:
            player_data = extract_player_info(player_info)
        
        # Check if successful
        if res.status_code == 200:
            status = "success"
        else:
            status = "failed"
            raise Exception(f"HTTP {res.status_code}: {res.text}")
        
        # Response with friends data from separate call
        response_data = {
            "remover_uid": author_uid,
            "nickname": player_data.get('nickname') if player_data else "Unknown",
            "removed_uid": target_uid,
            "level": player_data.get('level') if player_data else 0,
            "likes": player_data.get('likes') if player_data else 0,
            "friends_count": friends_count if friends_count else player_data.get('friends_count', 0),
            "friends_names": friends_names if friends_names else [],
            "region": player_data.get('region') if player_data else "Unknown",
            "release_version": player_data.get('release_version') if player_data else "Unknown",
            "status": status,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return response_data

    except Exception as e:
        print(f"Remove friend error: {e}")
        raise e

@retry_operation(max_retries=10, delay=1)
def send_friend_request_with_retry(author_uid, target_uid, token, server_name=None):
    """Send friend request with retry mechanism"""
    try:
        if not server_name:
            server_name = get_server_from_token(token)
            
        # Get player info
        player_info = get_player_info(target_uid, token, server_name)
        
        # Get friends list separately
        friends_names, friends_count = get_friends_list(target_uid, token, server_name)
        
        encrypted_id = Encrypt_ID(target_uid)
        payload = f"08a7c4839f1e10{encrypted_id}1801"
        encrypted_payload = encrypt_api(payload)

        url = get_base_url(server_name) + "RequestAddingFriend"
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": "OB52",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; Android 9)"
        }

        r = requests.post(url, headers=headers, data=bytes.fromhex(encrypted_payload), verify=False)
        
        # Extract player info
        player_data = None
        if player_info:
            player_data = extract_player_info(player_info)
        
        # Check if successful
        if r.status_code == 200:
            status = "success"
        else:
            status = "failed"
            raise Exception(f"HTTP {r.status_code}: {r.text}")
        
        # Response with friends data from separate call
        response_data = {
            "your_uid": author_uid,
            "nickname": player_data.get('nickname') if player_data else "Unknown",
            "friend_uid": target_uid,
            "level": player_data.get('level') if player_data else 0,
            "likes": player_data.get('likes') if player_data else 0,
            "friends_count": friends_count if friends_count else player_data.get('friends_count', 0),
            "friends_names": friends_names if friends_names else [],
            "region": player_data.get('region') if player_data else "Unknown",
            "release_version": player_data.get('release_version') if player_data else "Unknown",
            "status": status,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return response_data
        
    except Exception as e:
        print(f"Add friend error: {e}")
        raise e


# -----------------------------
# Routes - SAME URL /add and /remove
# -----------------------------

@app.route('/add', methods=['GET'])
def adding_friend_custom():
    """URL: /add?uid={uid}&password={password}&friend_uid={target_uid}"""
    uid = request.args.get('uid')
    password = request.args.get('password')
    friend_uid = request.args.get('friend_uid')
    server_name = 'VN'  # Default server

    if not uid or not password or not friend_uid:
        return jsonify({"status": "failed", "message": "Missing uid, password, or friend_uid"}), 400

    token, error = get_token_from_uid_password(uid, password)
    if error:
        return jsonify({"status": "failed", "message": error}), 400

    author_uid = decode_author_uid(token)
    result = send_friend_request_with_retry(author_uid, friend_uid, token, server_name)
    return jsonify(result)

@app.route('/remove', methods=['GET'])
def removing_friend_custom():
    """URL: /remove?uid={uid}&password={password}&friend_uid={target_uid}"""
    uid = request.args.get('uid')
    password = request.args.get('password')
    friend_uid = request.args.get('friend_uid')
    server_name = 'VN'  # Default server

    if not uid or not password or not friend_uid:
        return jsonify({"status": "failed", "message": "Missing uid, password, or friend_uid"}), 400

    token, error = get_token_from_uid_password(uid, password)
    if error:
        return jsonify({"status": "failed", "message": error}), 400

    author_uid = decode_author_uid(token)
    result = remove_friend_with_retry(author_uid, friend_uid, token, server_name)
    return jsonify(result)


@app.route('/player_info', methods=['GET'])
def player_info_custom():
    """URL: /player_info?uid={uid}&password={password}&friend_uid={target_uid}"""
    uid = request.args.get('uid')
    password = request.args.get('password')
    friend_uid = request.args.get('friend_uid')
    server_name = 'VN'  # Default server

    if not uid or not password or not friend_uid:
        return jsonify({"status": "failed", "message": "Missing uid, password, or friend_uid"}), 400

    token, error = get_token_from_uid_password(uid, password)
    if error:
        return jsonify({"status": "failed", "message": error}), 400

    player_info = get_player_info(friend_uid, token, server_name)
    if not player_info:
        return jsonify({"status": "failed", "message": "Info not found"}), 400

    player_data = extract_player_info(player_info)
    player_data.update({"status": "success", "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    return jsonify(player_data)

# -----------------------------
# JWT Generation Routes (Optional)
# -----------------------------
@app.route('/token', methods=['GET'])
def oauth_guest():
    """Get token using UID and password - FIXED"""
    uid = request.args.get('uid')
    password = request.args.get('password')
    
    if not uid or not password:
        return jsonify({"message": "Missing uid or password"}), 400

    token, error = get_token_from_uid_password(uid, password)
    if error:
        return jsonify({"message": error}), 400
        
    # Verify the token is valid
    author_uid = decode_author_uid(token)
    if not author_uid:
        return jsonify({"message": "Generated token is invalid"}), 400
        
    return jsonify({
        "status": "success",
        "token": token,
        "uid": uid,
        "author_uid": author_uid
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "FreeFire-API"}), 200

# -----------------------------
# Run Server
# ----------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
#MADE BY VAIBAHV @VAIBHAVFF570