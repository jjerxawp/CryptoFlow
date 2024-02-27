import scrapy
import json
from ..items import TokenItem
from scrapy.loader import ItemLoader
from urllib.parse import urljoin
from kafka import KafkaProducer



brokers     = ["kafka:9092"]
topic       = "lists"
headers     = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}


def serializer(message):
    return json.dumps(message).encode('utf-8')

def item_to_dict(item):
    """Convert Scrapy Item to dictionary."""
    return {key: item[key] for key in item.keys()}


producer = KafkaProducer(
    bootstrap_servers=brokers,
    value_serializer=serializer,
    api_version=(0, 10, 1)
)

class CoingeckoSpider(scrapy.Spider):
    name = 'coingecko-lists'

    def start_requests(self):
        yield scrapy.Request(
            url="https://api.coingecko.com/api/v3/coins/list?include_platform=true",
            callback=self.parse,
            headers=headers
        )
    def parse(self, response):
        json_data = json.loads(response.body)
        for item_data in json_data:
            item = TokenItem()

            item['gecko_id'] = item_data['id']
            item['symbol'] = item_data['symbol']
            item['name'] = item_data['name']
            item['platforms'] = item_data['platforms']
            loaded_item = item_to_dict(item)
            producer.send(topic=topic, value=loaded_item)
            yield loaded_item