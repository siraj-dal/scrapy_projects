taskkill /IM scrapy.exe /F
start "PART:1" scrapy crawl provider_data -a start=351 -a end=10000
start "PART:2" scrapy crawl provider_data -a start=10001 -a end=20000
start "PART:3" scrapy crawl provider_data -a start=8001 -a end=12000
start "PART:4" scrapy crawl provider_data -a start=12001 -a end=16000
start "PART:5" scrapy crawl provider_data -a start=16001 -a end=20000
start "PART:6" scrapy crawl provider_data -a start=20001 -a end=24000
start "PART:7" scrapy crawl provider_data -a start=24001 -a end=28000
start "PART:8" scrapy crawl provider_data -a start=28001 -a end=32000
start "PART:9" scrapy crawl provider_data -a start=32001 -a end=36000
start "PART:10" scrapy crawl provider_data -a start=36001 -a end=40000