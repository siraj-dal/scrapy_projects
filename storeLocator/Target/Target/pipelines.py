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
from Target.items import dataItem, stateItem
from Target.db_config import DbConfig
obj = DbConfig()

class TargetPipeline:
    def process_item(self, item, spider):
        if isinstance(item, dataItem):
            obj.insert_data_table(item)
        return item