# -*- coding: utf-8 -*-

import scrapy

from Tencent.items import TencentItem

class TencentpostionSpider(scrapy.Spider):
    name = 'tencentPosition'
    allowed_domains = ['tencent.com']

    offset = 0

    url = "http://hr.tencent.com/position.php?&start="

    start_urls = [url + str(offset)]

    def parse(self, response):
        # print(response.text)
        # print(response.body.decode("utf-8"))
        # print(response.headers)
        nodelist = response.xpath("//tr[@class='even'] | //tr[@class='odd']")

        #IndexError: list index out of range

        for node in nodelist:
            item = TencentItem()
            item['position_url']  = node.xpath('./td[1]/a/@href').extract()[0]
            item['position_name'] = node.xpath('./td[1]/a/text()').extract()[0]
            # position_type = node.xpath('./td[2]/text()').extract()[0] 爬取内容为空时，数组会报越界错误
            position_types_list = node.xpath('./td[2]/text()').extract()
            item['position_type'] = position_types_list[0] if position_types_list else None
            item['position_num'] = node.xpath('./td[3]/text()').extract()[0]
            item['position_address'] = node.xpath('./td[4]/text()').extract()[0]
            #position_time = node.xpath('./td[5]/text()').extract()[0] 爬取内容为空时，数组会报越界错误
            times = node.xpath('./td[5]/text()').extract()
            item['position_time'] = times[0] if times else None
            yield item

        if self.offset < 3040:
            self.offset += 10
            yield scrapy.Request(self.url+str(self.offset),callback=self.parse)