import scrapy
from blocket_scraper.items import BlocketScraperItem
import urllib.parse

class BlocketSpider(scrapy.Spider):
    name = 'blocket'
    allowed_domains = ['api.blocket.se']

    drivetrains = [
        "Fyrhjulsdriven", 
        "Tvåhjulsdriven"
    ]
    chassis = [
        "SUV", 
        "Kombi", 
        "Halvkombi", 
        "Yrkesfordon", 
        "Sedan", 
        "Coupé", 
        "Familjebuss", 
        "Cab"
    ]
    colors = [
        "Blå",
        "Brun",
        "Grå",
        "Grön",
        "Gul",
        "Röd",
        "Svart",
        "Vit"
    ]
    ownership_type = "Köpa"

    def start_requests(self):
        # Iterate through all combinations of drivetrain, chassis, and color
        for drivetrain in self.drivetrains:
            for chassi in self.chassis:
                for color in self.colors:
                    url = (
                        f'https://api.blocket.se/motor-search-service/v4/search/car?'
                        f'filter={urllib.parse.quote(f"{{\"key\":\"drivetrain\",\"values\":[\"{drivetrain}\"]}}")}&'
                        f'filter={urllib.parse.quote(f"{{\"key\":\"chassi\",\"values\":[\"{chassi}\"]}}")}&'
                        f'filter={urllib.parse.quote(f"{{\"key\":\"color\",\"values\":[\"{color}\"]}}")}&'
                        f'filter={urllib.parse.quote(f"{{\"key\":\"ownershipType\",\"values\":[\"{self.ownership_type}\"]}}")}&page=1'
                    )
                    yield scrapy.Request(
                        url,
                        callback=self.parse,
                        meta={'drivetrain': drivetrain, 'chassi': chassi, 'color': color, 'ownership_type': self.ownership_type}
                    )

    def parse(self, response):
        # Covert json response into python dictionary
        data = response.json()

        drivetrain = response.meta['drivetrain']
        chassi = response.meta['chassi']
        color = response.meta['color']

        for car in data.get('cars', []):
            item = BlocketScraperItem()
            item['dealId'] = car.get('dealId')
            item['link'] = car.get('link')
            item['listTime'] = car.get('listTime')
            item['originalListTime'] = car.get('originalListTime')
            item['seller_name'] = car.get('seller', {}).get('name')
            item['seller_type'] = car.get('seller', {}).get('type')
            item['drivetrain'] = drivetrain  # Add drivetrain to item
            item['chassi'] = chassi  # Add chassi to item
            item['color'] = color  # Add color to item
            item['heading'] = car.get('heading')
            item['price_amount'] = car.get('price', {}).get('amount')
            item['price_billing_period'] = car.get('price', {}).get('billingPeriod')
            item['ownership_type'] = response.meta['ownership_type']
            item['thumbnail'] = car.get('thumbnail')
            item['region'] = car.get('car', {}).get('location', {}).get('region')
            item['municipality'] = car.get('car', {}).get('location', {}).get('municipality')
            item['area'] = car.get('car', {}).get('location', {}).get('area')
            item['fuel'] = car.get('car', {}).get('fuel')
            item['gearbox'] = car.get('car', {}).get('gearbox')
            item['regDate'] = car.get('car', {}).get('regDate')
            item['mileage'] = car.get('car', {}).get('mileage')
            item['equipment'] = [equip['label'] for equip in (car.get('car', {}).get('equipment') or []) if isinstance(equip, dict) and 'label' in equip]
            item['description'] = car.get('description')
            item['images'] = [image['image'] for image in (car.get('car', {}).get('images') or []) if isinstance(image, dict) and 'image' in image]

            yield item

        # Handle pagination
        current_page = int(response.url.split("page=")[-1])
        # total_pages = data.get('pages', 1)
        total_pages = 1

        # If there are more pages, send a new request for the next page
        if current_page < total_pages:
            next_page = current_page + 1
            next_page_url = response.url.split("&page=")[0] + f"&page={next_page}"
            yield scrapy.Request(next_page_url, callback=self.parse)