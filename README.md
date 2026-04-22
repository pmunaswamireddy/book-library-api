# 📚 Premium Book Library API

A professional, full-stack Book Management System built with **FastAPI**, **SQLAlchemy**, and a stunning **Glassmorphism** frontend. This project transformed from a simple tutorial into a production-ready application with advanced features and a premium aesthetic.

![UI Preview](https://img.shields.io/badge/UI-Glassmorphism-blueviolet)
![Backend](https://img.shields.io/badge/Backend-FastAPI-009688)
![Database](https://img.shields.io/badge/Database-SQLite-003B57)

## ✨ Features

- **Premium UI:** A modern, dark-themed interface using glassmorphism principles and the "Outfit" typography.
- **Book Covers:** Support for custom book cover image URLs to bring your library to life.
- **Genre Tagging:** Categorize your books with genre labels for better organization.
- **Dynamic Stats:** Real-time dashboard showing total books, read count, and average ratings.
- **Advanced Filtering:** Search by title/author or filter by Read/Unread/Top Rated status.
- **Full CRUD:** Seamlessly add, edit, and delete books from your collection.
- **Production Ready:** Includes CORS security, input validation, and absolute pathing.

## 🛠️ Technology Stack

- **Backend:** FastAPI (Python)
- **Database:** SQLAlchemy (SQLite)
- **Validation:** Pydantic
- **Frontend:** Vanilla HTML5, CSS3 (Modern Glassmorphism), JavaScript (ES6+)
- **Containerization:** Docker

## 🚀 Getting Started

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pmunaswamireddy/book-library-api.git
   cd book-library-api
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   python -m uvicorn main:app --reload
   ```

4. **Access the UI:**
   Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## 📦 Deployment

This project is ready to be deployed to **Google Cloud Run**, **Render**, or **Railway** using the provided `Dockerfile`.

### Deploy to Render (Recommended)
1. Connect your GitHub repository to [Render.com](https://render.com).
2. Select **Web Service**.
3. Render will automatically detect the `Dockerfile` and deploy the app.

---
*Developed as a professional upgrade to the basic Book Library tutorial.*
