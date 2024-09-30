import requests

cookies = {
    'sapphire': '1',
    'visitorId': '01920DD750070201AD6D94CEEEAB097D',
    'TealeafAkaSid': 'x3uAlGisOjy4o2AEgSqEEkpxxZDl7d84',
    'UserLocation': '52404|41.9831|-91.6686|IA|US',
    'fiatsCookie': 'DSI_1771|DSN_Cedar%20Rapids%20South|DSZ_52404',
    'mdLogger': 'false',
    'kampyle_userid': 'e55e-f60d-20d7-006d-fd82-8a98-ef07-49da',
    'ci_pixmgr': 'other',
    'GuestLocation': '380051|22.990|72.500|GJ|IN',
    'accessToken': 'eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJiN2I5MDQ5ZC02YTI0LTQzMGMtOGJlNS0wNDIyODU1OWQ3YzEiLCJpc3MiOiJNSTYiLCJleHAiOjE3Mjc0MTg2MDMsImlhdCI6MTcyNzMzMjIwMywianRpIjoiVEdULmU4M2FmOGFlZmY1NjRjMDE4MDQ2NjBmMTJkMDg4MWIwLWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6ImZjZDQyYjYwZjI3YmEzMmFlNjM0NzU2MmI2OTdmNWVhZDE1YjFhMWJiYjE1M2E4ZTJjMGYxNDM2OWE1Y2M5YTYiLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.dXQE5ZSxW5BoKGdanQn0xGjbv8CNfWYcV1pVCB1uM51zwAIp3CyhxVHTsDN0hMXIJFfKLEV40sjuPJngQOqUD7q9yFbhaEcnZsP3KGkJe75qMwwI9X3Ldqu0Z2YfitCFegwPRIWy8Zc_Rjid5crc3HlA4YSJv7h8LRtnz2s8hmO5MRYoy66WkFzt-bJJhB2ALQPQd02uVPXBSOkWVd7MlMflzzSOUjYVX_aoOfVA1DbDawbBfve7pExfV8urbYBkymG4zIIAA0dLD-KUipREsSoKwd1WPWPQd-4tiG2b5TtL8rL4JBYSOkFOWv678uQ_5PcnX7F2UYf4NGYvKLP3Wg',
    'idToken': 'eyJhbGciOiJub25lIn0.eyJzdWIiOiJiN2I5MDQ5ZC02YTI0LTQzMGMtOGJlNS0wNDIyODU1OWQ3YzEiLCJpc3MiOiJNSTYiLCJleHAiOjE3Mjc0MTg2MDMsImlhdCI6MTcyNzMzMjIwMywiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZW0iOm51bGwsInBoIjpmYWxzZSwibGVkIjpudWxsLCJsdHkiOmZhbHNlLCJzdCI6IkdKIn19.',
    'refreshToken': 'cR22xzXXo8amqGB5dR3he5G6gLl9bHPse9_SoYnWgzoS1VictXq7XpwYxKGKqKERZEQ9cxiMpkF6Or8Y-G3LRQ',
    'adScriptData': 'GJ',
    'kampylePageLoadedTimestamp': '1727332336216',
    'LAST_INVITATION_VIEW': '1727332348295',
    'DECLINED_DATE': '1727332350532',
    'ffsession': '{%22sessionHash%22:%22cf4c8add746251727332203810%22%2C%22prevPageName%22:%22store%20locator:%20find%20stores%22%2C%22prevPageType%22:%22store%20locator%22%2C%22prevPageUrl%22:%22https://www.target.com/store-locator/find-stores/77954%22%2C%22sessionHit%22:7}',
    'kampyleUserSession': '1727342046973',
    'kampyleUserSessionsCount': '10',
    'kampyleSessionPageCounter': '1',
    'kampyleUserPercentile': '33.73265580952205',
    '__gads': 'ID=8540bfcb163c7de8:T=1726826249:RT=1727342044:S=ALNI_MbwpeKiZ_aKgq7JG702fvB8bfYzfg',
    '__gpi': 'UID=00000ef58ce8c9d7:T=1726826249:RT=1727342044:S=ALNI_MYHXQpIBAh9SSDg3PWLwNpZkXuwYA',
    '__eoi': 'ID=245db009438c31e0:T=1726809111:RT=1727342044:S=AA-AfjbjnNEFRxwdevLpXwXdhIbU',
}

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

# response = requests.get('https://www.target.com/store-locator/find-stores/77954', cookies=cookies, headers=headers)
response = requests.get('https://www.target.com/store-locator/find-stores/77954', headers=headers)
print(response.status_code)
with open('target_test_.html', 'w', encoding='utf-8') as f:
    f.write(response.text)

# import requests
#
# # cookies = {
# #     'sapphire': '1',
# #     'visitorId': '01920DD750070201AD6D94CEEEAB097D',
# #     'TealeafAkaSid': 'x3uAlGisOjy4o2AEgSqEEkpxxZDl7d84',
# #     'UserLocation': '52404|41.9831|-91.6686|IA|US',
# #     'ci_pixmgr': 'other',
# #     'accessToken': 'eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJiN2I5MDQ5ZC02YTI0LTQzMGMtOGJlNS0wNDIyODU1OWQ3YzEiLCJpc3MiOiJNSTYiLCJleHAiOjE3Mjc0MTg2MDMsImlhdCI6MTcyNzMzMjIwMywianRpIjoiVEdULmU4M2FmOGFlZmY1NjRjMDE4MDQ2NjBmMTJkMDg4MWIwLWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6ImZjZDQyYjYwZjI3YmEzMmFlNjM0NzU2MmI2OTdmNWVhZDE1YjFhMWJiYjE1M2E4ZTJjMGYxNDM2OWE1Y2M5YTYiLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.dXQE5ZSxW5BoKGdanQn0xGjbv8CNfWYcV1pVCB1uM51zwAIp3CyhxVHTsDN0hMXIJFfKLEV40sjuPJngQOqUD7q9yFbhaEcnZsP3KGkJe75qMwwI9X3Ldqu0Z2YfitCFegwPRIWy8Zc_Rjid5crc3HlA4YSJv7h8LRtnz2s8hmO5MRYoy66WkFzt-bJJhB2ALQPQd02uVPXBSOkWVd7MlMflzzSOUjYVX_aoOfVA1DbDawbBfve7pExfV8urbYBkymG4zIIAA0dLD-KUipREsSoKwd1WPWPQd-4tiG2b5TtL8rL4JBYSOkFOWv678uQ_5PcnX7F2UYf4NGYvKLP3Wg',
# #     'idToken': 'eyJhbGciOiJub25lIn0.eyJzdWIiOiJiN2I5MDQ5ZC02YTI0LTQzMGMtOGJlNS0wNDIyODU1OWQ3YzEiLCJpc3MiOiJNSTYiLCJleHAiOjE3Mjc0MTg2MDMsImlhdCI6MTcyNzMzMjIwMywiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZW0iOm51bGwsInBoIjpmYWxzZSwibGVkIjpudWxsLCJsdHkiOmZhbHNlLCJzdCI6IkdKIn19.',
# #     'refreshToken': 'cR22xzXXo8amqGB5dR3he5G6gLl9bHPse9_SoYnWgzoS1VictXq7XpwYxKGKqKERZEQ9cxiMpkF6Or8Y-G3LRQ',
# #     'adScriptData': 'GJ',
# #     'fiatsCookie': 'DSI_888|DSN_Victoria|DSZ_77904',
# #     'sddStore': 'DSI_1771|DSN_Cedar%20Rapids%20South|DSZ_52404',
# #     '_gcl_au': '1.1.777325940.1727343937',
# #     'crl8.fpcuid': '2052e3a0-2ef1-41d0-8227-e456f6a75f8e',
# #     '__gads': 'ID=8540bfcb163c7de8:T=1726826249:RT=1727345271:S=ALNI_MbwpeKiZ_aKgq7JG702fvB8bfYzfg',
# #     '__gpi': 'UID=00000ef58ce8c9d7:T=1726826249:RT=1727345271:S=ALNI_MYHXQpIBAh9SSDg3PWLwNpZkXuwYA',
# #     '__eoi': 'ID=245db009438c31e0:T=1726809111:RT=1727345271:S=AA-AfjbjnNEFRxwdevLpXwXdhIbU',
# #     'ffsession': '{%22sessionHash%22:%22cf4c8add746251727332203810%22%2C%22prevPageName%22:%22store%20locator:%20store%20details%22%2C%22prevPageType%22:%22store%20locator%22%2C%22prevPageUrl%22:%22https://www.target.com/sl/new-braunfels/2429%22%2C%22sessionHit%22:17%2C%22prevSearchTerm%22:%22non-search%22}',
# #     '_mitata': 'NzM2MWVlNThkMTUyOTE2N2M2ZjU0M2ExNWQ2ZGQ4N2JjZGM2YzZkNTBmMTJiOTJmZTI0MjU1NTk4OGFiNjA3MA==_/@#/1727345416_/@#/cYPrJM2KSZrTWNcb_/@#/ZWE4MDJkYTc2NTYzMWM2YmM4MDljZGI5ZjQ4ZjYxM2E0ZDE1ZGNjMDBhYWNjOWU2YjRmNzAxNGZjODFkNGNlOA==_/@#/000',
# # }
#
# headers = {
#     'accept': 'application/json',
#     'accept-language': 'en-US,en;q=0.9',
#     # 'cookie': 'sapphire=1; visitorId=01920DD750070201AD6D94CEEEAB097D; TealeafAkaSid=x3uAlGisOjy4o2AEgSqEEkpxxZDl7d84; UserLocation=52404|41.9831|-91.6686|IA|US; ci_pixmgr=other; accessToken=eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJiN2I5MDQ5ZC02YTI0LTQzMGMtOGJlNS0wNDIyODU1OWQ3YzEiLCJpc3MiOiJNSTYiLCJleHAiOjE3Mjc0MTg2MDMsImlhdCI6MTcyNzMzMjIwMywianRpIjoiVEdULmU4M2FmOGFlZmY1NjRjMDE4MDQ2NjBmMTJkMDg4MWIwLWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6ImZjZDQyYjYwZjI3YmEzMmFlNjM0NzU2MmI2OTdmNWVhZDE1YjFhMWJiYjE1M2E4ZTJjMGYxNDM2OWE1Y2M5YTYiLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.dXQE5ZSxW5BoKGdanQn0xGjbv8CNfWYcV1pVCB1uM51zwAIp3CyhxVHTsDN0hMXIJFfKLEV40sjuPJngQOqUD7q9yFbhaEcnZsP3KGkJe75qMwwI9X3Ldqu0Z2YfitCFegwPRIWy8Zc_Rjid5crc3HlA4YSJv7h8LRtnz2s8hmO5MRYoy66WkFzt-bJJhB2ALQPQd02uVPXBSOkWVd7MlMflzzSOUjYVX_aoOfVA1DbDawbBfve7pExfV8urbYBkymG4zIIAA0dLD-KUipREsSoKwd1WPWPQd-4tiG2b5TtL8rL4JBYSOkFOWv678uQ_5PcnX7F2UYf4NGYvKLP3Wg; idToken=eyJhbGciOiJub25lIn0.eyJzdWIiOiJiN2I5MDQ5ZC02YTI0LTQzMGMtOGJlNS0wNDIyODU1OWQ3YzEiLCJpc3MiOiJNSTYiLCJleHAiOjE3Mjc0MTg2MDMsImlhdCI6MTcyNzMzMjIwMywiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZW0iOm51bGwsInBoIjpmYWxzZSwibGVkIjpudWxsLCJsdHkiOmZhbHNlLCJzdCI6IkdKIn19.; refreshToken=cR22xzXXo8amqGB5dR3he5G6gLl9bHPse9_SoYnWgzoS1VictXq7XpwYxKGKqKERZEQ9cxiMpkF6Or8Y-G3LRQ; adScriptData=GJ; fiatsCookie=DSI_888|DSN_Victoria|DSZ_77904; sddStore=DSI_1771|DSN_Cedar%20Rapids%20South|DSZ_52404; _gcl_au=1.1.777325940.1727343937; crl8.fpcuid=2052e3a0-2ef1-41d0-8227-e456f6a75f8e; __gads=ID=8540bfcb163c7de8:T=1726826249:RT=1727345271:S=ALNI_MbwpeKiZ_aKgq7JG702fvB8bfYzfg; __gpi=UID=00000ef58ce8c9d7:T=1726826249:RT=1727345271:S=ALNI_MYHXQpIBAh9SSDg3PWLwNpZkXuwYA; __eoi=ID=245db009438c31e0:T=1726809111:RT=1727345271:S=AA-AfjbjnNEFRxwdevLpXwXdhIbU; ffsession={%22sessionHash%22:%22cf4c8add746251727332203810%22%2C%22prevPageName%22:%22store%20locator:%20store%20details%22%2C%22prevPageType%22:%22store%20locator%22%2C%22prevPageUrl%22:%22https://www.target.com/sl/new-braunfels/2429%22%2C%22sessionHit%22:17%2C%22prevSearchTerm%22:%22non-search%22}; _mitata=NzM2MWVlNThkMTUyOTE2N2M2ZjU0M2ExNWQ2ZGQ4N2JjZGM2YzZkNTBmMTJiOTJmZTI0MjU1NTk4OGFiNjA3MA==_/@#/1727345416_/@#/cYPrJM2KSZrTWNcb_/@#/ZWE4MDJkYTc2NTYzMWM2YmM4MDljZGI5ZjQ4ZjYxM2E0ZDE1ZGNjMDBhYWNjOWU2YjRmNzAxNGZjODFkNGNlOA==_/@#/000',
#     'origin': 'https://www.target.com',
#     'priority': 'u=1, i',
#     'referer': 'https://www.target.com/sl/new-braunfels/2429',
#     'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-site',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
# }
#
# params = {
#     'store_id': '888',
#     'key': '8df66ea1e1fc070a6ea99e942431c9cd67a80f02',
#     'visitor_id': '01920DD750070201AD6D94CEEEAB097D',
#     'channel': 'WEB',
#     'page': '/sl/new-braunfels/2429',
# }
#
# response = requests.get(
#     'https://redsky.target.com/redsky_aggregations/v1/web/store_location_v1',
#     params=params,
#     # cookies=cookies,
#     headers=headers,
# )
# print(response.text)

import requests

cookies = {
    'TealeafAkaSid': 'lC-cWty_4pWx6qhPe575w8mZaUGugVUD',
    'visitorId': '01922DE4352A020198CF019924290953',
    'sapphire': '1',
    'UserLocation': '07104|40.770|-74.170|NJ|US',
    'ffsession': '{%22sessionHash%22:%22cf4c8add746251727332203810%22%2C%22prevPageName%22:%22store%20locator:%20store%20details%22%2C%22prevPageType%22:%22store%20locator%22%2C%22prevPageUrl%22:%22https://www.target.com/sl/new-braunfels/2429%22%2C%22sessionHit%22:23%2C%22prevSearchTerm%22:%22non-search%22}',
    '_mitata': 'ZDMyMGFiZTRjNGFlOTg1YzA1OWM3ODA1N2Q1ZDU4YjY0NWRlMjQ1MjhmYWJhMWM3ZTYyYWZkMDhlMDc3ZDMwOA==_/@#/1727346845_/@#/cYPrJM2KSZrTWNcb_/@#/YTI5NWNiMDEzNDg3NmMyMjRlNDY4NGUwM2NjOGUwMjFkZDJkNDlhMzliZmUyMzUzNzEyYjBkYWQ5OWI5ZGVlMg==_/@#/000',
    'fiatsCookie': 'DSI_2881|DSN_Kearny|DSZ_07032',
}

headers = {
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
    'store_id': '2429',
    # 'store_id': '2881',
    'key': '8df66ea1e1fc070a6ea99e942431c9cd67a80f02',
    'visitor_id': '01922DE4352A020198CF019924290953',
    'channel': 'WEB',
    'page': '/sl/new-braunfels/2429',
}

# params = {
#     'store_id': '888',
#     'key': '8df66ea1e1fc070a6ea99e942431c9cd67a80f02',
#     'visitor_id': '01920DD750070201AD6D94CEEEAB097D',
#     'channel': 'WEB',
#     'page': '/sl/new-braunfels/2429',
# }

response = requests.get(
    'https://redsky.target.com/redsky_aggregations/v1/web/store_location_v1',
    params=params,
    # cookies=cookies,
    headers=headers,
)
print(response.text)
