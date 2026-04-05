# InvenAI — AI-Powered Inventory Management System

A full-stack Inventory Management System with AI demand prediction.

---

## 🗂 Project Structure

```
inventory-system/
├── frontend/
│   ├── pages/          login, dashboard, products, transactions, reports
│   └── assets/
│       ├── css/        style.css (dark industrial theme)
│       └── js/         config, api, sidebar, search, charts, toast
├── backend/
│   ├── app.py          Flask entry point
│   ├── routes/         auth, product, transaction, report, prediction
│   ├── controllers/    business logic layer
│   ├── models/         DB query layer
│   ├── ml/             prediction.py (Linear Regression)
│   └── config/         db.py (MySQL connection)
├── database/
│   └── schema.sql      Tables + seed data
├── requirements.txt
├── Procfile            For Render deployment
└── .env.example
```

---

## ⚡ Local Setup

### 1. MySQL Database

```sql
mysql -u root -p < database/schema.sql
```

This creates `inventory_db`, all tables, and seeds sample data.
Default admin login: `admin` / `admin123`

### 2. Backend (Python Flask)

```bash
cd backend
pip install -r ../requirements.txt

# Create .env from example
cp ../.env.example ../.env
# Edit .env with your DB credentials

python app.py
# API runs at http://localhost:5000
```

### 3. Frontend

Open `frontend/pages/login.html` in your browser, or serve with any static server:

```bash
cd frontend
npx serve .
# or: python -m http.server 8080
```

> **Note:** If backend is not on localhost:5000, update `CONFIG.API_BASE` in `frontend/assets/js/config.js`.

---

## 🌐 Deployment

### Backend → Render

1. Push the project to GitHub
2. Create a new **Web Service** on Render
3. Set **Root Directory** to `backend`
4. Set **Build Command**: `pip install -r ../requirements.txt`
5. Set **Start Command**: `gunicorn app:app`
6. Add environment variables from `.env.example`
7. Update `CONFIG.API_BASE` in `config.js` with your Render URL

### Frontend → Vercel

1. Set **Root Directory** to `frontend`
2. Deploy as static site (no build step needed)
3. Update `CONFIG.API_BASE` before deploying

---

## 📡 API Reference

| Method | Endpoint                        | Description              |
|--------|---------------------------------|--------------------------|
| POST   | `/api/login`                    | Authenticate user        |
| GET    | `/api/products`                 | List all products        |
| POST   | `/api/products`                 | Create product           |
| PUT    | `/api/products/<id>`            | Update product           |
| DELETE | `/api/products/<id>`            | Delete product           |
| GET    | `/api/transactions`             | List all transactions    |
| POST   | `/api/transactions`             | Record IN/OUT            |
| GET    | `/api/transactions/chart`       | Chart data (last 30d)    |
| GET    | `/api/reports/dashboard`        | Dashboard stats          |
| GET    | `/api/reports/export?type=...`  | Export CSV               |
| GET    | `/api/predict/<product_id>`     | AI demand prediction     |
| GET    | `/api/health`                   | Health check             |

All endpoints except `/api/login` require `Authorization: Bearer <token>` header.

---

## 🤖 AI Prediction

Located in `backend/ml/prediction.py`.

- Uses **scikit-learn LinearRegression**
- Trains on `OUT` transaction history (demand signal)
- Converts dates → numeric day offsets
- Returns: `predicted_quantity`, `trend`, `confidence (R²)`, `data_points`
- Requires ≥ 2 data points; returns "stable" with message if insufficient

---

## 🔐 Security Notes

- Passwords hashed with **bcrypt**
- Token is SHA-256 hash of `user_id:username:SECRET_KEY`
- For production: replace with **JWT** (`PyJWT`) with expiry
- Restrict CORS origins in `app.py` before deploying

---

## 🧩 Tech Stack

| Layer     | Technology              |
|-----------|-------------------------|
| Frontend  | HTML, CSS, JS, Chart.js |
| Backend   | Python Flask (REST API) |
| Database  | MySQL                   |
| AI/ML     | scikit-learn (LinearRegression) |
| Auth      | bcrypt + token auth     |
| Deploy    | Render (backend) + Vercel (frontend) |
