# 🍔 Analytics Service — Tetris Burger

Microservicio de **analítica y reportes** para un eCommerce de hamburguesas, construido con **FastAPI + Pandas + MySQL**. Diseñado para ser consumido por un backend en **Java Spring Boot** y un frontend en **React**.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-green?logo=fastapi)
![Pandas](https://img.shields.io/badge/Pandas-3.0.1-purple?logo=pandas)
![MySQL](https://img.shields.io/badge/MySQL-Railway-orange?logo=mysql)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Tabla de Contenidos

- [Descripción](#descripción)
- [Tecnologías](#tecnologías)
- [Arquitectura](#arquitectura)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Ejecución](#ejecución)
- [Endpoints](#endpoints)
- [Autenticación](#autenticación)
- [Exportación](#exportación)
- [Integración con Spring Boot](#integración-con-spring-boot)
- [Requerimientos Funcionales](#requerimientos-funcionales)

---

## 📖 Descripción

Este microservicio expone una API REST de **solo lectura** sobre la base de datos del eCommerce de hamburguesas. Permite generar reportes de ventas, pedidos, productos más vendidos y métricas generales, con soporte para filtros dinámicos y exportación en múltiples formatos.

---

## ⚙️ Tecnologías

| Tecnología | Versión | Uso |
|------------|---------|-----|
| Python | 3.11+ | Lenguaje base |
| FastAPI | 0.111.0 | API REST |
| Pandas | 3.0.1 | Procesamiento de datos |
| SQLAlchemy | 2.0.30 | Conexión a BD |
| PyMySQL | 1.1.1 | Driver MySQL |
| Pydantic | 2.7.1 | Validaciones |
| python-jose | 3.3.0 | Validación JWT |
| openpyxl | 3.1.2 | Exportación Excel |
| uvicorn | 0.29.0 | Servidor ASGI |

---

## 🏗️ Arquitectura
Implementa **arquitectura limpia** con separación en capas:

Request → Router → Service → Repository → Database
↓
Pandas (transformación)
↓
Response (JSON / CSV / XLSX)

analytics_service/
│
├── app/
│ ├── init.py
│ ├── main.py # Entry point FastAPI
│ │
│ ├── core/
│ │ ├── init.py
│ │ └── config.py # Settings con pydantic-settings
│ │
│ ├── db/
│ │ ├── init.py
│ │ └── database.py # Engine SQLAlchemy (solo lectura)
│ │
│ ├── repositories/
│ │ ├── init.py
│ │ ├── ventas_repository.py # Queries SQL de ventas
│ │ ├── pedidos_repository.py # Queries SQL de pedidos
│ │ ├── productos_repository.py # Queries SQL de productos
│ │ └── metricas_repository.py # Queries SQL de métricas
│ │
│ ├── services/
│ │ ├── init.py
│ │ ├── ventas_service.py # Lógica Pandas: ventas
│ │ ├── pedidos_service.py # Lógica Pandas: pedidos
│ │ ├── productos_service.py # Lógica Pandas: productos
│ │ └── metricas_service.py # Lógica Pandas: métricas
│ │
│ ├── api/
│ │ ├── init.py
│ │ └── routes/
│ │ ├── init.py
│ │ └── reports.py # 5 endpoints FastAPI
│ │
│ ├── schemas/
│ │ ├── init.py
│ │ └── reports.py # Modelos Pydantic
│ │
│ └── utils/
│ ├── init.py
│ ├── auth.py # JWT + API Key middleware
│ └── export.py # Helpers CSV / XLSX
│
├── requirements.txt
├── .env # Variables de entorno (no subir a git)
└── README.md


---

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/analytics-service.git
cd analytics-service

Implementa **arquitectura limpia** con separación en capas:
2. Crear entorno virtual con Python 3.11
   py -3.11 -m venv venv

3. Activar el entorno virtual
   # Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate

4. Instalar dependencias
  pip install -r requirements.txt


Configuración
Crea el archivo .env en la raíz del proyecto:
# Base de Datos MySQL (Railway)
DB_URL=mysql+pymysql://USER:PASSWORD@HOST:PORT/DATABASE

# JWT — debe ser el mismo secret que usa Spring Boot
JWT_SECRET=tu_jwt_secret_en_base64
JWT_ALGORITHM=HS256

# API Key para integración server-to-server con Spring Boot
API_KEY=tu_api_key_segura


Ejecución
# Activar entorno virtual
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

# Correr el servidor con auto-reload
uvicorn app.main:app --reload --port 8000


