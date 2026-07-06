import subprocess
import sys

SCRIPTS = [
    "02_import_to_staging.py",
    "03_import_company.py",
    "04_import_fund_category.py",
    "05_import_fund_subcat.py",
    "06_import_company_stage.py",
    "07_import_company_fund.py",
    "08_import_company_revenue.py",
    "09_import_invention.py",
    "10_import_patents.py",
    "11_import_valuation.py",
    "12_import_checklist.py"
]


def run_script(script):
    print("\n" + "=" * 70)
    print(f"Running: {script}")
    print("=" * 70)

    result = subprocess.run(
        [sys.executable, script],
        text=True
    )

    if result.returncode != 0:
        print(f"\nERROR : {script}")
        sys.exit(result.returncode)

    print(f"\nSUCCESS : {script}")


def main():

    print("=" * 70)
    print("VENTURE FUNDING ETL")
    print("=" * 70)

    for script in SCRIPTS:
        run_script(script)

    print("\n" + "=" * 70)
    print("ETL COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    main()