# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request

proxy_location = '180.183.223.227:8080'

class YtsSpider(scrapy.Spider):
    name = 'yts'
    # allowed_domains = ['https://yts.am']
    

    def parse(self, response):
        # print('Recording the response')
        movieList = response.css('a.browse-movie-link').xpath('@href')
        for movie in movieList:
            yield response.follow(movie.get(), self.parse_torrentlinks, meta ={'proxy':proxy_location})

    def parse_torrentlinks(self, response):
        print('Recording the response for each movie')
        downloadLink = {}
        movies = response.xpath('//div[@id="movie-info"]')
        downloadLink['Title'] = movies[0].css('div.hidden-xs').css('h1::text').get()
        downloadLink['Details']  = "-".join(movies[0].css('div.hidden-xs').css('h2::text').getall())
        links =  movies[0].css('p.hidden-xs').css('p.hidden-sm').css('a')        
        for item in links:
            downloadLink[item.css('a::text').get()] = item.css('a').attrib['href']
        yield downloadLink
        

    def start_requests(self):
        request = Request(url ='https://yts.am/browse-movies' )
        # request = Request(url ='http://quotes.toscrape.com/tag/humor/' )
        request.meta['proxy'] = proxy_location
        return [request]
