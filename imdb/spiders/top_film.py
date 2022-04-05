import scrapy
from ..items import ImdbItem
from scrapy.loader import ItemLoader


class TopFilmSpider(scrapy.Spider):
    name = 'top_film'
    allowed_domains = ['www.imdb.com']
    start_urls = [
        'https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc']

    def parse(self, response):
        list_films = response.xpath('//div[@class="lister-list"]/div')
        for film in list_films:
            loader = ItemLoader(
                item=ImdbItem(), selector=film, response=response)

            loader.add_xpath(
                'film_name', './/h3[@class="lister-item-header"]/a/text()')
            loader.add_xpath(
                'year', './/h3[@class="lister-item-header"]/span[2]/text()')
            loader.add_xpath(
                'star', './/div[contains(@class, "ratings-imdb-rating")]/strong/text()')
            loader.add_xpath(
                'rank', './/h3[@class="lister-item-header"]/span[1]/text()')
            loader.add_xpath(
                'duration', './/span[@class="runtime"]/text()')
            loader.add_xpath(
                'genre', './/span[@class="genre"]/text()')
            loader.add_xpath(
                'director', './/div[@class="lister-item-content"]/p[3]/a[1]/text()')

            yield loader.load_item()

        rel_url = response.xpath(
            '(//a[@class="lister-page-next next-page"]/@href)[2]').get()
        next_page = response.urljoin(rel_url)
        if next_page:
            yield scrapy.Request(
                url=next_page,
                callback=self.parse
            )
