"""
MIKE 21 Run Simulation
Run MIKE 21 FM simulation.
"""

import subprocess
from pathlib import Path
from datetime import datetime


class MIKE21Simulation:
    def __init__(self, model_dir):
        self.model_dir = Path(model_dir)

    def create_simulation_config(self, start_date, end_date, time_step=1.0):
        """Create simulation configuration file."""
        config = {
            'start_date': start_date,
            'end_date': end_date,
            'time_step': time_step,
            'output_interval': 60,
            'output_variables': ['U', 'V', 'zeta'],
            'output_file': 'results.dfs2',
        }

        output_file = self.model_dir / 'simulation.cfg'
        with open(output_file, 'w') as f:
            import json
            json.dump(config, f, indent=2)

        return output_file

    def run(self, config_file=None):
        """Run MIKE 21 FM simulation."""
        print(f"Starting MIKE 21 FM simulation...")
        start_time = datetime.now()

        # This would typically call MIKE 21 FM executable
        # For demonstration, we simulate the process
        if config_file:
            print(f"Using config: {config_file}")

        # Simulate execution
        print("Simulation in progress...")
        print("Simulation complete.")

        elapsed = datetime.now() - start_time
        print(f"Elapsed time: {elapsed}")

        return {
            'status': 'completed',
            'elapsed_time': str(elapsed),
        }


if __name__ == "__main__":
    sim = MIKE21Simulation('mike21_model')
    sim.create_simulation_config(
        start_date='2021-04-01',
        end_date='2021-05-01',
        time_step=1.0
    )
    sim.run()
