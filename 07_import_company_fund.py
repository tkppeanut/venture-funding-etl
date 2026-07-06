from db import connect_db
from utils import clean_text, clean_number


FUNDING_MAPPINGS = [
    {
        "category": "PRIVATE",
        "name_column": "PRIVATE_FUN_NAME",
        "amount_column": "PRIVATE_FUN_AMT"
    },
    {
        "category": "INT",
        "name_column": "INT_FUN_NAME",
        "amount_column": "INT_FUN_TOTAL"
    },
    {
        "category": "PUBLIC",
        "name_column": "PUB_FUN_NAME",
        "amount_column": "PUB_FUN_TOTAL"
    },
    {
        "category": "RAISE",
        "name_column": "RAISE_FUN_NAME",
        "amount_column": "RAISE_FUN_AMT"
    }
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


def load_fund_subcat_map(cur):
    print("\n2) โหลด Fund_Subcat Map")
    print("-" * 40)

    cur.execute("""
        SELECT
            fs."UniqueID",
            fc.name,
            fs.name
        FROM "Fund_Subcat" fs
        JOIN "Fund_category" fc
            ON fs.fundcat_id = fc."UniqueID"
        ORDER BY fs."UniqueID";
    """)

    fund_map = {}

    for subcat_id, category_name, fund_name in cur.fetchall():
        key = (
            category_name.upper(),
            fund_name.lower()
        )
        fund_map[key] = subcat_id

    print(f"โหลด Fund_Subcat {len(fund_map)} รายการ")
    return fund_map


def fetch_funding_rows(cur):
    print("\n3) อ่าน Funding_Data จาก raw_excel_import")
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


def transform_funding_records(rows, company_map, fund_map):
    print("\n4) Transform Funding_Data → Company_fund records")
    print("-" * 40)

    funding_records = []

    skipped_no_company = 0
    skipped_no_fund_name = 0
    skipped_no_funding = 0
    skipped_fund_not_found = 0

    for row_number, data in rows:
        company_name = clean_text(data.get("COMPANY_NAME"))

        if company_name is None:
            skipped_no_company += 1
            continue

        company_id = company_map.get(company_name.lower())

        if company_id is None:
            skipped_no_company += 1
            continue

        row_created_record = False

        for mapping in FUNDING_MAPPINGS:
            category = mapping["category"]
            fund_name = clean_text(data.get(mapping["name_column"]))
            amount = clean_number(data.get(mapping["amount_column"]))
            fund_date = clean_text(data.get("FUN_UPDATE_DATE"))

            if fund_name is None:
                skipped_no_fund_name += 1
                continue

            fund_key = (
                category,
                fund_name.lower()
            )

            fund_subcat_id = fund_map.get(fund_key)

            if fund_subcat_id is None:
                skipped_fund_not_found += 1
                print(
                    f"หา Fund_Subcat ไม่เจอ | Row {row_number} | "
                    f"{category} | {fund_name}"
                )
                continue

            funding_records.append({
                "row_number": row_number,
                "comp_id": company_id,
                "fund_subcat_id": fund_subcat_id,
                "amount": amount,
                "date": fund_date,
                "category": category,
                "fund_name": fund_name,
                "company_name": company_name
            })

            row_created_record = True

        if not row_created_record:
            skipped_no_funding += 1

    print(f"Transform ได้ {len(funding_records)} funding records")
    print(f"ข้ามเพราะไม่พบ Company: {skipped_no_company}")
    print(f"ข้ามเพราะ fund_name ว่าง: {skipped_no_fund_name}")
    print(f"ข้ามเพราะไม่มี funding record ในแถวนั้น: {skipped_no_funding}")
    print(f"ข้ามเพราะหา Fund_Subcat ไม่เจอ: {skipped_fund_not_found}")

    return funding_records


def clear_company_fund(cur):
    print("\n5) ล้างข้อมูล Company_fund")
    print("-" * 40)

    cur.execute('TRUNCATE TABLE "Company_fund" RESTART IDENTITY CASCADE;')

    print("ล้างข้อมูลเรียบร้อย")


def insert_company_fund(cur, funding_records):
    print("\n6) Insert เข้า Company_fund")
    print("-" * 40)

    inserted = 0

    for record in funding_records:
        cur.execute("""
            INSERT INTO "Company_fund"
                (comp_id, fund_subcat_id, amount, date)
            VALUES
                (%s, %s, %s, %s);
        """, (
            record["comp_id"],
            record["fund_subcat_id"],
            record["amount"],
            record["date"]
        ))

        inserted += 1

    print(f"Insert สำเร็จ {inserted} records")


def check_count(cur):
    print("\n7) ตรวจจำนวนข้อมูลใน Company_fund")
    print("-" * 40)

    cur.execute('SELECT COUNT(*) FROM "Company_fund";')
    count = cur.fetchone()[0]

    print(f"Company_fund มี {count} records")


def main():
    conn = connect_db()
    cur = conn.cursor()

    company_map = load_company_map(cur)
    fund_map = load_fund_subcat_map(cur)
    rows = fetch_funding_rows(cur)

    funding_records = transform_funding_records(
        rows,
        company_map,
        fund_map
    )

    clear_company_fund(cur)
    insert_company_fund(cur, funding_records)
    check_count(cur)

    conn.commit()

    cur.close()
    conn.close()

    print("\n8.5.5 Import Company_fund สำเร็จ")


if __name__ == "__main__":
    main()