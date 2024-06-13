from fetcher import DataFetcher
from parser import RestaurantParser
from saver import DataSaver
from logger import setup_logger

def main():
    BASE_URL = "https://portal.grab.com/foodweb/v2/search"
    HEADERS = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json",
        "X-Grab-Web-App-Version": "aAdsDhvSiBCysq_aKGUvA",
        "X-Hydra-Jwt": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnYWEiLCJhdWQiOiJnZnciLCJuYW1lIjoiZ3JhYnRheGkiLCJpYXQiOjE3MTgyODAzMzAsImV4cCI6MTcxODI4MDkzMCwibmJmIjoxNzE4MjgwMzMwLCJ2ZXIiOiIxLjE5LjAuMjQiLCJicklEIjoiZmViM2I2ZDU3YjI1NjE3ZWU1OTUzYWY0NDU0NmQ2ZjVjNTJ5NnIiLCJzdXMiOmZhbHNlLCJicklEdjIiOiJhYWY3MzczMzk1MTAyYWY2OWIwODc1ZmRmMzNiYmViYTkyZnk2ciIsImJyVUlEIjoiOWU4YjcwMDctOTc1Zi00ZTBmLTg2N2EtZGZhNWEzNWM1ZGM3In0.mzJWMCbfIRul0v5tvyvDdtE4BqHI6nVPvXlAg6UNjYXpfIo94YHA2zhtvFsIPyG-18Z7wyxd6y6PdAMJhLOFrEyigfLhL33wlwFb1Z_vrdws2rr3JJ7fNVqoDttSguXDJVlMxCfCoXqipyJ3FNk6RNkv_07HzyMMn_7B-gmwN_24-8z_HzjMuB1ZqRJXUzcFGLv9ADiIdlX02nO9vGARxwGmLgEVieR17Sy149hXsEpG0sFWyCMo5TVGE8Dp7ZiAgU7orBXPiPPvMxV4BhSErf99GmNciLXp-k4sWqlfqqUefExCWc6j7nL-xinFTw-OVrBAJrD-wj-OsRwlKl_SxQ"
    }
    BODY_TEMPLATE = {
        "latlng": "1.396364,103.747462",
        "keyword": "",
        "offset": 0,
        "pageSize": 32,
        "countryCode": "SG"
    }

    logger = setup_logger()
    
    fetcher = DataFetcher(BASE_URL, HEADERS, BODY_TEMPLATE, logger)
    parser = RestaurantParser(logger)
    saver = DataSaver('restaurants.ndjson.gz', logger)

    max_results = 25
    max_workers = 10

    restaurants = []
    offset = 0
    
    while len(restaurants) < max_results:
        logger.info(f"Fetching data from offset: {offset}")
        data = fetcher.fetch_data(offset)
        if not data or 'searchResult' not in data or 'searchMerchants' not in data['searchResult']:
            break
        
        merchants = data['searchResult']['searchMerchants']
        restaurants.extend(parser.parse_merchants(merchants, max_workers))
        
        if len(merchants) < BODY_TEMPLATE['pageSize']:
            break
        
        offset += len(merchants)

    logger.info(f"Scraped {len(restaurants)} restaurants")
    saver.save_data(restaurants)

if __name__ == "__main__":
    main()
