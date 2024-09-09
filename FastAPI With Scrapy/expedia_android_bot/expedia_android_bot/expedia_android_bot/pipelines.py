from datetime import datetime

from expedia_android_bot.items import ExpediaAndroidBotItem


class ExpediaAndroidBotPipeline:
    def process_item(self, item, spider):
        today_date = datetime.today().strftime('%Y_%m_%d')
        daily_data_table = spider.configs['tables']['data_table'] + '_' + today_date
        daily_link_table = spider.configs['tables']['link_table'] + '_' + today_date
        database_name = spider.configs['config']['database']

        create_db = f"""CREATE DATABASE IF NOT EXISTS {database_name};"""
        try:
            spider.cursor.execute(create_db)
            spider.client.commit()
        except Exception as e:
            print(e)

        create_table = f"""
                       CREATE TABLE IF NOT EXISTS {daily_data_table} (
                       id INT PRIMARY KEY AUTO_INCREMENT,
                       hotel_id VARCHAR(20),
                       hotel_name VARCHAR(255),
                       hotel_url VARCHAR(255),
                       hotel_address VARCHAR(1000),
                       checkin_date VARCHAR(20),
                       checkout_date VARCHAR(20),
                       room_id VARCHAR(20),
                       room_name VARCHAR(255),
                       currency VARCHAR(3),
                       room_price VARCHAR(10),
                       tax_amount VARCHAR(10),
                       availability VARCHAR(10),
                       occupancy VARCHAR(5),
                       page_hash VARCHAR(255),
                       UNIQUE(hotel_id, hotel_url, checkin_date, checkout_date, occupancy, room_id, room_price)
                       );"""
        try:
            spider.cursor.execute(create_table)
            spider.client.commit()
        except Exception as e:
            print(e)

        if isinstance(item, ExpediaAndroidBotItem):
            try:
                if item['hotel_address']:
                    insert_item = dict(item)
                    insert_item.pop('id')
                    cols = ", ".join(insert_item.keys()).strip(', ')
                    values = tuple(insert_item.values())
                    insert = f"""INSERT INTO {daily_data_table} ({cols}) VALUES {values}"""
                    spider.cursor.execute(insert)
                    spider.client.commit()
            except Exception as e:
                print(e)

            if not item['hotel_address']:
                update = f"""UPDATE {daily_link_table} SET status='Pending', page_hash='{item['page_hash']}' WHERE id={item['id']}"""
                spider.cursor.execute(update)
                spider.client.commit()
            elif item['room_id'] != 'NA':
                update = f"""UPDATE {daily_link_table} SET status='Done', page_hash='{item['page_hash']}' WHERE id={item['id']}"""
                spider.cursor.execute(update)
                spider.client.commit()
            else:
                update = f"""UPDATE {daily_link_table} SET status='Not Available', page_hash='{item['page_hash']}' WHERE id={item['id']}"""
                spider.cursor.execute(update)
                spider.client.commit()

        return item
