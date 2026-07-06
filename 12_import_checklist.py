from db import connect_db
from utils import clean_text

THAI_COMPANY_MAP = {
    "บริษัท เอียร์เอสเซนส์ จำกัด": "EARESSENCE CO., LTD.",
    "บริษัท เพอร์เฟค โพรเทคชั่น จำกัด": "PURRFECT PROTECTION CO., LTD.",
    "บริษัท ซาฮาร่า ดราย จำกัด": "SAHARA DRY CO., LTD.",
    "บริษัท ซาฮาร่า ดราย จำกัด ": "SAHARA DRY CO., LTD.",
    "บริษัท เซียร่า ไบโอไซเอนซ์ จำกัด": "SIERRA BIOSCIENCE CO., LTD.",
    "บริษัท เอ อาร์ ทิ เมด จำกัด": "ARTIMED CO., LTD.",
    "บริษัท เอเวอร์เจน เทคโนโลยี จํากัด": "EVERGEN TECHNOLOGIES CO., LTD.",
    "บริษัท บีซีไอ เทคโนโลยี จำกัด": "BCI TECHNOLOGY CO., LTD.",
    "บริษัท เอ็มยูไอ โรบอติกส์ จำกัด": "MUI ROBOTICS CO., LTD.",
    "บริษัท เซโนสติกส์ จำกัด": "ZENOSTIC CO., LTD.",
    "บริษัท เอ็ม เคมิ จำกัด": "M CHEMI CO., LTD.",
    "บริษัท ออลเทอร่า ไบโอเทค จำกัด": "ALLTHERA BIOTECH CO., LTD.",
    "บริษัท ออลเทอร่า ไบโอเทค จำกัด ": "ALLTHERA BIOTECH CO., LTD.",
    "บริษัท เบรนเอ็กซ์โซลูชั่น จำกัด": "BRAIN X SOLUTION CO., LTD."
}

CHECKLIST_PERIODS = [
    ("Sent_June", "Filled_June", "June"),
    ("Sent_Sep", "Filled_Sep", "September"),
    ("Sent_Mar_2025", "Filled_Mar_2025", "March 2025")
]


def to_bool(value):
    text = clean_text(value)

    if text is None:
        return None

    text = text.lower()

    if text in ["true", "yes", "y", "1", "sent", "filled", "done"]:
        return True

    if text in ["false", "no", "n", "0"]:
        return False

    return True


def load_company_map(cur):
    cur.execute("""
        SELECT "UniqueID", name_en
        FROM "Company";
    """)

    return {
        name.lower(): uid
        for uid, name in cur.fetchall()
    }


def load_invention_map(cur):
    cur.execute("""
        SELECT "UniqueID", name
        FROM "Invention";
    """)

    return {
        name.lower(): uid
        for uid, name in cur.fetchall()
    }


def fetch_rows(cur):
    cur.execute("""
        SELECT row_number, data
        FROM raw_excel_import
        WHERE sheet_name='Funding Checklist'
        ORDER BY row_number;
    """)

    return cur.fetchall()


def transform(rows, company_map, invention_map):
    records = []

    for _, data in rows:

        thai_company = clean_text(data.get("COMPANY_NAME"))

        english_company = THAI_COMPANY_MAP.get(thai_company)

        if english_company is None:
            continue

        comp_id = company_map.get(english_company.lower())

        if comp_id is None:
            continue

        invention_name = clean_text(data.get("INVENTION_NAME"))

        invention_id = None

        if invention_name:
            invention_id = invention_map.get(invention_name.lower())

        for sent_col, filled_col, round_name in CHECKLIST_PERIODS:

            sent = to_bool(data.get(sent_col))
            filled = to_bool(data.get(filled_col))

            if sent is None and filled is None:
                continue

            records.append((
                comp_id,
                invention_id,
                round_name,
                sent,
                filled,
                clean_text(data.get("Remark"))
            ))

    return records


def clear_table(cur):
    print("1) ล้างข้อมูล Checklist_records")
    print("-" * 40)

    cur.execute("""
        TRUNCATE TABLE "Checklist_records"
        RESTART IDENTITY
        CASCADE;
    """)

    print("ล้างข้อมูลเรียบร้อย")


def insert_records(cur, records):
    print("\n2) Insert Checklist_records")
    print("-" * 40)

    for record in records:
        cur.execute("""
            INSERT INTO "Checklist_records"
            (
                comp_id,
                invention_id,
                checklist_round,
                sent,
                filled,
                remark
            )
            VALUES
            (%s,%s,%s,%s,%s,%s);
        """, record)

    print(f"Insert สำเร็จ {len(records)} records")


def check_count(cur):
    print("\n3) ตรวจจำนวนข้อมูล")
    print("-" * 40)

    cur.execute("""
        SELECT COUNT(*)
        FROM "Checklist_records";
    """)

    print(f'Checklist_records มี {cur.fetchone()[0]} records')


def main():
    conn = connect_db()
    cur = conn.cursor()

    company_map = load_company_map(cur)
    invention_map = load_invention_map(cur)

    rows = fetch_rows(cur)

    records = transform(
        rows,
        company_map,
        invention_map
    )

    clear_table(cur)
    insert_records(cur, records)
    check_count(cur)

    conn.commit()

    cur.close()
    conn.close()

    print("\n8.10.2 Import Checklist_records สำเร็จ")


if __name__ == "__main__":
    main()