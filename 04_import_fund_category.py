import psycopg2


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "Venture Funding",
    "user": "postgres",
    "password": "090229"
}


CATEGORIES = [
    "PRIVATE",
    "INT",
    "PUBLIC",
    "RAISE"
]


def connect_db():
    return psycopg2.connect(**DB_CONFIG)


def clear_table(cur):
    print("1) ล้างข้อมูล Fund_category")
    print("-" * 40)

    cur.execute('TRUNCATE TABLE "Fund_category" RESTART IDENTITY CASCADE;')

    print("ล้างข้อมูลเรียบร้อย")


def insert_categories(cur):
    print("\n2) เพิ่มข้อมูล Fund_category")
    print("-" * 40)

    for category in CATEGORIES:

        cur.execute("""
            INSERT INTO "Fund_category"
            (name)
            VALUES
            (%s);
        """, (category,))

        print(f"✓ {category}")

    print(f"\nเพิ่มทั้งหมด {len(CATEGORIES)} records")


def check_count(cur):
    print("\n3) ตรวจจำนวนข้อมูล")
    print("-" * 40)

    cur.execute('SELECT COUNT(*) FROM "Fund_category";')

    count = cur.fetchone()[0]

    print(f"Fund_category มี {count} records")


def main():

    conn = connect_db()
    cur = conn.cursor()

    clear_table(cur)

    insert_categories(cur)

    check_count(cur)

    conn.commit()

    cur.close()
    conn.close()

    print("\nImport Fund_category สำเร็จ")


if __name__ == "__main__":
    main()