# Fitness Store Management System

A professional Django e-commerce platform for fitness supplements, fully containerized using **Docker** and **PostgreSQL**.

---

## Installation & Setup

Follow these steps to get the project running on your local machine: 

### 1. Clone & Start Containers
```bash
cd django
git clone https://github.com/ariszaharia/django.git
cd magazin_fitness
docker-compose up -d
```
### 2. Setup
```bash
docker exec django_db psql -U aris -d fitness -c "CREATE SCHEMA IF NOT EXISTS django;"
docker exec django_web python manage.py createcachetable
docker exec django_web python manage.py migrate
docker exec -i django_db psql -U aris -d fitness < backup.sql
```

### 3. Acces
http://localhost:8000

