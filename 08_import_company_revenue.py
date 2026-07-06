from db import connect_db
from utils import clean_text, clean_number


REVENUE_COLUMNS = [
    ("Q1_2024_REV", 2024, 1),
    ("Q2_2024_REV", 2024, 2),
    ("Q3_2024_REV", 2024, 3),
    ("Q4_2024_REV", 2024, 4),
    ("Q1_2025_REV", 2025, 1),
    ("Q2_2025_REV", 2025, 2),
    ("Q3_2025_REV", 2025, 3),
    ("Q4_2025_REV", 2025, 4),
]


def load_company_map(cur):
    print("1) โหลด Company Map")
    print("-" * 40)

    cur.execute("""
        SELECT "UniqueID", name_en
        FROM "Company"
        ORDER BY "UniqueID";
    """)

    company_map = {}

    for company_id, company_name in cur.fetchall():
        company_map[company_name.lower()] = company_id

    print(f"โหลดบริษัท {len(company_map)} บริษัท")
    return company_map


def fetch_revenue_rows(cur):
    print("\n2) อ่าน Funding_Data จาก raw_excel_import")
    print("-" * 40)

    cur.execute("""
        SELECT row_number, data
        FROM raw_excel_import
        WHERE sheet_name = 'Funding_Data'
        ORDER BY row_number;
    """)

    rows = cur.fetchall()

    print(f"อ่าน Funding_Data ได้ {len(rows)} records")
    return rows


def transform_revenue_records(rows, company_map):
    print("\n3) Transform Revenue records")
    print("-" * 40)

    revenue_records = []
    skipped_no_company = 0
    skipped_no_revenue = 0
    seen = set()

    for row_number, data in rows:
        company_name = clean_text(data.get("COMPANY_NAME"))

        if company_name is None:
            skipped_no_company += 1
            continue

        company_id = company_map.get(company_name.lower())

        if company_id is None:
            skipped_no_company += 1
            continue

        row_has_revenue = False

        for column_name, year, quarter in REVENUE_COLUMNS:
            amount = clean_number(data.get(column_name))

            if amount is None:
                continue

            key = (company_id, year, quarter)

            if key in seen:
                continue

            seen.add(key)

            revenue_records.append({
                "row_number": row_number,
                "comp_id": company_id,
                "amount": amount,
                "year": year,
                "quarter": quarter,
                "company_name": company_name,
                "source_column": column_name
            })

            row_has_revenue = True

        if not row_has_revenue:
            skipped_no_revenue += 1

    print(f"Transform ได้ {len(revenue_records)} revenue records")
    print(f"ข้ามเพราะไม่พบ Company: {skipped_no_company}")
    print(f"ข้ามเพราะไม่มี revenue ในแถวนั้น: {skipped_no_revenue}")

    return revenue_records


def clear_company_revenue(cur):
    print("\n4) ล้างข้อมูล Company_revenue")
    print("-" * 40)

    cur.execute('TRUNCATE TABLE "Company_revenue" RESTART IDENTITY CASCADE;')

    print("ล้างข้อมูลเรียบร้อย")


def insert_company_revenue(cur, revenue_records):
    print("\n5) Insert เข้า Company_revenue")
    print("-" * 40)

    inserted = 0

    for record in revenue_records:
        cur.execute("""
            INSERT INTO "Company_revenue"
                (comp_id, amount, quarter, year)
            VALUES
                (%s, %s, %s, %s);
        """, (
            record["comp_id"],
            record["amount"],
            record["quarter"],
            record["year"]
        ))

        inserted += 1

    print(f"Insert สำเร็จ {inserted} records")


def check_count(cur):
    print("\n6) ตรวจจำนวนข้อมูลใน Company_revenue")
    print("-" * 40)

    cur.execute('SELECT COUNT(*) FROM "Company_revenue";')
    count = cur.fetchone()[0]

    print(f"Company_revenue มี {count} records")


def main():
    conn = connect_db()
    cur = conn.cursor()

    company_map = load_company_map(cur)
    rows = fetch_revenue_rows(cur)

    revenue_records = transform_revenue_records(
        rows,
        company_map
    )

    clear_company_revenue(cur)
    insert_company_revenue(cur, revenue_records)
    check_count(cur)

    conn.commit()

    cur.close()
    conn.close()

    print("\n8.6.4 Import Company_revenue สำเร็จ")


if __name__ == "__main__":
    main()