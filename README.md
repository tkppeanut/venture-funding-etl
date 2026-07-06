# Venture Funding Database ETL

PostgreSQL database and Python ETL pipeline for Venture Funding Management.

---

## Overview

ระบบนี้ใช้สำหรับนำเข้าข้อมูล Venture Funding จาก Excel เข้าสู่ PostgreSQL Database

```text
Excel
  ↓
raw_excel_import
  ↓
Transform
  ↓
Normalized PostgreSQL Database
  ↓
Reporting Views
```

---

## Features

- ✅ Normalized PostgreSQL Database
- ✅ Automated ETL Pipeline
- ✅ Excel to PostgreSQL Import
- ✅ Data Validation during Import
- ✅ Foreign Key Integrity Check
- ✅ One-command Full ETL
- ✅ Funding Tracking
- ✅ Revenue Tracking by Quarter
- ✅ Invention and Patent Management
- ✅ Valuation Records
- ✅ Funding Checklist Tracking
- ✅ Reporting Views for Dashboard
- ✅ Git Version Control

---

## Technology Stack

- Python
- PostgreSQL
- pgAdmin 4
- pandas
- psycopg2
- openpyxl
- Git
- GitHub

---

## Database Schema

Main tables:

- Company
- Company_Stage
- Fund_category
- Fund_Subcat
- Company_fund
- Company_revenue
- Invention
- Patents
- Valuation_records
- Checklist_records
- Inventor
- Invention_inventors
- raw_excel_import

---

## ETL Pipeline

Run full ETL pipeline:

```bash
python run_all_imports.py
```

Import order:

```text
02_import_to_staging.py
03_import_company.py
04_import_fund_category.py
05_import_fund_subcat.py
06_import_company_stage.py
07_import_company_fund.py
08_import_company_revenue.py
09_import_invention.py
10_import_patents.py
11_import_valuation.py
12_import_checklist.py
```

---

## Reporting Views

- company_dashboard_view
- company_profile_view
- company_funding_summary
- company_revenue_summary
- company_patent_summary
- company_valuation_summary
- company_checklist_summary

---

## Current Imported Data

| Table | Records |
|---|---:|
| Company | 18 |
| Fund_category | 4 |
| Fund_Subcat | 33 |
| Company_Stage | 7 |
| Company_fund | 38 |
| Company_revenue | 21 |
| Invention | 10 |
| Patents | 12 |
| Valuation_records | 8 |
| Checklist_records | 24 |
| Inventor | 0 |
| Invention_inventors | 0 |

---

## Notes

- `Inventor` ยังไม่มีข้อมูลใน Excel
- `Invention_inventors` ยังไม่มีข้อมูลใน Excel
- บางบริษัทใน Funding Checklist ยังไม่มีใน `Company` จึงยังไม่สามารถ import ได้
- `Valuation` และ `Checklist` ใช้ Thai Company Mapping
- ไฟล์ Excel ถูก ignore ด้วย `.gitignore` เพราะเป็นข้อมูลจริง/ข้อมูลลับ

---

## Final QA

- ✅ Record Count
- ✅ Foreign Key Integrity
- ✅ Transform Validation
- ✅ ETL Pipeline
- ✅ Reporting Views

Database พร้อมใช้งานสำหรับ Dashboard, API, และการวิเคราะห์ข้อมูลต่อ