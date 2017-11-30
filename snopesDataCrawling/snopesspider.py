import scrapy
import logging

class ArticlesSpider(scrapy.Spider):
    name = "Article links"
    custom_settings = {
        'DNS_TIMEOUT': 120,
        'LOG_ENABLED': True,
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE': 'log_'+name,
        'DEPTH_LIMIT': 0,
        'DOWNLOAD_DELAY': .5
    }

    start_urls = [
        'http://www.snopes.com/category/facts/',
    ]

    i = 0
    
    def parse(self, response):
        next_button_text = "Next "
        
        for article in response.xpath('//*[@id="main-list"]/article'):
            yield {
                'title': article.xpath('a/h2/text()').extract_first(),
                'url': article.xpath('a/@href').extract_first(),
            }

        # The first page contains only the next page button. However, all other pages contain both
        # prev and next buttons.
        next_page = response.xpath('//*[@id="main-list"]/div[4]/div/a/@href').extract_first()
        next_page_text = response.xpath('//*[@id="main-list"]/div[4]/div/a/text()').extract_first()
        next_page_alternative = response.xpath('//*[@id="main-list"]/div[4]/div/a[2]/@href').extract_first()
        next_page_alternative_text = response.xpath('//*[@id="main-list"]/div[4]/div/a[2]/text()').extract_first()
        
        if next_page is not None and next_page_text == next_button_text:
            next_page = response.urljoin(next_page)
            '''
            i += 1
            self.printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
            '''
            yield scrapy.Request(next_page, callback=self.parse)
        elif next_page_alternative is not None and next_page_alternative_text == next_button_text:
            '''
            i += 1
            self.printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
            next_page_alternative = response.urljoin(next_page_alternative)
            '''
            yield scrapy.Request(next_page_alternative, callback=self.parse)
        else:
            print(next_page)

    # Print iterations progress
    def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        self.logger.info('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
        #print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
        # Print New Line on Complete
        if iteration == total: 
            #print()
            self.logger.info('\n')



