from db import connect_db
from utils import clean_text


def clean_request_no(value):
    value = clean_text(value)

    if value is None:
        return None

    if value.endswith(".0"):
        value = value[:-2]

    return value


def load_invention_map(cur):
    print("1) โหลด Invention Map")
    print("-" * 40)

    cur.execute("""
        SELECT "UniqueID", name
        FROM "Invention"
        ORDER BY "UniqueID";
    """)

    invention_map = {}

    for invention_id, invention_name in cur.fetchall():
        invention_map[invention_name.lower()] = invention_id

    print(f"โหลด Invention {len(invention_map)} รายการ")

    return invention_map


def fetch_rows(cur):
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


def transform_patents(rows, invention_map):
    print("\n3) Transform Patent")
    print("-" * 40)

    patent_records = []
    seen = set()

    skipped_no_invention = 0
    skipped_no_patent = 0
    skipped_duplicate = 0

    for row_number, data in rows:
        invention_name = clean_text(data.get("INVENTION_NAME"))
        patent_type = clean_text(data.get("PATENT_TYPE"))
        application_date = clean_text(data.get("APPLICATION_SUBMIT_DATE"))
        request_no = clean_request_no(data.get("REQUEST_NUMBER"))

        if invention_name is None:
            skipped_no_invention += 1
            continue

        invention_id = invention_map.get(invention_name.lower())

        if invention_id is None:
            skipped_no_invention += 1
            continue

        if patent_type is None and application_date is None and request_no is None:
            skipped_no_patent += 1
            continue

        key = (
            invention_id,
            patent_type,
            request_no
        )

        if key in seen:
            skipped_duplicate += 1
            continue

        seen.add(key)

        patent_records.append({
            "invention_id": invention_id,
            "patent_type": patent_type,
            "application_date": application_date,
            "request_no": request_no,
            "invention_name": invention_name
        })

    print(f"Transform ได้ {len(patent_records)} patent records")
    print(f"ไม่พบ Invention : {skipped_no_invention}")
    print(f"ไม่มีข้อมูล Patent : {skipped_no_patent}")
    print(f"Duplicate : {skipped_duplicate}")

    return patent_records


def clear_patents(cur):
    print("\n4) ล้างข้อมูล Patents")
    print("-" * 40)

    cur.execute("""
        TRUNCATE TABLE "Patents"
        RESTART IDENTITY
        CASCADE;
    """)

    print("ล้างข้อมูลเรียบร้อย")


def insert_patents(cur, records):
    print("\n5) Insert Patents")
    print("-" * 40)

    inserted = 0

    for record in records:
        cur.execute("""
            INSERT INTO "Patents"
                ("Invention_id", patent_type, application_submit_date, "request_no.")
            VALUES
                (%s, %s, %s, %s);
        """, (
            record["invention_id"],
            record["patent_type"],
            record["application_date"],
            record["request_no"]
        ))

        inserted += 1

    print(f"Insert สำเร็จ {inserted} records")


def check_count(cur):
    print("\n6) ตรวจจำนวนข้อมูลใน Patents")
    print("-" * 40)

    cur.execute('SELECT COUNT(*) FROM "Patents";')
    count = cur.fetchone()[0]

    print(f"Patents มี {count} records")


def main():
    conn = connect_db()
    cur = conn.cursor()

    invention_map = load_invention_map(cur)
    rows = fetch_rows(cur)

    records = transform_patents(rows, invention_map)

    clear_patents(cur)
    insert_patents(cur, records)
    check_count(cur)

    conn.commit()

    cur.close()
    conn.close()

    print("\n8.8.2 Import Patents สำเร็จ")


if __name__ == "__main__":
    main()