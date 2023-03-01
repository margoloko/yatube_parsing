import scrapy


class GroupSpider(scrapy.Spider):
    name = "group"
    #allowed_domains = ["."]
    start_urls = ["http://51.250.32.185/"]

    def parse(self, response):
        all_group = response.css('a.group_link::attr(href)').getall()
        for group in all_group:
            yield response.follow(group, callback=self.group_parse)

        next_page = response.xpath("//a[contains(., 'Следующая')]/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


    def group_parse(self, response):
        count = response.css('div.h6::text').get().replace('Записей:', '').strip()
        post_count = int(count)
        yield {'group_name': response.css('h2::text').get(),
               'description': response.css('p.group_descr::text').getall(),
               'posts_count': post_count
               }


