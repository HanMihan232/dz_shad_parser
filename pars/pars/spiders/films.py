import scrapy


class FilmsSpider(scrapy.Spider):
    name = "films"
    allowed_domains = ["ru.wikipedia.org"]
    # start_urls = ["https://ru.wikipedia.org"]

    start_urls = ["https://ru.wikipedia.org/wiki/Категория:Фильмы_по_годам"]

    # def start_requests(self):
    #     URL = "https://ru.wikipedia.org/wiki/Категория:Фильмы_по_годам"


    # def parse(self, response):
    #     print(response)



    def get_film(self, response):
        yield {
            'title': response.css('th.infobox-above::text').get(),
            'genre': response.css('td.plainlist > span[data-wikidata-property-id="P136"] > a::text').getall() \
            if response.css('td.plainlist > span[data-wikidata-property-id="P136"] > a::text').getall() \
            else response.css('td.plainlist > span[data-wikidata-property-id="P136"] > span > a::text').get(),
            'director':  response.css('td.plainlist > span[data-wikidata-property-id="P57"] > a::text').getall(),
            'country': response.css('td.plainlist > span.wrap::text').getall(),
            'year': response.css('span.dtstart::text').getall()
        }


    def parse_local_page(self, response):
        for local_link in response.css('div.mw-category-group > ul > li > a::attr(href)').getall():
            if local_link:
                yield response.follow(local_link, callback=self.get_film)


    def parse(self, response):
        for global_link in response.css("div.CategoryTreeItem > a::attr(href)").getall():
            if global_link:
                yield response.follow(global_link, callback=self.parse_local_page)
