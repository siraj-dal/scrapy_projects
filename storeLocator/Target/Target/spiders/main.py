import datetime
import json
import scrapy
from scrapy.cmdline import execute as ex
from Target.db_config import DbConfig
from Target.items import dataItem,stateItem
import os
import hashlib
import requests

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
        uniq_provider = 'Target'
        for row in rows:
            search_state = row['state']
            zipcode = row['zipcode']
            # zipcode = '77954'
            # create table for provider data
            obj.create_provider_data_table()
            hashid = create_md5_hash(f'{zipcode}_{uniq_provider}_{search_state}')
            pagesave_dir = rf"C:/Siraj/Actowiz/Desktop/pagesave/{uniq_provider}/{today_date}/HTML"
            print(pagesave_dir)
            file_name = fr"{pagesave_dir}/{hashid}.html"
            meta_dict = {"file_name" : file_name,"hashid":hashid,"search_state":search_state,"zipcode":zipcode,"uniq_provider":uniq_provider,"pagesave_dir":pagesave_dir}
            if os.path.exists(file_name):
                yield scrapy.Request(url='file:///'+file_name,cb_kwargs=meta_dict,callback=self.parse_)
            else:
                import requests
                url = f'https://www.target.com/store-locator/find-stores/{zipcode}'
                headers = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'max-age=0',
                    # 'cookie': 'sapphire=1; visitorId=01920DD750070201AD6D94CEEEAB097D; TealeafAkaSid=x3uAlGisOjy4o2AEgSqEEkpxxZDl7d84; UserLocation=52404|41.9831|-91.6686|IA|US; fiatsCookie=DSI_1771|DSN_Cedar%20Rapids%20South|DSZ_52404; mdLogger=false; kampyle_userid=e55e-f60d-20d7-006d-fd82-8a98-ef07-49da; ci_pixmgr=other; GuestLocation=380051|22.990|72.500|GJ|IN; accessToken=eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJiN2I5MDQ5ZC02YTI0LTQzMGMtOGJlNS0wNDIyODU1OWQ3YzEiLCJpc3MiOiJNSTYiLCJleHAiOjE3Mjc0MTg2MDMsImlhdCI6MTcyNzMzMjIwMywianRpIjoiVEdULmU4M2FmOGFlZmY1NjRjMDE4MDQ2NjBmMTJkMDg4MWIwLWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6ImZjZDQyYjYwZjI3YmEzMmFlNjM0NzU2MmI2OTdmNWVhZDE1YjFhMWJiYjE1M2E4ZTJjMGYxNDM2OWE1Y2M5YTYiLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.dXQE5ZSxW5BoKGdanQn0xGjbv8CNfWYcV1pVCB1uM51zwAIp3CyhxVHTsDN0hMXIJFfKLEV40sjuPJngQOqUD7q9yFbhaEcnZsP3KGkJe75qMwwI9X3Ldqu0Z2YfitCFegwPRIWy8Zc_Rjid5crc3HlA4YSJv7h8LRtnz2s8hmO5MRYoy66WkFzt-bJJhB2ALQPQd02uVPXBSOkWVd7MlMflzzSOUjYVX_aoOfVA1DbDawbBfve7pExfV8urbYBkymG4zIIAA0dLD-KUipREsSoKwd1WPWPQd-4tiG2b5TtL8rL4JBYSOkFOWv678uQ_5PcnX7F2UYf4NGYvKLP3Wg; idToken=eyJhbGciOiJub25lIn0.eyJzdWIiOiJiN2I5MDQ5ZC02YTI0LTQzMGMtOGJlNS0wNDIyODU1OWQ3YzEiLCJpc3MiOiJNSTYiLCJleHAiOjE3Mjc0MTg2MDMsImlhdCI6MTcyNzMzMjIwMywiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZW0iOm51bGwsInBoIjpmYWxzZSwibGVkIjpudWxsLCJsdHkiOmZhbHNlLCJzdCI6IkdKIn19.; refreshToken=cR22xzXXo8amqGB5dR3he5G6gLl9bHPse9_SoYnWgzoS1VictXq7XpwYxKGKqKERZEQ9cxiMpkF6Or8Y-G3LRQ; adScriptData=GJ; kampylePageLoadedTimestamp=1727332336216; LAST_INVITATION_VIEW=1727332348295; DECLINED_DATE=1727332350532; ffsession={%22sessionHash%22:%22cf4c8add746251727332203810%22%2C%22prevPageName%22:%22store%20locator:%20find%20stores%22%2C%22prevPageType%22:%22store%20locator%22%2C%22prevPageUrl%22:%22https://www.target.com/store-locator/find-stores/77954%22%2C%22sessionHit%22:7}; kampyleUserSession=1727342046973; kampyleUserSessionsCount=10; kampyleSessionPageCounter=1; kampyleUserPercentile=33.73265580952205; __gads=ID=8540bfcb163c7de8:T=1726826249:RT=1727342044:S=ALNI_MbwpeKiZ_aKgq7JG702fvB8bfYzfg; __gpi=UID=00000ef58ce8c9d7:T=1726826249:RT=1727342044:S=ALNI_MYHXQpIBAh9SSDg3PWLwNpZkXuwYA; __eoi=ID=245db009438c31e0:T=1726809111:RT=1727342044:S=AA-AfjbjnNEFRxwdevLpXwXdhIbU',
                    'priority': 'u=0, i',
                    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                }

                # Try to request with requests module...
                # response = requests.get(
                #     f'https://easylocator.net/ajax/search_by_lat_lon/Oiselle%20Dealer%20Search/{lat}/{long}/2000/10/null/null',
                #     headers=headers,
                # )
                # print(response.text)

                yield scrapy.Request(url=url,headers=headers,cb_kwargs=meta_dict,callback=self.parse_,dont_filter=True)

    def parse_(self,response,**kwargs):
        print("Parse Calling.......")
        file_name = kwargs['file_name']
        hashid = kwargs['hashid']
        search_state = kwargs['search_state']
        uniq_provider = kwargs['uniq_provider']
        pagesave_dir = kwargs['pagesave_dir']
        zipcode = kwargs['zipcode']
        # print(response.text)

        if "Sorry, no stores matched your search." not in response.text:

            if "view_storeCardGrid___yTnq" in response.text:
                page_write(pagesave_dir, file_name, response.text)
            else:
                print(f"No record Found for {search_state}")
                file_name = str(file_name).replace('.html','') + '_NF.html'
                page_write(pagesave_dir, file_name, response.text)
                c_status = "Not Found"
                obj.update_store_status(c_status, search_state)
                return None

            # store_list = response.xpath('//div[@class="view_storeCardGrid___yTnq"]/div[@class="view_storeCardWrapper__qERCW"]')
            store_list = response.xpath('//fieldset/following-sibling::div/div[@class="view_storeCardWrapper__qERCW"]')
            for store_data in store_list:
                store_url = store_data.xpath('.//a[contains(@aria-label,"Store info")]/@href').get()
                map_url = store_data.xpath('.//a[@data-test="@store-locator/StoreAddress"]/@href').get()
                if store_url:
                    store_id = str(store_url).split('/')[-1]
                    store_name = str(store_url).split('/')[-2]
                    if 'https://www.target.com/' not in store_url:
                        store_url = 'https://www.target.com/' + store_url
                    # Request on Store_Url for get Data
                    store_headers = {
                        'accept': 'application/json',
                        'accept-language': 'en-US,en;q=0.9',
                        # 'cookie': 'TealeafAkaSid=lC-cWty_4pWx6qhPe575w8mZaUGugVUD; visitorId=01922DE4352A020198CF019924290953; sapphire=1; UserLocation=07104|40.770|-74.170|NJ|US; ffsession={%22sessionHash%22:%22cf4c8add746251727332203810%22%2C%22prevPageName%22:%22store%20locator:%20store%20details%22%2C%22prevPageType%22:%22store%20locator%22%2C%22prevPageUrl%22:%22https://www.target.com/sl/new-braunfels/2429%22%2C%22sessionHit%22:23%2C%22prevSearchTerm%22:%22non-search%22}; _mitata=ZDMyMGFiZTRjNGFlOTg1YzA1OWM3ODA1N2Q1ZDU4YjY0NWRlMjQ1MjhmYWJhMWM3ZTYyYWZkMDhlMDc3ZDMwOA==_/@#/1727346845_/@#/cYPrJM2KSZrTWNcb_/@#/YTI5NWNiMDEzNDg3NmMyMjRlNDY4NGUwM2NjOGUwMjFkZDJkNDlhMzliZmUyMzUzNzEyYjBkYWQ5OWI5ZGVlMg==_/@#/000; fiatsCookie=DSI_2881|DSN_Kearny|DSZ_07032',
                        'origin': 'https://www.target.com',
                        'priority': 'u=1, i',
                        'referer': 'https://www.target.com/sl/new-braunfels/2429',
                        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-site',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                    }

                    params = {
                        'store_id': f'{store_id}',
                        'key': '8df66ea1e1fc070a6ea99e942431c9cd67a80f02',
                        'visitor_id': '01922DE4352A020198CF019924290953',
                        'channel': 'WEB',
                        'page': f'/sl/{store_name}/{store_id}',
                    }

                    store_response = requests.get(
                        'https://redsky.target.com/redsky_aggregations/v1/web/store_location_v1',
                        params=params,
                        headers=store_headers,
                    )
                    print(store_response.text)

                    if "store" in store_response.text:
                        store_file_name = str(file_name).replace('.html', '') + f'_{store_id}.html'
                        page_write(pagesave_dir, store_file_name, response.text)
                    else:
                        print(f"No record Found for {search_state}")
                        store_file_name = str(file_name).replace('.html', '') + f'_{store_id}_NF.html'
                        page_write(pagesave_dir, store_file_name, response.text)
                        c_status = "Not Found"
                        obj.update_store_status(c_status, zipcode)
                        return None

                    if store_response.text:
                        store_data = json.loads(store_response.text)

                        for i in range(len(store_data)):

                            store_no = store_id
                            name = store_name
                            latitude = store_data.get('data', {}).get('store', {}).get('geographic_specifications', {}).get('latitude', '')
                            longitude =store_data.get('data', {}).get('store', {}).get('geographic_specifications', {}).get('longitude', '')
                            street = store_data['data']['store']['mailing_address']['address_line1']
                            city = store_data['data']['store']['mailing_address']['city']
                            state = store_data['data']['store']['mailing_address']['state']
                            state = str(state).strip()
                            zip_code = store_data['data']['store']['mailing_address']['postal_code']
                            county = store_data['data']['store']['mailing_address']['county']
                            phone = store_data['data']['store']['main_voice_phone_number']
                            open_hours_list = []
                            main_hours = store_data['data']['store']['rolling_operating_hours']['main_hours']['days']
                            for day_hrs in range(len(main_hours)):
                                day_name = main_hours[day_hrs]['day_name']
                                begin_time = main_hours[day_hrs]['hours'][0]['begin_time']
                                end_time = main_hours[day_hrs]['hours'][0]['end_time']
                                day_hours = f"{day_name}:{begin_time}-{end_time}"
                                open_hours_list.append(day_hours)
                            if open_hours_list:
                                open_hours = ' | '.join(open_hours_list)
                            else:
                                open_hours = ''
                            website_url = store_url
                            provider = uniq_provider
                            category = 'Apparel And Accessory Stores'
                            updated_date = datetime.datetime.today().strftime("%d-%m-%Y")
                            country = store_data['data']['store']['mailing_address']['country']
                            if not country or country == "United States":
                                country = "US"
                            status = store_data['data']['store']['status']
                            direction_url = map_url

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
                            item['search_state'] = search_state
                            print(item)
                            yield item

            # Update Store Table
            c_status = "Done"
            obj.update_store_status(c_status,zipcode)
        else:
            # Update Store Table
            c_status = "Not Found"
            obj.update_store_status(c_status, zipcode)

if __name__ == '__main__':
    ex("scrapy crawl provider_data -a start=1083 -a end=1083".split())