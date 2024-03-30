import scrapy
import re

class PetlebiSpider(scrapy.Spider):
    name = "petlebi"
    start_urls = [
        "https://www.petlebi.com/kedi-mamasi",
        "https://www.petlebi.com/kedi-vitamin-ve-ek-besinleri",
        "https://www.petlebi.com/kedi-konserve-mamasi",
        "https://www.petlebi.com/kedi-odul-mamasi",
        "https://www.petlebi.com/kedi-kumu",
        "https://www.petlebi.com/kedi-tirmalama-tahtasi",
        "https://www.petlebi.com/kedi-tasmasi",
        "https://www.petlebi.com/kedi-evi",
        "https://www.petlebi.com/kedi-tuvaleti",
        "https://www.petlebi.com/kedi-mama-ve-su-kabi",
        "https://www.petlebi.com/kedi-yataklari",
        "https://www.petlebi.com/kedi-oyuncaklari",
        "https://www.petlebi.com/kedi-kapisi",
        "https://www.petlebi.com/kedi-tasima-cantasi",
        "https://www.petlebi.com/kedi-sampuani",
        "https://www.petlebi.com/kedi-cimi",
        "https://www.petlebi.com/kedi-pire-kene-urunleri",
        "https://www.petlebi.com/kedi-bakim-urunleri",
        "https://www.petlebi.com/kedi-otu",
        "https://www.petlebi.com/kedi-tarak-ve-fircalari",
        "https://www.petlebi.com/kedi-uzaklastirici-sprey",
        "https://www.petlebi.com/kopek-mamasi",
        "https://www.petlebi.com/kopek-kemigi",
        "https://www.petlebi.com/kopek-konserve-mamasi",
        "https://www.petlebi.com/kopek-vitamin-ve-ek-besini",
        "https://www.petlebi.com/kopek-odul-mamasi",
        "https://www.petlebi.com/kopek-oyuncaklari",
        "https://www.petlebi.com/kopek-tasmalari-kayislari",
        "https://www.petlebi.com/egitim-ekipmani",
        "https://www.petlebi.com/kopek-bahce-urunleri",
        "https://www.petlebi.com/kopek-yataklari",
        "https://www.petlebi.com/kopek-tasima-cantasi",
        "https://www.petlebi.com/kopek-kulubesi",
        "https://www.petlebi.com/kopek-mama-ve-su-kabi",
        "https://www.petlebi.com/kopek-elbiseleri",
        "https://www.petlebi.com/kopek-araba-urunleri",
        "https://www.petlebi.com/kopek-bakim-urunleri",
        "https://www.petlebi.com/kopek-parfumu",
        "https://www.petlebi.com/kopek-tarak-ve-fircasi",
        "https://www.petlebi.com/kopek-uzaklastirici-sprey",
        "https://www.petlebi.com/kopek-sampuani",
        "https://www.petlebi.com/kopek-paraziter-pire-kene-engelleyici",
        "https://www.petlebi.com/kus-yemleri",
        "https://www.petlebi.com/kus-kafesleri",
        "https://www.petlebi.com/kus-oyuncaklari",
        "https://www.petlebi.com/kus-yuvalari",
        "https://www.petlebi.com/kus-kumu",
        "https://www.petlebi.com/kus-bakim-urunleri",
        "https://www.petlebi.com/kus-vitaminleri-saglik-urunleri",
        "https://www.petlebi.com/kus-gaga-taslari",
        "https://www.petlebi.com/kus-krakeri-ve-odulleri",
        "https://www.petlebi.com/kus-kafesi-ekipmanlari",
        "https://www.petlebi.com/hamster-petshop-urunleri",
        "https://www.petlebi.com/tavsan-petshop-urunleri",
        "https://www.petlebi.com/guinea-pig-urunleri",
    ]
    allowed_domains = [
        "petlebi.com",
    ]
    # custom_settings = {
    #     'DOWNLOAD_DELAY': 2,  # Add a 2-second delay between requests
    # }

    start_urls = [url + "?page=1" for url in start_urls]

    def parse(self, response):

        products = response.css('div a.p-link')
        
        for product in products:
            url = product.css('::attr(href)').get()
            name = product.css('::attr(title)').get()
            stock = product.css('::attr(data-gtm-product)').get().split('dimension2')[1].split('dimension3')[0].split('"')[2]
            category = product.css('::attr(data-gtm-product)').get().split('category":')[1].split('","quantity')[0].split('"')[1]
            product_id = product.css('::attr(id)').get().replace('product', '')
            brand = product.css('::attr(data-gtm-product)').get().split('brand":"')[1].split('"')[0]

            yield scrapy.Request(url,
                                 callback=self.parse_product,
                                 meta={
                                     'url': url, 
                                     'name': name,
                                     'stock': stock, 
                                     'category': category,
                                     'id': product_id,
                                     'brand': brand
                                 }
                                )

        current_page = response.url.split('=')[-1]
        current_page = int(current_page)
        next_page = response.url.split('?')[0] + '?page=' + str(current_page + 1)
        yield scrapy.Request(next_page, callback=self.parse)

            
            
    def parse_product(self, response):
        # Extract data from the product page
        barcode = response.xpath('//div[text()="BARKOD"]/following-sibling::div/text()').get()
        price = response.css('div p span.new-price::text').get()
        images = response.css('div a::attr(data-image)').getall()
        description = re.sub(r'\s+', ' ', ' '.join([text.strip() for text in response.xpath('//*[@id="productDescription"]//text()').getall()]))

        # Yield a dictionary with the product data
        yield {
            'url': response.meta['url'],
            'name': response.meta['name'],
            'barcode': barcode,
            'price': price,
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