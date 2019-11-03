# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SuperjobRuSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']

    def __init__(self, vacancy = None):
        super(SuperjobRuSpider, self).__init__()
        self.start_urls = [
            f'https://hh.ru/search/vacancy?only_with_salary=false&clusters=true&area=1&enable_snippets=true&salary=&st=searchVacancy&text=%D0%BC%D0%BE%D1%82%D0%B8%D0%B2%D0%B0%D1%82%D0%BE%D1%80'
        ]

    def parse(self, response):
        next_page = response.css('a.f-test-link-dalshe::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)
        vacancy_items = response.css(
            'div.f-test-vacancy-item a[class*=f-test-link][href^="/vakansii"]::attr(href)').extract()
        for vacancy_link in vacancy_items:
            yield response.follow(vacancy_link, self.vacancy_parse)

    def vacancy_parse(self, response:HtmlResponse):
        name = response.css('h1 ::text').extract()
        salary = response.css(
            'div._3MVeX span[class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc" ::text').extract()
        vacancy_link = response.url
        site_scraping = self.allowed_domains[0]

        yield JobparserItem(
            name=name,
            salary=salary,
            vacancy_link=vacancy_link,
            site_scraping=site_scraping
        )

