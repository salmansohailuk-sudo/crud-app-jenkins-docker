# 🚀 CRUD App Deployment (Flask + Nginx + RDS MySQL)

---

## 🧱 Architecture

Browser → Nginx → Flask Backend → AWS RDS MySQL

---

## ⚙️ Step 1: Prepare RDS

- Ensure MySQL RDS exists
- Allow inbound:
  - Port: 3306
  - Source: your server IP

---

## 🗄 Step 2: Create Database

Run:

mysql -h your-rds-endpoint -u admin -p < init.sql

---

## 🔧 Step 3: Configure App

Edit docker-compose.yml:

- DB_USER
- DB_PASS
- DB_HOST
- DB_NAME

---

## 🐳 Step 4: Run Application

docker-compose build  
docker-compose up -d  

---

## 🌐 Step 5: Access

http://localhost

---

## ⚙️ Jenkins Flow

1. Pull latest code  
2. Build backend Docker image  
3. Stop old containers  
4. Start new containers  
5. Verify deployment  

---

## ✅ Done

Your app is now live with:
- Nginx frontend
- Python backend
- AWS RDS MySQL

---

## ⚠️ Troubleshooting

If DB fails:
- Check RDS security group
- Verify DB credentials
- Ensure DB exists
