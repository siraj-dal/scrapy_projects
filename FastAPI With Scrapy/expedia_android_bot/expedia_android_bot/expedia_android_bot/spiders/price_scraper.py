import hashlib
import json
import os
from datetime import datetime

import pymysql
from typing import Iterable
from pymysql.connections import Connection
from pymysql.cursors import Cursor
from scrapy.cmdline import execute


import scrapy
from scrapy import Request

from expedia_android_bot import headers
from expedia_android_bot.items import ExpediaAndroidBotItem


class PriceScraperSpider(scrapy.Spider):
    name: str = "price_scraper"
    allowed_domains: list = ["expedia.com"]

    today_date: str = datetime.today().strftime('%Y_%m_%d')
    config_file: str = "C:/project_files/travel_project/expedia/project_configs.json"

    if os.path.exists(config_file):
        with open(config_file, 'r') as config:
            configs: dict = json.load(config)
    else:
        project_config_path: str = "/".join(config_file.split('/')[:-1])
        os.makedirs(project_config_path)

        print(f'Project config file missing, please add project config file on path as {config_file}')
        exit(-1)

    pricing_page_save: str = "C:/project_files/travel_project/expedia/pricing_page_save" + f"/{today_date}"

    for path in [pricing_page_save]:
        if not os.path.exists(path):
            os.makedirs(path)

    client: Connection = pymysql.connect(host=configs['config']['host'],
                                         user=configs['config']['user'],
                                         password=configs['config']['password'],
                                         database=configs['config']['database'])
    cursor: Cursor = client.cursor()

    daily_link_table: str = configs['tables']['link_table'] + '_' + today_date

    def __init__(self, name=None, start=None, end=None, **kwargs):
        super().__init__(name, **kwargs)
        self.start = start
        self.end = end

    def start_requests(self) -> Iterable[Request]:
        fetch = f"""
        SELECT id, url, hotel_url, hotel_id, hotel_name, hotel_address, currency, checkin_date, checkout_date
        FROM {self.daily_link_table} 
        WHERE status='Pending'
        and id between {self.start} and {self.end}
"""

        self.cursor.execute(fetch)
        fetched_data: tuple = self.cursor.fetchall()
        print('Fetched URLs', len(fetched_data))

        for url_id, url, hotel_url, hotel_id, hotel_name, hotel_address, currency, checkin_date, checkout_date in fetched_data:
            yield scrapy.Request(url=url.replace('com.br', 'com'),
                                 meta={"impersonate": 'chrome99_android'},
                                 headers=headers.headers,
                                 cb_kwargs={"url_id": url_id,
                                            "req_url": url,
                                            "hotel_id": hotel_id,
                                            "hotel_url": hotel_url,
                                            "hotel_name": hotel_name,
                                            "hotel_address": hotel_address,
                                            "currency": currency,
                                            "checkin_date": checkin_date,
                                            "checkout_date": checkout_date})
            # break

    def parse(self, response, **kwargs):
        json_data = json.loads(response.text)
        data = dict()

        pricing_page_hash: str = hashlib.sha256((kwargs['req_url']).encode()).hexdigest()
        data['page_hash'] = pricing_page_hash

        with open(self.pricing_page_save + '/' + f'{pricing_page_hash}.html', 'wb') as page:
            page.write(response.body)

        listing_data = json_data['data']['propertyOffers']['categorizedListings']

        data['id'] = kwargs['url_id']
        data['hotel_id'] = kwargs['hotel_id']
        data['hotel_url'] = kwargs['hotel_url']
        data['hotel_name'] = kwargs['hotel_name']
        data['hotel_address'] = kwargs['hotel_address']
        data['currency'] = kwargs['currency']
        data['checkin_date'] = kwargs['checkin_date']
        data['checkout_date'] = kwargs['checkout_date']

        if listing_data:
            for room_category in listing_data:
                scraped_data = ExpediaAndroidBotItem()
                data['id'] = kwargs['url_id']
                data['room_id'] = room_category['unitId'] if 'unitId' in room_category else 'NA'
                data['room_name'] = room_category['header']['text'] if 'header' in room_category else 'NA'

                if 'features' in room_category:
                    for feature in room_category['features']:
                        if 'Sleeps' in feature['text']:
                            data['occupancy'] = feature['text'].replace('Sleeps ', '')

                if 'primarySelections' in room_category:
                    data['availability'] = True if not room_category['primarySelections'][0]['propertyUnit']['availabilityCallToAction'] else False
                else:
                    data['availability'] = False
                try:
                    data['room_price'] = room_category['primarySelections'][0]['propertyUnit']['ratePlans'][0]['priceDetails'][0]['price']['displayMessages'][0]['lineItems'][0]['price']['formatted'].replace('$', '').replace(',', '').replace('MXN', '').replace('R\xa0', '')
                    data['tax_amount'] = room_category['primarySelections'][0]['propertyUnit']['ratePlans'][0]['priceDetails'][0]['pricePresentation']['sections'][0]['subSections'][0]['items'][-1]['enrichedValue']['primaryMessage']['primary'].replace('$', '').replace(',', '').replace('MXN', '').replace('R\xa0', '')
                except Exception as e:
                    data['room_price'] = 'NA'
                    data['tax_amount'] = 'NA'

                for key in data:
                    scraped_data[key] = data[key]
                yield scraped_data
        else:
            scraped_data = ExpediaAndroidBotItem()
            data['id'] = kwargs['url_id']
            data['room_id'] = 'NA'
            data['room_name'] = 'NA'
            data['availability'] = False
            data['occupancy'] = 'NA'
            data['room_price'] = 'NA'
            data['tax_amount'] = 'NA'

            for key in data:
                scraped_data[key] = data[key]
            yield scraped_data


if __name__ == '__main__':
    execute(f"scrapy crawl {PriceScraperSpider.name} -a start=1 -a end=4650".split())
    # execute(f"scrapy crawl {PriceScraperSpider.name} -a start=2 -a end=2".split())
    # import sys
    # start = int(sys.argv[1])
    # end = int(sys.argv[2])
    # execute(f"scrapy crawl {PriceScraperSpider.name} -a start={start} -a end={end}".split())
