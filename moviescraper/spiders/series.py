import scrapy
from moviescraper.items import SerieItem


class SeriesSpider(scrapy.Spider):
    name = "series"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/chart/toptv/"]

    custom_settings = {
    'FEEDS' : {
        'seriesdata.json' : {'format' : 'json', 'overwrite' : True},
    }
    }

    def parse(self, response):
        series = response.css('li.ipc-metadata-list-summary-item')
        for serie in series:
            relative_url = serie.css('a.ipc-title-link-wrapper ::attr(href)').get()

            if 'title/' in relative_url:
                serie_url = 'https://www.imdb.com/' + relative_url
            else:
                serie_url = 'https://www.imdb.com/title/' + relative_url
            yield response.follow(serie_url, callback=self.parse_movie_page)
        
    def parse_movie_page(self, response):
        serie_item = SerieItem()

        serie_item['url'] = response.url
        serie_item['title'] = response.css('span.hero__primary-text::text').get()
        serie_item['score'] = response.css('span.cMEQkK::text').get()
        serie_item['genre'] = response.css('span.ipc-chip__text::text').getall()
        serie_item['year'] = response.css('a[href*="releaseinfo"]::text').get()
        serie_item['duration'] = response.xpath('//li[@class="ipc-inline-list__item"]/following-sibling::li[1]/text()').get()
        serie_item['description'] = response.css('span.chnFO::text').get()
        serie_item['top_cast'] = response.css('a.gCQkeh::text').getall()
        serie_item['public'] = response.css('a[href*="certificates"]::text').get()
        serie_item['country'] = response.css('a[href*="country_of_origin"]::text').get()
        serie_item['language'] = response.css('a[href*="title_type"]::text').get()

        yield serie_item     
