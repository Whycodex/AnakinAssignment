from concurrent.futures import ThreadPoolExecutor, as_completed

class RestaurantParser:
    def __init__(self, logger):
        self.logger = logger

    def parse_merchants(self, merchants, max_workers):
        restaurants = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.parse_restaurant, merchant) for merchant in merchants]
            for future in as_completed(futures):
                restaurants.append(future.result())
        return restaurants

    def parse_restaurant(self, restaurant):
        merchant_brief = restaurant.get("merchantBrief", {})
        estimated_delivery_fee = restaurant.get("estimatedDeliveryFee", {})
        
        return {
            "Restaurant Name": restaurant.get("address", {}).get("name"),
            "Restaurant Cuisine": merchant_brief.get("cuisine"),
            "Restaurant Rating": merchant_brief.get("rating"),
            "Estimate time of Delivery": restaurant.get("estimatedDeliveryTime"),
            "Restaurant Distance from Delivery Location": merchant_brief.get("distanceInKm"),
            "Promotional Offers Listed for the Restaurant": merchant_brief.get("promo"),
            "Restaurant Notice If Visible": merchant_brief.get("operationHours"),
            "Image Link of the Restaurant": merchant_brief.get("photoHref"),
            "Is promo available": bool(merchant_brief.get("promo")),
            "Restaurant ID": restaurant.get("id"),
            "Restaurant latitude and longitude": {
                "latitude": restaurant.get("latlng", {}).get("latitude"),
                "longitude": restaurant.get("latlng", {}).get("longitude"),
            },
            "Estimate Delivery Fee": estimated_delivery_fee.get("priceDisplay")
        }
