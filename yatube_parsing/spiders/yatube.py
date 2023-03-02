import scrapy
from yatube_parsing.items import YatubeParsingItem


class YatubeSpider(scrapy.Spider):
    name = "yatube"
    #allowed_domains = ["51.250.32.185"]
    start_urls = ["http://51.250.32.185/"]

    def parse(self, response):
        for quote in response.css('div.card-body'):
            data = {'author': quote.css('strong.d-block::text').get().strip(),
                   'text': ' '.join(t.strip() for t in quote.css('p::text').getall()).strip(),
                   'date': quote.css('small.text-muted::text').get().strip(),
                   }
            yield YatubeParsingItem(data)

        next_page = response.xpath("//a[contains(., 'Следующая')]/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

