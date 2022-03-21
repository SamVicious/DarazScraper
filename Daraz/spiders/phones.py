import scrapy
from ..items import DarazItem, ProductItem


class PhonesSpider(scrapy.Spider):
    name = 'phones'
    start_urls = ['http://daraz.com.np/smartphones/']
    allowed_domains = ['daraz.com.np']

    def parse(self, response, **kwargs):
        pages = response.css('.ant-pagination-item-22 a').css('::text').get()
        for page in range(2, int(pages)):
            next_page = '/smartphones/?page=' + str(page)
            yield response.follow(next_page, callback=self.parse_page)
            break
    def parse_page(self, response):
        items = DarazItem()
        titles = response.css('.c2prKC .c16H9d a').css('::text').extract()
        prices = response.css('.c2prKC .c3gUW0 .c13VH6').css('::text').extract()
        # images = response.css('div div div div a img').css('::attr(src)').extract()
        links = response.css('.c2prKC .cRjKsc a').css('::attr(href)').extract()
        for title, price, link in zip(titles, prices, links):
            items['title'] = title
            items['price'] = price
            items['link'] = link[:-9]
            yield response.follow(link, callback=self.parse_details, meta={'title': title, 'price': price})
        # items['image'] = images   # images are not working, use selenium

    def parse_details(self, response):
        items = ProductItem()
        items['discounted_price'] = response.request.meta['price']
        try:
            original_price = response.css('.pdp-price_size_xs::text')[1].extract()
        except:
            original_price = response.request.meta['price']
            items['original_price'] = original_price
        items['title'] = response.request.meta['title']
        image = response.css('.gallery-preview-panel__image::attr(src)').get()
        items['image'] = image
        yield items

