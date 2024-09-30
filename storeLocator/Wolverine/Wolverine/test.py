import json

import requests

# cookies = {
#     'lg_session_v1': 'eyJpdiI6IllDZUpNeVUzZnB5RXVvdjArWWpMUmRGYTY2ak1QcGtjMjA0SW5BbW5IWHM9IiwidmFsdWUiOiJoejFKWTg5MDc2c2k2cHhXbko5MmVxaUg4UEJEZFNUTEFaeVlXSTl5UXoyRE5kQ1NVd0lOT0t6dWEzeWI4Y0NMcUdCK3dCVzgwOHJYN2cydHRHS0VHZz09IiwibWFjIjoiZjNmMWQ5MjdkYTJkMDc2MmIyOTExZjQ4MjJkYTUxNTlhMWUyMTBiZmFiNzVjOGZhYjE4MTEzN2U2YTA4ZDQ2YyJ9',
# }

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

# response = requests.get('https://wolverine.locally.com/stores/conversion_data', params=params, cookies=cookies, headers=headers)
response = requests.get('https://wolverine.locally.com/stores/conversion_data', params=params,headers=headers)
print(response.text)
data_json = response.text.split("<div id")[0]
data_json = data_json + '"}'
with open('target_test_2.html', 'w', encoding='utf-8') as f:
    f.write(data_json)
try:
    load_json = json.loads(data_json)
except Exception as e:
    print(e)