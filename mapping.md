# Venture Funding Database Mapping

## 1. Company

| Excel | PostgreSQL |
|--------|------------|
| COMPANY_NAME | Company.name_en |
| COM_REGIS_CAP | Company.registered_capital |
| STATUS | Company.status |

---

## 2. Company_Stage

| Excel | PostgreSQL |
|--------|------------|
| COMPANY_NAME | Company_Stage.comp_id (lookup Company) |
| STATUS | Company_Stage.stage |

---

## 3. Fund_category

สร้างข้อมูลเริ่มต้น

- PRIVATE
- INT
- PUBLIC
- RAISE

---

## 4. Fund_Subcat

| Excel | Category |
|--------|----------|
| PRIVATE_FUN_NAME | PRIVATE |
| INT_FUN_NAME | INT |
| PUB_FUN_NAME | PUBLIC |
| RAISE_FUN_NAME | RAISE |

---

## 5. Comapany_fund

| Excel | PostgreSQL |
|--------|------------|
| COMPANY_NAME | comp_id |
| *_FUN_NAME | fund_subcat_id |
| *_FUN_AMT | amount |
| FUN_UPDATE_DATE | fund_date |

หนึ่งแถวใน Excel
=
หลายแถวใน Company_fund

---

## 6. Company_revenue

| Excel | PostgreSQL |
|--------|------------|
| Q1_2024_REV | year=2024 quarter=1 |
| Q2_2024_REV | year=2024 quarter=2 |
| Q3_2024_REV | year=2024 quarter=3 |
| Q4_2024_REV | year=2024 quarter=4 |
| Q1_2025_REV | year=2025 quarter=1 |
| Q2_2025_REV | year=2025 quarter=2 |
| Q3_2025_REV | year=2025 quarter=3 |
| Q4_2025_REV | year=2025 quarter=4 |

---

## 7. Invention

| Excel | PostgreSQL |
|--------|------------|
| INVENTION_NAME | Invention.name |
| COMPANY_NAME | comp_id |

หมายเหตุ:
INVENT_ID, INVENTION_CATEGORY, INVENTION_OTHER_SUBCATEGORY, TRL, MAIN_INVENTION, UNITS
ยังไม่ลง table จริง เพราะไม่มี field ใน ER ปัจจุบัน
---

## 8. Inventor

ยังไม่มีข้อมูลใน Excel

---

## 9. Invention_inventors

ยังไม่มีข้อมูลใน Excel

---

## 10. Patents

| Excel | PostgreSQL |
|--------|------------|
| INVENTION_NAME | invention_id |
| PATENT_TYPE | patent_type |
| APPLICATION_SUBMIT_DATE | application_submit_date |
| REQUEST_NUMBER | request_no |

---

## 11. Valuation_records

| Excel | PostgreSQL |
|--------|------------|
| Company | comp_id |
| Link | link |
| Pitch Deck | pitch_deck |
| Valuation 2024 | valuation |

---

## 12. Checklist_records

| Excel | PostgreSQL |
|--------|------------|
| COMPANY_NAME | comp_id |
| INVENTION_NAME | invention_id |
| Sent_June | sent |
| Filled_June | filled |
| Sent_Sep | sent |
| Filled_Sep | filled |
| Sent_Mar_2025 | sent |
| Filled_Mar_2025 | filled |
| Remark | remark |

หนึ่งแถวใน Excel
=
หลายแถวใน Checklist_records