# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class QidianHotPipeline:

    def open_spider(self, spider):
        # 连接mysql
        db_name = spider.settings.get('MYSQL_DB_NAME', 'qidian')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        user = spider.settings.get('MYSQL_USER', 'root')
        password = spider.settings.get('MYSQL_PASSWORD', '000')

        self.db_connect = pymysql.connect(db=db_name, host=host, user=user, password=password)
        self.db_cursor = self.db_connect.cursor()


    def process_item(self, item, spider):
        # 写入信息
        sql = "INSERT INTO qidian_hot(name, author, type_, form) VALUES (%s, %s, %s, %s)"
        values = (item['title'], item['author'], item['type'], item['state'],)
        self.db_cursor.execute(sql, values)
        return item

    def close_spider(self, spider):
        self.db_connect.commit()
        # 关闭mysql
        self.db_cursor.close()
        self.db_connect.close()
