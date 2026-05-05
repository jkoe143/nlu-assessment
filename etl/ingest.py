import csv
from datetime import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db import connect_db


def ingest_violations(cursor):
    # csv is pre-filtered to start from 01/01/2024
    with open("datasets/Building_Violations_20250815.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # check required fields
            missing = []
            if not row.get("ID"):
                missing.append("ID")
            if not row.get("ADDRESS"):
                missing.append("ADDRESS")
            if not row.get("VIOLATION DATE"):
                missing.append("VIOLATION DATE")

            if missing:
                print(f"Row {row.get('ID', 'UNKNOWN ID')} skipped - due to missing required field of {', '.join(missing)}")
                continue

            # normalizing address
            address = row["ADDRESS"].strip().lower()

            # make sure date is in datetime format
            try:
                date = datetime.strptime(row["VIOLATION DATE"].strip(), "%m/%d/%Y").date()
            except ValueError:
                print(f"Row {row['ID']} skipped - due to missing required field of VIOLATION DATE (invalid format)")
                continue
            
            # avoid reinserting if rows exist already
            cursor.execute("""
                INSERT INTO violations (id, date, code, status, description, inspector_comments, address)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING 
            """, (
                int(row["ID"]),
                date,
                row.get("VIOLATION CODE") or None,
                row.get("VIOLATION STATUS") or None,
                row.get("VIOLATION DESCRIPTION") or None,
                row.get("VIOLATION INSPECTOR COMMENTS") or None,
                address
            ))

def ingest_scofflaws(cursor):
    with open("datasets/Building_Code_Scofflaw_List_20250807.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # check required fields
            missing = []
            if not row.get("RECORD ID"):
                missing.append("RECORD ID")
            if not row.get("ADDRESS"):
                missing.append("ADDRESS")

            if missing:
                print(f"Row {row.get('RECORD ID', 'UNKNOWN ID')} skipped - due to missing required field of {', '.join(missing)}")
                continue

            # normalizing address
            address = row["ADDRESS"].strip().lower()

            # avoid reinserting if rows exist already
            cursor.execute("""
                INSERT INTO scofflaws (record_id, address)
                VALUES (%s, %s)
                ON CONFLICT (record_id) DO NOTHING
            """, (
                row["RECORD ID"].strip(),
                address
            ))

def main():
    conn = connect_db()
    cursor = conn.cursor()

    print("Ingesting violations dataset...")
    ingest_violations(cursor)

    print("Ingesting scofflaws dataset...")
    ingest_scofflaws(cursor)

    conn.commit()
    cursor.close()
    conn.close()
    print("Ingestion complete.")

if __name__ == "__main__":
    main()