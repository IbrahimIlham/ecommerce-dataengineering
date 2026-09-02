# Project Architecture

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Sources                             │
│  (CSV Files, APIs, External Systems)                        │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              Data Ingestion Layer                           │
│  (Python Scripts - load_*.py, validate_*.py)               │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│          Raw Data Layer (Staging)                           │
│  (PostgreSQL - raw_customers, raw_products, etc.)          │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│           Transformation Layer (dbt)                        │
│  (Cleaning, Validating, Aggregating)                       │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│         Business Logic Layer (Mart)                         │
│  (Dimensional Models, Aggregations)                        │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              Consumption Layer                              │
│  (Analytics Tools, Reports, Dashboards)                   │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Component Details

### 1. Data Ingestion
**Purpose:** Extract data dari berbagai sumber

**Komponen:**
- `data/generate_dataset.py` - Generate sample data
- `ingestion/load_*.py` - Load data ke database
- `data/validate_dataset.py` - Validate data quality

**Input:** CSV files, APIs, databases
**Output:** Raw tables di PostgreSQL

### 2. Raw Data Layer (Bronze)
**Purpose:** Store data apa adanya dari source

**Tables:**
- `raw_customers`
- `raw_products`
- `raw_orders`
- `raw_order_items`
- `raw_payments`

**Characteristics:**
- Minimal transformation
- Full audit trail
- Source compatibility

### 3. Staging Layer (Silver)
**Purpose:** Clean dan standardize data

**dbt Models (stg_*.sql):**
- Remove duplicates
- Handle nulls
- Data type standardization
- Basic validation

**Example:**
```sql
-- stg_customers
SELECT 
    customer_id,
    TRIM(first_name) as first_name,
    TRIM(last_name) as last_name,
    LOWER(email) as email,
    signup_date,
    CURRENT_TIMESTAMP as dbt_loaded_at
FROM raw_customers
WHERE customer_id IS NOT NULL
```

### 4. Transformation Layer
**Purpose:** Business logic dan aggregations

**dbt Models (mart_*.sql):**
- Customer RFM analysis
- Sales by product
- Regional performance
- Time-based aggregations

### 5. Mart Layer (Gold)
**Purpose:** Analytics-ready tables

**Key Tables:**
- `dim_customers` - Customer dimensions
- `dim_products` - Product dimensions
- `fact_orders` - Order facts
- `agg_daily_sales` - Daily sales aggregations

## 🗄️ Data Flow Example

### Scenario: Ingest Customer Data

```
Step 1: Raw Data
┌────────────────────┐
│ customers.csv      │ (1,000 rows)
├────────────────────┤
│ customer_id, name, │
│ email, signup_date │
└────────────────────┘
         │
         ▼
Step 2: Load
python ingestion/load_customers.py
         │
         ▼
Step 3: Raw Table
┌────────────────────────────┐
│ raw_customers              │
├────────────────────────────┤
│ customer_id (PK)           │
│ first_name                 │
│ last_name                  │
│ email (possibly dirty)      │
│ signup_date                │
└────────────────────────────┘
         │
         ▼
Step 4: dbt Staging
stg_customers.sql
- Trim whitespace
- Lowercase email
- Handle nulls
- Type conversion
         │
         ▼
Step 5: Mart
dim_customers (Dimension Table)
- Add surrogate keys
- Slowly changing dimension logic
- Historical tracking
```

## 🔄 Transformation Pipeline

```yaml
# dbt workflow
dbt run
├── sources (raw_*)
├── staging (stg_*)
│   ├── stg_customers
│   ├── stg_products
│   ├── stg_orders
│   └── stg_order_items
├── intermediate (int_*)
│   ├── int_order_items_with_prices
│   └── int_customer_lifetime_value
└── mart (fct_*, dim_*)
    ├── dim_customers
    ├── dim_products
    ├── dim_dates
    └── fct_orders
```

## 🔗 Relationships

```
dim_customers ◄──┐
                 │
            fct_orders ──► dim_products
                 │
                 └──► dim_dates
```

## 🗃️ Entity-Relationship Diagram

```
┌──────────────────┐
│ dim_customers    │
├──────────────────┤
│ PK customer_id   │────┐
│ first_name       │    │
│ email            │    │
│ city             │    │ FK
│ signup_date      │    │
└──────────────────┘    │
                        │
                    ┌───▼──────────────┐
                    │ fct_orders       │
                    ├──────────────────┤
                    │ PK order_id      │
                    │ FK customer_id   │◄───────┐
                    │ FK product_id    │───┐    │
                    │ order_date       │   │    │
                    │ total_amount     │   │  ┌─┴──────────────┐
                    │ quantity         │   │  │ dim_products   │
                    └──────────────────┘   │  ├────────────────┤
                                           └─►│ PK product_id  │
                                              │ product_name   │
                                              │ category       │
                                              │ price          │
                                              │ stock          │
                                              └────────────────┘
```

## 📈 Naming Conventions

| Layer | Prefix | Example | Notes |
|-------|--------|---------|-------|
| Raw | `raw_` | `raw_customers` | As-is dari source |
| Staging | `stg_` | `stg_customers` | Cleaned, deduplicated |
| Intermediate | `int_` | `int_order_summary` | Reusable logic |
| Fact | `fct_` | `fct_orders` | Transaction-level |
| Dimension | `dim_` | `dim_customers` | Slowly changing |
| Aggregation | `agg_` | `agg_daily_sales` | Pre-calculated |

## 🔐 Security Layers

```
┌─────────────────────────────────────┐
│ External Access Layer               │
│ (API, BI Tools)                     │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│ Mart Layer (Public views)           │
│ (Approved for consumption)          │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│ Transformation Layer                │
│ (Internal processing)               │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│ Raw Layer                           │
│ (Restricted access)                 │
└─────────────────────────────────────┘
```

## 🚀 Deployment Strategy

```
Development Environment
│
├─ Local Docker
├─ Local PostgreSQL
└─ Python venv
  │
  ▼
Staging Environment
│
├─ Docker containers
├─ Staging PostgreSQL
└─ Staging data (10% sample)
  │
  ▼
Production Environment
│
├─ Cloud Infrastructure
├─ Production PostgreSQL
└─ Full data
```

## 📊 Monitoring & Quality

```
Data Quality Checks
├─ Schema tests (dbt)
│  ├─ unique
│  ├─ not_null
│  └─ relationships
├─ Data tests (Python)
│  ├─ duplicate detection
│  ├─ data type validation
│  └─ business logic tests
└─ Performance monitoring
   ├─ Query execution time
   ├─ Data freshness
   └─ Pipeline run time
```

## 🔄 Update Frequency

| Component | Frequency | Method |
|-----------|-----------|--------|
| Raw data | Hourly | Batch load |
| Staging | Hourly | dbt run |
| Mart | Daily | dbt run schedule |
| Aggregations | Daily | Scheduled job |

---

See [README.md](../README.md) untuk setup instructions.
