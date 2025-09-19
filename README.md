# FastShop API

A backend demo project built with FastAPI, demonstrating modern API development, authentication, and database management.  
The project highlights skills in building secure and scalable services using Python, PostgreSQL, and Docker.

---

## Features
- User registration and authentication with hashed passwords  
- JWT-based token generation and validation  
- Product management: create and list products  
- Health-check endpoint for monitoring  
- Database schema migrations with Alembic

---

## Tech Stack
- **Python 3.12** with FastAPI  
- **SQLAlchemy (asyncio)** as ORM  
- **Alembic** for schema migrations  
- **PostgreSQL** for persistent storage  
- **Docker & Docker Compose** for containerized services  
- **JWT & Passlib (bcrypt)** for authentication and password security

---

## How to Run
Clone the repository and start with Docker Compose:

```bash
git clone https://github.com/anamariadarii/fastshop.git
cd fastshop
docker compose up --build
