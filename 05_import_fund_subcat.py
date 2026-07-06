from db import connect_db
from utils import clean_text


def clear_table(cur):
    print("1) ล้างข้อมูล Fund_Subcat")
    print("-" * 40)

    cur.execute('TRUNCATE TABLE "Fund_Subcat" RESTART IDENTITY CASCADE;')

    print("ล้างข้อมูลเรียบร้อย")


def load_category_map(cur):
    """
    อ่าน Fund_category มาเก็บเป็น Dictionary
    เช่น
    {
        "PRIVATE": 1,
        "INT": 2,
        "PUBLIC": 3,
        "RAISE": 4
    }
    """

    cur.execute("""
        SELECT "UniqueID", name
        FROM "Fund_category";
    """)

    category_map = {}

    for unique_id, name in cur.fetchall():
        category_map[name] = unique_id

    return category_map


def fetch_funding_names(cur):
    cur.execute("""
        SELECT data
        FROM raw_excel_import
        WHERE sheet_name = 'Funding_Data';
    """)

    return cur.fetchall()


def import_subcategories(cur, rows, category_map):

    print("\n2) Import Fund_Subcat")
    print("-" * 40)

    inserted = 0

    seen = set()

    mapping = [
        ("PRIVATE_FUN_NAME", "PRIVATE"),
        ("INT_FUN_NAME", "INT"),
        ("PUB_FUN_NAME", "PUBLIC"),
        ("RAISE_FUN_NAME", "RAISE")
    ]

    for (data,) in rows:

        for excel_column, category_name in mapping:

            fund_name = clean_text(data.get(excel_column))

            if fund_name is None:
                continue

            key = (category_name, fund_name.lower())

            if key in seen:
                continue

            seen.add(key)

            cur.execute("""
                INSERT INTO "Fund_Subcat"
                (fundcat_id, name)
                VALUES
                (%s, %s);
            """, (
                category_map[category_name],
                fund_name
            ))

            inserted += 1

    print(f"เพิ่ม Fund_Subcat สำเร็จ {inserted} records")


def check_count(cur):

    print("\n3) ตรวจจำนวนข้อมูล")

    print("-" * 40)

    cur.execute("""
        SELECT COUNT(*)
        FROM "Fund_Subcat";
    """)

    count = cur.fetchone()[0]

    print(f"Fund_Subcat มี {count} records")


def main():

    conn = connect_db()
    cur = conn.cursor()

    clear_table(cur)

    category_map = load_category_map(cur)

    rows = fetch_funding_names(cur)

    import_subcategories(cur, rows, category_map)

    check_count(cur)

    conn.commit()

    cur.close()
    conn.close()

    print("\nImport Fund_Subcat สำเร็จ")


if __name__ == "__main__":
    main()