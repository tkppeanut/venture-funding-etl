from pathlib import Path
import pandas as pd


EXCEL_FILE = Path("Venture Funding.xlsx")


def check_file():
    print("1) ตรวจไฟล์ Excel")
    print("-" * 40)

    if EXCEL_FILE.exists():
        print("เจอไฟล์ Excel แล้ว:", EXCEL_FILE)
        return True
    else:
        print("ไม่เจอไฟล์ Excel")
        return False


def open_excel():
    print("\n2) เปิดไฟล์ Excel")
    print("-" * 40)

    excel = pd.ExcelFile(EXCEL_FILE)

    print("เปิดไฟล์ Excel สำเร็จ")
    return excel


def list_sheets(excel):
    print("\n3) รายชื่อ Sheet ในไฟล์ Excel")
    print("-" * 40)

    for sheet in excel.sheet_names:
        print("-", sheet)


def sheet_summary(excel):
    print("\n4) สรุปโครงสร้างของแต่ละ Sheet")
    print("-" * 40)

    for sheet in excel.sheet_names:
        df = pd.read_excel(EXCEL_FILE, sheet_name=sheet)

        print(f"\nSheet : {sheet}")
        print(f"Rows : {df.shape[0]}")
        print(f"Cols : {df.shape[1]}")


def show_columns(excel):
    print("\n5) รายชื่อคอลัมน์ของแต่ละ Sheet")
    print("-" * 40)

    for sheet in excel.sheet_names:
        df = pd.read_excel(EXCEL_FILE, sheet_name=sheet)

        print(f"\nSheet : {sheet}")
        print("-" * 40)

        for i, col in enumerate(df.columns, start=1):
            print(f"{i}. {col}")


def check_missing_values(excel):
    print("\n6) ตรวจข้อมูลว่างในแต่ละ Sheet")
    print("-" * 40)

    for sheet in excel.sheet_names:
        df = pd.read_excel(EXCEL_FILE, sheet_name=sheet)

        print(f"\nSheet : {sheet}")
        print("-" * 40)

        empty_count = df.isna().sum()
        has_empty = False

        for column_name, count in empty_count.items():
            if count > 0:
                has_empty = True
                print(f"{column_name}: ว่าง {count} ช่อง")

        if not has_empty:
            print("ไม่มีข้อมูลว่าง")


def check_duplicates(excel):
    print("\n7) ตรวจข้อมูลซ้ำในแต่ละ Sheet")
    print("-" * 40)

    for sheet in excel.sheet_names:

        df = pd.read_excel(EXCEL_FILE, sheet_name=sheet)

        duplicate_rows = df[df.duplicated()]

        print(f"\nSheet : {sheet}")

        if duplicate_rows.empty:
            print("ไม่มีข้อมูลซ้ำ")
        else:
            print(f"จำนวนแถวซ้ำ : {len(duplicate_rows)}")

            print("พบที่แถว:")

            for row in duplicate_rows.index:
                print(f"Row {row + 2}")


def check_required_columns(excel):
    print("\n8) ตรวจ Required Fields")
    print("-" * 40)

    required = {
        "Funding_Data": [
            "INVENT_ID",
            "COMPANY_NAME"
        ],
        "Funding Checklist": [
            "COMPANY_NAME"
        ],
        "Valuation": [
            "Company"
        ]
    }

    for sheet, columns in required.items():
        df = pd.read_excel(EXCEL_FILE, sheet_name=sheet)

        print(f"\nSheet : {sheet}")

        for column in columns:
            missing_rows = df[df[column].isna()]

            if missing_rows.empty:
                print(f"✓ {column} ครบ")
            else:
                print(f"✗ {column} ขาด {len(missing_rows)} แถว")

                for row in missing_rows.index:
                    print(f"   Row {row + 2}")


def main():
    file_ok = check_file()

    if not file_ok:
        return

    excel = open_excel()

    list_sheets(excel)
    sheet_summary(excel)
    show_columns(excel)
    check_missing_values(excel)
    check_duplicates(excel)
    check_required_columns(excel)


main()