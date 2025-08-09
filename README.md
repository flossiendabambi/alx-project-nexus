# 🛒 Project Nexus: eCommerce Backend System

Welcome to **alx-project-nexus**, the documentation hub for my major backend engineering project — a fully-featured **eCommerce backend system**. Built using modern technologies like **Django**, **Django REST Framework**, and **PostgreSQL**, this project demonstrates practical backend architecture, robust API design, and real-world engineering practices.

---

## 📦 Project Overview

This eCommerce backend powers a digital store where users can browse products, filter by category, read and leave reviews, manage their cart, and place orders — all through a secure and well-structured API. The system is designed with scalability, maintainability, and performance in mind, offering JWT-based authentication and API documentation via Swagger.

---

## 🛠️ Technologies Used

- **Python** — Core programming language  
- **Django** — High-level web framework for backend logic  
- **Django REST Framework (DRF)** — RESTful API for frontend consumption  
- **Djoser** — Authentication and user management endpoints  
- **drf-yasg** — Interactive Swagger/OpenAPI documentation  
- **PostgreSQL** — Relational database  
- **django-filter** — Query filtering for products and other models  
- **Simple JWT** — Secure token-based authentication  
- **Whitenoise** — Static file serving for production  
- **dotenv** — Environment variable management  

---

## 🧠 Key Backend Concepts

### 🏗 System Design
- Modular app structure under a dedicated `api` app
- Layered architecture with models, serializers, and viewsets
- Pagination and filtering support for product browsing
- JWT authentication for secure API access

### 🛒 Core Features
- **User Authentication** — Secure registration, login, and profile handling via Djoser & JWT  
- **Product Management** — Create, update, and delete products (admin only)  
- **Category Management** — Organize products into categories  
- **Image Uploads** — Support for product and category images  
- **Reviews** — Users can review products, average rating auto-calculated  
- **Cart & Checkout Flow** — Add/remove items, automatic price totals  
- **Order Tracking** — Order creation linked to authenticated users  

---

## 📜 API Endpoints & Examples

### Authentication

**Register**  
`POST /auth/users/`
```json
{
  "email": "jane@example.com",
  "username": "jane_doe",
  "password": "StrongPass123"
}
```

**Login**  
`POST /auth/jwt/create/`
```json
{
  "username": "jane_doe",
  "password": "StrongPass123"
}
```

**Response:**
```json
{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}
```

---

### Products

**List Products**  
`GET /products/?category=electronics&search=laptop`
```json
[
  {
    "id": 1,
    "name": "Gaming Laptop",
    "description": "High performance laptop",
    "price": "1500.00",
    "category": {
      "id": 2,
      "name": "Electronics"
    },
    "average_rating": 4.5
  }
]
```

**Retrieve Product**  
`GET /products/1/`
```json
{
  "id": 1,
  "name": "Gaming Laptop",
  "description": "High performance laptop",
  "price": "1500.00",
  "category": {
    "id": 2,
    "name": "Electronics"
  },
  "reviews": [
    {
      "id": 10,
      "user": "john_doe",
      "rating": 5,
      "comment": "Fantastic machine!"
    }
  ]
}
```

---

### Cart

**Add to Cart**  
`POST /cart/items/`
```json
{
  "product_id": 1,
  "quantity": 2
}
```

**View Cart**  
`GET /cart/`
```json
{
  "id": "cart_uuid",
  "items": [
    {
      "id": "item_uuid",
      "product": {
        "id": 1,
        "name": "Gaming Laptop"
      },
      "quantity": 2,
      "total_price": "3000.00"
    }
  ],
  "total": "3000.00"
}
```

---

### Orders

**Create Order**  
`POST /orders/`
```json
{
  "cart_id": "cart_uuid",
  "shipping_address": "123 Main Street, NY"
}
```

**Response:**
```json
{
  "id": 5,
  "status": "pending",
  "total": "3000.00",
  "items": [
    {
      "product": "Gaming Laptop",
      "quantity": 2,
      "price": "1500.00"
    }
  ]
}
```

---

## ⚙ Project Configuration

### Environment Variables
```env
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your_secret_key
```

### Installation & Setup
```bash
git clone https://github.com/flossiendabambi/alx-project-nexus.git
cd alx-project-nexus
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## ✅ Best Practices & Takeaways

- Keep serializers lean — use `SerializerMethodField` for computed values  
- Implement pagination for large datasets  
- Use environment variables for sensitive credentials  
- Leverage Django admin for quick management  
- Write docstrings and tests for all endpoints  

---

> *"Engineering robust systems means building for the user you have today, and scaling for the user you'll meet tomorrow."*  
> — Florence Ndabambi


