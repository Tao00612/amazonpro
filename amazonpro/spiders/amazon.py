import scrapy
import requests
from copy import deepcopy

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    # allowed_domains = ['www.amazon.com']
    start_urls = ['https://www.amazon.cn/b?ie=UTF8&node=42689071&ref_=sa_menu_top_pc_l1']

    def parse(self, response,*args,**kwargs):
        li_list = response.xpath('//div[@class="left_nav browseBox"]/ul/li')
        for li in li_list:
            item = {}
            item['cate'] = li.xpath('./a/text()').extract_first()
            item['cate_url'] = response.urljoin(li.xpath('./a/@href').extract_first())
            yield scrapy.Request(
                url=item['cate_url'],
                callback=self.parse_detail_cate,
                meta={'item':deepcopy(item)}
            )

    def parse_detail_cate(self, response):
        item = deepcopy(response.meta['item'])
        li_list = response.xpath('//div[@id="mainResults"]/ul/li')
        data = response.xpath('//div[@data-index > -1]')[:-2]

        # print(item['cate'],len(li_list))
        if li_list:
            # 第一页
            for li in li_list:
                item['product_name'] = li.xpath('./div/div[3]//h2/text() | ./div/div/div/div[2]/div[1]/div[1]/a/h2/text()').extract_first()
                item['product_price'] = li.xpath('./div/div[5]//a/span[2]/text() | ./div/div/div/div[2]/div[2]/div[1]/div/a/span[2]/text()').extract_first()
                item['product_url'] = li.xpath('./div/div[3]/div[1]/a/@href | ./div/div/div/div[2]/div[1]/div[1]/a/@href').extract_first()
                yield item
            # 翻页 div[contains(@class,"a")
            next_url = response.urljoin(response.xpath('//a[contains(@title,"下一页")]/@href').extract_first())
            if next_url:
                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse_detail_cate,
                    meta={'item':{'cate':item['cate'],'cate_url':item['cate_url']}}
                )
        elif data:

            div_list = response.xpath('//div[@data-index > -1]')[:-2]
            for div in div_list: # a-size-medium s-inline s-access-title a-text-normal
                item['product_name'] = div.xpath('.//span[@class="a-size-base-plus a-color-base a-text-normal"]/text() | .//span[@class="a-size-medium a-color-base a-text-normal"]/text() | .//h2[@class="a-size-medium s-inline s-access-title a-text-normal"]/text()').extract_first()
                item['product_price'] = div.xpath('.//span[@class="a-price-whole"]/text()').extract_first()
                item['product_url'] = response.urljoin(div.xpath('.//h2[@class="a-size-mini a-spacing-none a-color-base s-line-clamp-4"]/a/@href | .//a[@class="a-link-normal a-text-normal"]/@href').extract_first())
                yield item

            # 翻页
            next_url = response.urljoin(response.xpath('//a[contains(text(),"下一页")]/@href').extract_first())
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_detail_cate,
                meta={'item':{'cate':item['cate'],'cate_url':item['cate_url']}}
            )