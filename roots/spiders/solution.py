from curses import meta
from datetime import datetime,timedelta
from importlib.resources import contents
import scrapy
from scrapy.exceptions import DropItem
from bs4 import BeautifulSoup
import os 
import json
import requests

class SolutionSpider(scrapy.Spider):
    name='solution'
    allowed_domains=[]


    def start_requests(self):
        with open(os.path.join('output','all.json'), 'r') as f:
            questions=json.load(f)
        for question in questions:
            if not question['solution'] or not question ['solution']['canSeeDetail']:
                continue
        question_dir=os.path.join(
            'output', question['id']+'.'+question['title'].replace(' ','')

        )

        yield scrapy.Request(
            url='https://leetcode.com/articles/' + question['slug'] + '/',
            headers={
                'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
             },
            callback=self.parse,
            meta={
                'question': question,
                'question_dir': question_dir
                
            }
        )
    def parse(self,response):
        question=response.meta['question']
        question_dir=response.meta['question_dir']
        content=response.css('.article-body').get()
        if not content:
            return
        with open(os.path.join(question_dir,'solution.md'),'w') as f:
            f.write(content)
        with open(os.path.join(question_dir,'meta.json'),'r+') as f:
            meta=json.load(f)
            solution_format = '{"operationName":"fetchPlayground","variables":{},"query":"query fetchPlayground {\\n  playground(uuid: \\"%s\\") {\\n    name\\n    selectedLangSlug\\n   }\\n  allPlaygroundCodes(uuid: \\"%s\\") {\\n    code\\n    langSlug\\n    }\\n}\\n"}'
            for name in response.css('iframe').xpath('@name').getall():
                res = requests.post('https://leetcode.com/graphql',
                    headers={
                        'Origin': 'https://leetcode.com',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
                        'content-type': 'application/json',
                    },
                    data=solution_format % (name, name)
                )
                if res.status_code != 200:
                    print('^^ error status code ' + res.status_code)
                    return
                res_json = res.json()
                meta['solution'][name] = res_json['data']['allPlaygroundCodes']
            f.seek(0)
            json.dump(meta, f, indent=2)
            f.truncate()

