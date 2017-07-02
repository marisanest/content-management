# -*- coding: utf-8 -*-
import scrapy
import re
import json


class SiteSpiderSpider(scrapy.Spider):
    name = 'site_spider'

    start_urls = [
        'http://people.f4.htw-berlin.de/~zhangg/pages/teaching/pages/d01.html',
        'http://people.f4.htw-berlin.de/~zhangg/pages/teaching/pages/d06.html',
        'http://people.f4.htw-berlin.de/~zhangg/pages/teaching/pages/d08.html'
    ]

    def parse(self, response):
        id = response.url.split('/')[-1].split('.')[0]

        with open("sites/%s.json" % id, 'w') as f:
            data = {'id': id,
                    'text': "".join(line for line in response.css('body::text').extract()),
                    'url': response.url,
                    'back_links': [link.split('.')[0] for link in response.css('a::attr(href)').extract()]
                    }

            json.dump(data, f)

        for next_page in response.css('a::attr(href)').extract():
            yield response.follow(next_page, callback=self.parse)
