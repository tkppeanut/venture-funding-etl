# Venture Funding Database ETL

## Overview

ระบบนี้ใช้สำหรับนำเข้าข้อมูล Venture Funding จาก Excel
เข้าสู่ PostgreSQL Database

Pipeline

```
Excel
        ↓
raw_excel_import
        ↓
Transform
        ↓
Normalized Database
```

---

# Database

PostgreSQL

Schema

- Company
- Company_Stage
- Fund_category
- Fund_Subcat
- Comapany_fund
- Company_revenue
- Invention
- Patents
- Valuation_records
- Checklist_records
- Inventor
- Invention_inventors

---

# Import Order

## 1

```
01_import_excel_to_staging.py
```

อ่าน Excel

↓

Import เข้า

```
raw_excel_import
```

---

## 2

```
03_import_company.py
```

↓

Company

---

## 3

```
04_import_fund_category.py
```

↓

Fund_category

---

## 4

```
05_import_fund_subcat.py
```

↓

Fund_Subcat

---

## 5

```
06_import_company_stage.py
```

↓

Company_Stage

---

## 6

```
07_import_company_fund.py
```

↓

Comapany_fund

---

## 7

```
08_import_company_revenue.py
```

↓

Company_revenue

---

## 8

```
09_import_invention.py
```

↓

Invention

---

## 9

```
10_import_patents.py
```

↓

Patents

---

## 10

```
11_import_valuation.py
```

↓

Valuation_records

---

## 11

```
12_import_checklist.py
```

↓

Checklist_records

---

# Current Imported Data

| Table | Records |
|-------|---------|
| Company | 18 |
| Fund_category | 4 |
| Fund_Subcat | 33 |
| Company_Stage | 7 |
| Comapany_fund | 38 |
| Company_revenue | 21 |
| Invention | 10 |
| Patents | 12 |
| Valuation_records | 8 |
| Checklist_records | 24 |
| Inventor | 0 |
| Invention_inventors | 0 |

---

# Notes

Inventor

ยังไม่มีข้อมูลใน Excel

Invention_inventors

ยังไม่มีข้อมูลใน Excel

Checklist

มีบางบริษัทใน Excel ที่ยังไม่มีใน Company
จึงยังไม่สามารถ Import ได้

Valuation

ใช้ Thai Company Mapping

---

# Final QA

- Record Count ✔
- Foreign Key ✔
- Transform ✔
- ETL ✔

Database พร้อมใช้งาน