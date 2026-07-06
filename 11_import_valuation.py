from db import connect_db
from utils import clean_text, clean_number


THAI_COMPANY_MAP = {
    "บริษัท เอียร์เอสเซนส์ จำกัด": "EARESSENCE CO., LTD.",
    "บริษัท เพอร์เฟค โพรเทคชั่น จำกัด": "PURRFECT PROTECTION CO., LTD.",
    "บริษัท ซาฮาร่า ดราย จำกัด": "SAHARA DRY CO., LTD.",
    "บริษัท เซียร่า ไบโอไซเอนซ์ จำกัด": "SIERRA BIOSCIENCE CO., LTD.",
    "บริษัท เอ อาร์ ทิ เมด จำกัด": "ARTIMED CO., LTD.",
    "บริษัท เอเวอร์เจน เทคโนโลยี จํากัด": "EVERGEN TECHNOLOGIES CO., LTD.",
    "บริษัท บีซีไอ เทคโนโลยี จำกัด": "BCI TECHNOLOGY CO., LTD.",
    "บริษัท เอ็มยูไอ โรบอติกส์ จำกัด": "MUI ROBOTICS CO., LTD."
}


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


def fetch_rows(cur):
    print("\n2) อ่าน Valuation")
    print("-" * 40)

    cur.execute("""
        SELECT row_number, data
        FROM raw_excel_import
        WHERE sheet_name='Valuation'
        ORDER BY row_number;
    """)

    rows = cur.fetchall()
    print(f"อ่านได้ {len(rows)} records")

    return rows


def transform_valuation(rows, company_map):
    print("\n3) Transform Valuation")
    print("-" * 40)

    records = []
    skipped_company = 0
    skipped_lookup = 0

    for row_number, data in rows:
        thai_name = clean_text(data.get("Company"))

        if thai_name is None:
            skipped_company += 1
            continue

        english_name = THAI_COMPANY_MAP.get(thai_name)

        if english_name is None:
            skipped_lookup += 1
            print(f"ไม่มี Mapping | Row {row_number} | {thai_name}")
            continue

        company_id = company_map.get(english_name.lower())

        if company_id is None:
            skipped_lookup += 1
            print(f"ไม่พบ Company | Row {row_number} | {english_name}")
            continue

        records.append({
            "comp_id": company_id,
            "valuation_year": 2024,
            "valuation": clean_number(data.get("Valuation 2024")),
            "equity_percent": None,
            "value_of_equity": None,
            "pitchdeck_status": clean_text(data.get("Pitch Deck")),
            "link": clean_text(data.get("Link")),
            "company_name": english_name
        })

    print(f"Transform ได้ {len(records)} records")
    print(f"Company ว่าง : {skipped_company}")
    print(f"Lookup ไม่สำเร็จ : {skipped_lookup}")

    return records


def clear_valuation(cur):
    print("\n4) ล้างข้อมูล Valuation_records")
    print("-" * 40)

    cur.execute("""
        TRUNCATE TABLE "Valuation_records"
        RESTART IDENTITY
        CASCADE;
    """)

    print("ล้างข้อมูลเรียบร้อย")


def insert_valuation(cur, records):
    print("\n5) Insert Valuation_records")
    print("-" * 40)

    inserted = 0

    for record in records:
        cur.execute("""
            INSERT INTO "Valuation_records"
                (
                    comp_id,
                    valuation_year,
                    valuation,
                    equity_percent,
                    value_of_equity,
                    pitchdeck_status,
                    link
                )
            VALUES
                (%s, %s, %s, %s, %s, %s, %s);
        """, (
            record["comp_id"],
            record["valuation_year"],
            record["valuation"],
            record["equity_percent"],
            record["value_of_equity"],
            record["pitchdeck_status"],
            record["link"]
        ))

        inserted += 1

    print(f"Insert สำเร็จ {inserted} records")


def check_count(cur):
    print("\n6) ตรวจจำนวนข้อมูล")
    print("-" * 40)

    cur.execute("""
        SELECT COUNT(*)
        FROM "Valuation_records";
    """)

    count = cur.fetchone()[0]
    print(f"Valuation_records มี {count} records")


def main():
    conn = connect_db()
    cur = conn.cursor()

    company_map = load_company_map(cur)
    rows = fetch_rows(cur)

    records = transform_valuation(rows, company_map)

    clear_valuation(cur)
    insert_valuation(cur, records)
    check_count(cur)

    conn.commit()

    cur.close()
    conn.close()

    print("\n8.9.2 Import Valuation_records สำเร็จ")


if __name__ == "__main__":
    main()