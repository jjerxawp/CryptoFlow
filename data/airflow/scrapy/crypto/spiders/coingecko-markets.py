import scrapy
import json
from ..items import CoingeckoCoinItems
from scrapy.loader import ItemLoader
from urllib.parse import urljoin

from kafka import KafkaProducer

brokers     = ["kafka:9092"]
topic       = "markets"
headers     = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

def serializer(message):
    return json.dumps(message).encode('utf-8')

producer = KafkaProducer(
    bootstrap_servers=brokers,
    value_serializer=serializer,
    api_version=(0, 10, 1)
)
def item_to_dict(item):
    """Convert Scrapy Item to dictionary."""
    return {key: item[key] for key in item.keys()}

class CoingeckoSpider(scrapy.Spider):
    name = 'coingecko-markets'

    def start_requests(self):
        yield scrapy.Request(
            url="https://api.coingecko.com/api/v3/coins/list?include_platform=true",
            callback=self.coins_listing,
            headers=headers
        )
    
    def parse(self, response):
        details = json.loads(response.body)
        for detail in details:
            item = CoingeckoCoinItems()
            item['gecko_id'] = detail.get("id")
            item['symbol'] = detail.get("symbol")
            item['name'] = detail.get("name")
            item['current_price'] = detail.get("current_price")
            item['market_cap'] = detail.get("market_cap")
            item['market_cap_rank'] = detail.get("market_cap_rank")
            item['fully_diluted_valuation'] = detail.get("fully_diluted_valuation")
            item['total_volume'] = detail.get("total_volume")
            item['high_24h'] = detail.get("high_24h")
            item['low_24h'] = detail.get("low_24h")
            item['price_change_24h'] = detail.get("price_change_24h")
            item['price_change_percentage_24h'] = detail.get("price_change_percentage_24h")
            item['circulating_supply'] = detail.get("circulating_supply")
            item['total_supply'] = detail.get("total_supply")
            item['max_supply'] = detail.get("max_supply")
            item['ath'] = detail.get("ath")
            item['ath_change_percentage'] = detail.get("ath_change_percentage")
            item['ath_date'] = detail.get("ath_date")
            item['atl'] = detail.get("ath_change_percentage")
            item['atl_change_percentage'] = detail.get("atl_change_percentage")
            item['atl_date'] = detail.get("atl_date")
            item['last_updated'] = detail.get("last_updated")
            loaded_item = item_to_dict(item)
            producer.send(topic=topic, value=loaded_item)
            yield item

    def coins_listing(self, response):

        base_url = "https://api.coingecko.com/api/v3/coins/markets"

        # Configuration parameters
        vs_currency = "usd"
        gecko_id = ""
        order = "market_cap_desc"
        per_page = 50
        page = 1
        sparkline = False
        locale = "en"

        # Construct the API URL with parameters
        api_params = {
            'vs_currency': vs_currency,
            'ids': gecko_id,
            'order': order,
            'per_page': per_page,
            'page': page,
            'sparkline': sparkline,
            'locale': locale
        }

        coins = json.loads(response.body)
        print(len(coins))
        current_pos = 0
        new_pos = 50
        while (current_pos < len(coins)) and (new_pos <= 100):
            
            gecko_id_list = []
            
            for coin in coins[current_pos:new_pos]:
                coin_gecko_id = coin.get("id")
                gecko_id_list.append(coin_gecko_id)

            join_gecko_id = ','.join(gecko_id_list)
            loop_coin_id = {"ids":join_gecko_id}
            api_params |= loop_coin_id
            api_url = urljoin(
                base_url,
                '?' + '&'.join(f"{key}={value}" for key, value in api_params.items())
            )

            yield scrapy.Request(
                url=api_url,
                callback=self.parse,
                headers=headers
            )
            gecko_id_list.clear()
            current_pos = new_pos
            new_pos += 50