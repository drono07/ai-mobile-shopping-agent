# 📡 API Documentation

Complete API reference for the AI Mobile Shopping Agent.

## 🔗 Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com`

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```http
Authorization: Bearer <your-jwt-token>
```

## 📱 Chat Endpoints

### Send Message to AI Agent

**POST** `/chat`

Send a message to the AI agent and get intelligent responses.

**Request Body:**
```json
{
  "message": "Best camera phone under ₹30,000?",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "Here are some excellent camera phones under ₹30,000...",
  "recommendations": [
    {
      "id": 1,
      "name": "Samsung Galaxy A55 5G",
      "brand": "Samsung",
      "price": 39999.0,
      "display_size": 6.6,
      "processor": "Exynos 1480",
      "ram": 8,
      "storage": 128,
      "camera_main": "50MP + 12MP + 5MP",
      "battery_capacity": 5000,
      "features": "5G, Samsung Knox, 4 years updates"
    }
  ],
  "session_id": "generated-session-id",
  "used_web_search": false,
  "user_intent": {
    "intent": "recommendation",
    "budget_range": {"min": null, "max": 30000},
    "preferred_brands": [],
    "feature_focus": ["camera"]
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Best camera phone under ₹30,000?"}'
```

## 📱 Phone Endpoints

### Get All Phones

**GET** `/phones`

Retrieve phones with optional filtering.

**Query Parameters:**
- `brand` (string): Filter by brand (e.g., "Samsung", "Apple")
- `min_price` (number): Minimum price filter
- `max_price` (number): Maximum price filter
- `limit` (number): Number of results (default: 20)
- `offset` (number): Pagination offset

**Example:**
```http
GET /phones?brand=Samsung&max_price=50000&limit=10
```

**Response:**
```json
{
  "phones": [
    {
      "id": 1,
      "name": "Samsung Galaxy S24",
      "brand": "Samsung",
      "price": 79999.0,
      "display_size": 6.2,
      "processor": "Snapdragon 8 Gen 3",
      "ram": 8,
      "storage": 256,
      "camera_main": "50MP + 10MP + 10MP",
      "battery_capacity": 4000,
      "features": "AI features, 7 years updates, Compact design"
    }
  ],
  "total": 1,
  "limit": 10,
  "offset": 0
}
```

### Get Phone by ID

**GET** `/phones/{id}`

Get detailed information about a specific phone.

**Response:**
```json
{
  "id": 1,
  "name": "Samsung Galaxy S24",
  "brand": "Samsung",
  "price": 79999.0,
  "display_size": 6.2,
  "display_resolution": "2340 x 1080",
  "processor": "Snapdragon 8 Gen 3",
  "ram": 8,
  "storage": 256,
  "camera_main": "50MP + 10MP + 10MP",
  "camera_front": "12MP",
  "battery_capacity": 4000,
  "charging_speed": "25W",
  "os": "Android 14",
  "weight": 167.0,
  "dimensions": "147.0 x 70.6 x 7.6 mm",
  "colors": "Onyx Black, Marble Gray, Cobalt Violet",
  "features": "AI features, 7 years updates, Compact design",
  "ois": true,
  "eis": true,
  "wireless_charging": true,
  "water_resistance": "IP68",
  "fingerprint_sensor": true,
  "face_unlock": true
}
```

### Get All Brands

**GET** `/brands`

Get list of all available phone brands.

**Response:**
```json
{
  "brands": [
    {
      "id": 1,
      "name": "Samsung",
      "display_name": "Samsung",
      "aliases": ["Galaxy", "Note"],
      "phone_count": 5
    },
    {
      "id": 2,
      "name": "Apple",
      "display_name": "Apple",
      "aliases": ["iPhone"],
      "phone_count": 3
    }
  ]
}
```

## 🔄 Comparison Endpoints

### Compare Phones

**POST** `/compare`

Compare multiple phones side-by-side.

**Request Body:**
```json
{
  "phone_ids": [1, 2, 3]
}
```

**Response:**
```json
{
  "comparison": {
    "phones": [
      {
        "id": 1,
        "name": "Samsung Galaxy S24",
        "brand": "Samsung",
        "price": 79999.0,
        "display_size": 6.2,
        "processor": "Snapdragon 8 Gen 3",
        "ram": 8,
        "storage": 256,
        "camera_main": "50MP + 10MP + 10MP",
        "battery_capacity": 4000
      }
    ],
    "comparison_matrix": {
      "price": {"winner": 1, "values": [79999.0, 134900.0, 64999.0]},
      "camera": {"winner": 2, "values": ["50MP", "48MP", "50MP"]},
      "battery": {"winner": 3, "values": [4000, 3274, 5400]}
    }
  }
}
```

## 🔐 Authentication Endpoints

### User Registration

**POST** `/auth/register`

Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

### User Login

**POST** `/auth/login`

Authenticate user and get JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Get Current User

**GET** `/auth/me`

Get current authenticated user information.

**Headers:**
```http
Authorization: Bearer <your-jwt-token>
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "created_at": "2024-01-15T10:30:00Z",
  "last_login": "2024-01-15T10:30:00Z"
}
```

## 💬 Conversation Endpoints

### Get User Conversations

**GET** `/conversations`

Get all conversations for the authenticated user.

**Headers:**
```http
Authorization: Bearer <your-jwt-token>
```

**Response:**
```json
{
  "conversations": [
    {
      "id": 1,
      "title": "Best camera phone under ₹30,000?",
      "created_at": "2024-01-15T10:30:00Z",
      "message_count": 3
    }
  ]
}
```

### Get Conversation Messages

**GET** `/conversations/{conversation_id}/messages`

Get all messages in a specific conversation.

**Headers:**
```http
Authorization: Bearer <your-jwt-token>
```

**Response:**
```json
{
  "messages": [
    {
      "id": 1,
      "content": "Best camera phone under ₹30,000?",
      "role": "user",
      "timestamp": "2024-01-15T10:30:00Z"
    },
    {
      "id": 2,
      "content": "Here are some excellent camera phones...",
      "role": "assistant",
      "timestamp": "2024-01-15T10:30:05Z"
    }
  ]
}
```

## 🔧 Utility Endpoints

### Health Check

**GET** `/health`

Check if the API is running and healthy.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "database": "connected",
  "ai_service": "operational"
}
```

### API Information

**GET** `/`

Get basic API information and available endpoints.

**Response:**
```json
{
  "name": "AI Mobile Shopping Agent API",
  "version": "1.0.0",
  "description": "AI-powered mobile phone shopping assistant",
  "endpoints": {
    "chat": "/chat",
    "phones": "/phones",
    "compare": "/compare",
    "auth": "/auth",
    "health": "/health"
  }
}
```

## 📊 Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

## 🔍 Error Responses

**Validation Error (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "message"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Authentication Error (401):**
```json
{
  "detail": "Could not validate credentials"
}
```

**Not Found Error (404):**
```json
{
  "detail": "Phone not found"
}
```

## 🧪 Testing Examples

### Test Chat with Different Queries

```bash
# Budget recommendation
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Best phone under ₹25,000?"}'

# Brand-specific query
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me all Samsung phones"}'

# Comparison query
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Compare iPhone 15 vs Samsung S24"}'

# Technical question
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the difference between OIS and EIS?"}'
```

### Test Authentication Flow

```bash
# Register user
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123", "full_name": "Test User"}'

# Login user
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Use token for authenticated request
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 📈 Rate Limits

- **Chat endpoint**: 60 requests per minute per user
- **Phone endpoints**: 100 requests per minute
- **Authentication**: 10 requests per minute per IP

## 🔒 Security Notes

- All API keys should be kept secure
- Use HTTPS in production
- JWT tokens expire after 30 minutes
- Rate limiting is enforced to prevent abuse
- Input validation is performed on all endpoints

---

For setup instructions, see [SETUP.md](./SETUP.md)  
For technical architecture details, see [TECHNICAL.md](./TECHNICAL.md)
