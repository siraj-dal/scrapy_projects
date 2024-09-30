# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from Wolverine.items import dataItem, stateItem
from Wolverine.db_config import DbConfig
obj = DbConfig()

class WolverinePipeline:
    def process_item(self, item, spider):
        if isinstance(item, dataItem):
            obj.insert_data_table(item)
        if isinstance(item,stateItem):
            obj.insert_store_table(item)
        return item