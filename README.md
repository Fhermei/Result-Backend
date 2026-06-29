# Blockchain Student Result Management System - Backend

A secure, decentralized student result management system built with Django REST Framework and blockchain technology for Nigerian universities.

## 📋 Table of Contents
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [System Requirements](#-system-requirements)
- [Installation Guide](#-installation-guide)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create Virtual Environment](#2-create-virtual-environment)
  - [3. Activate Virtual Environment](#3-activate-virtual-environment)
  - [4. Install Dependencies](#4-install-dependencies)
  - [5. Configure Environment Variables](#5-configure-environment-variables)
  - [6. Run Migrations](#6-run-migrations)
  - [7. Create Superuser](#7-create-superuser)
  - [8. Populate Database](#8-populate-database)
  - [9. Run Development Server](#9-run-development-server)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

- **🔐 Secure Authentication** - JWT-based authentication with role-based access control
- **📊 Result Management** - Upload, edit, view, and publish student results
- **🎓 GPA/CGPA Calculation** - Automatic calculation following NUC 5-point grading scale
- **⛓️ Blockchain Integration** - SHA-256 hashing for tamper-proof result verification
- **👥 Role-Based Access** - Separate dashboards for Admin, Lecturer, and Student
- **📈 Analytics & Reports** - Comprehensive academic performance reports
- **📱 Responsive Design** - Works on desktop, tablet, and mobile devices

## 🛠️ Technology Stack

| Category | Technology |
|----------|------------|
| Backend Framework | Django 4.2.16 |
| API Framework | Django REST Framework 3.15.2 |
| Authentication | JWT (SimpleJWT) |
| Database | PostgreSQL / SQLite |
| Blockchain | web3.py, Ganache |
| API Documentation | drf-spectacular (Swagger) |
| Deployment | Render / PythonAnywhere |
| Version Control | Git & GitHub |

## 💻 System Requirements

### Hardware Requirements
- **Processor**: Intel Core i5 or equivalent
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 256GB SSD minimum
- **Network**: Stable internet connection

### Software Requirements
- **Operating System**: Windows 10/11, Linux (Ubuntu 20.04+), or macOS 10.15+
- **Python**: 3.10 or higher (3.12 recommended)
- **PostgreSQL**: 14 or higher (optional, SQLite works for development)
- **Git**: Latest version

## 🚀 Installation Guide

### 1. Clone the Repository

```bash
# Clone the repository
git clone https://github.com/your-username/result-backend.git

# Navigate to project directory
cd result-backend

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python populate_custom_db.py