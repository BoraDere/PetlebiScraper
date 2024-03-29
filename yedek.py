import scrapy
import re

class PetlebiSpider(scrapy.Spider):
    name = "petlebi"
    start_urls = [
        "https://www.petlebi.com/kedi-mamasi",
    ]
    allowed_domains = [
        "petlebi.com",
    ]

    def parse(self, response):
        
        for i in range(30):
            url = response.css('div a.p-link::attr(href)').extract()[i]
            name = response.css('div a.p-link::attr(title)').getall()[i]
            price = response.xpath('//*[@class="commerce-discounts"]/text()').getall()[i]
            stock = response.css('div a.p-link::attr(data-gtm-product)').getall()[i].split('dimension2')[1].split('dimension3')[0].split('"')[2]
            category = response.css('div a.p-link::attr(data-gtm-product)').getall()[i].split('category":')[1].split('","quantity')[0].split('"')[1]
            product_id = response.css('div a.p-link::attr(id)').getall()[i].replace('product', '')
            brand = response.css('div a.p-link::attr(data-gtm-product)').getall()[i].split('brand":"')[1].split('"')[0]

            yield scrapy.Request(url,
                                 callback=self.parse_product,
                                 meta={
                                     'url': url, 
                                     'name': name,
                                     'price': price, 
                                     'stock': stock, 
                                     'category': category,
                                     'id': product_id,
                                     'brand': brand
                                 }
                                )
            
        current_page = response.url.split('=')[-1] if '=page' in response.url else 1
        current_page = int(current_page)
        next_page = response.url.split('?')[0] + '?page=' + str(current_page + 1)
        yield scrapy.Request(next_page, callback=self.parse)
        
    def parse_product(self, response):
        # Extract data from the product page
        barcode = response.xpath('//div[text()="BARKOD"]/following-sibling::div/text()').get()
        images = response.css('div a::attr(data-image)').getall()
        description = re.sub(r'\s+', ' ', ' '.join([text.strip() for text in response.xpath('//*[@id="productDescription"]//text()').getall()]))

        # Yield a dictionary with the product data
        yield {
            'url': response.meta['url'],
            'name': response.meta['name'],
            'barcode': barcode,
            'price': response.meta['price'],
            'stock': response.meta['stock'],
            'images': images,
            'description': description,
            'sku': barcode,
            'category': response.meta['category'],
            'id': response.meta['id'],
            'brand': response.meta['brand']
        }


    # product URL: response.css('div a.p-link::attr(href)').extract()
    # product name: response.css('div a.p-link::attr(title)').get()
    # product barcode: product URL -> response.xpath('//div[text()="BARKOD"]/following-sibling::div/text()').get()
    # product price: response.xpath('//*[@class="commerce-discounts"]/text()').get()
    # product stock: response.css('div a.p-link::attr(data-gtm-product)').get().split('dimension2')[1].split('dimension3')[0].split('"')[2]
    # product images: product URL -> response.css('div a::attr(data-image)').getall()
    # description: re.sub(r'\s+', ' ', ' '.join([text.strip() for text in response.xpath('//*[@id="productDescription"]//text()').getall()]))
    # sku: barcode ?
    # category: response.css('div a.p-link::attr(data-gtm-product)').get().split('category":')[1].split('","quantity')[0].split('"')[1]
    # product id: response.css('div a.p-link::attr(id)').get().replace('product', '')
    # brand: response.css('div a.p-link::attr(data-gtm-product)').get().split('brand":"')[1].split('"')[0]