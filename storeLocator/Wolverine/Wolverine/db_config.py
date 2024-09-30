import pymysql

class DbConfig():

    def __init__(self):
        self.con = pymysql.Connect(host='localhost',
                                   user='root',
                                   password='actowiz',
                                   database='apparel_store_locator')
        self.cur = self.con.cursor(pymysql.cursors.DictCursor)
        self.store_table = 'wolverine_storeid'
        self.data_table = 'wolverine'

    def create_provider_data_table(self):
        # Check if the table already exists
        check_table_query = f"SHOW TABLES LIKE '{self.data_table}';"
        try:
            self.cur.execute(check_table_query)
            result = self.cur.fetchone()

            if result:
                print(f"Table `{self.data_table}` already exists.")
            else:
                # Proceed with creating the table if it does not exist
                create_table_query = f'''CREATE TABLE IF NOT EXISTS `{self.data_table}` (
                                          `id` int NOT NULL AUTO_INCREMENT,
                                          `store_no` varchar(255) DEFAULT NULL,
                                          `name` varchar(255) DEFAULT NULL,
                                          `latitude` varchar(255) DEFAULT NULL,
                                          `longitude` varchar(255) DEFAULT NULL,
                                          `street` varchar(500) DEFAULT NULL,
                                          `city` varchar(50) DEFAULT NULL,
                                          `state` varchar(50) DEFAULT NULL,
                                          `zip_code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                                          `county` varchar(50) DEFAULT NULL,
                                          `phone` varchar(50) DEFAULT NULL,
                                          `open_hours` varchar(500) DEFAULT NULL,
                                          `url` varchar(255) DEFAULT NULL,
                                          `provider` varchar(50) DEFAULT NULL,
                                          `category` text,
                                          `updated_date` varchar(255) DEFAULT NULL,
                                          `country` tinytext,
                                          `status` tinytext,
                                          `direction_url` varchar(255) DEFAULT NULL,
                                          `pagesave_path` varchar(255) DEFAULT NULL,
                                          `search_state` varchar(255) DEFAULT NULL,
                                          PRIMARY KEY (`id`),
                                          UNIQUE KEY `StoreNo` (`store_no`)
                                          )'''
                self.cur.execute(create_table_query)
                self.con.commit()
                print(f"Table `{self.data_table}` created successfully.")
        except Exception as e:
            print(f"Error: {e}")

    def insert_store_table(self, item):

        query = f'''INSERT INTO {self.data_table} (store_no, status) VALUES (%s, %s)'''
        data = (
            item["store_no"],
            item["status"]
        )

        try:
            self.cur.execute(query.format(data_table=self.data_table), data)
            self.con.commit()
            print(item)
        except Exception as e:
            print(e)

    def insert_data_table(self, item):

        query = f'''
                        INSERT INTO {self.data_table} (store_no, name, latitude, longitude, street, city, state, zip_code, county, phone, open_hours, url, provider, category, updated_date, country, status, direction_url, pagesave_path,search_state)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        '''
        data = (
            item["store_no"],
            item["name"],
            item["latitude"],
            item["longitude"],
            item["street"],
            item["city"],
            item["state"],
            item["zip_code"],
            item["county"],
            item["phone"],
            item["open_hours"],
            item["url"],
            item["provider"],
            item["category"],
            item["updated_date"],
            item["country"],
            item["status"],
            item["direction_url"],
            item["pagesave_path"],
            item["search_state"]

        )

        try:
            self.cur.execute(query.format(data_table=self.data_table), data)
            self.con.commit()
            print(item)
        except Exception as e:
            print(e)

    def update_store_status(self,c_status,store_no):
        qr = f'''update {self.store_table} set status = "{c_status}" where store_no = {store_no}'''
        print(qr)
        try:
            self.cur.execute(qr)
            self.con.commit()
        except Exception as e:
            print(e)

