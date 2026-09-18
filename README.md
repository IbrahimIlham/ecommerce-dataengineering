# E-Commerce Data Engineering Project

# Stop-Service -Name postgresql-x64-18

Proyek data engineering untuk pipeline ETL e-commerce dengan PostgreSQL, Python, dan dbt.

## Daftar Isi

- [Overview](#overview)
- [Prasyarat](#prasyarat)
- [Setup Project](#setup-project)
- [Struktur Project](#struktur-project)
- [Cara Menggunakan](#cara-menggunakan)
- [Database Schema](#database-schema)
- [Troubleshooting](#troubleshooting)

## Overview

Proyek ini adalah **data warehouse pipeline** untuk e-commerce dengan fitur:

- **Data Generation**: Membuat dataset sample customers, products, orders, payments
- **Data Validation**: Validasi kualitas data sebelum loading
- **Database**: PostgreSQL untuk centralized data storage
- **Transformation**: dbt untuk data modeling dan transformation
- **Testing**: Unit tests dan data quality checks

### Tech Stack

| Komponen | Teknologi |
|----------|-----------|
| Database | PostgreSQL 16 |
| Data Gen | Python (Pandas) |
| Orchestration | Docker Compose |
| Transformation | dbt |
| Testing | pytest |

## Prasyarat

Pastikan sudah install:

```bash
- Docker & Docker Compose
- Python 3.8+
- Git
```

**Check version:**
```bash
docker --version
docker-compose --version
python --version
```

## Setup Project

### 1. Clone & Navigate

```bash
cd c:\Users\ibrah\OneDrive\Desktop\ecommerce-data-engineering
```

### 2. Setup Environment

```bash
# Copy template env (jika ada)
copy .env.template .env

# Install Python dependencies
pip install -r requirements.txt
```

**Dependencies yang diperlukan:**
- `pandas>=1.3.0` - Data manipulation
- `psycopg2-binary>=2.9.0` - PostgreSQL adapter
- `dbt-postgres>=1.0.0` - Data build tool

### 3. Start Database dengan Docker

```bash
# Start PostgreSQL container
docker-compose up -d

# Verify container berjalan
docker ps
```

**Output yang diharapkan:**
```
CONTAINER ID   IMAGE        STATUS       PORTS
abc123...      postgres:16  Up 2 minutes 5432->5432/tcp
```

### 4. Generate Sample Data

```bash
# Generate dataset
python data/generate_dataset.py

# Output: CSV files di data/source/
```

**File yang dihasilkan:**
```
data/source/
├── customers.csv      (1,000 records)
├── products.csv       (200 records)
├── orders.csv         (3,000 records)
├── order_items.csv    
└── payments.csv       
```

### 5. Validate Data

```bash
python data/validate_dataset.py
```
