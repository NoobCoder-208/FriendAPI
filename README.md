# Free Fire Add Friend API

API quản lý bạn bè và xem thông tin người chơi Free Fire, được xây dựng bằng Python Flask.

## 📋 Tính năng

- **Thêm bạn bè** - Gửi yêu cầu kết bạn đến UID bất kỳ
- **Xóa bạn bè** - Gỡ kết bạn với UID bất kỳ
- **Xem thông tin người chơi** - Lấy thông tin chi tiết của tài khoản (nickname, level, region, likes...)
- **Tạo JWT Token** - Xác thực tài khoản bằng UID và mật khẩu

## 🚀 Cài đặt

### Yêu cầu hệ thống

- Python 3.8+
- pip

### Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### Chạy server

```bash
python app.py
```

Server sẽ chạy tại `http://localhost:5000`

## 📡 API Endpoints

### 1. Thêm bạn bè

**Endpoint:** `GET /adding_friend`

**Tham số:**
| Tham số | Mô tả |
|---------|-------|
| `uid` | UID tài khoản của bạn |
| `password` | Mật khẩu tài khoản |
| `friend_uid` | UID người cần thêm |
| `server_name` | Server (VN, BR, US, SAC, NA, IND) - Mặc định: IND |

**Ví dụ:**
```
http://localhost:5000/adding_friend?uid=123456789&password=matkhau&friend_uid=987654321
```

**Phản hồi:**
```json
{
  "author_uid": "123456789",
  "nickname": "TenNguoiDung",
  "uid": "987654321",
  "level": 65,
  "likes": 1234,
  "region": "VN",
  "release_version": "1.108.3",
  "status": "success",
  "time": "2026-03-01 12:00:00"
}
```

---

### 2. Xóa bạn bè

**Endpoint:** `GET /remove_friend`

**Tham số:**
| Tham số | Mô tả |
|---------|-------|
| `uid` | UID tài khoản của bạn |
| `password` | Mật khẩu tài khoản |
| `friend_uid` | UID người cần xóa |
| `server_name` | Server (VN, BR, US, SAC, NA, IND) - Mặc định: IND |

**Ví dụ:**
```
http://localhost:5000/remove_friend?uid=123456789&password=matkhau&friend_uid=987654321
```

---

### 3. Xem thông tin người chơi

**Endpoint:** `GET /player_info`

**Tham số:**
| Tham số | Mô tả |
|---------|-------|
| `uid` | UID tài khoản của bạn (dùng để xác thực) |
| `password` | Mật khẩu tài khoản |
| `friend_uid` | UID người cần xem thông tin |
| `server_name` | Server (VN, BR, US, SAC, NA, IND) - Mặc định: IND |

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
  "release_version": "1.108.3",
  "status": "success",
  "time": "2026-03-01 12:00:00"
}
```

---

### 4. Lấy JWT Token

**Endpoint:** `GET /token`

**Tham số:**
| Tham số | Mô tả |
|---------|-------|
| `uid` | UID tài khoản |
| `password` | Mật khẩu tài khoản |

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

### 5. Health Check

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

## 🌐 Server Region

API hỗ trợ nhiều server khu vực:

| Server | URL |
|--------|-----|
| VN | https://clientbp.ggblueshark.com/ |
| BR, US, SAC, NA | https://client.us.freefiremobile.com/ |
| Khác | https://clientbp.ggblueshark.com/ |

## 🔧 Cấu hình

### AES Encryption

API sử dụng AES-CBC để mã hóa dữ liệu:

- **Key:** `89 103 38 116 99 37 68 69 117 104 54 37 90 99 94 56`
- **IV:** `54 111 121 90 68 114 50 50 69 51 121 99 104 106 77 37`

### Retry Mechanism

Các thao tác thêm/xóa bạn bè có cơ chế tự động thử lại tối đa **10 lần** nếu thất bại.

## 📦 Deploy lên Vercel

Dự án đã có sẵn file cấu hình `vercel.json`. Để deploy:

```bash
vercel deploy
```

## ⚠️ Lưu ý

- API này chỉ dùng cho mục đích học tập và nghiên cứu
- Không sử dụng cho các mục đích vi phạm chính sách của Garena
- Tự chịu trách nhiệm khi sử dụng
- HTTPS verification đã được tắt để hỗ trợ testing

## 📄 License

Sử dụng cho mục đích học tập và nghiên cứu.

## 🛠️ Công nghệ sử dụng

- **Flask** - Web framework
- **Requests** - HTTP client
- **PyCryptodome** - Mã hóa AES
- **Protobuf** - Serialization
- **PyJWT** - JWT token handling
- **urllib3** - HTTP library
