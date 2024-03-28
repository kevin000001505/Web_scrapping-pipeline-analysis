# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2

def process_item(self, item, spider):
    try:
        self.cur.execute(
            """
            INSERT INTO earthquakes (maximum, date, time, scale, depth, place)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (item['maximum'], item['date'], item['time'], item['scale'], item['depth'], item['place'])
        )
        self.connection.commit()
    except Exception as e:
        spider.logger.error(f"Database error: {e}")
        self.connection.rollback()  # Reset the transaction
        raise



class PostgresPipeline(object):
    
    def open_spider(self, spider):
        hostname = 'localhost'
        database = 'Earthquake'
        username = 'postgres'
        pwd = '0105'
        port_id = 5432

        self.connection = psycopg2.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id
        )
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        insert_query = """INSERT INTO earthquakes (maximum, date, time, scale, depth, place) VALUES (%s, %s, %s, %s, %s, %s);"""
        self.cur.execute(insert_query, (
            item.get('maximum', 0),
            item.get('date', ''),
            item.get('time', ''),
            item.get('scale', 0),
            item.get('depth', 0),
            item.get('place', '')
        ))
        self.connection.commit()
        return item