import scrapy
from itertools import tee, zip_longest

#Required to extract poem-author pair from related poems section
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

class QuotesSpider(scrapy.Spider):
    name = "arana_poetisa"
    start_urls = [
        'https://www.poemas-del-alma.com/',
    ]

    # Initial parse requests front page and assembles url for each letter
    def parse(self, response):
        site_url = self.start_urls[0]
        author_abc = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        for author_letter in author_abc:
            letter_url = site_url+author_letter+'.html'
            yield scrapy.Request(letter_url,callback=self.authorsPageParse)
    
    # Second parsing method parses authors page and requests individual authors
    def authorsPageParse(self,response):
        author_urls = response.xpath('//ul[@class="list-poems"]/li/a/@href').extract()
        for author_url in author_urls:
            yield scrapy.Request(author_url,callback=self.parseAuthor)

    # Third parsing method parses a given author's page and returns individual poems
    def parseAuthor(self,response):
        poems_urls = response.xpath('//ul[@class="list-poems"]/li/a/@href').extract()
        for poem_url in poems_urls:
            url = response.urljoin(poem_url)
            yield scrapy.Request(url,callback=self.parsePoem)

    # Fourth parsing method parses a given poem and returns its content
    def parsePoem(self,response):
        r = response.xpath("//div[contains(h3,'Poemas relacionados')]/ul/li/a/text()").extract()
        related = dict(grouper(r,2))

        yield {
            'author': response.xpath("//h3[@class='title-content']/text()").extract_first(),
            'title': response.xpath("//h2[@class='title-poem']/text()").extract_first(),
            'text': "".join(response.xpath("//div[@class='poem-entry']/p/text()").extract()),
            'related': related
        }