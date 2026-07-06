from pathlib import Path
import json
import pandas as pd
import psycopg2


EXCEL_FILE = Path("Venture Funding.xlsx")

SHEETS_TO_IMPORT = [
    "Funding_Data",
    "Funding Checklist",
    "Valuation"
]

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "Venture Funding",
    "user": "postgres",
    "password": "090229"
}


def connect_db():
    return psycopg2.connect(**DB_CONFIG)


def to_clean_value(value):
    if pd.isna(value):
        return None

    if hasattr(value, "isoformat"):
        return value.isoformat()

    if hasattr(value, "item"):
        return value.item()

    return value


def clean_column_name(column):
    return str(column).strip()


def test_connection():
    print("1) ทดสอบเชื่อมต่อ PostgreSQL")
    print("-" * 40)

    conn = connect_db()
    conn.close()

    print("เชื่อมต่อ PostgreSQL สำเร็จ")


def check_staging_table():
    print("\n2) ตรวจสอบตาราง raw_excel_import")
    print("-" * 40)

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = 'raw_excel_import'
        );
    """)

    exists = cur.fetchone()[0]

    cur.close()
    conn.close()

    if exists:
        print("พบตาราง raw_excel_import")
    else:
        raise Exception("ไม่พบตาราง raw_excel_import")


def clear_staging_table():
    print("\n3) ล้างข้อมูลใน raw_excel_import")
    print("-" * 40)

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("TRUNCATE TABLE raw_excel_import RESTART IDENTITY;")
    conn.commit()

    cur.close()
    conn.close()

    print("ล้างข้อมูลเรียบร้อย")


def import_excel_to_staging():
    print("\n4) Import Excel เข้า raw_excel_import")
    print("-" * 40)

    conn = connect_db()
    cur = conn.cursor()

    total_inserted = 0

    for sheet_name in SHEETS_TO_IMPORT:
        print(f"\nกำลัง import sheet: {sheet_name}")

        df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name)

        sheet_inserted = 0

        for index, row in df.iterrows():
            row_data = {}

            for column_name, value in row.items():
                clean_name = clean_column_name(column_name)
                row_data[clean_name] = to_clean_value(value)

            cur.execute(
                """
                INSERT INTO raw_excel_import (sheet_name, row_number, data)
                VALUES (%s, %s, %s::jsonb);
                """,
                (
                    sheet_name,
                    int(index) + 2,
                    json.dumps(row_data, ensure_ascii=False)
                )
            )

            sheet_inserted += 1
            total_inserted += 1

        print(f"import สำเร็จ {sheet_inserted} rows")

    conn.commit()

    cur.close()
    conn.close()

    print(f"\nรวม import ทั้งหมด {total_inserted} rows")


def main():
    test_connection()
    check_staging_table()
    clear_staging_table()
    import_excel_to_staging()


if __name__ == "__main__":
    main()