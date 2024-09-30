import requests
import http.client
import json
import httpx
import asyncio
import aiohttp


proxy = {
        "http": "http://9dbe950ef6284a5da9e7749db9f7cbd1:@api.zyte.com:8011/",
        "https": "http://9dbe950ef6284a5da9e7749db9f7cbd1:@api.zyte.com:8011/"
    }
# Function to make the request using requests
def make_request_requests():
    print("Try with make_request_requests")
    cookies = {
        '''ANONYMOUS_USER_CONFIG=j%3A%7B%22clientId%22%3A%227c68c5fc-7b55-4bf5-8187-7dbc9005%22%2C%22instanceId%22%3A%227c68c5fc-7b55-4bf5-8187-7dbc9005%22%2C%22xo%22%3A%22eyJ0eXBlIjoiY29tcG9zaXRlIn0%3D.eyJqd3QiOiJleUpvZEhSd2N6b3ZMMjFsWlhOb2J5NWpiMjB2ZG1WeWMybHZiaUk2SWpFaUxDSm9kSFJ3Y3pvdkwyMWxaWE5vYnk1amIyMHZhWE52WDJOdmRXNTBjbmxmWTI5a1pTSTZJa2xPSWl3aVlXeG5Jam9pU0ZNeU5UWWlmUS5leUpwWVhRaU9qRTNNalkzTWpjMU1EWXNJbVY0Y0NJNk1UZzRORFF3TnpVd05pd2lhSFIwY0hNNkx5OXRaV1Z6YUc4dVkyOXRMMmx1YzNSaGJtTmxYMmxrSWpvaU4yTTJPR00xWm1NdE4ySTFOUzAwWW1ZMUxUZ3hPRGN0TjJSaVl6a3dNRFVpTENKb2RIUndjem92TDIxbFpYTm9ieTVqYjIwdllXNXZibmx0YjNWelgzVnpaWEpmYVdRaU9pSTBOVFU0WldOalpDMDRPVFpoTFRRMU1ESXRPVEJrWmkwM01HVTNZVFJtWXpRM1pEVWlmUS5oNEg4VGItcW50UElUZ0hxdFFlSWw3ellYd1JvUC1TQkRRNm0zeEtJbmE4IiwieG8iOm51bGx9%22%2C%22createdAt%22%3A%222024-09-19T06%3A31%3A46.792Z%22%7D; CAT_NAV_V2_COOKIE=0.732209005778147; ak_bmsc=4206D701613F598A8B800E6C2646DD4D~000000000000000000000000000000~YAAQDQkgF/Hyl9uRAQAAUNP6CBmf3INBoxDTE8YRyYlUI2BMo6pieUZgp3WQOOPb/7ai+xc98UPk1HA+VgnzjQPvkyQ7JOHZ0cP4wPWpOcI9x/wCOnHfBqM9vKoFks7HPJDJhYSmqjxmYrwK8AIloThoeMqHYZRX5SreRmd5l3jZrPj0P/GV9Xxj1LVHC++EwENNft1bfZnrPqwCQJ0bqy10PoHPYLa4H4SHurM66IELGDtepOe3OxGKOwf4yX3vLUnIjgCcUSnTaEhmhbIP1SVBfpEi+Uek0xmExUqFi70eAo3Zci+/e2dhZrJb5r5rcdDAjZCiX7NJ+qbljbHcavw3W/l9KSlq5R0XM8nWQKHbnTE++fnPxaNZQx4Ff3KIbSDGDf/aBIr0LKfDKCbYieQeB4I6LZ+HL3VgxYVfIkXrw1Sg35Obf0/Cmgp6tM27x4jofbo=; __logged_in_user_id_=122190837; _is_logged_in_=1; __connect.sid__=s%3AGyTlSALkWbhAPW_8d5C0Qcn6K0P67izU.uLAOHACRKCPsc%2F4wr536lrn16FJbo7HngMxKsW437Ks; _abck=231D5B0C4AB0E82BDE15F18FC1B827D3~0~YAAQDQkgFx0dmNuRAQAAN1/7CAwW/WcGviUsIyp5ktVM8g42Kt9eDrYASn4T9OH2P7Q2rwYtVmExSuyKQVD3n/vU4416VGoM80BIDr3OhnOoI9153v9Q8kq2E8SQDTj6gAj02qxDGnGNR+WWehRHFwKROTwBBGWzzBvUBgRaozAXhEgexsgubJk8E5NDPBWwsizHBm4NJ6cpZFJVVqe8xdHGgjq/z7vx4xqV/ygaGP5PU22e19RMHXBP+Pj07thsmSV302qJP8zGB+p+XUlWydX3yh/bo0+ZeKbuzHypdecdvYVblwAXz3/G28TG3XO45SeMl2z+3jYMrYynD/7zkbVxAesvEr0gP31TeRG9QSHLD17F1wRPHn+iTdda4Sm/PJmBV2mx7kegJ7pqjYT7YU94DM4y4f1ezBXmXBB1X9Clk0N2ekpeJFadx6zE3OFVlZIXM2bedHAcMHTlbrcVzwFkl3UIOp6WWyrJsZNGpzZ4IwMOi8lZ5mRqZPMvtx9fmU5zzEJNHQpnhx+Hx7bYjUx28uVKRieTy33+tkQxS1Z02vAi90h/c2FOz9FIIe7DJw92n2qge58=~-1~-1~1726731108; bm_sz=3165F22D376EF5293D3645180EF194B9~YAAQDQkgFx8dmNuRAQAAN1/7CBkJi/DHHvA26uImXxlNAGJqspUiDKrVXywPNm4EPj4CQQ0HDu3E/m0JaPZcv5icSAjXH8eQk/BJoJM1drN2yYUUMgByrh0hin6V9ui9X0b82jSIXeH8K6BuuL5F7728tQQiuHjqKj/JalmT2XhZ/Vi2DaMTOLcMbwQEEzP1XQjvkcpzAnL/KBzBTW1PyUC9t9O8D4YSqdPa+lAQx0ipRx5NjvBRNdpcot6Sm29bwJ8/Mgv898j19d7xvSnzQtlA5LCsmXX8WmflbgVPAyvDTMFG3rs/eU8YLqM4YJdtXRKrO0laWx0sg2XWky80boG5OgKr+Pxd9l4qLiHk2zFrM7gAa3xK45vhwozCMh9K0kROZlkwXLalKjAXUG26i4AAW99RSMO33A==~3355954~3553093; location-details=%7B%22city%22%3A%22Bengaluru%22%2C%22pincode%22%3A%22560001%22%2C%22lat%22%3A%2213.2257%22%2C%22long%22%3A%2277.575%22%7D; INP_POW=0.5202813040675851; bm_sv=637023C546B89F59D04AEAA4E9FE8F9D~YAAQDQkgF04nmNuRAQAAFoP7CBmeoQvqOmodBiUjKG0KkRG80LyHBh/Lar+7ZJsh47aDgCNcYz9n7+x34OeLFZ/BWNxBTSHefAfHpTMY0LRvFSPhGPqXyRZVShh/fKkkMoKxhJNikp544pOIBVBZ3ecHiM7MW4SOWvIZoiRqqDRzqlEXHKdGmoi3glBA5kiTiKWFbGCF02vFv0dPUcVj8XCWUsbEdmDgoZjPjG0wLVD4T0o8wqL6JlcQ9VxZE7DeJA==~1; mp_60483c180bee99d71ee5c084d7bb9d20_mixpanel=%7B%22distinct_id%22%3A%20%2219208facf441158-0d1a6c5c8fef46-26001051-100200-19208facf45160f%22%2C%22%24device_id%22%3A%20%2219208facf441158-0d1a6c5c8fef46-26001051-100200-19208facf45160f%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22Is%20Anonymous%22%3A%20%22False%22%2C%22Instance_Id%22%3A%20%227c68c5fc-7b55-4bf5-8187-7dbc9005%22%2C%22Session%20ID%22%3A%20%2280ec3624-528c-4943-8a52-a0a97d18%22%2C%22V2%20Cat-Nav%20Exp%20Enabled%22%3A%20true%2C%22last%20event%20time%22%3A%201726727562356%2C%22__alias%22%3A%20122190837%2C%22%24user_id%22%3A%20122190837%7D'''
        }
    headers = {
        'authority': 'www.meesho.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'ANONYMOUS_USER_CONFIG=j%3A%7B%22clientId%22%3A%22eb790bc6-0396-404e-8f52-9b6913fa%22%2C%22instanceId%22%3A%22eb790bc6-0396-404e-8f52-9b6913fa%22%2C%22xo%22%3A%22eyJ0eXBlIjoiY29tcG9zaXRlIn0%3D.eyJqd3QiOiJleUpvZEhSd2N6b3ZMMjFsWlhOb2J5NWpiMjB2ZG1WeWMybHZiaUk2SWpFaUxDSm9kSFJ3Y3pvdkwyMWxaWE5vYnk1amIyMHZhWE52WDJOdmRXNTBjbmxmWTI5a1pTSTZJa2xPSWl3aVlXeG5Jam9pU0ZNeU5UWWlmUS5leUpwWVhRaU9qRTNNalkyTmpjNU5UWXNJbVY0Y0NJNk1UZzRORE0wTnprMU5pd2lhSFIwY0hNNkx5OXRaV1Z6YUc4dVkyOXRMMmx1YzNSaGJtTmxYMmxrSWpvaVpXSTNPVEJpWXpZdE1ETTVOaTAwTURSbExUaG1OVEl0T1dJMk9URXpabUVpTENKb2RIUndjem92TDIxbFpYTm9ieTVqYjIwdllXNXZibmx0YjNWelgzVnpaWEpmYVdRaU9pSXpPR1l5T1dJM1lpMHdaVFl3TFRReU1Ea3RZVGxtTVMwek16VXpOR1kzTXpjNE1ERWlmUS5Vb2gzWmJQazl3dzZiU0lKSS1YMjBLOTFFLWlmTHpjeDRjUFlHaU5FMFdBIiwieG8iOm51bGx9%22%2C%22createdAt%22%3A%222024-09-18T13%3A59%3A16.973Z%22%7D; CAT_NAV_V2_COOKIE=0.3651788913543481; ak_bmsc=B0CBAB39BE72932B3E98919E287581D0~000000000000000000000000000000~YAAQZB0gF7YaGMWRAQAAltn7DRm8YvLHaN2FZxux3CQ5qSOxkkOrnehlOfJnbxayL3201G6H5wmI5zl7lPqrWPMVq5J2grdiVVpDN/3iMq75Z0gT7C0aFQsnL9ydBJOpVYjS83/PwJH1dVqj3xZWRDO134d+ZpnZTMks132cJpI/4oZK6rWjo+CubK95dVlzzXjma3qyKyYgtGTMXhuf60ZC/F7EfBBrVcuvVBzEMfizkrO7+8D9z3UFerfMVTlmo9TzOci/15+OTw1+o2rWXNboXOSHHaX7GougDAzFe+luO01/yWszMFQKzwCXjjjoM51hHSllrhz3CEExPwRh3SR5rBG6JXC+xfYsQ0aPPhtebaXsNn0BdWrFIrhBeAMnSvC+/LlbVG9E6w5e3ksPgHtwZG7vdhY9g0AwCVvJ7loxF1DQBrq+dBAb9ams; __logged_in_user_id_=407056230; _is_logged_in_=1; __connect.sid__=s%3AxABlza7mm1v4gWT8vsAyMWPxqWolfuqx.JmbiVQP0a0Llf%2F1wYyp%2BVKgws%2BoWkpDp8QKcV%2FQEIPU; _abck=2F29253D8F0510BD848D713A2400B3D9~0~YAAQZB0gFxInGMWRAQAA8nf8DQx7wM21FE7Idz6JoKhDlTVWy3FAGCFn0etY/Xwd58kx0YIToxy0DjrlaIhPQY7kUvWBwJYzhPmDNp+BGRmCeN5wykd/EO0JqbJ60sDPC1YoiRvSHt0qk/lRdSiBZpUNWkwGJPl8LeoDD26qHxwHQKfiM0qGZXNR2qTnDJcEVFBQHZbTw/xidSGKpKxP8B225dUsC0J1SpqKK7J04tiKJh04eqNEhBbQgZVTjob18WSzjzSvL9W9vk9fisO1FyzwyaMlWoZpJnYqPB5ST7dVg/x73EiUPpG9DmxJ9hS1/LEht6FX6DweWWp28KUxcxkpK87SgD/McOVwtqT86A27aQaMMMOSVTvRwrMpAWI5NKMWnaMnVNdDGe8zmPKWRJGPodHWoAs27wyxmE2L8sBfSY/i1u9M4jghtOYgogOiIUznJ3DIyk2b+1IrahPKE5Aj5Hak4Tuac+2eRYqXdgWVscHa0jMfSxHmeqzFzLou7DpSfAE1AMcYM8oWPXDG64aRtQ5oMx97rjVQ4ksW0ydub4PQHWTgMwiR+B7fKtKrO+WjKks7Zqp3h6i0dkmXDmfKU4U5y/gSC5Tczr5ca83FzyhicxHjf+KYeD7VXgalMXzNHu1d1Ueti5SwjQ3joZsEkcCP/+m0aQk9dMytcAX6CH0Bqez2RNC1G6E=~-1~-1~1726815062; bm_sz=6AADC554B3DA6772A3A3102CAD13495C~YAAQZB0gFxQnGMWRAQAA8nf8DRkQaiAWtGGBM0lBQ//4rAIKgFe0UYn30I41S5+GbmlGjdF9MHNc+vnM8s9YOK5+IG6e7zCFSI5tvcqpbrQMPvV9znNOjVJZSDTdQI5vc13LgUSyVrdyhWzISo8opZUhdnmnubwpzrSzARusBsIqLPzljdsSomduD5DKH93+BO/zj3T11ZGN0a+kBW0IHir6/ojQvCzOWGEHM+hcCEnVglpPBBLpy3Glg2ojFgaAMIqAPnjG41veiv5zig2sUOTOqRIWBoQ59Rf/tQ1w2+MUCo3phYkZp8gAmhEiuJpXMZ84Gc3XajtLM2pTLtd9kblyPXzz5F+Z68vdNnYZYDuaqcgHx+ql9pzPCz0FxQ/FrNsVUIp5dJFnujdLgETl2ObAoe1RR/i5SKs2wdpphXx8~4337716~4272695; location-details=%7B%22city%22%3A%22Bengaluru%22%2C%22pincode%22%3A%22560001%22%2C%22lat%22%3A%2213.2257%22%2C%22long%22%3A%2277.575%22%7D; bm_sv=E0D842B63D7305B8D37C51AEB41E25BC~YAAQZB0gF0UnGMWRAQAAlHr8DRl4n2Q5BOGgi89g5IOLk4LacVjWQMhLoREthUiNkzGrrx/zNhqX/x/AsMTUFrgU8zfigInjZKlgN+BbktZWZrn2a5376/cRpIR1hgejwapWKEeCys3b6FiBJdY6AeSGjzJA6IFxiFAJqSv1DDuSkYjseYoXUJfjrVWti5o733e2xTTBH3LioelOdd3WZ7rVfvHoBcH/87x5b/40Zs6LG59TndCYPrS0MyADyU0P~1; mp_60483c180bee99d71ee5c084d7bb9d20_mixpanel=%7B%22distinct_id%22%3A%20%221920dfbd9c15a4-082861802bbb87-26001051-100200-1920dfbd9c295c%22%2C%22%24device_id%22%3A%20%221920dfbd9c15a4-082861802bbb87-26001051-100200-1920dfbd9c295c%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22%24user_id%22%3A%20407056230%2C%22Is%20Anonymous%22%3A%20%22False%22%2C%22Instance_Id%22%3A%20%22eb790bc6-0396-404e-8f52-9b6913fa%22%2C%22Session%20ID%22%3A%20%2293dc78af-91f5-4c9a-aebd-9c5979b8%22%2C%22V2%20Cat-Nav%20Exp%20Enabled%22%3A%20true%2C%22last%20event%20time%22%3A%201726811503437%2C%22__alias%22%3A%20407056230%7D',
        'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61',
    }
    # headers = {
    #     'accept': 'application/json, text/plain, */*',
    #     'accept-language': 'en-US,en;q=0.9',
    #     'content-type': 'application/json',
    #     # 'cookie': 'ANONYMOUS_USER_CONFIG=j%3A%7B%22clientId%22%3A%227c68c5fc-7b55-4bf5-8187-7dbc9005%22%2C%22instanceId%22%3A%227c68c5fc-7b55-4bf5-8187-7dbc9005%22%2C%22xo%22%3A%22eyJ0eXBlIjoiY29tcG9zaXRlIn0%3D.eyJqd3QiOiJleUpvZEhSd2N6b3ZMMjFsWlhOb2J5NWpiMjB2ZG1WeWMybHZiaUk2SWpFaUxDSm9kSFJ3Y3pvdkwyMWxaWE5vYnk1amIyMHZhWE52WDJOdmRXNTBjbmxmWTI5a1pTSTZJa2xPSWl3aVlXeG5Jam9pU0ZNeU5UWWlmUS5leUpwWVhRaU9qRTNNalkzTWpjMU1EWXNJbVY0Y0NJNk1UZzRORFF3TnpVd05pd2lhSFIwY0hNNkx5OXRaV1Z6YUc4dVkyOXRMMmx1YzNSaGJtTmxYMmxrSWpvaU4yTTJPR00xWm1NdE4ySTFOUzAwWW1ZMUxUZ3hPRGN0TjJSaVl6a3dNRFVpTENKb2RIUndjem92TDIxbFpYTm9ieTVqYjIwdllXNXZibmx0YjNWelgzVnpaWEpmYVdRaU9pSTBOVFU0WldOalpDMDRPVFpoTFRRMU1ESXRPVEJrWmkwM01HVTNZVFJtWXpRM1pEVWlmUS5oNEg4VGItcW50UElUZ0hxdFFlSWw3ellYd1JvUC1TQkRRNm0zeEtJbmE4IiwieG8iOm51bGx9%22%2C%22createdAt%22%3A%222024-09-19T06%3A31%3A46.792Z%22%7D; CAT_NAV_V2_COOKIE=0.732209005778147; ak_bmsc=4206D701613F598A8B800E6C2646DD4D~000000000000000000000000000000~YAAQDQkgF/Hyl9uRAQAAUNP6CBmf3INBoxDTE8YRyYlUI2BMo6pieUZgp3WQOOPb/7ai+xc98UPk1HA+VgnzjQPvkyQ7JOHZ0cP4wPWpOcI9x/wCOnHfBqM9vKoFks7HPJDJhYSmqjxmYrwK8AIloThoeMqHYZRX5SreRmd5l3jZrPj0P/GV9Xxj1LVHC++EwENNft1bfZnrPqwCQJ0bqy10PoHPYLa4H4SHurM66IELGDtepOe3OxGKOwf4yX3vLUnIjgCcUSnTaEhmhbIP1SVBfpEi+Uek0xmExUqFi70eAo3Zci+/e2dhZrJb5r5rcdDAjZCiX7NJ+qbljbHcavw3W/l9KSlq5R0XM8nWQKHbnTE++fnPxaNZQx4Ff3KIbSDGDf/aBIr0LKfDKCbYieQeB4I6LZ+HL3VgxYVfIkXrw1Sg35Obf0/Cmgp6tM27x4jofbo=; __logged_in_user_id_=122190837; _is_logged_in_=1; __connect.sid__=s%3AGyTlSALkWbhAPW_8d5C0Qcn6K0P67izU.uLAOHACRKCPsc%2F4wr536lrn16FJbo7HngMxKsW437Ks; _abck=231D5B0C4AB0E82BDE15F18FC1B827D3~0~YAAQDQkgFx0dmNuRAQAAN1/7CAwW/WcGviUsIyp5ktVM8g42Kt9eDrYASn4T9OH2P7Q2rwYtVmExSuyKQVD3n/vU4416VGoM80BIDr3OhnOoI9153v9Q8kq2E8SQDTj6gAj02qxDGnGNR+WWehRHFwKROTwBBGWzzBvUBgRaozAXhEgexsgubJk8E5NDPBWwsizHBm4NJ6cpZFJVVqe8xdHGgjq/z7vx4xqV/ygaGP5PU22e19RMHXBP+Pj07thsmSV302qJP8zGB+p+XUlWydX3yh/bo0+ZeKbuzHypdecdvYVblwAXz3/G28TG3XO45SeMl2z+3jYMrYynD/7zkbVxAesvEr0gP31TeRG9QSHLD17F1wRPHn+iTdda4Sm/PJmBV2mx7kegJ7pqjYT7YU94DM4y4f1ezBXmXBB1X9Clk0N2ekpeJFadx6zE3OFVlZIXM2bedHAcMHTlbrcVzwFkl3UIOp6WWyrJsZNGpzZ4IwMOi8lZ5mRqZPMvtx9fmU5zzEJNHQpnhx+Hx7bYjUx28uVKRieTy33+tkQxS1Z02vAi90h/c2FOz9FIIe7DJw92n2qge58=~-1~-1~1726731108; bm_sz=3165F22D376EF5293D3645180EF194B9~YAAQDQkgFx8dmNuRAQAAN1/7CBkJi/DHHvA26uImXxlNAGJqspUiDKrVXywPNm4EPj4CQQ0HDu3E/m0JaPZcv5icSAjXH8eQk/BJoJM1drN2yYUUMgByrh0hin6V9ui9X0b82jSIXeH8K6BuuL5F7728tQQiuHjqKj/JalmT2XhZ/Vi2DaMTOLcMbwQEEzP1XQjvkcpzAnL/KBzBTW1PyUC9t9O8D4YSqdPa+lAQx0ipRx5NjvBRNdpcot6Sm29bwJ8/Mgv898j19d7xvSnzQtlA5LCsmXX8WmflbgVPAyvDTMFG3rs/eU8YLqM4YJdtXRKrO0laWx0sg2XWky80boG5OgKr+Pxd9l4qLiHk2zFrM7gAa3xK45vhwozCMh9K0kROZlkwXLalKjAXUG26i4AAW99RSMO33A==~3355954~3553093; location-details=%7B%22city%22%3A%22Bengaluru%22%2C%22pincode%22%3A%22560001%22%2C%22lat%22%3A%2213.2257%22%2C%22long%22%3A%2277.575%22%7D; INP_POW=0.5202813040675851; bm_sv=637023C546B89F59D04AEAA4E9FE8F9D~YAAQDQkgF04nmNuRAQAAFoP7CBmeoQvqOmodBiUjKG0KkRG80LyHBh/Lar+7ZJsh47aDgCNcYz9n7+x34OeLFZ/BWNxBTSHefAfHpTMY0LRvFSPhGPqXyRZVShh/fKkkMoKxhJNikp544pOIBVBZ3ecHiM7MW4SOWvIZoiRqqDRzqlEXHKdGmoi3glBA5kiTiKWFbGCF02vFv0dPUcVj8XCWUsbEdmDgoZjPjG0wLVD4T0o8wqL6JlcQ9VxZE7DeJA==~1; mp_60483c180bee99d71ee5c084d7bb9d20_mixpanel=%7B%22distinct_id%22%3A%20%2219208facf441158-0d1a6c5c8fef46-26001051-100200-19208facf45160f%22%2C%22%24device_id%22%3A%20%2219208facf441158-0d1a6c5c8fef46-26001051-100200-19208facf45160f%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22Is%20Anonymous%22%3A%20%22False%22%2C%22Instance_Id%22%3A%20%227c68c5fc-7b55-4bf5-8187-7dbc9005%22%2C%22Session%20ID%22%3A%20%2280ec3624-528c-4943-8a52-a0a97d18%22%2C%22V2%20Cat-Nav%20Exp%20Enabled%22%3A%20true%2C%22last%20event%20time%22%3A%201726727562356%2C%22__alias%22%3A%20122190837%2C%22%24user_id%22%3A%20122190837%7D',
    #     'meesho-iso-country-code': 'IN',
    #     'origin': 'https://www.meesho.com',
    #     'priority': 'u=1, i',
    #     'referer': 'https://www.meesho.com/new-trendy-woman-kurti-with-dupatta/p/76hjbx',
    #     # 'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    #     # 'sec-ch-ua-mobile': '?0',
    #     # 'sec-ch-ua-platform': '"Windows"',
    #     # 'sec-fetch-dest': 'empty',
    #     # 'sec-fetch-mode': 'cors',
    #     # 'sec-fetch-site': 'same-origin',
    #     # 'X-Crawlera-Cookies': 'disable',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    # }

    json_data = {
        'dest_pin': '560001',
        'product_id': '76hjbx',
        'supplier_id': 1879049,
        'quantity': 1,
    }  # Same json_data as in your original request

    response = requests.post(
        'https://www.meesho.com/api/v1/check-shipping-delivery-date',
        # cookies=cookies,
        headers=headers,
        json=json_data,
        proxies=proxy,
        verify=False
    )
    print(response.text)
    return response.text

# Function to make the request using http.client
def make_request_http_client():
    print("Try with make_request_http_client")
    conn = http.client.HTTPSConnection("www.meesho.com")
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'cookie': 'ANONYMOUS_USER_CONFIG=j%3A%7B%22clientId%22%3A%227c68c5fc-7b55-4bf5-8187-7dbc9005%22%2C%22instanceId%22%3A%227c68c5fc-7b55-4bf5-8187-7dbc9005%22%2C%22xo%22%3A%22eyJ0eXBlIjoiY29tcG9zaXRlIn0%3D.eyJqd3QiOiJleUpvZEhSd2N6b3ZMMjFsWlhOb2J5NWpiMjB2ZG1WeWMybHZiaUk2SWpFaUxDSm9kSFJ3Y3pvdkwyMWxaWE5vYnk1amIyMHZhWE52WDJOdmRXNTBjbmxmWTI5a1pTSTZJa2xPSWl3aVlXeG5Jam9pU0ZNeU5UWWlmUS5leUpwWVhRaU9qRTNNalkzTWpjMU1EWXNJbVY0Y0NJNk1UZzRORFF3TnpVd05pd2lhSFIwY0hNNkx5OXRaV1Z6YUc4dVkyOXRMMmx1YzNSaGJtTmxYMmxrSWpvaU4yTTJPR00xWm1NdE4ySTFOUzAwWW1ZMUxUZ3hPRGN0TjJSaVl6a3dNRFVpTENKb2RIUndjem92TDIxbFpYTm9ieTVqYjIwdllXNXZibmx0YjNWelgzVnpaWEpmYVdRaU9pSTBOVFU0WldOalpDMDRPVFpoTFRRMU1ESXRPVEJrWmkwM01HVTNZVFJtWXpRM1pEVWlmUS5oNEg4VGItcW50UElUZ0hxdFFlSWw3ellYd1JvUC1TQkRRNm0zeEtJbmE4IiwieG8iOm51bGx9%22%2C%22createdAt%22%3A%222024-09-19T06%3A31%3A46.792Z%22%7D; CAT_NAV_V2_COOKIE=0.732209005778147; ak_bmsc=4206D701613F598A8B800E6C2646DD4D~000000000000000000000000000000~YAAQDQkgF/Hyl9uRAQAAUNP6CBmf3INBoxDTE8YRyYlUI2BMo6pieUZgp3WQOOPb/7ai+xc98UPk1HA+VgnzjQPvkyQ7JOHZ0cP4wPWpOcI9x/wCOnHfBqM9vKoFks7HPJDJhYSmqjxmYrwK8AIloThoeMqHYZRX5SreRmd5l3jZrPj0P/GV9Xxj1LVHC++EwENNft1bfZnrPqwCQJ0bqy10PoHPYLa4H4SHurM66IELGDtepOe3OxGKOwf4yX3vLUnIjgCcUSnTaEhmhbIP1SVBfpEi+Uek0xmExUqFi70eAo3Zci+/e2dhZrJb5r5rcdDAjZCiX7NJ+qbljbHcavw3W/l9KSlq5R0XM8nWQKHbnTE++fnPxaNZQx4Ff3KIbSDGDf/aBIr0LKfDKCbYieQeB4I6LZ+HL3VgxYVfIkXrw1Sg35Obf0/Cmgp6tM27x4jofbo=; __logged_in_user_id_=122190837; _is_logged_in_=1; __connect.sid__=s%3AGyTlSALkWbhAPW_8d5C0Qcn6K0P67izU.uLAOHACRKCPsc%2F4wr536lrn16FJbo7HngMxKsW437Ks; _abck=231D5B0C4AB0E82BDE15F18FC1B827D3~0~YAAQDQkgFx0dmNuRAQAAN1/7CAwW/WcGviUsIyp5ktVM8g42Kt9eDrYASn4T9OH2P7Q2rwYtVmExSuyKQVD3n/vU4416VGoM80BIDr3OhnOoI9153v9Q8kq2E8SQDTj6gAj02qxDGnGNR+WWehRHFwKROTwBBGWzzBvUBgRaozAXhEgexsgubJk8E5NDPBWwsizHBm4NJ6cpZFJVVqe8xdHGgjq/z7vx4xqV/ygaGP5PU22e19RMHXBP+Pj07thsmSV302qJP8zGB+p+XUlWydX3yh/bo0+ZeKbuzHypdecdvYVblwAXz3/G28TG3XO45SeMl2z+3jYMrYynD/7zkbVxAesvEr0gP31TeRG9QSHLD17F1wRPHn+iTdda4Sm/PJmBV2mx7kegJ7pqjYT7YU94DM4y4f1ezBXmXBB1X9Clk0N2ekpeJFadx6zE3OFVlZIXM2bedHAcMHTlbrcVzwFkl3UIOp6WWyrJsZNGpzZ4IwMOi8lZ5mRqZPMvtx9fmU5zzEJNHQpnhx+Hx7bYjUx28uVKRieTy33+tkQxS1Z02vAi90h/c2FOz9FIIe7DJw92n2qge58=~-1~-1~1726731108; bm_sz=3165F22D376EF5293D3645180EF194B9~YAAQDQkgFx8dmNuRAQAAN1/7CBkJi/DHHvA26uImXxlNAGJqspUiDKrVXywPNm4EPj4CQQ0HDu3E/m0JaPZcv5icSAjXH8eQk/BJoJM1drN2yYUUMgByrh0hin6V9ui9X0b82jSIXeH8K6BuuL5F7728tQQiuHjqKj/JalmT2XhZ/Vi2DaMTOLcMbwQEEzP1XQjvkcpzAnL/KBzBTW1PyUC9t9O8D4YSqdPa+lAQx0ipRx5NjvBRNdpcot6Sm29bwJ8/Mgv898j19d7xvSnzQtlA5LCsmXX8WmflbgVPAyvDTMFG3rs/eU8YLqM4YJdtXRKrO0laWx0sg2XWky80boG5OgKr+Pxd9l4qLiHk2zFrM7gAa3xK45vhwozCMh9K0kROZlkwXLalKjAXUG26i4AAW99RSMO33A==~3355954~3553093; location-details=%7B%22city%22%3A%22Bengaluru%22%2C%22pincode%22%3A%22560001%22%2C%22lat%22%3A%2213.2257%22%2C%22long%22%3A%2277.575%22%7D; INP_POW=0.5202813040675851; bm_sv=637023C546B89F59D04AEAA4E9FE8F9D~YAAQDQkgF04nmNuRAQAAFoP7CBmeoQvqOmodBiUjKG0KkRG80LyHBh/Lar+7ZJsh47aDgCNcYz9n7+x34OeLFZ/BWNxBTSHefAfHpTMY0LRvFSPhGPqXyRZVShh/fKkkMoKxhJNikp544pOIBVBZ3ecHiM7MW4SOWvIZoiRqqDRzqlEXHKdGmoi3glBA5kiTiKWFbGCF02vFv0dPUcVj8XCWUsbEdmDgoZjPjG0wLVD4T0o8wqL6JlcQ9VxZE7DeJA==~1; mp_60483c180bee99d71ee5c084d7bb9d20_mixpanel=%7B%22distinct_id%22%3A%20%2219208facf441158-0d1a6c5c8fef46-26001051-100200-19208facf45160f%22%2C%22%24device_id%22%3A%20%2219208facf441158-0d1a6c5c8fef46-26001051-100200-19208facf45160f%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22Is%20Anonymous%22%3A%20%22False%22%2C%22Instance_Id%22%3A%20%227c68c5fc-7b55-4bf5-8187-7dbc9005%22%2C%22Session%20ID%22%3A%20%2280ec3624-528c-4943-8a52-a0a97d18%22%2C%22V2%20Cat-Nav%20Exp%20Enabled%22%3A%20true%2C%22last%20event%20time%22%3A%201726727562356%2C%22__alias%22%3A%20122190837%2C%22%24user_id%22%3A%20122190837%7D',
        'meesho-iso-country-code': 'IN',
        'origin': 'https://www.meesho.com',
        'priority': 'u=1, i',
        'referer': 'https://www.meesho.com/new-trendy-woman-kurti-with-dupatta/p/76hjbx',
        # 'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        # 'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"Windows"',
        # 'sec-fetch-dest': 'empty',
        # 'sec-fetch-mode': 'cors',
        # 'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }  # Same headers as in your original request
    json_data = json.dumps({
        'dest_pin': '560001',
        'product_id': '76hjbx',
        'supplier_id': 1879049,
        'quantity': 1,
    })  # Convert json_data to string

    conn.request("POST", "/api/v1/check-shipping-delivery-date", json_data, headers)
    response = conn.getresponse()
    print(response.read().decode())
    return response.read().decode()

# Function to make the request using httpx
def make_request_httpx():
    print("Try with make_request_httpx")
    cookies = {'ANONYMOUS_USER_CONFIG=j%3A%7B%22clientId%22%3A%227c68c5fc-7b55-4bf5-8187-7dbc9005%22%2C%22instanceId%22%3A%227c68c5fc-7b55-4bf5-8187-7dbc9005%22%2C%22xo%22%3A%22eyJ0eXBlIjoiY29tcG9zaXRlIn0%3D.eyJqd3QiOiJleUpvZEhSd2N6b3ZMMjFsWlhOb2J5NWpiMjB2ZG1WeWMybHZiaUk2SWpFaUxDSm9kSFJ3Y3pvdkwyMWxaWE5vYnk1amIyMHZhWE52WDJOdmRXNTBjbmxmWTI5a1pTSTZJa2xPSWl3aVlXeG5Jam9pU0ZNeU5UWWlmUS5leUpwWVhRaU9qRTNNalkzTWpjMU1EWXNJbVY0Y0NJNk1UZzRORFF3TnpVd05pd2lhSFIwY0hNNkx5OXRaV1Z6YUc4dVkyOXRMMmx1YzNSaGJtTmxYMmxrSWpvaU4yTTJPR00xWm1NdE4ySTFOUzAwWW1ZMUxUZ3hPRGN0TjJSaVl6a3dNRFVpTENKb2RIUndjem92TDIxbFpYTm9ieTVqYjIwdllXNXZibmx0YjNWelgzVnpaWEpmYVdRaU9pSTBOVFU0WldOalpDMDRPVFpoTFRRMU1ESXRPVEJrWmkwM01HVTNZVFJtWXpRM1pEVWlmUS5oNEg4VGItcW50UElUZ0hxdFFlSWw3ellYd1JvUC1TQkRRNm0zeEtJbmE4IiwieG8iOm51bGx9%22%2C%22createdAt%22%3A%222024-09-19T06%3A31%3A46.792Z%22%7D; CAT_NAV_V2_COOKIE=0.732209005778147; ak_bmsc=4206D701613F598A8B800E6C2646DD4D~000000000000000000000000000000~YAAQDQkgF/Hyl9uRAQAAUNP6CBmf3INBoxDTE8YRyYlUI2BMo6pieUZgp3WQOOPb/7ai+xc98UPk1HA+VgnzjQPvkyQ7JOHZ0cP4wPWpOcI9x/wCOnHfBqM9vKoFks7HPJDJhYSmqjxmYrwK8AIloThoeMqHYZRX5SreRmd5l3jZrPj0P/GV9Xxj1LVHC++EwENNft1bfZnrPqwCQJ0bqy10PoHPYLa4H4SHurM66IELGDtepOe3OxGKOwf4yX3vLUnIjgCcUSnTaEhmhbIP1SVBfpEi+Uek0xmExUqFi70eAo3Zci+/e2dhZrJb5r5rcdDAjZCiX7NJ+qbljbHcavw3W/l9KSlq5R0XM8nWQKHbnTE++fnPxaNZQx4Ff3KIbSDGDf/aBIr0LKfDKCbYieQeB4I6LZ+HL3VgxYVfIkXrw1Sg35Obf0/Cmgp6tM27x4jofbo=; __logged_in_user_id_=122190837; _is_logged_in_=1; __connect.sid__=s%3AGyTlSALkWbhAPW_8d5C0Qcn6K0P67izU.uLAOHACRKCPsc%2F4wr536lrn16FJbo7HngMxKsW437Ks; _abck=231D5B0C4AB0E82BDE15F18FC1B827D3~0~YAAQDQkgFx0dmNuRAQAAN1/7CAwW/WcGviUsIyp5ktVM8g42Kt9eDrYASn4T9OH2P7Q2rwYtVmExSuyKQVD3n/vU4416VGoM80BIDr3OhnOoI9153v9Q8kq2E8SQDTj6gAj02qxDGnGNR+WWehRHFwKROTwBBGWzzBvUBgRaozAXhEgexsgubJk8E5NDPBWwsizHBm4NJ6cpZFJVVqe8xdHGgjq/z7vx4xqV/ygaGP5PU22e19RMHXBP+Pj07thsmSV302qJP8zGB+p+XUlWydX3yh/bo0+ZeKbuzHypdecdvYVblwAXz3/G28TG3XO45SeMl2z+3jYMrYynD/7zkbVxAesvEr0gP31TeRG9QSHLD17F1wRPHn+iTdda4Sm/PJmBV2mx7kegJ7pqjYT7YU94DM4y4f1ezBXmXBB1X9Clk0N2ekpeJFadx6zE3OFVlZIXM2bedHAcMHTlbrcVzwFkl3UIOp6WWyrJsZNGpzZ4IwMOi8lZ5mRqZPMvtx9fmU5zzEJNHQpnhx+Hx7bYjUx28uVKRieTy33+tkQxS1Z02vAi90h/c2FOz9FIIe7DJw92n2qge58=~-1~-1~1726731108; bm_sz=3165F22D376EF5293D3645180EF194B9~YAAQDQkgFx8dmNuRAQAAN1/7CBkJi/DHHvA26uImXxlNAGJqspUiDKrVXywPNm4EPj4CQQ0HDu3E/m0JaPZcv5icSAjXH8eQk/BJoJM1drN2yYUUMgByrh0hin6V9ui9X0b82jSIXeH8K6BuuL5F7728tQQiuHjqKj/JalmT2XhZ/Vi2DaMTOLcMbwQEEzP1XQjvkcpzAnL/KBzBTW1PyUC9t9O8D4YSqdPa+lAQx0ipRx5NjvBRNdpcot6Sm29bwJ8/Mgv898j19d7xvSnzQtlA5LCsmXX8WmflbgVPAyvDTMFG3rs/eU8YLqM4YJdtXRKrO0laWx0sg2XWky80boG5OgKr+Pxd9l4qLiHk2zFrM7gAa3xK45vhwozCMh9K0kROZlkwXLalKjAXUG26i4AAW99RSMO33A==~3355954~3553093; location-details=%7B%22city%22%3A%22Bengaluru%22%2C%22pincode%22%3A%22560001%22%2C%22lat%22%3A%2213.2257%22%2C%22long%22%3A%2277.575%22%7D; INP_POW=0.5202813040675851; bm_sv=637023C546B89F59D04AEAA4E9FE8F9D~YAAQDQkgF04nmNuRAQAAFoP7CBmeoQvqOmodBiUjKG0KkRG80LyHBh/Lar+7ZJsh47aDgCNcYz9n7+x34OeLFZ/BWNxBTSHefAfHpTMY0LRvFSPhGPqXyRZVShh/fKkkMoKxhJNikp544pOIBVBZ3ecHiM7MW4SOWvIZoiRqqDRzqlEXHKdGmoi3glBA5kiTiKWFbGCF02vFv0dPUcVj8XCWUsbEdmDgoZjPjG0wLVD4T0o8wqL6JlcQ9VxZE7DeJA==~1; mp_60483c180bee99d71ee5c084d7bb9d20_mixpanel=%7B%22distinct_id%22%3A%20%2219208facf441158-0d1a6c5c8fef46-26001051-100200-19208facf45160f%22%2C%22%24device_id%22%3A%20%2219208facf441158-0d1a6c5c8fef46-26001051-100200-19208facf45160f%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22Is%20Anonymous%22%3A%20%22False%22%2C%22Instance_Id%22%3A%20%227c68c5fc-7b55-4bf5-8187-7dbc9005%22%2C%22Session%20ID%22%3A%20%2280ec3624-528c-4943-8a52-a0a97d18%22%2C%22V2%20Cat-Nav%20Exp%20Enabled%22%3A%20true%2C%22last%20event%20time%22%3A%201726727562356%2C%22__alias%22%3A%20122190837%2C%22%24user_id%22%3A%20122190837%7D'
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'cookie': 'ANONYMOUS_USER_CONFIG=j%3A%7B%22clientId%22%3A%227c68c5fc-7b55-4bf5-8187-7dbc9005%22%2C%22instanceId%22%3A%227c68c5fc-7b55-4bf5-8187-7dbc9005%22%2C%22xo%22%3A%22eyJ0eXBlIjoiY29tcG9zaXRlIn0%3D.eyJqd3QiOiJleUpvZEhSd2N6b3ZMMjFsWlhOb2J5NWpiMjB2ZG1WeWMybHZiaUk2SWpFaUxDSm9kSFJ3Y3pvdkwyMWxaWE5vYnk1amIyMHZhWE52WDJOdmRXNTBjbmxmWTI5a1pTSTZJa2xPSWl3aVlXeG5Jam9pU0ZNeU5UWWlmUS5leUpwWVhRaU9qRTNNalkzTWpjMU1EWXNJbVY0Y0NJNk1UZzRORFF3TnpVd05pd2lhSFIwY0hNNkx5OXRaV1Z6YUc4dVkyOXRMMmx1YzNSaGJtTmxYMmxrSWpvaU4yTTJPR00xWm1NdE4ySTFOUzAwWW1ZMUxUZ3hPRGN0TjJSaVl6a3dNRFVpTENKb2RIUndjem92TDIxbFpYTm9ieTVqYjIwdllXNXZibmx0YjNWelgzVnpaWEpmYVdRaU9pSTBOVFU0WldOalpDMDRPVFpoTFRRMU1ESXRPVEJrWmkwM01HVTNZVFJtWXpRM1pEVWlmUS5oNEg4VGItcW50UElUZ0hxdFFlSWw3ellYd1JvUC1TQkRRNm0zeEtJbmE4IiwieG8iOm51bGx9%22%2C%22createdAt%22%3A%222024-09-19T06%3A31%3A46.792Z%22%7D; CAT_NAV_V2_COOKIE=0.732209005778147; ak_bmsc=4206D701613F598A8B800E6C2646DD4D~000000000000000000000000000000~YAAQDQkgF/Hyl9uRAQAAUNP6CBmf3INBoxDTE8YRyYlUI2BMo6pieUZgp3WQOOPb/7ai+xc98UPk1HA+VgnzjQPvkyQ7JOHZ0cP4wPWpOcI9x/wCOnHfBqM9vKoFks7HPJDJhYSmqjxmYrwK8AIloThoeMqHYZRX5SreRmd5l3jZrPj0P/GV9Xxj1LVHC++EwENNft1bfZnrPqwCQJ0bqy10PoHPYLa4H4SHurM66IELGDtepOe3OxGKOwf4yX3vLUnIjgCcUSnTaEhmhbIP1SVBfpEi+Uek0xmExUqFi70eAo3Zci+/e2dhZrJb5r5rcdDAjZCiX7NJ+qbljbHcavw3W/l9KSlq5R0XM8nWQKHbnTE++fnPxaNZQx4Ff3KIbSDGDf/aBIr0LKfDKCbYieQeB4I6LZ+HL3VgxYVfIkXrw1Sg35Obf0/Cmgp6tM27x4jofbo=; __logged_in_user_id_=122190837; _is_logged_in_=1; __connect.sid__=s%3AGyTlSALkWbhAPW_8d5C0Qcn6K0P67izU.uLAOHACRKCPsc%2F4wr536lrn16FJbo7HngMxKsW437Ks; _abck=231D5B0C4AB0E82BDE15F18FC1B827D3~0~YAAQDQkgFx0dmNuRAQAAN1/7CAwW/WcGviUsIyp5ktVM8g42Kt9eDrYASn4T9OH2P7Q2rwYtVmExSuyKQVD3n/vU4416VGoM80BIDr3OhnOoI9153v9Q8kq2E8SQDTj6gAj02qxDGnGNR+WWehRHFwKROTwBBGWzzBvUBgRaozAXhEgexsgubJk8E5NDPBWwsizHBm4NJ6cpZFJVVqe8xdHGgjq/z7vx4xqV/ygaGP5PU22e19RMHXBP+Pj07thsmSV302qJP8zGB+p+XUlWydX3yh/bo0+ZeKbuzHypdecdvYVblwAXz3/G28TG3XO45SeMl2z+3jYMrYynD/7zkbVxAesvEr0gP31TeRG9QSHLD17F1wRPHn+iTdda4Sm/PJmBV2mx7kegJ7pqjYT7YU94DM4y4f1ezBXmXBB1X9Clk0N2ekpeJFadx6zE3OFVlZIXM2bedHAcMHTlbrcVzwFkl3UIOp6WWyrJsZNGpzZ4IwMOi8lZ5mRqZPMvtx9fmU5zzEJNHQpnhx+Hx7bYjUx28uVKRieTy33+tkQxS1Z02vAi90h/c2FOz9FIIe7DJw92n2qge58=~-1~-1~1726731108; bm_sz=3165F22D376EF5293D3645180EF194B9~YAAQDQkgFx8dmNuRAQAAN1/7CBkJi/DHHvA26uImXxlNAGJqspUiDKrVXywPNm4EPj4CQQ0HDu3E/m0JaPZcv5icSAjXH8eQk/BJoJM1drN2yYUUMgByrh0hin6V9ui9X0b82jSIXeH8K6BuuL5F7728tQQiuHjqKj/JalmT2XhZ/Vi2DaMTOLcMbwQEEzP1XQjvkcpzAnL/KBzBTW1PyUC9t9O8D4YSqdPa+lAQx0ipRx5NjvBRNdpcot6Sm29bwJ8/Mgv898j19d7xvSnzQtlA5LCsmXX8WmflbgVPAyvDTMFG3rs/eU8YLqM4YJdtXRKrO0laWx0sg2XWky80boG5OgKr+Pxd9l4qLiHk2zFrM7gAa3xK45vhwozCMh9K0kROZlkwXLalKjAXUG26i4AAW99RSMO33A==~3355954~3553093; location-details=%7B%22city%22%3A%22Bengaluru%22%2C%22pincode%22%3A%22560001%22%2C%22lat%22%3A%2213.2257%22%2C%22long%22%3A%2277.575%22%7D; INP_POW=0.5202813040675851; bm_sv=637023C546B89F59D04AEAA4E9FE8F9D~YAAQDQkgF04nmNuRAQAAFoP7CBmeoQvqOmodBiUjKG0KkRG80LyHBh/Lar+7ZJsh47aDgCNcYz9n7+x34OeLFZ/BWNxBTSHefAfHpTMY0LRvFSPhGPqXyRZVShh/fKkkMoKxhJNikp544pOIBVBZ3ecHiM7MW4SOWvIZoiRqqDRzqlEXHKdGmoi3glBA5kiTiKWFbGCF02vFv0dPUcVj8XCWUsbEdmDgoZjPjG0wLVD4T0o8wqL6JlcQ9VxZE7DeJA==~1; mp_60483c180bee99d71ee5c084d7bb9d20_mixpanel=%7B%22distinct_id%22%3A%20%2219208facf441158-0d1a6c5c8fef46-26001051-100200-19208facf45160f%22%2C%22%24device_id%22%3A%20%2219208facf441158-0d1a6c5c8fef46-26001051-100200-19208facf45160f%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22Is%20Anonymous%22%3A%20%22False%22%2C%22Instance_Id%22%3A%20%227c68c5fc-7b55-4bf5-8187-7dbc9005%22%2C%22Session%20ID%22%3A%20%2280ec3624-528c-4943-8a52-a0a97d18%22%2C%22V2%20Cat-Nav%20Exp%20Enabled%22%3A%20true%2C%22last%20event%20time%22%3A%201726727562356%2C%22__alias%22%3A%20122190837%2C%22%24user_id%22%3A%20122190837%7D',
        'meesho-iso-country-code': 'IN',
        'origin': 'https://www.meesho.com',
        'priority': 'u=1, i',
        'referer': 'https://www.meesho.com/new-trendy-woman-kurti-with-dupatta/p/76hjbx',
        # 'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        # 'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"Windows"',
        # 'sec-fetch-dest': 'empty',
        # 'sec-fetch-mode': 'cors',
        # 'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }

    json_data = {
        'dest_pin': '560001',
        'product_id': '76hjbx',
        'supplier_id': 1879049,
        'quantity': 1,
    }  # Same json_data as in your original request

    # with httpx.Client(cookies=cookies) as client:
    with httpx.Client() as client:
        response = client.post(
            'https://www.meesho.com/api/v1/check-shipping-delivery-date',
            headers=headers,
            json=json_data,
        )
    print(response.text)
    return response.text

# Asynchronous function to make the request using aiohttp
async def make_request_aiohttp():
    print("Try with make_request_aiohttp")
    cookies = {
        'ANONYMOUS_USER_CONFIG=j%3A%7B%22clientId%22%3A%227c68c5fc-7b55-4bf5-8187-7dbc9005%22%2C%22instanceId%22%3A%227c68c5fc-7b55-4bf5-8187-7dbc9005%22%2C%22xo%22%3A%22eyJ0eXBlIjoiY29tcG9zaXRlIn0%3D.eyJqd3QiOiJleUpvZEhSd2N6b3ZMMjFsWlhOb2J5NWpiMjB2ZG1WeWMybHZiaUk2SWpFaUxDSm9kSFJ3Y3pvdkwyMWxaWE5vYnk1amIyMHZhWE52WDJOdmRXNTBjbmxmWTI5a1pTSTZJa2xPSWl3aVlXeG5Jam9pU0ZNeU5UWWlmUS5leUpwWVhRaU9qRTNNalkzTWpjMU1EWXNJbVY0Y0NJNk1UZzRORFF3TnpVd05pd2lhSFIwY0hNNkx5OXRaV1Z6YUc4dVkyOXRMMmx1YzNSaGJtTmxYMmxrSWpvaU4yTTJPR00xWm1NdE4ySTFOUzAwWW1ZMUxUZ3hPRGN0TjJSaVl6a3dNRFVpTENKb2RIUndjem92TDIxbFpYTm9ieTVqYjIwdllXNXZibmx0YjNWelgzVnpaWEpmYVdRaU9pSTBOVFU0WldOalpDMDRPVFpoTFRRMU1ESXRPVEJrWmkwM01HVTNZVFJtWXpRM1pEVWlmUS5oNEg4VGItcW50UElUZ0hxdFFlSWw3ellYd1JvUC1TQkRRNm0zeEtJbmE4IiwieG8iOm51bGx9%22%2C%22createdAt%22%3A%222024-09-19T06%3A31%3A46.792Z%22%7D; CAT_NAV_V2_COOKIE=0.732209005778147; ak_bmsc=4206D701613F598A8B800E6C2646DD4D~000000000000000000000000000000~YAAQDQkgF/Hyl9uRAQAAUNP6CBmf3INBoxDTE8YRyYlUI2BMo6pieUZgp3WQOOPb/7ai+xc98UPk1HA+VgnzjQPvkyQ7JOHZ0cP4wPWpOcI9x/wCOnHfBqM9vKoFks7HPJDJhYSmqjxmYrwK8AIloThoeMqHYZRX5SreRmd5l3jZrPj0P/GV9Xxj1LVHC++EwENNft1bfZnrPqwCQJ0bqy10PoHPYLa4H4SHurM66IELGDtepOe3OxGKOwf4yX3vLUnIjgCcUSnTaEhmhbIP1SVBfpEi+Uek0xmExUqFi70eAo3Zci+/e2dhZrJb5r5rcdDAjZCiX7NJ+qbljbHcavw3W/l9KSlq5R0XM8nWQKHbnTE++fnPxaNZQx4Ff3KIbSDGDf/aBIr0LKfDKCbYieQeB4I6LZ+HL3VgxYVfIkXrw1Sg35Obf0/Cmgp6tM27x4jofbo=; __logged_in_user_id_=122190837; _is_logged_in_=1; __connect.sid__=s%3AGyTlSALkWbhAPW_8d5C0Qcn6K0P67izU.uLAOHACRKCPsc%2F4wr536lrn16FJbo7HngMxKsW437Ks; _abck=231D5B0C4AB0E82BDE15F18FC1B827D3~0~YAAQDQkgFx0dmNuRAQAAN1/7CAwW/WcGviUsIyp5ktVM8g42Kt9eDrYASn4T9OH2P7Q2rwYtVmExSuyKQVD3n/vU4416VGoM80BIDr3OhnOoI9153v9Q8kq2E8SQDTj6gAj02qxDGnGNR+WWehRHFwKROTwBBGWzzBvUBgRaozAXhEgexsgubJk8E5NDPBWwsizHBm4NJ6cpZFJVVqe8xdHGgjq/z7vx4xqV/ygaGP5PU22e19RMHXBP+Pj07thsmSV302qJP8zGB+p+XUlWydX3yh/bo0+ZeKbuzHypdecdvYVblwAXz3/G28TG3XO45SeMl2z+3jYMrYynD/7zkbVxAesvEr0gP31TeRG9QSHLD17F1wRPHn+iTdda4Sm/PJmBV2mx7kegJ7pqjYT7YU94DM4y4f1ezBXmXBB1X9Clk0N2ekpeJFadx6zE3OFVlZIXM2bedHAcMHTlbrcVzwFkl3UIOp6WWyrJsZNGpzZ4IwMOi8lZ5mRqZPMvtx9fmU5zzEJNHQpnhx+Hx7bYjUx28uVKRieTy33+tkQxS1Z02vAi90h/c2FOz9FIIe7DJw92n2qge58=~-1~-1~1726731108; bm_sz=3165F22D376EF5293D3645180EF194B9~YAAQDQkgFx8dmNuRAQAAN1/7CBkJi/DHHvA26uImXxlNAGJqspUiDKrVXywPNm4EPj4CQQ0HDu3E/m0JaPZcv5icSAjXH8eQk/BJoJM1drN2yYUUMgByrh0hin6V9ui9X0b82jSIXeH8K6BuuL5F7728tQQiuHjqKj/JalmT2XhZ/Vi2DaMTOLcMbwQEEzP1XQjvkcpzAnL/KBzBTW1PyUC9t9O8D4YSqdPa+lAQx0ipRx5NjvBRNdpcot6Sm29bwJ8/Mgv898j19d7xvSnzQtlA5LCsmXX8WmflbgVPAyvDTMFG3rs/eU8YLqM4YJdtXRKrO0laWx0sg2XWky80boG5OgKr+Pxd9l4qLiHk2zFrM7gAa3xK45vhwozCMh9K0kROZlkwXLalKjAXUG26i4AAW99RSMO33A==~3355954~3553093; location-details=%7B%22city%22%3A%22Bengaluru%22%2C%22pincode%22%3A%22560001%22%2C%22lat%22%3A%2213.2257%22%2C%22long%22%3A%2277.575%22%7D; INP_POW=0.5202813040675851; bm_sv=637023C546B89F59D04AEAA4E9FE8F9D~YAAQDQkgF04nmNuRAQAAFoP7CBmeoQvqOmodBiUjKG0KkRG80LyHBh/Lar+7ZJsh47aDgCNcYz9n7+x34OeLFZ/BWNxBTSHefAfHpTMY0LRvFSPhGPqXyRZVShh/fKkkMoKxhJNikp544pOIBVBZ3ecHiM7MW4SOWvIZoiRqqDRzqlEXHKdGmoi3glBA5kiTiKWFbGCF02vFv0dPUcVj8XCWUsbEdmDgoZjPjG0wLVD4T0o8wqL6JlcQ9VxZE7DeJA==~1; mp_60483c180bee99d71ee5c084d7bb9d20_mixpanel=%7B%22distinct_id%22%3A%20%2219208facf441158-0d1a6c5c8fef46-26001051-100200-19208facf45160f%22%2C%22%24device_id%22%3A%20%2219208facf441158-0d1a6c5c8fef46-26001051-100200-19208facf45160f%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22Is%20Anonymous%22%3A%20%22False%22%2C%22Instance_Id%22%3A%20%227c68c5fc-7b55-4bf5-8187-7dbc9005%22%2C%22Session%20ID%22%3A%20%2280ec3624-528c-4943-8a52-a0a97d18%22%2C%22V2%20Cat-Nav%20Exp%20Enabled%22%3A%20true%2C%22last%20event%20time%22%3A%201726727562356%2C%22__alias%22%3A%20122190837%2C%22%24user_id%22%3A%20122190837%7D'
        }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'cookie': 'ANONYMOUS_USER_CONFIG=j%3A%7B%22clientId%22%3A%227c68c5fc-7b55-4bf5-8187-7dbc9005%22%2C%22instanceId%22%3A%227c68c5fc-7b55-4bf5-8187-7dbc9005%22%2C%22xo%22%3A%22eyJ0eXBlIjoiY29tcG9zaXRlIn0%3D.eyJqd3QiOiJleUpvZEhSd2N6b3ZMMjFsWlhOb2J5NWpiMjB2ZG1WeWMybHZiaUk2SWpFaUxDSm9kSFJ3Y3pvdkwyMWxaWE5vYnk1amIyMHZhWE52WDJOdmRXNTBjbmxmWTI5a1pTSTZJa2xPSWl3aVlXeG5Jam9pU0ZNeU5UWWlmUS5leUpwWVhRaU9qRTNNalkzTWpjMU1EWXNJbVY0Y0NJNk1UZzRORFF3TnpVd05pd2lhSFIwY0hNNkx5OXRaV1Z6YUc4dVkyOXRMMmx1YzNSaGJtTmxYMmxrSWpvaU4yTTJPR00xWm1NdE4ySTFOUzAwWW1ZMUxUZ3hPRGN0TjJSaVl6a3dNRFVpTENKb2RIUndjem92TDIxbFpYTm9ieTVqYjIwdllXNXZibmx0YjNWelgzVnpaWEpmYVdRaU9pSTBOVFU0WldOalpDMDRPVFpoTFRRMU1ESXRPVEJrWmkwM01HVTNZVFJtWXpRM1pEVWlmUS5oNEg4VGItcW50UElUZ0hxdFFlSWw3ellYd1JvUC1TQkRRNm0zeEtJbmE4IiwieG8iOm51bGx9%22%2C%22createdAt%22%3A%222024-09-19T06%3A31%3A46.792Z%22%7D; CAT_NAV_V2_COOKIE=0.732209005778147; ak_bmsc=4206D701613F598A8B800E6C2646DD4D~000000000000000000000000000000~YAAQDQkgF/Hyl9uRAQAAUNP6CBmf3INBoxDTE8YRyYlUI2BMo6pieUZgp3WQOOPb/7ai+xc98UPk1HA+VgnzjQPvkyQ7JOHZ0cP4wPWpOcI9x/wCOnHfBqM9vKoFks7HPJDJhYSmqjxmYrwK8AIloThoeMqHYZRX5SreRmd5l3jZrPj0P/GV9Xxj1LVHC++EwENNft1bfZnrPqwCQJ0bqy10PoHPYLa4H4SHurM66IELGDtepOe3OxGKOwf4yX3vLUnIjgCcUSnTaEhmhbIP1SVBfpEi+Uek0xmExUqFi70eAo3Zci+/e2dhZrJb5r5rcdDAjZCiX7NJ+qbljbHcavw3W/l9KSlq5R0XM8nWQKHbnTE++fnPxaNZQx4Ff3KIbSDGDf/aBIr0LKfDKCbYieQeB4I6LZ+HL3VgxYVfIkXrw1Sg35Obf0/Cmgp6tM27x4jofbo=; __logged_in_user_id_=122190837; _is_logged_in_=1; __connect.sid__=s%3AGyTlSALkWbhAPW_8d5C0Qcn6K0P67izU.uLAOHACRKCPsc%2F4wr536lrn16FJbo7HngMxKsW437Ks; _abck=231D5B0C4AB0E82BDE15F18FC1B827D3~0~YAAQDQkgFx0dmNuRAQAAN1/7CAwW/WcGviUsIyp5ktVM8g42Kt9eDrYASn4T9OH2P7Q2rwYtVmExSuyKQVD3n/vU4416VGoM80BIDr3OhnOoI9153v9Q8kq2E8SQDTj6gAj02qxDGnGNR+WWehRHFwKROTwBBGWzzBvUBgRaozAXhEgexsgubJk8E5NDPBWwsizHBm4NJ6cpZFJVVqe8xdHGgjq/z7vx4xqV/ygaGP5PU22e19RMHXBP+Pj07thsmSV302qJP8zGB+p+XUlWydX3yh/bo0+ZeKbuzHypdecdvYVblwAXz3/G28TG3XO45SeMl2z+3jYMrYynD/7zkbVxAesvEr0gP31TeRG9QSHLD17F1wRPHn+iTdda4Sm/PJmBV2mx7kegJ7pqjYT7YU94DM4y4f1ezBXmXBB1X9Clk0N2ekpeJFadx6zE3OFVlZIXM2bedHAcMHTlbrcVzwFkl3UIOp6WWyrJsZNGpzZ4IwMOi8lZ5mRqZPMvtx9fmU5zzEJNHQpnhx+Hx7bYjUx28uVKRieTy33+tkQxS1Z02vAi90h/c2FOz9FIIe7DJw92n2qge58=~-1~-1~1726731108; bm_sz=3165F22D376EF5293D3645180EF194B9~YAAQDQkgFx8dmNuRAQAAN1/7CBkJi/DHHvA26uImXxlNAGJqspUiDKrVXywPNm4EPj4CQQ0HDu3E/m0JaPZcv5icSAjXH8eQk/BJoJM1drN2yYUUMgByrh0hin6V9ui9X0b82jSIXeH8K6BuuL5F7728tQQiuHjqKj/JalmT2XhZ/Vi2DaMTOLcMbwQEEzP1XQjvkcpzAnL/KBzBTW1PyUC9t9O8D4YSqdPa+lAQx0ipRx5NjvBRNdpcot6Sm29bwJ8/Mgv898j19d7xvSnzQtlA5LCsmXX8WmflbgVPAyvDTMFG3rs/eU8YLqM4YJdtXRKrO0laWx0sg2XWky80boG5OgKr+Pxd9l4qLiHk2zFrM7gAa3xK45vhwozCMh9K0kROZlkwXLalKjAXUG26i4AAW99RSMO33A==~3355954~3553093; location-details=%7B%22city%22%3A%22Bengaluru%22%2C%22pincode%22%3A%22560001%22%2C%22lat%22%3A%2213.2257%22%2C%22long%22%3A%2277.575%22%7D; INP_POW=0.5202813040675851; bm_sv=637023C546B89F59D04AEAA4E9FE8F9D~YAAQDQkgF04nmNuRAQAAFoP7CBmeoQvqOmodBiUjKG0KkRG80LyHBh/Lar+7ZJsh47aDgCNcYz9n7+x34OeLFZ/BWNxBTSHefAfHpTMY0LRvFSPhGPqXyRZVShh/fKkkMoKxhJNikp544pOIBVBZ3ecHiM7MW4SOWvIZoiRqqDRzqlEXHKdGmoi3glBA5kiTiKWFbGCF02vFv0dPUcVj8XCWUsbEdmDgoZjPjG0wLVD4T0o8wqL6JlcQ9VxZE7DeJA==~1; mp_60483c180bee99d71ee5c084d7bb9d20_mixpanel=%7B%22distinct_id%22%3A%20%2219208facf441158-0d1a6c5c8fef46-26001051-100200-19208facf45160f%22%2C%22%24device_id%22%3A%20%2219208facf441158-0d1a6c5c8fef46-26001051-100200-19208facf45160f%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22Is%20Anonymous%22%3A%20%22False%22%2C%22Instance_Id%22%3A%20%227c68c5fc-7b55-4bf5-8187-7dbc9005%22%2C%22Session%20ID%22%3A%20%2280ec3624-528c-4943-8a52-a0a97d18%22%2C%22V2%20Cat-Nav%20Exp%20Enabled%22%3A%20true%2C%22last%20event%20time%22%3A%201726727562356%2C%22__alias%22%3A%20122190837%2C%22%24user_id%22%3A%20122190837%7D',
        'meesho-iso-country-code': 'IN',
        'origin': 'https://www.meesho.com',
        'priority': 'u=1, i',
        'referer': 'https://www.meesho.com/new-trendy-woman-kurti-with-dupatta/p/76hjbx',
        # 'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        # 'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"Windows"',
        # 'sec-fetch-dest': 'empty',
        # 'sec-fetch-mode': 'cors',
        # 'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }

    json_data = {
        'dest_pin': '560001',
        'product_id': '76hjbx',
        'supplier_id': 1879049,
        'quantity': 1,
    }# Same json_data as in your original request

    # async with aiohttp.ClientSession(cookies=cookies) as session:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'https://www.meesho.com/api/v1/check-shipping-delivery-date',
            headers=headers,
            json=json_data,
            proxies=proxy,
            verify=False
        ) as response:
            print(response.text())
            return await response.text()

async def main():
    count = 0
    # Make requests with different libraries
    for i in range(20):

        response = make_request_requests()
        if 'delivery_date' in response:
            count += 1
            print("Response successful..", count)
        else:
            response = make_request_http_client()
            if 'delivery_date' in response:
                count += 1
                print("Response successful..", count)
            else:
                response = make_request_httpx()
                if 'delivery_date' in response:
                    count += 1
                    print("Response successful..", count)
                else:
                    response = await make_request_aiohttp()
                    if 'delivery_date' in response:
                        count += 1
                        print("Response successful..", count)
                    else:
                        count += 1
                        print("Retry for..", count)


if __name__ == '__main__':
    asyncio.run(main())
