from db import connect_db
from utils import clean_text


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


def fetch_invention_rows(cur):
    print("\n2) อ่าน Funding_Data")
    print("-" * 40)

    cur.execute("""
        SELECT row_number, data
        FROM raw_excel_import
        WHERE sheet_name='Funding_Data'
        ORDER BY row_number;
    """)

    rows = cur.fetchall()

    print(f"อ่านได้ {len(rows)} records")

    return rows


def transform_invention_records(rows, company_map):

    print("\n3) Transform Invention")
    print("-" * 40)

    invention_records = []

    seen = set()

    skipped_company = 0
    skipped_name = 0
    skipped_duplicate = 0

    for row_number, data in rows:

        company_name = clean_text(data.get("COMPANY_NAME"))
        invention_name = clean_text(data.get("INVENTION_NAME"))

        if company_name is None:
            skipped_company += 1
            continue

        company_id = company_map.get(company_name.lower())

        if company_id is None:
            skipped_company += 1
            continue

        if invention_name is None:
            skipped_name += 1
            continue

        key = (
            company_id,
            invention_name.lower()
        )

        if key in seen:
            skipped_duplicate += 1
            continue

        seen.add(key)

        invention_records.append({
            "comp_id": company_id,
            "name": invention_name
        })

    print(f"Transform ได้ {len(invention_records)} records")
    print(f"Company ไม่พบ : {skipped_company}")
    print(f"INVENTION_NAME ว่าง : {skipped_name}")
    print(f"Duplicate : {skipped_duplicate}")

    return invention_records


def clear_invention(cur):

    print("\n4) ล้างข้อมูล Invention")
    print("-" * 40)

    cur.execute("""
        TRUNCATE TABLE "Invention"
        RESTART IDENTITY
        CASCADE;
    """)

    print("ล้างข้อมูลเรียบร้อย")


def insert_invention(cur, invention_records):

    print("\n5) Insert Invention")
    print("-" * 40)

    inserted = 0

    for record in invention_records:

        cur.execute("""
            INSERT INTO "Invention"
            (comp_id, name)
            VALUES
            (%s,%s);
        """, (
            record["comp_id"],
            record["name"]
        ))

        inserted += 1

    print(f"Insert สำเร็จ {inserted} records")


def check_count(cur):

    print("\n6) ตรวจจำนวนข้อมูล")
    print("-" * 40)

    cur.execute("""
        SELECT COUNT(*)
        FROM "Invention";
    """)

    count = cur.fetchone()[0]

    print(f"Invention มี {count} records")


def main():

    conn = connect_db()

    cur = conn.cursor()

    company_map = load_company_map(cur)

    rows = fetch_invention_rows(cur)

    invention_records = transform_invention_records(
        rows,
        company_map
    )

    clear_invention(cur)

    insert_invention(cur, invention_records)

    check_count(cur)

    conn.commit()

    cur.close()
    conn.close()

    print("\n8.7.2 Import Invention สำเร็จ")


if __name__ == "__main__":
    main()