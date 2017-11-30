import scrapy
import json
import os

class ArticlesSpider(scrapy.Spider):
    name = "Article properties"

    custom_settings = {
        'DNS_TIMEOUT': 120,
        'LOG_ENABLED': True,
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE': 'log_'+name,
        'DEPTH_LIMIT': 0,
        'DOWNLOAD_DELAY': .5
    }
    
    # Read all urls to crawl from a file
    def __init__(self, filename=None):
        self.start_urls = []
        self.data = []  # list of dict
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                for entry in data:
                    # read in urls into start_urls
                    self.start_urls.append(entry['url'])
        elif os.path.isdir(filename):
            for filePath in os.listdir(lgFeaturesPath):
                with open(filePath, 'r') as f:
                    data = json.load(f)
                    self.data.append(data)
                    self.start_urls.append(entry['URL'])
    '''
    def parse(self, response):
        topic = response.css('body > main > section > div.main-content-wrapper > div > div > a:nth-child(2)::text').extract()
        yield {
            "url": response.url,
            "topic": topic
        }
        
    '''
    def parse(self, response):
        '''
        category = response.css('body > main > section > div.main-content-wrapper > div > div > a:nth-child(2)::text').extract()

        title = '. '.join(response.css('body > main > section > div.main-content-wrapper > div > article > header > h1::text').extract())
        description = '. '.join(response.css('body > main > section > div.main-content-wrapper > div > article > header > h2::text').extract())
        '''
        
        claim = None
        rating = ''
        '''
        sources = []
        
        content = response.css('body > main > section > div.main-content-wrapper > div > article > div.entry-content.article-text > p::text').extract()
        url = response.url
        quotes = []
        '''

        # asp webpage
        if response.url.endswith(".asp"):
            claim_selector = response.xpath('//p[@itemprop="claimReviewed"]/text()')
            if claim_selector != []:
                claim = response.xpath('//p[@itemprop="claimReviewed"]/text()').extract()
            else:
                claim = response.xpath('//div[contains(@class, "article-text")]/p[font/b/text()="Claim:"]/text()').extract()
            
            claim = '. '.join(claim)
            '''
            description = '. '.join(response.xpath('//*[@class="article-description"]//text()').extract())
            quotes = response.xpath('//div[@class="quoteBlock"]//text()').extract()
            quotes = '. '.join(quotes)

            if response.xpath('//h3[@itemprop="origin"]').extract() == []:
                # This content may contain quotes
                content = response.xpath('//div[contains(@class, "article-text")]/div[contains(@class, "claim")]/following-sibling::p//text()').extract()
                content = '. '.join(content)
            else:
                content = response.xpath('//div[contains(@class, "article-text")]/h3[@itemprop="origin"]/following-sibling::p//text()').extract()
            '''

            rating_selector = response.xpath('//table//font[@class="status_color"]/b//text()').extract()
            if rating_selector == []:
                rating_selector = response.xpath('//*[contains(@itemprop, "description") and span[text()="RATING"]]/following-sibling::div[contains(@class, "claim")]//text()').extract()
            rating = '. '.join(rating_selector)
            '''
            sources_selector = response.xpath('//dl/dd/nobr') # source, publisher&date, source, pub&date, ...
            if sources_selector != []:

                
                for sel in sources_selector:
                    source_str = sel.xpath('.//text()').extract()
                    publisher = sel.xpath('./i/text()').extract()
                     
                    sources.append({'source sentence': source_str, 'publisher':publisher})
            else:
                sources_selector = response.css('body > main > section > div.main-content-wrapper.clearfix > div > article > div.entry-content.article-text.legacy > footer > div.article-sources-box > p')
                sources = []
                for s in sources_selector:
                    source_str = ''
                    for sentence in s.css('::text'):
                        source_str += sentence.extract();
                    publisher = ' '.join(s.css('em::text').extract());
  
                    sources.append({'source sentence': source_str, 'publisher':publisher});
            '''

        # page not end with asp
        else:
            claim = response.css('body > main > section > div.main-content-wrapper > div > article > div.entry-content.article-text > p:nth-child(2)::text').extract()
            claim = '. '.join(claim)
            '''
            quotes = response.css('body > main > section > div.main-content-wrapper > div > article > div.entry-content.article-text > blockquote > p::text').extract()
            quotes = '. '.join(quotes)

            content =  response.xpath('//div[contains(@class, "article-text")]/div[contains(@class, "claim")]/following-sibling::p//text()').extract()
            content = '. '.join(content)
            '''
            '''
            sources_selector = response.css('body > main > section > div.main-content-wrapper.clearfix > div > article > div.entry-content.article-text.legacy > footer > div.article-sources-box > p')
            sources = []
            '''
            rating = response.xpath('//div[contains(@class, "claim")]/span/text()').extract()
            rating = ' '.join(rating)
            '''
            for s in sources_selector:
                source_str = ''
                for sentence in s.css('::text'):
                    source_str += sentence.extract();
                publisher = ' '.join(s.css('em::text').extract());

                 
                sources.append({'source sentence': source_str, 'publisher':publisher});
            '''
        yield {
            
            #"title":title,
            #"description": description,
            #"category":category,
            "claim": claim,
            "rating": rating,
            #"content": content,
            #"quotes":quotes,
            #"sources": sources,
            #"url": url
        }