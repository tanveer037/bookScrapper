import scrapy
from ..items import BookscraperItem


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books = response.css('.product_pod')

        for book in books:
            book_url = book.css('h3 a::attr(href)').get()
            if 'catalogue/' in book_url:
                follow_book_url = 'https://books.toscrape.com/' + book_url
            else:
                follow_book_url = 'https://books.toscrape.com/catalogue/' + book_url
            yield scrapy.Request(follow_book_url, callback=self.parse_book_details)

        next_page = response.css('.next a::attr(href)').get()

        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback=self.parse)

    def parse_book_details(self, response):
        book_item = BookscraperItem()
        book_item['name'] = response.css('h1::text').get()
        book_item['bookType'] = response.xpath("//ul[@class = 'breadcrumb']/li[@class = 'active']/preceding-sibling::li[1]/a/text()").get()
        book_item['price'] = response.css('.product_main .price_color::text').get()
        book_item['rating'] = response.css("p.star-rating::attr(class)").get()
        book_item['url'] = response.url
        yield book_item
        
        # 'name': response.css('h1::text').get(),
        # 'type': response.xpath("//ul[@class = 'breadcrumb']/li[@class = 'active']/preceding-sibling::li[1]/a/text()").get(),
        # 'price': response.css('.product_main .price_color::text').get(),
        # 'rating': response.css("p.star-rating::attr(class)").get()
