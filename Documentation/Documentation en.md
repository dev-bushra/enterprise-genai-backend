
# FastAPI Project Documentation – Enterprise RBAC System – Complete Guide

---

## 1. Project Introduction

This project is an advanced Backend system using **FastAPI** to build a secure and robust API with an advanced Role-Based Access Control (RBAC) system.  
The project aims to:

- Manage users and permissions in an enterprise-level manner.
- Secure access to resources based on user roles (e.g., admin, regular user, viewer).
- Provide a scalable architecture for large enterprise projects.
- Support integration with external systems such as Google Login and AI workflows in the future.

---

## 2. Technologies Used

| Technology      | Purpose                              |
|-----------------|------------------------------------|
| FastAPI         | Modern, fast web API framework      |
| Python 3.11+    | Primary programming language        |
| SQLAlchemy      | ORM for database management         |
| PostgreSQL      | Relational database                  |
| Alembic         | Database migrations management      |
| OAuth2 + JWT    | Authentication and authorization    |
| Google OAuth2   | Google account login integration    |
| Async SQLAlchemy| Asynchronous DB operations          |
| Docker (future) | Containerization for easy deployment|

---

## 3. Project Structure

```
app/
 ├── api/                  # API endpoints (routes)
 │    ├── tasks.py
 │    └── users.py
 ├── auth/                 # Authentication and RBAC modules
 │    ├── oauth2.py
 │    ├── rbac.py
 │    └── deps.py
 ├── db/                   # Database models and connections
 │    ├── models/
 │    │    ├── user.py
 │    │    ├── role.py
 │    │    └── user_role.py
 │    ├── database.py
 │    └── session.py
 ├── core/                 # Core settings and configuration
 ├── main.py               # Application entry point (FastAPI app)
 └── tests/                # Unit tests (under development)
```

---

## 4. What We Have Done So Far? Steps Implemented

### 4.1 Database Setup

- Using **PostgreSQL** as the primary database.
- Created **SQLAlchemy ORM** models for:
  - Users (`User`)
  - Roles (`Role`)
  - User-role association (`UserRole`)
- Managed database migrations with **Alembic**.

### 4.2 Building RBAC System

- Designed `roles` and `user_roles` tables with many-to-many relationships with users.
- Linked users to roles through the `roles` relationship inside the `User` model.
- Created helper functions to fetch user roles from the database.
- Created FastAPI Dependencies to check user permissions per endpoint.
- Protected endpoints so that only users with the required roles can access.
- Integrated Google OAuth2 login as an authentication method with JWT.

---

## 5. How to Use the System?

### 5.1 Registration and Login

- Login is based on Google OAuth2.
- After login, the user receives a **JWT** token containing user data.
- User ID is extracted from the token for access control.

### 5.2 Roles and Permissions Management

- Users can be linked to multiple roles in the `user_roles` table.
- Endpoints can be protected by Dependency:  
  `Depends(require_roles(["admin", "viewer"]))`
- If the user does not have the proper role, a 403 Forbidden error is returned.

---

## 6. How to Add New Roles?

1. Create a new record in the `roles` table (e.g., "admin", "user", "viewer").
2. Link users to roles in the `user_roles` table.
3. Refresh the token if needed (or load roles on each request).
4. Protect endpoints using the Dependency `require_roles`.

---

## 7. External Resources Used

| Resource                  | Purpose                                  |
|---------------------------|------------------------------------------|
| Google OAuth2             | Login and authentication via Google      |
| PostgreSQL                | Storing users and roles data              |
| Alembic                   | Managing database migrations              |
| FastAPI                   | Building a fast and scalable API          |

---

## 8. How to Run the Project

1. **Setup virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scriptsctivate     # Windows
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Update database connection settings** in `app/core/config.py` or `app/db/database.py`.

4. **Run Alembic migrations**

```bash
alembic upgrade head
```

5. **Run the application**

```bash
uvicorn app.main:app --reload
```

6. **Test the API using Postman or similar tools.**

---

## 9. What’s Next?

Upcoming project steps:

- Design an **AI Prompts Management system** to support AI operations.
- Add **Background Tasks (Celery + Redis)** for heavy operations like waiting for AI responses, generating files, or sending notifications.

---

# ⚠️ Important Note for New Developers

- Make sure to understand how OAuth2 and JWT token generation works.
- Understand SQLAlchemy relationships (especially many-to-many).
- Each endpoint is protected with Dependencies for access control.
- Always consider performance and security when adding new features.

---

If you need any extra explanations or developer onboarding files, just ask and I’ll prepare them for you immediately!
