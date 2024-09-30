import datetime
import json
import scrapy
from scrapy.cmdline import execute as ex
from Oiselle.db_config import DbConfig
# from fake_useragent import UserAgent
from Oiselle.items import dataItem,stateItem
import os
import hashlib

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
        qr = f"select * from {obj.store_table} where status='Pending' and index_id between {self.start} and {self.end}"
        print(qr)
        try:
            obj.cur.execute(qr)
            rows = obj.cur.fetchall()
        except Exception as e:
            print(e)
        uniq_provider = 'Oiselle'
        for row in rows:
            search_state = row['state']
            lat = row['latitude']
            long = row['longitude']
            lat_lng = row['lat_lng']
            # create table for provider data
            obj.create_provider_data_table()
            hashid = create_md5_hash(f'{lat_lng}_{uniq_provider}_{search_state}')
            pagesave_dir = rf"C:/Siraj/Actowiz/Desktop/pagesave/{uniq_provider}/{today_date}/HTML"
            print(pagesave_dir)
            file_name = fr"{pagesave_dir}/{hashid}.html"
            meta_dict = {"file_name" : file_name,"hashid":hashid,"search_state":search_state,"lat_lng":lat_lng,"uniq_provider":uniq_provider,"pagesave_dir":pagesave_dir}
            if os.path.exists(file_name):
                yield scrapy.Request(url='file:///'+file_name,cb_kwargs=meta_dict,callback=self.parse_)
            else:
                import requests
                url = f'https://easylocator.net/ajax/search_by_lat_lon/Oiselle%20Dealer%20Search/{lat}/{long}/2000/10/null/null'
                headers = {
                    'accept': 'application/json, text/javascript, */*; q=0.01',
                    'accept-language': 'en-US,en;q=0.9',
                    'priority': 'u=1, i',
                    'referer': 'https://easylocator.net/search/map3/Oiselle%20Dealer%20Search/template/template3_2',
                    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest',
                }
                # Try to request with requests module...
                # response = requests.get(
                #     f'https://easylocator.net/ajax/search_by_lat_lon/Oiselle%20Dealer%20Search/{lat}/{long}/2000/10/null/null',
                #     headers=headers,
                # )
                # print(response.text)
                
                yield scrapy.Request(url=url,method="POST",headers=headers,cb_kwargs=meta_dict,callback=self.parse_,dont_filter=True)

    def parse_(self,response,**kwargs):
        print("Parse Calling.......")
        file_name = kwargs['file_name']
        hashid = kwargs['hashid']
        search_state = kwargs['search_state']
        uniq_provider = kwargs['uniq_provider']
        pagesave_dir = kwargs['pagesave_dir']
        lat_lng = kwargs['lat_lng']
        print(response.text)
        json_data = json.loads(response.text)
        collection_count = ''
        try:
            physical_count = len(json_data['physical'])
            online_count = len(json_data['online'])
            if physical_count == 0  and online_count == 0:
                collection_count = 0
            else:
                collection_count = physical_count + online_count
        except:
            collection_count = 0

        if int(collection_count) >= 1:
            page_write(pagesave_dir, file_name, response.text)
        else:
            print(f"No record Found for {search_state}")
            file_name = file_name + '_NF'
            page_write(pagesave_dir, file_name, response.text)
            c_status = "Not Found"
            obj.update_store_status(c_status,search_state)
            return None

        # Start the Crawl the data
        store_list_type = ['physical','online']
        for store_type in store_list_type:
            store_list = json_data[f'{store_type}']
            for i in range(len(store_list)):
                store_no = store_list[i]['id']
                name = store_list[i]['name']
                latitude = store_list[i]['lat']
                longitude = store_list[i]['lon']
                street_1 = store_list[i]['street_address']
                street_2 = store_list[i]['street_address_line2']
                street_3 = store_list[i]['street_address_line3']
                street = f"{street_1} {street_2} {street_3}"
                city = store_list[i]['city']
                state = store_list[i]['state_province']
                zip_code = store_list[i]['zip_postal_code']
                county = store_list[i]['country']
                if not county or county == "United States":
                    county = "US"
                phone = store_list[i]['phone']
                open_hours = ''
                store_status = "Open"
                website_url = store_list[i]['website_url']
                if website_url and ('http://' or 'https://') not in website_url:
                    website_url = 'http://' + website_url
                provider = uniq_provider
                category = 'Apparel And Accessory Stores'
                updated_date = datetime.datetime.today().strftime("%d-%m-%Y")
                country = store_list[i]['country']
                if not country or country == "United States":
                    country = "US"
                status = store_status
                direction_url = ""
                pagesave_path = file_name

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
                item['pagesave_path'] = pagesave_path
                item['search_state'] = search_state
                print(item)
                yield item

        # Update Store Table
        c_status = "Done"
        obj.update_store_status(c_status,lat_lng)

if __name__ == '__main__':
    ex("scrapy crawl provider_data -a start=37537 -a end=37537".split())