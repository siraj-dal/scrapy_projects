from datetime import datetime, timedelta
import pytz

db_host = 'localhost'
db_user = 'root'
db_password = 'actowiz'
db_port = 3306

today = datetime.now(pytz.timezone('Asia/Calcutta'))

# FOR TODAY's Date (in case running after 1:30 PM in india and RUNNING IN OVH)
delivery_date = str(datetime.today().strftime("%d_%m_%Y"))
# delivery_date_time = datetime.now().strftime('%d_%m_%Y_%H_%M')

# FOR TODAY's + 1  Date (in case running before 1:30 PM in india and RUNNING IN OVH)
# delivery_date = (datetime.today() + timedelta(days=1)).strftime("%d%m%Y")

db_name = 'storeLocator'
db_data_table = None

# table query
# CREATE TABLE IF NOT EXISTS {db_config.db_data_table} (
#             `index_id` INT AUTO_INCREMENT PRIMARY KEY,
#             `store_no` VARCHAR(500),
#             `name` VARCHAR(500),
#             `latitude` VARCHAR(500),
#             `longitude` VARCHAR(500),
#             `street` VARCHAR(500),
#             `city` VARCHAR(500),
#             `state` VARCHAR(500),
#             `zip_code` VARCHAR(500),
#             `county` VARCHAR(500),
#             `phone` VARCHAR(500),
#             `open_hours` VARCHAR(500),
#             `url` VARCHAR(500),
#             `provider` VARCHAR(500),
#             `category` VARCHAR(500),
#             `updated_date` VARCHAR(500),
#             `country` VARCHAR(500),
#             `status` VARCHAR(500),
#             `direction_url` VARCHAR(500)
#         );
