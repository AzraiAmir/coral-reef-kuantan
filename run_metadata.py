"""
Metadata Manager Runner — Build SQLite database from acquisition log
"""

import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime


def main():
    # Find latest acquisition log
    log_dir = Path("acquisition_logs")
    logs = sorted(log_dir.glob("acquisition_log_*.csv"))
    if not logs:
        print("No acquisition logs found. Run Phase A.2 first.")
        return
    log_file = logs[-1]
    print(f"Using log: {log_file}")

    # Load CSV
    df = pd.read_csv(log_file)
    print(f"Loaded {len(df)} rows")

    # Connect to DB
    db_path = "coral_metadata.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create images table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            image_id TEXT PRIMARY KEY,
            filename TEXT,
            site_id TEXT,
            quadrat_id TEXT,
            campaign INTEGER,
            depth_m REAL,
            temperature_c REAL,
            salinity_psu REAL,
            ph REAL,
            gps_latitude REAL,
            gps_longitude REAL,
            quality_score REAL,
            annotation_status TEXT,
            created_at TEXT
        )
    """)

    # Insert records
    for _, row in df.iterrows():
        image_id = row["filename"].replace(".jpg", "")
        cursor.execute("""
            INSERT OR REPLACE INTO images VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            image_id,
            row["filename"],
            row["site_id"],
            row["quadrat_id"],
            1,
            row.get("depth_m", 0.0),
            row.get("temperature_c", 0.0),
            row.get("salinity_psu", 0.0),
            row.get("ph", 0.0),
            row.get("gps_latitude", 0.0),
            row.get("gps_longitude", 0.0),
            None,
            "pending",
            datetime.now().isoformat(),
        ))

    conn.commit()

    # Verify
    cursor.execute("SELECT COUNT(*) FROM images")
    count = cursor.fetchone()[0]
    print(f"Inserted {count} rows into {db_path}")

    cursor.execute("SELECT site_id, quadrat_id, COUNT(*) FROM images GROUP BY site_id, quadrat_id")
    print("\nBreakdown by site/quadrat:")
    for row in cursor.fetchall():
        print(f"  {row[0]} | {row[1]} | {row[2]} images")

    conn.close()
    print(f"\nMetadata database saved: {db_path}")


if __name__ == "__main__":
    main()