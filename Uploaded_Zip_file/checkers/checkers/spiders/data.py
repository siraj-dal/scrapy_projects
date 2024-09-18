import html
import json
from datetime import datetime
import pymysql
import scrapy
import self
import checkers.DB_CONFIG as DB
from scrapy.cmdline import execute
import checkers.SAVE_SEND_EXCEL_SLACK_FUNCTION as sl
from checkers.items import CheckersItem, CheckersData

st = datetime.now()


class ButterDataSpider(scrapy.Spider):
    name = 'data_butter'
    website = 'checkers'
    country = 'South_Africa'
    allowed_domains = ["www.checkers.co.za"]
    # channel_name = '#test-csv'
    # file_path = r'C:\Users\DELL\Desktop\KARAN\files'
    # final_file_path_slack = file_path + f'{website}_{st.day}_{st.month}_{st.year}_{country}.xlsx'
    cookies = {
        'anonymous-consents': '%5B%5D',
        'checkersZA-preferredStore': '57861',
        'cookie-notification': 'NOT_ACCEPTED',
        'JSESSIONID': 'Y23-514e3df8-a253-457d-ba47-cf82f0e377b9',
        'webp_supported': 'true',
        'cookie-promo-alerts-popup': 'true',
        'checkersZA-cart': '1869e2d4-92e9-45c6-b8fd-bd05e7b2cba5',
        'AWSALB': 'fN7nL98c8P0pQua/erFP509NiryLwc3NX3LAwBnSFCp0cYpS7TjiZITdEC8rfzebqSvIFttndeUE5K+OCMlCflNASWff/8OnmuE7LVybXRR3GDfEOKx0LSi2v8TH',
        'AWSALBCORS': 'fN7nL98c8P0pQua/erFP509NiryLwc3NX3LAwBnSFCp0cYpS7TjiZITdEC8rfzebqSvIFttndeUE5K+OCMlCflNASWff/8OnmuE7LVybXRR3GDfEOKx0LSi2v8TH',
    }
    cursor = DB.cursor
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-GB,en;q=0.6',
        'cache-control': 'max-age=0',
        # 'cookie': 'anonymous-consents=%5B%5D; checkersZA-preferredStore=57861; cookie-notification=NOT_ACCEPTED; JSESSIONID=Y23-514e3df8-a253-457d-ba47-cf82f0e377b9; webp_supported=true; cookie-promo-alerts-popup=true; checkersZA-cart=1869e2d4-92e9-45c6-b8fd-bd05e7b2cba5; AWSALB=fN7nL98c8P0pQua/erFP509NiryLwc3NX3LAwBnSFCp0cYpS7TjiZITdEC8rfzebqSvIFttndeUE5K+OCMlCflNASWff/8OnmuE7LVybXRR3GDfEOKx0LSi2v8TH; AWSALBCORS=fN7nL98c8P0pQua/erFP509NiryLwc3NX3LAwBnSFCp0cYpS7TjiZITdEC8rfzebqSvIFttndeUE5K+OCMlCflNASWff/8OnmuE7LVybXRR3GDfEOKx0LSi2v8TH',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Brave";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }

    def start_requests(self):
        self.cursor.execute(f'SELECT * FROM {DB.LINK_TABLE} WHERE status="pending"')
        links = self.cursor.fetchall()
        for x in links:
            pd_id = x[0]
            url = x[1]

            yield scrapy.Request(url=url,
                                 dont_filter=True,
                                 headers=self.headers,
                                 cookies=self.cookies,
                                 cb_kwargs={"pd_id": pd_id,
                                            "url": url})
            # break

    def parse(self, response, **kwargs):
        file_path = r"C:\Users\DELL\Documents\PAGESAVE\checkers"
        final_path = file_path + fr'\{kwargs["pd_id"]}.html'
        with open(final_path, 'w') as f:
            f.write(response.text)
        item = CheckersData()
        item["pd_id"] = kwargs["pd_id"]
        item["url"] = kwargs["url"]
        item["country"] = 'South Africa'
        item["currency"] = 'ZAR'
        data_brand = json.loads(response.text.split(
            '''(window, document, 'script', 'dataLayer', 'GTM-597TTQ');</script> <script defer type="application/ld+json">''')[
                                    -1].split("</script> <script defer src='https://securepubads.g.doubleclic")[
                                    0].strip())
        item["brand"] = data_brand['brand']
        category = data_brand["cat"]
        data = json.loads(response.text.split("  dataLayer.push(")[-1].split(");")[0].replace("'", '"'))
        for y in data['ecommerce']["detail"]["products"]:
            item["name"] = html.unescape(y["name"])
            # item["price"] = float(y["unit_sale_price"].replace('R','')) if not None else "NA"
            # item["mrp"] = float(y["price"].replace('R','')) if not None else item["price"]
            item["price"] = float(y["unit_sale_price"].replace('R', '')) if y.get("unit_sale_price") not in [None,''] else "NA"
            item["mrp"] = float(y["price"].replace('R', '')) if y.get("price") not in [None, ''] else item["price"]

            item["sku"] = y["id"]
            item["product_type"] = "cheese" if 'cheese' in category.lower() else "Butter"
            item["size"] = y["name"].split(" ")[-1]
            yield item

    #     self.cursor.execute(f"""
    # def close(self, spider):
    #     DELETE FROM {DB.DATA_TABLE}
    #     WHERE brand NOT IN ('Lurpak', 'Clover', 'Crystal Valley', 'Ladismith', 'Bonnita', 'Dewfresh', 'Parmalat', 'Castello', 'Fairview', 'Presiden', 'First choice', 'Clover Mooi River', 'Clove Butter', 'Spar', 'Underberg');
    #     """)
    #     DB.con.commit()
        # sl.send_file(self.channel_name, self.final_file_path_slack)


if __name__ == '__main__':
    execute('scrapy crawl data_butter'.split())
