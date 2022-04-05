import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose


def clean_genre(genre_text):
    return genre_text.strip()


def clear_rank(rank_text):
    return int(rank_text.replace('.', ''))


def clear_star(star_text):
    return float(star_text)


def clean_year(year_text):
    try:
        year_int = int(year_text.strip('()'))
    except:
        year_int = int(year_text.strip('(I)').replace(' (', ''))
    return year_int


class ImdbItem(scrapy.Item):
    film_name = scrapy.Field(output_processor=TakeFirst())
    year = scrapy.Field(
        input_processor=MapCompose(clean_year),
        output_processor=TakeFirst()
    )
    star = scrapy.Field(
        input_processor=MapCompose(clear_star),
        output_processor=TakeFirst()
    )
    rank = scrapy.Field(
        input_processor=MapCompose(clear_rank),
        output_processor=TakeFirst()
    )
    duration = scrapy.Field(output_processor=TakeFirst())
    genre = scrapy.Field(
        input_processor=MapCompose(clean_genre),
        output_processor=TakeFirst()
    )
    director = scrapy.Field(output_processor=TakeFirst())
