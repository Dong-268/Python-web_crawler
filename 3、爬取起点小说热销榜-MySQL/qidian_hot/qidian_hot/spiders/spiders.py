# coding:utf-8

from scrapy import Request
from scrapy.spiders import Spider
from qidian_hot.items import QidianHotItem


class HotSpider(Spider):
    name = "hot_novel"
    page = 1
    headers = {
        'User-Agent': 'ozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/8'
                      '8.0.4324.190 Safari/537.36'
    }

    def start_requests(self):
        url = 'https://www.qidian.com/rank/hotsales?style=1&page=1'
        yield Request(url=url, headers=self.headers, callback=self.hot_parse)

    def hot_parse(self, response):
        # 使用xpath定位到小说内容的div元素中，保存与列表
        list_selector = response.xpath("//div[@class='book-mid-info']")
        for one_selector in list_selector:
            # 小说名称
            title = one_selector.xpath("h4/a/text()").extract_first()
            # 小说作者
            author = one_selector.xpath("p[1]/a[1]/text()").extract()[0]
            # 类型
            type_ = one_selector.xpath("p[1]/a[2]/text()").extract()[0]
            # 状态
            state = one_selector.xpath("p[1]/span/text()").extract()[0]
            print(title, author, type_, state)

            # 将抓取到的一部小说信息保存到item中
            item = QidianHotItem()
            item['title'] = title
            item['author'] = author
            item['type'] = type_
            item['state'] = state

            yield item

            # 爬取下一页
            self.page += 1
            # 爬取最大是5页数据
            if self.page <= 5:
                next_url = 'https://www.qidian.com/rank/hotsales?style=1&page=%s'%self.page
                yield Request(url=next_url, headers=self.headers, callback=self.hot_parse)