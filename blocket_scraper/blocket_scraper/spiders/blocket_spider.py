import scrapy
from blocket_scraper.items import BlocketScraperItem

class BlocketSpider(scrapy.Spider):
    name = 'blocket'
    allowed_domains = ['api.blocket.se']
    start_urls = [
        'https://api.blocket.se/motor-search-service/v4/search/car?filter=%7B%22key%22%3A%22region%22%2C%22values%22%3A%5B%22G%C3%B6teborg%22%5D%7D&filter=%7B%22key%22%3A%22price%22%2C%22range%22%3A%7B%22start%22%3A%2210000%22%2C%22end%22%3A%22%22%7D%7D&sortOrder=Billigast&page=1'
    ]

    def parse(self, response):
        # Covert json response into python dictionary
        data = response.json()

        for car in data.get('cars', []):
            item = BlocketScraperItem()
            item['dealId'] = car.get('dealId')
            item['link'] = car.get('link')
            item['listTime'] = car.get('listTime')
            item['originalListTime'] = car.get('originalListTime')
            item['seller_name'] = car.get('seller', {}).get('name')
            item['seller_type'] = car.get('seller', {}).get('type')
            item['heading'] = car.get('heading')
            item['price_amount'] = car.get('price', {}).get('amount')
            item['price_billing_period'] = car.get('price', {}).get('billingPeriod')
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
        current_page = response.url.split("page=")[-1]
        total_pages = data.get('pages', 1)

        # If there are more pages, send a new request for the next page
        if int(current_page) < total_pages:
            next_page = int(current_page) + 1
            next_page_url = f'https://api.blocket.se/motor-search-service/v4/search/car?filter=%7B%22key%22%3A%22region%22%2C%22values%22%3A%5B%22G%C3%B6teborg%22%5D%7D&filter=%7B%22key%22%3A%22price%22%2C%22range%22%3A%7B%22start%22%3A%2210000%22%2C%22end%22%3A%22%22%7D%7D&sortOrder=Billigast&page={next_page}'
            yield scrapy.Request(next_page_url, callback=self.parse)