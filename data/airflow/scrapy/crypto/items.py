# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst

class CoingeckoCoinItems(scrapy.Item):
    gecko_id = scrapy.Field(
        output_processor=TakeFirst()
    )
    symbol = scrapy.Field(
        output_processor=TakeFirst()
    )
    name = scrapy.Field(
        output_processor=TakeFirst()
    )
    current_price = scrapy.Field(
        output_processor=TakeFirst()
    )
    market_cap = scrapy.Field(
        output_processor=TakeFirst()
    )
    market_cap_rank = scrapy.Field(
        output_processor=TakeFirst()
    )
    fully_diluted_valuation = scrapy.Field(
        output_processor=TakeFirst()
    )
    total_volume = scrapy.Field(
        output_processor=TakeFirst()
    )
    high_24h = scrapy.Field(
        output_processor=TakeFirst()
    )
    low_24h = scrapy.Field(
        output_processor=TakeFirst()
    )
    price_change_24h = scrapy.Field(
        output_processor=TakeFirst()
    )
    price_change_percentage_24h = scrapy.Field(
        output_processor=TakeFirst()
    )
    circulating_supply = scrapy.Field(
        output_processor=TakeFirst()
    )
    total_supply = scrapy.Field(
        output_processor=TakeFirst()
    )
    max_supply = scrapy.Field(
        output_processor=TakeFirst()
    )
    ath = scrapy.Field(
        output_processor=TakeFirst()
    )
    ath_change_percentage = scrapy.Field(
        output_processor=TakeFirst()
    )
    ath_date = scrapy.Field(
        output_processor=TakeFirst()
    )
    atl = scrapy.Field(
        output_processor=TakeFirst()
    )
    atl_change_percentage = scrapy.Field(
        output_processor=TakeFirst()
    )
    atl_date = scrapy.Field(
        output_processor=TakeFirst()
    )
    last_updated = scrapy.Field(
        output_processor=TakeFirst()
    )

class TokenItem(scrapy.Item):
    gecko_id = scrapy.Field()
    symbol = scrapy.Field()
    name = scrapy.Field()
    platforms = scrapy.Field()