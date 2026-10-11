"""
Metadata Manager
Manages metadata database for all images and field data.
"""

import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime


class MetadataManager:
    def __init__(self, db_path="metadata.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        """Connect to SQLite database."""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        return self.conn

    def create_tables(self):
        """Create metadata tables."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS images (
                image_id TEXT PRIMARY KEY,
                filename TEXT,
                site_id TEXT,
                transect_id TEXT,
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

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS environmental_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_id TEXT,
                campaign INTEGER,
                parameter TEXT,
                value REAL,
                unit TEXT,
                timestamp TEXT
            )
        """)

        self.conn.commit()
        print("Tables created successfully.")

    def insert_image(self, image_data):
        """Insert image metadata."""
        self.cursor.execute("""
            INSERT OR REPLACE INTO images VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        """, (
            image_data['image_id'],
            image_data['filename'],
            image_data['site_id'],
            image_data['transect_id'],
            image_data['campaign'],
            image_data['depth_m'],
            image_data['temperature_c'],
            image_data['salinity_psu'],
            image_data['ph'],
            image_data['gps_latitude'],
            image_data['gps_longitude'],
            image_data['quality_score'],
            image_data['annotation_status'],
            datetime.now().isoformat()
        ))
        self.conn.commit()

    def query_images(self, site_id=None, campaign=None):
        """Query images by site and campaign."""
        query = "SELECT * FROM images WHERE 1=1"
        params = []

        if site_id:
            query += " AND site_id = ?"
            params.append(site_id)
        if campaign:
            query += " AND campaign = ?"
            params.append(campaign)

        return pd.read_sql_query(query, self.conn, params=params)

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    manager = MetadataManager("coral_metadata.db")
    manager.connect()
    manager.create_tables()
    manager.close()
