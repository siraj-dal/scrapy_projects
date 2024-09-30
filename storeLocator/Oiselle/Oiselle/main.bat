taskkill /IM scrapy.exe /F
start "PART:1" scrapy crawl provider_data -a start=1 -a end=10000
start "PART:2" scrapy crawl provider_data -a start=10001 -a end=20000
start "PART:3" scrapy crawl provider_data -a start=20001 -a end=30000
start "PART:4" scrapy crawl provider_data -a start=30001 -a end=40000