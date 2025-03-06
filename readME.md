# Django API & WebSocket Chat Application

## 🚀 Overview
This Django-based project provides:
- **Google OAuth 2.0 Authentication** for user login.
- **Google Picker API Integration** for Google Drive file uploads and retrieval.
- **WebSocket-based Real-Time Chat** for instant messaging between users.

## 🛠️ Setup Instructions

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/yourusername/django-chat-app.git
cd django-chat-app
```

### 2️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 3️⃣ Set Up Environment Variables
Create a `.env` file in the root directory and add the following:
```env
SECRET_KEY=your_secret_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://127.0.0.1:8000/auth/callback/
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 4️⃣ Apply Migrations
```sh
python manage.py migrate
```

### 5️⃣ Run the Server
```sh
python manage.py runserver
```
---

## 🔐 Google OAuth 2.0 Authentication

### **Initiate Google Auth Flow**
- **Endpoint:** `GET /auth/login/`
- **Description:** Redirects the user to Google’s authentication page.
- **Response:** Redirect URL.

```sh
curl -X GET http://127.0.0.1:8000/auth/login/
```

### **Google Auth Callback**
- **Endpoint:** `GET /auth/callback/`
- **Description:** Google sends authentication data to this endpoint.
- **Response:** JSON object containing user details and access tokens.

Example Response:
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "access_token": "ya29.ABC123..."
}
```

---

## 📂 Google Drive Integration (Google Picker API)



## 💬 WebSocket Chat

### **Connecting to WebSocket**
- **WebSocket URL:** `ws://127.0.0.1:8000/ws/chat/`
- **Description:** Establish a WebSocket connection for real-time chat.

### **How to Connect Using JavaScript**
```js
const socket = new WebSocket("ws://127.0.0.1:8000/ws/chat/");

socket.onopen = function () {
    console.log("Connected to WebSocket");
    socket.send(JSON.stringify({
        "message": "Hello!"
    }));
};

socket.onmessage = function (event) {
    console.log("Received:", event.data);
};

socket.onclose = function () {
    console.log("WebSocket Disconnected");
};
```

### **Sending a Chat Message**
When connected, send a message in JSON format:
```json
{
  "message": "Hello, how are you?"
}
```

### **Receiving a Chat Message**
When a message is received from another user, the server sends:
```json
{
  "sender": "user1",
  "message": "I'm good! What about you?"
}
```

---

## 🚀 Deployment

### **1️⃣ Install Daphne for ASGI Server**
```sh
pip install daphne
```

### **2️⃣ Run with ASGI**
```sh
daphne -b 127.0.0.1 -p 8000 myproject.asgi:application
```

### **3️⃣ Deploy on Heroku / Railway / Render**
- Add `Procfile` for Heroku:
  ```
  web: daphne -b 0.0.0.0 -p $PORT myproject.asgi:application
  ```
- Push to your repository and deploy.

---

## 📩 API Documentation (Postman Collection)
Import the provided **Postman collection** (`postman_collection.json`) into Postman for testing all endpoints.

---

## 🔥 Contributors
- **Sagar Sangwan** - [GitHub](https://github.com/sagarsangwan)

**i have hosted it here you can check basic features like (chat app )( https://north-assignment-2.onrender.com/)**

