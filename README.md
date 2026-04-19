# 📚 BookVault — Online Library Management System

**BookVault** is a sophisticated Django-based web application designed for library management. It features a modern, dark-themed UI with Glassmorphism aesthetics and follows the Django MVT (Model-View-Template) architecture.

This project was developed as a final examination project to demonstrate proficiency in backend development, database optimization, and user authentication.

---

## ✨ Key Features

### 📖 Book Management (CRUD)
* **Full Lifecycle**: Create, Read, Update, and Delete books through a secure interface.
* **Smart Search**: Real-time filtering by book title using case-insensitive lookups.
* **Advanced Filters**: Filter books by Category, Author, and Price Range (Min/Max).

### 📊 Data Analytics & Optimization
* **Statistics Dashboard**: Real-time library analytics using Django `aggregate` and `annotate`.
* **Performance**: Optimized database queries using `select_related` and `prefetch_related` to minimize SQL hits.
* **Clean Logic**: Automated data exclusion (e.g., hidden or invalid items) using `.exclude()`.

### 🔐 Security & Auth
* **User System**: Secure Registration, Login, and Logout functionality.
* **Access Control**: Only authenticated users can contribute books; only owners or admins can edit/delete entries.
* **Profile Management**: Personalized user profiles and secure password features.

---

## 🛠️ Tech Stack
* **Backend**: Django 5.0 (Python)
* **Database**: SQLite (Development) / PostgreSQL (Production ready)
* **Frontend**: HTML5, CSS3 (Custom Glassmorphism Framework), FontAwesome 6
* **Images**: Pillow (for dynamic cover image processing)

---

## 📸 Screenshots

### 🖼️ Catalog View
![Catalog](Снимок%20экрана%202026-04-15%20151800.jpg)

### 📈 Statistics Dashboard
![Statistics](image_95425d.jpg)

### ✍️ Add New Book Form
![Add Book](Снимок%20экрана%202026-04-19%20171356.jpg)

---

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/miryusuf899/Django-Book-Catalog.git](https://github.com/miryusuf899/Django-Book-Catalog.git)
   cd Django-Book-Catalog
