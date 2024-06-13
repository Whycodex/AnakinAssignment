import gzip
import json

class DataSaver:
    def __init__(self, filename, logger):
        self.filename = filename
        self.logger = logger
    
    def save_data(self, data):
        with gzip.open(self.filename, 'wt', encoding='utf-8') as f:
            for item in data:
                f.write(json.dumps(item) + '\n')
        self.logger.info(f"Data saved to {self.filename}")
