import scrapy
from moviescraper.items import MovieItem


class MoviespiderSpider(scrapy.Spider):
    name = "moviespider"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]

    custom_settings = {
        'FEEDS' : {
            'moviesdata.json' : {'format' : 'json', 'overwrite' : True},
    }
    }
        

    def parse(self, response):
        movies = response.css('li.ipc-metadata-list-summary-item')
        for movie in movies:
            relative_url = movie.css('a.ipc-title-link-wrapper ::attr(href)').get()

            if 'title/' in relative_url:
                movie_url = 'https://www.imdb.com/' + relative_url
            else:
                movie_url = 'https://www.imdb.com/title/' + relative_url
            yield response.follow(movie_url, callback=self.parse_movie_page)
        
    def parse_movie_page(self, response):
        movie_item = MovieItem()

        movie_item['url'] = response.url
        movie_item['title'] = response.css('span.hero__primary-text::text').get()
        movie_item['score'] = response.css('span.cMEQkK::text').get()
        movie_item['genre'] = response.css('span.ipc-chip__text::text').getall()
        movie_item['year'] = response.css('a[href*="releaseinfo"]::text').get()
        movie_item['duration'] = response.css('li.ipc-inline-list__item::text').get()
        movie_item['description'] = response.css('span.chnFO::text').get()
        movie_item['top_cast'] = response.css('a.gCQkeh::text').getall()
        movie_item['public'] = response.css('a[href*="certificates"]::text').get()
        movie_item['country'] = response.css('a[href*="country_of_origin"]::text').get()
        movie_item['language'] = response.css('a[href*="title_type"]::text').get()

        yield movie_item        