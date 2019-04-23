import scrapy

class quoteScraper(scrapy.Spider):
    name = 'quoteScraperAgain'

    def start_requests(self):
        urls = ['http://quotes.toscrape.com/page/1/',]
        for url in urls:
            yield scrapy.Request(url = url, callback=self.parse)    
    
    def parse(self, response):
        # file_name = response.url.split('/')[-2]+'.html'
        # print(response.body)

        for quote in response.css('div.quote'):
            yield{
                'text' : quote.css('span.text::text').get(),
                'author' : quote.css('small.author::text').get(),
                'tags' : quote.css('div.tags a.tag::text').getall(),
            }
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield scrapy.Request(response.urljoin(next_page), callback= self.parse)