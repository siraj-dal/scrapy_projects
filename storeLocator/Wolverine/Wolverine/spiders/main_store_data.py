import datetime
import json
import scrapy
from scrapy.cmdline import execute as ex
from Wolverine.db_config import DbConfig
import urllib.parse
from Wolverine.items import dataItem,stateItem
import os
import hashlib
import requests
from scrapy import Selector
import unicodedata

# ua = UserAgent()
obj = DbConfig()
today_date = datetime.datetime.now().strftime("%d_%m_%Y")
def create_md5_hash(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8'))
    return md5_hash.hexdigest()
def page_write(pagesave_dir, file_name, data):
    if not os.path.exists(pagesave_dir):
        os.makedirs(pagesave_dir)
    file = open(file_name, "w", encoding='utf8')
    file.write(data)
    file.close()
    return "Page written successfully"

class DataSpider(scrapy.Spider):
    name = "provider_data"
    handle_httpstatus_list = [403, 401]

    def __init__(self,start='',end=''):
        self.start = start
        self.end = end

    def start_requests(self):
        qr = f"select * from {obj.store_table} where status='pending' and id between {self.start} and {self.end}"
        print(qr)
        try:
            obj.cur.execute(qr)
            rows = obj.cur.fetchall()
        except Exception as e:
            print(e)
        for row in rows:
            store_no = row['store_no']
            uniq_provider = 'Wolverine'
            country_code = 'US'
            obj.create_provider_data_table()
            hashid = create_md5_hash(f'{uniq_provider}_{country_code}')
            pagesave_dir = rf"C:/Siraj/Actowiz/Desktop/pagesave/{uniq_provider}/{today_date}/HTML"
            print(pagesave_dir)
            file_name = fr"{pagesave_dir}/{hashid}.html"
            meta_dict = {"file_name": file_name, "hashid": hashid, "country_code": country_code,
                         "uniq_provider": uniq_provider, "pagesave_dir": pagesave_dir,"store_no":store_no}
            if os.path.exists(file_name):
                yield scrapy.Request(url='file:///' + file_name, cb_kwargs=meta_dict, callback=self.parse_)
            else:
                import requests
                base_url = 'https://wolverine.locally.com/stores/conversion_data'
                headers = {
                    'accept': 'application/json, text/javascript, */*; q=0.01',
                    'accept-language': 'en-US,en;q=0.9',
                    # 'cookie': 'lg_session_v1=eyJpdiI6IllDZUpNeVUzZnB5RXVvdjArWWpMUmRGYTY2ak1QcGtjMjA0SW5BbW5IWHM9IiwidmFsdWUiOiJoejFKWTg5MDc2c2k2cHhXbko5MmVxaUg4UEJEZFNUTEFaeVlXSTl5UXoyRE5kQ1NVd0lOT0t6dWEzeWI4Y0NMcUdCK3dCVzgwOHJYN2cydHRHS0VHZz09IiwibWFjIjoiZjNmMWQ5MjdkYTJkMDc2MmIyOTExZjQ4MjJkYTUxNTlhMWUyMTBiZmFiNzVjOGZhYjE4MTEzN2U2YTA4ZDQ2YyJ9',
                    'priority': 'u=1, i',
                    'referer': 'https://wolverine.locally.com/conversion?company_name=Wolverine&company_id=1610&inline=1&lang=en-us&currency=USD&no_link=1&dealers_company_id=1610&host_domain=www.wolverine.com',
                    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest',
                }

                params = {
                    'has_data': 'true',
                    'company_id': '1610',
                    'store_mode': '',
                    'style': '',
                    'color': '',
                    'upc': '',
                    'category': '',
                    'inline': '1',
                    'show_links_in_list': '',
                    'parent_domain': '',
                    'map_ne_lat': '63.15806113498567',
                    'map_ne_lng': '-144.08604388124976',
                    'map_sw_lat': '42.55912567337498',
                    'map_sw_lng': '-187.46006731875',
                    'map_center_lat': '52.858593404180326',
                    'map_center_lng': '-165.77305559999988',
                    'map_distance_diag': '2334.772158210643',
                    'sort_by': 'proximity',
                    'no_variants': '0',
                    'only_retailer_id': '',
                    'dealers_company_id': '1610',
                    'only_store_id': 'false',
                    'uses_alt_coords': 'false',
                    'q': 'false',
                    'zoom_level': '4',
                    'lang': 'en-us',
                    'currency': 'USD',
                }

                # Construct the URL
                url = f"{base_url}?{urllib.parse.urlencode(params)}"
                print(url)
                # response = requests.get(url=url, params=params,headers=headers)
                # print(response.text)
                yield scrapy.Request(url=url, headers=headers, cb_kwargs=meta_dict, callback=self.parse_, dont_filter=True)

    def parse_(self,response,**kwargs):
        print("Parse Calling.......")
        file_name = kwargs['file_name']
        hashid = kwargs['hashid']
        country_code = kwargs['country_code']
        uniq_provider = kwargs['uniq_provider']
        pagesave_dir = kwargs['pagesave_dir']
        store_no = kwargs['store_no']
        # print(response.text)

        if "n_markers" in response.text:
            if "markers" in response.text:
                if not os.path.exists(file_name):
                    data_json = response.text.split("<div id")[0]
                    data_json = data_json + '"}'
                    page_write(pagesave_dir, file_name, data_json)
                else:
                    data_json = response.text
                    print("Page Already saved...")
            else:
                print(f"No record Found for {country_code}")
                file_name = str(file_name).replace('.html','') + '_NF.html'
                page_write(pagesave_dir, file_name, response.text)
                c_status = "Not Found"
                obj.update_store_status(c_status,store_no)
                return None
            print(data_json)
            load_json = json.loads(data_json)
            store_list = load_json['markers']
            for i in range(len(store_list)):
                store_no = store_list[i].get('id','')
                name = store_list[i].get('name','')
                latitude = store_list[i].get('lat','')
                longitude = store_list[i].get('lng','')
                street = store_list[i]['address']
                city = store_list[i]['city']
                state = store_list[i]['state']
                zip_code = store_list[i]['zip']
                county = store_list[i]['country']
                phone = store_list[i]['phone']
                provider = uniq_provider
                category = 'Apparel And Accessory Stores'
                updated_date = datetime.datetime.today().strftime("%d-%m-%Y")
                country = store_list[i]['country']
                store_file_name = file_name
                open_hours = ''
                website_url = ''
                status = ''
                direction_url = ''
                if store_no:
                    store_url = f'https://wolverine.locally.com/conversion/location/store/{store_no}?company_id=1610&only_retailer_id=&service=store-locator&lang=en-us&currency=USD'
                    store_headers = {
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                        'accept-language': 'en-US,en;q=0.9',
                        'cache-control': 'max-age=0',
                        # 'cookie': 'lg_session_v1=eyJpdiI6Im4yeTQ3bHFqRXpmbmE4enRuZXlYd3AySENGUE5HVGo5N1pPc3MzZjNGSTg9IiwidmFsdWUiOiJNOVJVaWZcL1hQNHNLNjVNcnptNktMTVNUMXFFcEk3NzR5aTRCNzY5aWRPYURNRGxHTnpLbnVUeHplMVV6TE9jRTBld0dud1V3Tk5Yd3VNdTU2TklVTkE9PSIsIm1hYyI6ImIzOGM1NDM3MmM1YWI4MjQ2ZWI4ZGVmM2I5MzdiNmRmYzYzMTlmZTQwMjhjNWZmNjJhMTZlNDlmYjQ0Y2JkZmMifQ%3D%3D',
                        'priority': 'u=0, i',
                        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'document',
                        'sec-fetch-mode': 'navigate',
                        'sec-fetch-site': 'none',
                        'sec-fetch-user': '?1',
                        'upgrade-insecure-requests': '1',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                    }

                    params = {
                        'company_id': '1610',
                        'only_retailer_id': '',
                        'service': 'store-locator',
                        'lang': 'en-us',
                        'currency': 'USD',
                    }
                    store_file_name = str(file_name).replace('.html', '') + f'_{store_no}.html'
                    store_response = ''
                    if os.path.exists(store_file_name):
                        store_response = open(store_file_name,'r',encoding='utf-8').read()
                    else:
                        store_response = requests.get(url=store_url, headers=store_headers)
                        if "store_html" in store_response.text:
                            store_file_name = str(file_name).replace('.html', '') + f'_{store_no}.html'
                            page_write(pagesave_dir, store_file_name, store_response.text)
                            store_response = store_response.text
                        else:
                            print(f"No record Found for {state}")
                            store_file_name = str(file_name).replace('.html', '') + f'_{store_no}_NF.html'
                            page_write(pagesave_dir, store_file_name, response.text)
                            c_status = "Not Found"
                            obj.update_store_status(c_status, store_no)
                            return None

                    if "store_html" in store_response:
                        store_data = json.loads(store_response)
                        store_html_text = store_data['store_html'] #
                        tab_html_text = store_data['tabs_html'] # tabs_html
                        store_html_data = Selector(text=store_html_text)
                        tab_html_data = Selector(text=tab_html_text)
                        hours_data = tab_html_data.xpath('//a[@id="conv-store-hours-back"]/following-sibling::div//div[@class="store-hours-days"]/div[@class="store-hours-day"]')
                        open_hours = []
                        if hours_data:
                            for hours in hours_data:
                                day_name = hours.xpath('.//span[@class="store-hours-day-label"]//text()').get()
                                open_close_hrs = hours.xpath('.//span[@class="store-hours-time"]//text()').get()
                                if str(open_close_hrs).strip() != "Closed":
                                    begin_time = open_close_hrs.split('-')[0]
                                    end_time = open_close_hrs.split('-')[-1]
                                    day_hours = f"{day_name}:{begin_time}-{end_time}"
                                    if day_hours not in open_hours:
                                        open_hours.append(day_hours)
                                else:
                                    day_hours = f"{day_name}:{open_close_hrs}"
                                    if day_hours not in open_hours:
                                        open_hours.append(day_hours)
                            open_hours = ' | '.join(open_hours)
                        if open_hours and "Closed" not in open_hours:
                            status = "Open"
                        else:
                            status = "Close"

                        website_url = tab_html_data.xpath('//span[contains(text(),"Visit Website")]/../@href').get('')
                        direction_url = store_html_data.xpath('//a[@data-tooltip="Directions" and @rel="noreferrer noopener"]/@href').get('')

                item = dataItem()
                item['store_no'] = store_no
                item['name'] = name
                item['latitude'] = latitude
                item['longitude'] = longitude
                item['street'] = street
                item['city'] = city
                item['state'] = state
                item['zip_code'] = zip_code
                item['county'] = county
                item['phone'] = phone
                item['open_hours'] = open_hours
                item['url'] = website_url
                item['provider'] = provider
                item['category'] = category
                item['updated_date'] = updated_date
                item['country'] = country
                item['status'] = status
                item['direction_url'] = direction_url
                item['pagesave_path'] = store_file_name
                item['search_state'] = state
                print(item)
                yield item
                # Update Store Table
                c_status = "Done"
                obj.update_store_status(c_status,store_no)
        else:
            # Update Store Table
            c_status = "Not Found"
            obj.update_store_status(c_status,store_no)

if __name__ == '__main__':
    ex("scrapy crawl provider_data -a start=1 -a end=1".split())