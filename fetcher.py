import requests

class DataFetcher:
    def __init__(self, base_url, headers, body_template, logger):
        self.base_url = base_url
        self.headers = headers
        self.body_template = body_template
        self.logger = logger
    
    def fetch_data(self, offset):
        body = self.body_template.copy()
        body['offset'] = offset
        response = requests.post(self.base_url, headers=self.headers, json=body)
        if response.status_code == 200:
            return response.json()
        else:
            self.logger.error(f"Failed to fetch data with status code {response.status_code}")
            return None
