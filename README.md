# Free Fire Friend API

API quản lý bạn bè và thông tin người chơi Free Fire, được xây dựng bằng Python Flask với cơ chế retry tự động và hỗ trợ đa server.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Latest-green.svg)
![License](https://img.shields.io/badge/License-Educational-red.svg)

---

## 📋 Tính năng chính

| Tính năng | Endpoint | Mô tả |
|-----------|----------|-------|
| **Thêm bạn** | `/add` | Gửi yêu cầu kết bạn đến UID bất kỳ |
| **Xóa bạn** | `/remove` | Gỡ kết bạn với UID bất kỳ |
| **Xem thông tin** | `/player_info` | Lấy thông tin chi tiết người chơi (nickname, level, region, likes, friends_count) |
| **Join Guild** | `/join` | Gửi yêu cầu tham gia guild |
| **Lấy Token** | `/token` | Tạo JWT token để xác thực |
| **Friends List** | `/friends` | Lấy danh sách bạn bè của tài khoản |
| **Health Check** | `/health` | Kiểm tra trạng thái server |

---

## 🚀 Cài đặt

### Yêu cầu hệ thống

- Python 3.8 trở lên
- pip

### Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### Chạy server local

```bash
python app.py
```

Server chạy tại `http://localhost:5000`

---

## 📡 API Endpoints

### 1. Thêm bạn bè

**Endpoint:** `GET /add`

**Tham số:**

| Tham số | Bắt buộc | Mô tả |
|---------|----------|-------|
| `uid` | ✅ | UID tài khoản của bạn |
| `password` | ✅ | Mật khẩu tài khoản |
| `friend_uid` | ✅ | UID người cần thêm |

**Ví dụ:**
```
http://localhost:5000/add?uid=123456789&password=matkhau&friend_uid=987654321
```

**Phản hồi:**
```json
{
  "your_uid": "123456789",
  "nickname": "TenNguoiDung",
  "friend_uid": "987654321",
  "level": 65,
  "likes": 1234,
  "friends_count": 150,
  "friends_names": ["Ban1", "Ban2", "Ban3"],
  "region": "VN",
  "release_version": "1.108.3",
  "status": "success",
  "time": "2026-03-15 12:00:00"
}
```

---

### 2. Xóa bạn bè

**Endpoint:** `GET /remove`

**Tham số:**

| Tham số | Bắt buộc | Mô tả |
|---------|----------|-------|
| `uid` | ✅ | UID tài khoản của bạn |
| `password` | ✅ | Mật khẩu tài khoản |
| `friend_uid` | ✅ | UID người cần xóa |

**Ví dụ:**
```
http://localhost:5000/remove?uid=123456789&password=matkhau&friend_uid=987654321
```

**Phản hồi:**
```json
{
  "remover_uid": "123456789",
  "nickname": "TenNguoiDung",
  "removed_uid": "987654321",
  "level": 65,
  "likes": 1234,
  "friends_count": 149,
  "friends_names": ["Ban1", "Ban2"],
  "region": "VN",
  "release_version": "1.108.3",
  "status": "success",
  "time": "2026-03-15 12:00:00"
}
```

---

### 3. Xem thông tin người chơi

**Endpoint:** `GET /player_info`

**Tham số:**

| Tham số | Bắt buộc | Mô tả |
|---------|----------|-------|
| `uid` | ✅ | UID tài khoản (dùng để xác thực) |
| `password` | ✅ | Mật khẩu tài khoản |
| `friend_uid` | ✅ | UID người cần xem thông tin |

**Ví dụ:**
```
http://localhost:5000/player_info?uid=123456789&password=matkhau&friend_uid=987654321
```

**Phản hồi:**
```json
{
  "uid": "987654321",
  "nickname": "TenNguoiDung",
  "level": 65,
  "region": "VN",
  "likes": 1234,
  "friends_count": 150,
  "release_version": "1.108.3",
  "status": "success",
  "time": "2026-03-15 12:00:00"
}
```

---

### 4. Join Guild

**Endpoint:** `GET /join`

**Tham số:**

| Tham số | Bắt buộc | Mô tả |
|---------|----------|-------|
| `guild_id` | ✅ | ID guild muốn tham gia |
| `uid` | ✅ | UID tài khoản của bạn |
| `password` | ✅ | Mật khẩu tài khoản |

**Ví dụ:**
```
http://localhost:5000/join?guild_id=12345&uid=123456789&password=matkhau
```

**Phản hồi:**
```json
{
  "your_uid": "123456789",
  "nickname": "TenNguoiDung",
  "guild_id": "12345",
  "level": 65,
  "likes": 1234,
  "region": "VN",
  "release_version": "1.108.3",
  "status": "success",
  "time": "2026-03-15 12:00:00"
}
```

---

### 5. Lấy JWT Token

**Endpoint:** `GET /token`

**Tham số:**

| Tham số | Bắt buộc | Mô tả |
|---------|----------|-------|
| `uid` | ✅ | UID tài khoản |
| `password` | ✅ | Mật khẩu tài khoản |

**Ví dụ:**
```
http://localhost:5000/token?uid=123456789&password=matkhau
```

**Phản hồi:**
```json
{
  "status": "success",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "uid": "123456789",
  "author_uid": "123456789"
}
```

---

### 6. Friends List - Danh sách bạn bè

**Endpoint:** `GET /friends`

**Tham số:**

| Tham số | Bắt buộc | Mô tả |
|---------|----------|-------|
| `uid` | ✅ | UID tài khoản của bạn |
| `password` | ✅ | Mật khẩu tài khoản |

**Ví dụ:**
```
http://localhost:5000/friends?uid=123456789&password=matkhau
```

**Phản hồi:**
```json
{
  "friends_count": 150,
  "friends_list": [
    {"uid": "987654321", "name": "Ban1"},
    {"uid": "111222333", "name": "Ban2"},
    {"uid": "444555666", "name": "Ban3"}
  ],
  "my_info": {"uid": "123456789", "name": "TenNguoiDung"},
  "status": "success",
  "timestamp": 1710512345
}
```

---

### 7. Health Check

**Endpoint:** `GET /health`

**Ví dụ:**
```
http://localhost:5000/health
```

**Phản hồi:**
```json
{
  "status": "healthy",
  "service": "FreeFire-API"
}
```

---

## 🌐 Server Region

API tự động xác định server region từ JWT token hoặc sử dụng mặc định:

| Server | URL |
|--------|-----|
| IND | `https://client.ind.freefiremobile.com/` |
| BR, US, SAC, NA | `https://client.us.freefiremobile.com/` |
| VN, Khác | `https://clientbp.ggblueshark.com/` |

---

## 🔧 Cấu hình kỹ thuật

### AES Encryption

API sử dụng **AES-CBC** để mã hóa dữ liệu:

- **Key:** `89 103 38 116 99 37 68 69 117 104 54 37 90 99 94 56`
- **IV:** `54 111 121 90 68 114 50 50 69 51 121 99 104 106 77 37`

### Retry Mechanism

Các thao tác thêm/xóa bạn bè và join guild có cơ chế **tự động thử lại tối đa 10 lần** nếu thất bại, với delay 1 giây giữa mỗi lần thử.

### JWT Token

Token được tạo thông qua external API: `https://jwt-genall.vercel.app/token`

---

## 📦 Deploy lên Vercel

Dự án đã có sẵn file cấu hình `vercel.json`. Để deploy:

```bash
# Cài đặt Vercel CLI
npm install -g vercel

# Deploy
vercel deploy
```

---

## 🛠️ Công nghệ sử dụng

| Công nghệ | Mục đích |
|-----------|----------|
| **Flask** | Web framework |
| **Requests** | HTTP client |
| **PyCryptodome** | Mã hóa AES |
| **Protobuf** | Serialization dữ liệu |
| **PyJWT** | Xử lý JWT token |
| **urllib3** | HTTP library (disable warnings) |
| **google-protobuf** | Protobuf library |

---

## 📁 Cấu trúc file

```
FriendAPI/
├── app.py                 # Main application
├── protobuf_parser.py     # Protobuf parser utility
├── byte.py               # AES encryption/decryption helpers
├── data_pb2.py           # Protobuf definitions
├── friends_pb2.py        # Friends list protobuf
├── RemoveFriend_Req_pb2.py
├── uid_generator_pb2.py
├── requirements.txt      # Dependencies
├── vercel.json          # Vercel config
└── README.md            # Documentation
```

---

## ⚠️ Lưu ý quan trọng

- 🔒 **Mục đích học tập**: API này chỉ dùng cho mục đích học tập và nghiên cứu
- ⚠️ **Không vi phạm chính sách**: Không sử dụng cho các mục đích vi phạm chính sách của Garena
- 🔐 **Bảo mật**: Tự chịu trách nhiệm bảo mật thông tin tài khoản của bạn
- 🌐 **HTTPS**: HTTPS verification đã được tắt để hỗ trợ testing (`verify=False`)

---

## 📄 License

Sử dụng cho mục đích **học tập và nghiên cứu**. Không chịu trách nhiệm cho các hành vi lạm dụng.

---

## 🆘 Hỗ trợ

Nếu gặp vấn đề khi sử dụng API:

1. Kiểm tra lại UID và password
2. Đảm bảo tài khoản không bị khóa/ban
3. Thử lại sau vài phút nếu server target đang bảo trì
4. Kiểm tra logs để xem chi tiết lỗi
