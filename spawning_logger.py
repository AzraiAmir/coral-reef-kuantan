"""
Coral Spawning Data Logger
Records histological analysis results for spawning timing estimation.
"""

import pandas as pd
from datetime import datetime


class SpawningLogger:
    def __init__(self, output_file="spawning_data.csv"):
        self.output_file = output_file
        self.records = []

    def log_sample(self, colony_id, species, collection_date,
                   gonad_stage, gonad_score, notes=""):
        """Log histological analysis result for a single colony."""
        record = {
            'colony_id': colony_id,
            'species': species,
            'collection_date': collection_date,
            'gonad_stage': gonad_stage,
            'gonad_score': gonad_score,
            'notes': notes,
            'logged_at': datetime.now().isoformat(),
        }
        self.records.append(record)
        return record

    def estimate_spawning_timing(self):
        """Estimate spawning timing based on gonad maturity."""
        df = pd.DataFrame(self.records)

        mature = df[df['gonad_stage'] == 'mature']

        if len(mature) == 0:
            return "No mature colonies detected"

        latest_collection = pd.to_datetime(mature['collection_date']).max()
        estimated_spawning = latest_collection + pd.Timedelta(days=7)

        return {
            'estimated_spawning_date': estimated_spawning.strftime('%Y-%m-%d'),
            'confidence': 'High' if len(mature) >= 5 else 'Medium',
            'n_mature_colonies': len(mature),
        }

    def save(self):
        """Save all records to CSV."""
        df = pd.DataFrame(self.records)
        df.to_csv(self.output_file, index=False)
        print(f"Spawning data saved to {self.output_file}")
