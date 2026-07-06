from db import connect_db
from utils import clean_text


def clear_table(cur):
    print("1) ล้างข้อมูล Company_Stage")
    print("-" * 40)

    cur.execute('TRUNCATE TABLE "Company_Stage" RESTART IDENTITY CASCADE;')

    print("ล้างข้อมูลเรียบร้อย")


def load_company_map(cur):
    """
    สร้าง Dictionary

    {
        "ABC CO., LTD.": 1,
        "XYZ CO., LTD.": 2
    }
    """

    cur.execute("""
        SELECT "UniqueID", name_en
        FROM "Company";
    """)

    company_map = {}

    for unique_id, company_name in cur.fetchall():

        company_map[company_name.lower()] = unique_id

    return company_map


def fetch_rows(cur):

    cur.execute("""
        SELECT data
        FROM raw_excel_import
        WHERE sheet_name='Funding_Data';
    """)

    return cur.fetchall()


def import_company_stage(cur, rows, company_map):

    print("\n2) Import Company_Stage")
    print("-" * 40)

    inserted = 0

    seen = set()

    skipped_company = 0

    skipped_status = 0

    for (data,) in rows:

        company_name = clean_text(data.get("COMPANY_NAME"))
        status = clean_text(data.get("STATUS"))

        if company_name is None:
            skipped_company += 1
            continue

        if status is None:
            skipped_status += 1
            continue

        company_id = company_map.get(company_name.lower())

        if company_id is None:
            skipped_company += 1
            continue

        key = (company_id, status.lower())

        if key in seen:
            continue

        seen.add(key)

        cur.execute("""
            INSERT INTO "Company_Stage"
            (c_id, stage)
            VALUES
            (%s, %s);
        """, (
            company_id,
            status
        ))

        inserted += 1

    print(f"เพิ่ม Company_Stage : {inserted}")
    print(f"ข้าม STATUS ว่าง : {skipped_status}")
    print(f"ข้าม Company ไม่พบ : {skipped_company}")


def check_count(cur):

    print("\n3) ตรวจจำนวนข้อมูล")
    print("-" * 40)

    cur.execute("""
        SELECT COUNT(*)
        FROM "Company_Stage";
    """)

    count = cur.fetchone()[0]

    print(f"Company_Stage มี {count} records")


def main():

    conn = connect_db()

    cur = conn.cursor()

    clear_table(cur)

    company_map = load_company_map(cur)

    rows = fetch_rows(cur)

    import_company_stage(cur, rows, company_map)

    check_count(cur)

    conn.commit()

    cur.close()
    conn.close()

    print("\nImport Company_Stage สำเร็จ")


if __name__ == "__main__":
    main()