import psycopg2


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "Venture Funding",
    "user": "postgres",
    "password": "090229"
}


def connect_db():
    return psycopg2.connect(**DB_CONFIG)


def clean_text(value):
    if value is None:
        return None

    value = str(value).strip()

    if value == "":
        return None

    return value


def clean_number(value):
    if value is None:
        return None

    try:
        value = str(value).replace(",", "").strip()

        if value == "":
            return None

        return float(value)

    except ValueError:
        return None


def clear_company_table(cur):
    print("1) ล้างข้อมูล Company เดิม")
    print("-" * 40)

    cur.execute('TRUNCATE TABLE "Company" RESTART IDENTITY CASCADE;')

    print("ล้างข้อมูล Company เรียบร้อย")


def fetch_company_rows(cur):
    print("\n2) อ่านข้อมูลบริษัทจาก raw_excel_import")
    print("-" * 40)

    cur.execute("""
        SELECT
            data ->> 'COMPANY_NAME' AS company_name,
            data ->> 'COM_REGIS_CAP' AS registered_capital,
            data ->> 'STATUS' AS status
        FROM raw_excel_import
        WHERE sheet_name = 'Funding_Data';
    """)

    rows = cur.fetchall()

    print(f"อ่านข้อมูลจาก Funding_Data ได้ {len(rows)} rows")

    return rows


def import_company(cur, rows):
    print("\n3) Import เข้า Company")
    print("-" * 40)

    seen_companies = set()
    inserted_count = 0
    skipped_duplicate = 0
    skipped_blank = 0

    for row in rows:
        company_name = clean_text(row[0])
        registered_capital = clean_number(row[1])
        status = clean_text(row[2])

        if company_name is None:
            skipped_blank += 1
            continue

        company_key = company_name.lower()

        if company_key in seen_companies:
            skipped_duplicate += 1
            continue

        seen_companies.add(company_key)

        cur.execute("""
            INSERT INTO "Company"
                ("name_th", "name_en", "registered_capital", "status")
            VALUES
                (%s, %s, %s, %s);
        """, (
            None,
            company_name,
            registered_capital,
            status
        ))

        inserted_count += 1

    print(f"เพิ่ม Company สำเร็จ: {inserted_count} records")
    print(f"ข้ามชื่อบริษัทซ้ำ: {skipped_duplicate} rows")
    print(f"ข้ามชื่อบริษัทว่าง: {skipped_blank} rows")


def check_company_count(cur):
    print("\n4) ตรวจจำนวนข้อมูลใน Company")
    print("-" * 40)

    cur.execute('SELECT COUNT(*) FROM "Company";')
    count = cur.fetchone()[0]

    print(f"Company มีทั้งหมด {count} records")


def main():
    conn = connect_db()
    cur = conn.cursor()

    clear_company_table(cur)

    rows = fetch_company_rows(cur)

    import_company(cur, rows)

    check_company_count(cur)

    conn.commit()

    cur.close()
    conn.close()

    print("\nImport Company เสร็จสมบูรณ์")


if __name__ == "__main__":
    main()