import datetime
import os
import urllib.parse
from typing import Iterable
import json
import gzip
import pymysql
import scrapy
from scrapy import Request
from scrapy.cmdline import execute
from storeLocator import db_config
from storeLocator.items import StorelocatorItem


def dynamic_drive(delivery_date, company):
    drives = os.listdrives()
    drives_remove = ['C:\\', 'Z:\\']
    for drive in drives_remove:
        if drive in drives:
            del drives[drives.index(drive)]
    if drives:
        drive = 'D' if 'D:\\' in drives else drives[0][0]
    else:
        drive = 'C'
    page_save_path = fr'{drive}:/Project Files Live (using Scrapy)/storeLocator/{delivery_date}/{company}/'
    os.makedirs(page_save_path, exist_ok=True)
    return page_save_path


def get_store_no(store_dict):
    store_no = store_dict['storeId']
    return store_no


def get_store_name(store_dict):
    store_name = store_dict['title']
    return store_name


def get_lat(store_dict):
    lat = store_dict['latitude']
    return lat


def get_lon(store_dict):
    lon = store_dict['longitude']
    return lon


def get_street(store_dict):
    street = store_dict['street1']
    return street


def get_city(store_dict):
    city = store_dict['city']
    return city


def get_postal_code(store_dict):
    postal_code = store_dict['postalCode']
    return postal_code


def get_phone(store_dict):
    phone = store_dict['phone']
    return phone


def get_url(store_dict):
    url = store_dict['storeWeb']
    return url


def get_direction_url(store_dict):
    direction_url = f'https://maps.apple.com/?saddr={store_dict['latitude']},{store_dict['longitude']}&daddr=32.3050651550293,-90.18304443359375&&hl=en'
    return direction_url


def get_county(store_dict):
    county = store_dict.get('district', 'N/A')
    return county


def get_date():
    return datetime.date.today().strftime('%d-%m-%Y')


class AppleSpider(scrapy.Spider):
    name = "apple"

    # allowed_domains = ["abc.com"]
    # start_urls = ["https://abc.com"]
    # today_date_time = db_config.delivery_date_time

    def __init__(self):
        """Initialize database connection and set file paths."""
        # self.page_save_path = rf'C:\Project Files Live (using Scrapy)\storeLocator\{self.today_date_time}\{self.name}'
        self.client = pymysql.connect(host=db_config.db_host, user=db_config.db_user, password=db_config.db_password, database=db_config.db_name, autocommit=True)
        self.cursor = self.client.cursor()  # Create a cursor object to interact with the database

        self.input_table = 'states_store_locator'

    def start_requests(self) -> Iterable[Request]:
        """Generates initial requests with cookies and headers."""
        # cookies_ms = {
        #     'geo': 'IN',
        #     'at_check': 'true',
        #     'dssid2': '6b9372ea-095c-4f93-889d-eab853f11a0e',
        #     'dssf': '1',
        #     'as_pcts': 'eKBku4cb+8BOgP1Zs-+DKsL6Nzv-BFZCIjQ6jdlptOFpMirr32q0kE2:tSpUvFL-OLpWEkNGi+ghrtVZtsI92xM6oxZUii+wwKuskIMv7JTBDDuS-:j3BQBkrdXDDiP-BAen:d-I7XBIY1B4Bcu3KsiIa+rR-J5-oQM0TEOwwoZUnrfO1',
        #     's_cc': 'true',
        #     'route': '1726490777.838.37.824861|90c93c2533ff58fc0c23c45e84411b26',
        #     'pt-dm': 'v1~x~3wp1bzq4~m~2~n~retail%20-%20overview%20(us)',
        #     'mk_epub': '%7B%22btuid%22%3A%221081xtj%22%2C%22events%22%3A%22event220%3D0.606%2Cevent221%3D0.000%2Cevent222%3D0.000%2Cevent223%3D0.000%2Cevent224%3D1.900%2Cevent225%3D0.036%2Cevent226%3D0.710%2Cevent227%3D0.439%2Cevent228%3D0.477%2Cevent229%3D1.629%2C%22%2C%22prop57%22%3A%22www.us.retailstore%22%7D',
        #     's_fid': '0580027CEB4B4528-170BAE4A53697C5D',
        #     's_vi': '[CS]v1|3374838D85A60460-40001FD8C1AD850F[CE]',
        #     'as_dc': 'ucp5',
        #     'SESSION': 'f990332b-65e7-4fa9-84f5-952962508344',
        #     's_ppvl': 'acs%253A%253Atools%253A%253Acontact%253A%253Afind%2520locations%253A%253Asales%2520%2528en-us%2529%2C52%2C52%2C587.8000030517578%2C1536%2C423%2C1536%2C864%2C1.25%2CP',
        #     's_ppv': 'acs%253A%253Atools%253A%253Acontact%253A%253Afind%2520locations%253A%253Asales%2520%2528en-us%2529%2C83%2C40%2C1461%2C1536%2C423%2C1536%2C864%2C1.25%2CP',
        #     's_sq': 'applesupportlocateprod%3D%2526pid%253Dacs%25253A%25253Atools%25253A%25253Acontact%25253A%25253Afind%252520locations%25253A%25253Asales%252520%252528en-us%252529%2526pidt%253D1%2526oid%253DfunctionBr%252528%252529%25257B%25257D%2526oidt%253D2%2526ot%253DSUBMIT',
        # }
        #
        # headers_ms = {
        #     'accept': 'application/json, text/plain, */*',
        #     'accept-language': 'en-US,en;q=0.9',
        #     'priority': 'u=1, i',
        #     # 'referer': 'https://locate.apple.com/sales?pt=all&lat=32.3050651550293&lon=-90.18304443359375&address=Mississippi',
        #     'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        #     'sec-ch-ua-mobile': '?0',
        #     'sec-ch-ua-platform': '"Windows"',
        #     'sec-fetch-dest': 'empty',
        #     'sec-fetch-mode': 'cors',
        #     'sec-fetch-site': 'same-origin',
        #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        # }
        #
        # params_ms = {
        #     'pt': 'all',
        #     'lat': '32.3050651550293',
        #     'lon': '-90.18304443359375',
        #     'carrier': '',
        #     'maxrad': '100',
        #     'maxResult': '99',
        #     'repairType': '',
        # }
        fetch = f'''SELECT index_id, state, lat, lon FROM {self.input_table} where status = "pending"'''
        self.cursor.execute(fetch)
        results = self.cursor.fetchall()
        for result in results:
            index_id = result[0]
            state = result[1]
            lat = result[2]
            lon = result[3]
            cookies = {
                'geo': 'IN',
                'at_check': 'true',
                'dssid2': '6b9372ea-095c-4f93-889d-eab853f11a0e',
                'dssf': '1',
                'as_pcts': 'eKBku4cb+8BOgP1Zs-+DKsL6Nzv-BFZCIjQ6jdlptOFpMirr32q0kE2:tSpUvFL-OLpWEkNGi+ghrtVZtsI92xM6oxZUii+wwKuskIMv7JTBDDuS-:j3BQBkrdXDDiP-BAen:d-I7XBIY1B4Bcu3KsiIa+rR-J5-oQM0TEOwwoZUnrfO1',
                's_cc': 'true',
                'route': '1726490777.838.37.824861|90c93c2533ff58fc0c23c45e84411b26',
                'pt-dm': 'v1~x~3wp1bzq4~m~2~n~retail%20-%20overview%20(us)',
                'mk_epub': '%7B%22btuid%22%3A%221081xtj%22%2C%22events%22%3A%22event220%3D0.606%2Cevent221%3D0.000%2Cevent222%3D0.000%2Cevent223%3D0.000%2Cevent224%3D1.900%2Cevent225%3D0.036%2Cevent226%3D0.710%2Cevent227%3D0.439%2Cevent228%3D0.477%2Cevent229%3D1.629%2C%22%2C%22prop57%22%3A%22www.us.retailstore%22%7D',
                's_fid': '0580027CEB4B4528-170BAE4A53697C5D',
                's_vi': '[CS]v1|3374838D85A60460-40001FD8C1AD850F[CE]',
                'as_dc': 'ucp5',
                's_ppvl': 'acs%253A%253Atools%253A%253Acontact%253A%253Afind%2520locations%253A%253Asales%2520%2528en-us%2529%2C81%2C81%2C1189.4000244140625%2C1536%2C423%2C1536%2C864%2C1.25%2CP',
                'SESSION': '0265ee5d-a669-42f6-a305-7f1430b893a7',
                's_ppv': 'acs%253A%253Atools%253A%253Acontact%253A%253Afind%2520locations%253A%253Asales%2520%2528en-us%2529%2C83%2C81%2C1211%2C1536%2C423%2C1536%2C864%2C1.25%2CP',
                's_sq': 'applesupportlocateprod%3D%2526pid%253Dacs%25253A%25253Atools%25253A%25253Acontact%25253A%25253Afind%252520locations%25253A%25253Asales%252520%252528en-us%252529%2526pidt%253D1%2526oid%253DfunctionBr%252528%252529%25257B%25257D%2526oidt%253D2%2526ot%253DSUBMIT',
            }

            headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'en-US,en;q=0.9',
                'priority': 'u=1, i',
                'referer': f'https://locate.apple.com/sales?pt=all&lat={lat}"&lon={lon}&address={state}',
                'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            }

            params = {
                'pt': 'all',
                'lat': lat,
                'lon': lon,
                'carrier': '',
                'maxrad': '100',
                'maxResult': '99',
                'repairType': '',
            }

            browsers = [
                "chrome110",
                "edge99",
                "safari15_5"
            ]
            # meta = {"impersonate": random.choice(browsers)}

            area_latlon = [
                ('MS', '32.3050651550293', '-90.18304443359375'),
                ('IN', '39.7672004699707', '-86.16349792480469')
            ]
            url = 'https://locate.apple.com/api/v1/grlui/us/en/sales'
            url = url + '?' + urllib.parse.urlencode(params)
            # cb_kwargs = {'state_code': area[0]}
            cb_kwargs = {'state': state, 'index_id': index_id}
            yield scrapy.Request(url=url,
                                 cookies=cookies,
                                 headers=headers,
                                 # meta=meta,
                                 dont_filter=True,
                                 cb_kwargs=cb_kwargs
                                 )

    def parse(self, response, **kwargs):
        cb_kwargs = response.cb_kwargs
        # state_code = cb_kwargs['state_code']
        index_id = cb_kwargs['index_id']
        state = cb_kwargs['state']
        file_path = dynamic_drive(delivery_date=db_config.delivery_date, company=self.name)
        filename = file_path + self.name + '_' + state + ".html.gz"
        gzip.open(filename, "wb").write(response.body)
        print('Page saved.')

        response_dict = json.loads(response.text)
        stores_list = response_dict['results']['stores']
        for store_dict in stores_list:
            item = StorelocatorItem()
            item['index_id'] = index_id

            item['store_no'] = get_store_no(store_dict)
            item['name'] = get_store_name(store_dict)
            item['latitude'] = get_lat(store_dict)
            item['longitude'] = get_lon(store_dict)
            item['street'] = get_street(store_dict)
            item['city'] = get_city(store_dict)
            item['state'] = store_dict['state']
            item['zip_code'] = get_postal_code(store_dict)
            item['county'] = get_county(store_dict)
            item['phone'] = get_phone(store_dict)
            item['open_hours'] = 'N/A'
            item['url'] = get_url(store_dict)
            item['provider'] = 'Apple'
            item['category'] = 'Computer And Electronics Stores'
            item['updated_date'] = get_date()
            item['country'] = 'USA'
            item['status'] = 'Open'
            item['direction_url'] = get_direction_url(store_dict)
            # print('item', item)
            print('*' * 50)
            yield item
        print('-' * 100)


if __name__ == '__main__':
    execute(f'scrapy crawl {AppleSpider.name}'.split())
