import datetime
import json
import scrapy
from scrapy.cmdline import execute as ex
from storeLocator.db_config import DbConfig
# from fake_useragent import UserAgent
from storeLocator.items import dataItem,stateItem
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
        qr = f"select * from {obj.store_table} where status='Pending' and id between {self.start} and {self.end}"
        print(qr)
        try:
            obj.cur.execute(qr)
            rows = obj.cur.fetchall()
        except Exception as e:
            print(e)
        uniq_provider = 'Burlington'
        for row in rows:
            search_state = row['state']
            # create table for provider data
            obj.create_provider_data_table()
            hashid = create_md5_hash(f'{uniq_provider}_{search_state}')
            pagesave_dir = rf"C:/Siraj/Actowiz/Desktop/pagesave/{uniq_provider}/{today_date}"
            print(pagesave_dir)
            file_name = fr"{pagesave_dir}/{hashid}.html"
            meta_dict = {"file_name" : file_name,"hashid":hashid,"search_state":search_state,"uniq_provider":uniq_provider,"pagesave_dir":pagesave_dir}
            if os.path.exists(file_name):
                yield scrapy.Request(url='file:///'+file_name,cb_kwargs=meta_dict,callback=self.parse_)
            else:
                headers = {
                    'accept': 'application/json, text/javascript, */*; q=0.01',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/json',
                    'origin': 'https://hosted.meetsoci.com',
                    'priority': 'u=1, i',
                    'referer': 'https://hosted.meetsoci.com/burlington/index.html',
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
                    'like': '0.6129401151487692',
                    'lang': 'en_US',
                    'isSOCiLocator': 'true',
                }
                json_data = {
                    'request': {
                        'appkey': 'D312B21C-26E1-11EC-95AF-DE19919C4603',
                        'formdata': {
                            'gps': 'first',
                            'dataview': 'store_default',
                            'limit': 20,
                            'geolocs': {
                                'geoloc': [
                                    {
                                        'addressline': f'{search_state}',
                                        'country': '',
                                        'latitude': '',
                                        'longitude': '',
                                    },
                                ],
                            },
                            'searchradius': '15|25|50|100|250',
                            'radiusuom': 'mile',
                            'where': {
                                'facilitystatus': {
                                    'in': 'Active|Planned',
                                },
                            },
                        },
                    },
                }

                # Construct the URL with query parameters
                base_url = 'https://hosted.meetsoci.com/burlington/rest/locatorsearch'

                # Construct the full URL with parameters
                url = f"{base_url}?like={params['like']}&lang={params['lang']}&isSOCiLocator={params['isSOCiLocator']}"

                # Make a POST request with Scrapy
                # import requests
                # response = requests.post(
                #     'https://hosted.meetsoci.com/burlington/rest/locatorsearch',
                #     params=params,
                #     headers=headers,
                #     json=json_data,
                # )
                # print(response.text)

                yield scrapy.Request(url=url,method="POST",headers=headers,body=json.dumps(json_data),cb_kwargs=meta_dict,callback=self.parse_,dont_filter=True)

    def parse_(self,response,**kwargs):
        print("Parse Calling.......")
        file_name = kwargs['file_name']
        search_state = kwargs['search_state']
        pagesave_dir = kwargs['pagesave_dir']

        # Load the the response text
        json_data = json.loads(response.text)
        try:
            collection_count = len(json_data['response']['collection'])
        except:
            collection_count = 0

        # Process for page save.....
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
        store_list = json_data['response']['collection']
        for i in range(len(store_list)):
            try:
                store_no = store_list[i]['clientkey']
            except Exception as e:
                store_no = ''
                print(e)
            try:
                name = store_list[i]['city']
            except Exception as e:
                name = ''
                print(e)
            try:
                latitude = store_list[i]['latitude']
            except Exception as e:
                latitude = ''
                print(e)
            try:
                longitude = store_list[i]['longitude']
            except Exception as e:
                longitude = ''
                print(e)
            try:
                street = store_list[i]['address1']
            except Exception as e:
                street = ''
                print(e)
            try:
                city = store_list[i]['city']
            except Exception as e:
                city = ''
                print(e)
            try:
                state = store_list[i]['state']
            except Exception as e:
                print(e)
            try:
                zip_code = store_list[i]['postalcode']
            except Exception as e:
                zip_code = ''
                print(e)
            try:
                county = store_list[i]['country']
            except Exception as e:
                county = ''
                print(e)
            try:
                phone = store_list[i]['phone']
            except Exception as e:
                phone = ''
                print(e)
            try:
                open_hours_list = []
                week_tag = ['mon','tue','wed','thurs','fri','sat','sun']
                for week_day in week_tag:
                    open = store_list[i][f'{week_day}open']
                    close = store_list[i][f'{week_day}close']
                    if week_day == 'mon':
                        day_hours = f"Monday:{open}-{close}"
                    elif week_day == 'tue':
                        day_hours = f"Tuesday:{open}-{close}"
                    elif week_day == 'wed':
                        day_hours = f"Wednesday:{open}-{close}"
                    elif week_day == 'thurs':
                        day_hours = f"Thursday:{open}-{close}"
                    elif week_day == 'fri':
                        day_hours = f"Friday:{open}-{close}"
                    elif week_day == 'sat':
                        day_hours = f"Saturday:{open}-{close}"
                    elif week_day == 'sun':
                        day_hours = f"Sunday:{open}-{close}"
                    else:
                        day_hours = ''
                    if day_hours not in open_hours_list:
                        open_hours_list.append(day_hours)
                if open_hours_list:
                    open_hours = ' | '.join(open_hours_list)
                    store_status = "Open"
                else:
                    open_hours = ''
                    store_status = "Close"
            except Exception as e:
                open_hours = ''
                store_status = ''
                print(e)
            try:
                url = store_list[i]['website']
            except Exception as e:
                url = ''
                print(e)
            try:
                provider = store_list[i]['name']
            except Exception as e:
                provider = ''
                print(e)
            try:
                category = 'Apparel And Accessory Stores'
            except Exception as e:
                category = ''
                print(e)
            try:
                updated_date = datetime.datetime.today().strftime("%d-%m-%Y")
            except Exception as e:
                updated_date = ''
                print(e)
            try:
                country = store_list[i]['country']
            except Exception as e:
                country = ''
                print(e)
            try:
                status = store_status
            except Exception as e:
                status = ''
                print(e)
            try:
                direction_url = f"http://maps.apple.com?q={name} {street},{city},{zip_code}"
            except Exception as e:
                direction_url = ''
                print(e)
            try:
                pagesave_path = file_name
            except Exception as e:
                pagesave_path = ''
                print(e)

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
            item['url'] = url
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
        obj.update_store_status(c_status,search_state)

if __name__ == '__main__':
    ex("scrapy crawl provider_data -a start=1 -a end=50".split())


# ['2643196194','7862565410','764473683','163256840','3046170532','906478824','5668881561','1664688098','524619789','5185413561','806625365','6983701500','648210937','157560046','7720019014']