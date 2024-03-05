# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 12:16:10 2019

@author: bijay.dahal
"""

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from new_drinks import settings as my_settings


from scrapy.http.request import Request
# =============================================================================
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
# =============================================================================
from new_drinks.items import NewDrinksItem
from goose3 import Goose
from bs4 import BeautifulSoup as bs
import re

#################################################################################


#(works_fine)
class BevIndustrySpider(scrapy.Spider):
    name = 'bevindustry'
    allowed_domains = ['bevindustry.com']
    start_urls = [
            'https://www.bevindustry.com/articles/topic/5045-news?page=1'
            ]

# =============================================================================
#     rules = [
#             Rule(LinkExtractor(restrict_xpaths=['//div[@class="pagination"]']), callback='parse_listings', follow=True),
#     ]
# =============================================================================
    custom_settings = {
            'FEED_FORMAT':'csv',
            'FEED_URI' : 'tmp/bev-industry.csv'
   }

    
    
    def parse(self, response):
        
        articles = response.xpath('//article[@class="record article-summary "]')
        
 
        for article in articles:
            
            links = article.css('h2>a::attr(href)').extract_first()
            yield Request(links,callback=self.parse_item)
                
    
    
    def parse_item(self, response):
        
        item = NewDrinksItem()
        goose = Goose({'enable_image_fetching': True,'browser_user_agent': 'Mozilla'})
        raw_html = response.text
        txt = goose.extract(raw_html=raw_html)
       
        articles = response.xpath('//article[@class="main-body page-article-show "]')
        for article in articles:
            item['text'] = txt.cleaned_text
            item['abstract']=txt.meta_description
            item['title'] = txt.title
            item['link'] = response.url
            item['date_published'] = article.css('.date::text').extract_first()
            item['image_link'] = txt.top_image.src
            yield item
            
            


#################################################################################################





#(works_fine)
class TheSpritBusinessSpider(scrapy.Spider):
    name = 'sprit_business'
    allowed_domains = ['thespiritsbusiness.com']
    start_urls = [
            'https://www.thespiritsbusiness.com/category/news/page/1'
            ]

# =============================================================================
#     rules = [
#             Rule(LinkExtractor(restrict_xpaths=['//div[@class="wp-pagenavi"]']), callback='parse_listings', follow=True),
#     ]
# =============================================================================
    custom_settings = {
            'FEED_FORMAT':'csv',
            'FEED_URI' : 'tmp/sprit_business.csv'
   }

    
    
    def parse(self, response):
        
        
        articles = response.xpath('//div[@class="archiveEntry"]')
         
        
 
        for article in articles:
            
            links = article.css('div>a::attr(href)').extract_first()
            
            yield Request(links,callback=self.parse_item)
                
    
  
    def parse_item(self, response):
        
        item = NewDrinksItem()
        goose = Goose({'enable_image_fetching': True,'browser_user_agent': 'Mozilla'})
        raw_html = response.text
        txt = goose.extract(raw_html=raw_html)
       
        item['text'] = txt.cleaned_text
        item['abstract']=response.css('p.standfirst::text').extract_first()
        item['title'] = txt.title
        item['link'] = response.url
        date = response.css('div>small::text').extract_first()
        regex = re.search('\s([0-9]{1,2})[a-z]{2}\s([A-Z]{1}[a-z]*),\s([0-9]{4})',date)
        item['date_published'] = ' '.join(regex.groups())
        item['image_link'] = txt.top_image.src
        yield item
            
        
        
        
###################################################################################################################


# (works_fine)
        
class FoodbevSpider(scrapy.Spider):
    name = 'food_bev'
    allowed_domains = ['foodbev.com']
    start_urls = [
            'https://www.foodbev.com/news/category/industries/page/1',
            'https://www.foodbev.com/news/category/industries/page/2',
            'https://www.foodbev.com/news/category/industries/page/3',
            'https://www.foodbev.com/news/category/industries/page/4',
            'https://www.foodbev.com/news/category/industries/page/5',
            'https://www.foodbev.com/news/category/industries/page/6',
            'https://www.foodbev.com/news/category/industries/page/7',
            'https://www.foodbev.com/news/category/industries/page/8'
            ]
            
            

# =============================================================================
#     rules = [
#             Rule(LinkExtractor(restrict_xpaths=['//div[@class="pagination"]']), callback='parse_listings', follow=True),
#     ]
# =============================================================================
    custom_settings = {
            'FEED_FORMAT':'csv',
            'FEED_URI' : 'tmp/foodbev.csv'
   }

    
    
    def parse(self, response):
        
        
        articles = response.xpath('//div[@class="mom-grid-item first"]')
        articles1 = response.xpath('//div[@class="mom-grid-item last"]')
        
        all = articles + articles1
        
 
        for article in all:
            
            links = article.css('h2>a::attr(href)').extract_first()
           
            yield Request(links,callback=self.parse_item)
                
    
  
    def parse_item(self, response):
        
        item = NewDrinksItem()
        goose = Goose({'enable_image_fetching': True,'browser_user_agent': 'Mozilla'})
        raw_html = response.text
        txt = goose.extract(raw_html=raw_html)
       
        item['text'] = txt.cleaned_text
        item['abstract']=txt.meta_description
        item['title'] = txt.title
        item['link'] = response.url
        item['date_published'] = response.css('span>time.updated::text').extract_first()
        item['image_link'] = txt.top_image.src
        yield item       

        
####################################################################################
        ########################################################################
        ##########################################################################
        #####################################################################
        
        

class BevDailySpider(scrapy.Spider):
    name = 'bevdaily'
    allowed_domains = ['beveragedaily.com']
    start_urls = [
            'https://www.beveragedaily.com/News/?page=1',
            'https://www.beveragedaily.com/News/?page=2'
            ]

# =============================================================================
#     rules = [
#             Rule(LinkExtractor(restrict_xpaths=['//ul[@class="Pagination-list"]']), callback='parse_listings', follow=True),
#     ]
# =============================================================================
    custom_settings = {
            'FEED_FORMAT':'csv',
            'FEED_URI' : 'tmp/bev_daily.csv'
   }
   
    def parse(self, response):
        
        
        articles = response.xpath('//article[@class="Teaser"]')
        
 
        for article in articles:
            
            links = 'https://www.beveragedaily.com' + str(article.css('.Teaser-title>a::attr(href)').extract_first())
            
            yield Request(links,callback=self.parse_item)
    
    
    def parse_item(self, response):
        
        item = NewDrinksItem()
        goose = Goose({'enable_image_fetching': True,'browser_user_agent': 'Mozilla'})
        raw_html = response.text
        txt = goose.extract(raw_html=raw_html)
       
        
        item['text'] = txt.cleaned_text
        item['abstract']=response.css('div.Detail-intro::text').extract_first().strip()
        item['title'] = txt.title
        item['link'] = response.url 
        item['date_published'] = response.css('.Detail-date>time::text').extract_first()
        item['image_link'] = txt.top_image.src
        yield item


        
#####################################################################################################################################        


class BevNetSpider(scrapy.Spider):
    name = 'bevnet'
    allowed_domains = ['www.bevnet.com']
    start_urls = [
            'https://www.bevnet.com/news/page/1/',
            'https://www.bevnet.com/news/page/2/',
            'https://www.bevnet.com/news/page/3/',
            'https://www.bevnet.com/news/page/4/'
            ]
   
# =============================================================================
#     rules = [
#             
#             Rule(LinkExtractor(restrict_xpaths=['//div[@class="nav-post-pages"]']),callback= 'parse_listings',follow=True),
#     ]
# =============================================================================
    custom_settings = {
            'FEED_FORMAT':'csv',
            'FEED_URI' : 'tmp/bev_net.csv'
   }
    
    def parse(self, response):
        
        articles = response.xpath('//article')
        
 
        for article in articles:
            
            links = article.css('.post-header *::attr(href)').extract_first()
            
            yield Request(links,callback=self.parse_item)
            
    
    def parse_item(self, response):
        
        item = NewDrinksItem()
        raw_html = response.text
        goose = Goose({'enable_image_fetching': True,'browser_user_agent': 'Mozilla'})
        txt = goose.extract(raw_html=raw_html)
# =============================================================================
#         soup = bs(raw_html,"html.parser")
# =============================================================================
        
        item['text'] = txt.cleaned_text
        item['abstract']= response.css('div.post-content-wrap>p::text').extract_first()
        item['title'] = txt.title
        item['link'] = response.url
        item['date_published'] = response.css('.post-date *::attr(datetime)').extract_first()
        item['image_link'] = txt.top_image.src
        yield item


######################################################################################################
        
        
        
class BevSoftSpider(scrapy.Spider):
    name = 'bsd'
    allowed_domains = ['britishsoftdrinks.com']
    start_urls = [
            'http://www.britishsoftdrinks.com/Press-releases-/Page-1'
            ]

# =============================================================================
#     rules = [
#             Rule(LinkExtractor(restrict_xpaths=['//div[@class="pager style1"]']), callback='parse_listings', follow=True),
#     ]
# =============================================================================
    custom_settings = {
            'FEED_FORMAT':'csv',
            'FEED_URI' : 'tmp/british_soft_drinks.csv'
   }
    
    def parse(self, response):
        
        articles = response.xpath('//div[@class="grid_4 module_list_item"]')
        
 
        for article in articles:
            
            links = 'http://www.britishsoftdrinks.com'+ article.css('h3>a *::attr(href)').extract_first()
           
            yield Request(links,callback=self.parse_item)
                
    
    def parse_item(self, response):
        
        item = NewDrinksItem()
        raw_html = response.text
        soup = bs(raw_html,"html.parser")
       
        mango = response.css('div#divArticle.news_article>p *::text').extract()
                             
        item['text'] = '\n'.join(mango)
        item['abstract']= mango[0]
        item['title'] = response.css('h2>span::text').extract_first()
        item['link'] = response.url
        item['date_published'] = response.css('h4>em::text').extract_first()
        item['image_link'] = soup.find('img')['src']
        yield item       




#########################################################################################
        
   

class DrinkSpider(scrapy.Spider):
    name = 'drinkb'
    allowed_domains = ['thedrinksbusiness.com']
    start_urls = [
            'https://www.thedrinksbusiness.com/category/news/page/1',
            'https://www.thedrinksbusiness.com/category/news/page/2',
            'https://www.thedrinksbusiness.com/category/news/page/3'
            ]
    
# =============================================================================
#     rules = [
#             
#             Rule(LinkExtractor(restrict_xpaths=['//div[@class="wp-pagenavi"]']),callback= 'parse_listings',follow=True),
#     ]
# =============================================================================
    custom_settings = {
            'FEED_FORMAT':'csv',
            'FEED_URI' : 'tmp/drink_business.csv'
   }
    
    def parse(self, response):
        
        articles = response.xpath('//section')
        
 
        for article in articles:
            
            links = article.css('h3>a::attr(href)').extract_first()
            
            yield Request(links,callback=self.parse_item)
    
    
    def parse_item(self, response):
        
        item = NewDrinksItem()
      
        raw_html = response.text
        soup = bs(raw_html,"html.parser")
       
        item['text'] = soup.find("div",{"class":"entry"}).get_text().strip()
        item['abstract'] = soup.h2.text
        item['title'] = response.css('h1::text').extract_first()
        item['link'] = response.url
        item['date_published'] = response.css('small>span::text').extract_first()
        item['image_link'] = soup.find("img")['src']
        yield item


#####################################################################################
        
        
class DrinkpreneurSpider(scrapy.Spider):
    name = 'drinkpreneur'
    allowed_domains = ['drinkpreneur.com']
    start_urls = [
            'https://www.drinkpreneur.com/beverage-industry-news/page/1'
            ]
   
# =============================================================================
#     rules = [
#             
#             Rule(LinkExtractor(restrict_xpaths=['//div[@class="wp-pagenavi"]']),callback= 'parse_listings',follow=True),
#     ]
# =============================================================================
    
    custom_settings = {
            'FEED_FORMAT':'csv',
            'FEED_URI' : 'tmp/drinkpreneur.csv'
   }
    
    def parse(self, response):
        
        articles = response.xpath('//div[@class="post_content "]')
        
 
        for article in articles:
            
            links = article.xpath('h2/a/@href').extract_first()
            
            yield Request(links,callback=self.parse_item)
    
    
    def parse_item(self, response):
        
        item = NewDrinksItem()
        goose = Goose({'enable_image_fetching': True,'browser_user_agent': 'Mozilla'})
        raw_html = response.text
        txt = goose.extract(raw_html=raw_html)
        
        item['text'] = txt.cleaned_text
        item['abstract']=txt.meta_description
        item['title'] = response.css('h1::text').extract_first()
        item['link'] = response.url
        item['date_published'] = response.css('.entry-date::text').extract_first()
        item['image_link'] = txt.top_image.src
        yield item
        
################################################################################
        
        
        
class DrinksInsightSpider(scrapy.Spider):
    name = 'drinks_insight'
    allowed_domains = ['drinks-insight-network.com']
    start_urls = [
            'https://www.drinks-insight-network.com/news/page/1',
            'https://www.drinks-insight-network.com/news/page/2',
            'https://www.drinks-insight-network.com/news/page/3'
            ]

# =============================================================================
#     rules = [
#             Rule(LinkExtractor(restrict_xpaths=['//div[@class="nav-links"]']), callback='parse_listings', follow=True),
#     ]
# =============================================================================
    
    custom_settings = {
            'FEED_FORMAT':'csv',
            'FEED_URI' : 'tmp/drinks_insight.csv'
   }
    
    
    def parse(self, response):
        
        articles = response.xpath('//ul[@class="category_list_new pal"]/li/article')
        
 
        for article in articles:
            
            links = article.css('h2>a::attr(href)').extract_first()
           
            yield Request(links,callback=self.parse_item)
                
    
    def parse_item(self, response):
        
        item = NewDrinksItem()
        goose = Goose({'enable_image_fetching': True,'browser_user_agent': 'Mozilla'})
        raw_html = response.text
        txt = goose.extract(raw_html=raw_html)
       
        item['text'] = txt.cleaned_text
        item['abstract']=txt.meta_description
        item['title'] = response.css('.entry-title::text').extract_first()
        item['link'] = response.url
        item['date_published'] = response.css('.article-date::text').extract_first()
        item['image_link'] = txt.top_image.src

        yield item


###########################################################################################
        
class RetailingSpider(scrapy.Spider):
    name = 'retailing'
    allowed_domains = ['drinksretailingnews.co.uk']
    start_urls = [
            'http://drinksretailingnews.co.uk/news/categoryfront.php/id/11/Latest_News.html?page=1',
            'http://drinksretailingnews.co.uk/news/categoryfront.php/id/11/Latest_News.html?page=2',
            'http://drinksretailingnews.co.uk/news/categoryfront.php/id/11/Latest_News.html?page=3'
            ]

# =============================================================================
#     rules = [
#             Rule(LinkExtractor(restrict_xpaths=['//div[@class="page_links"]']), callback='parse_listings', follow=True),
#     ]
# =============================================================================
    custom_settings = {
            'FEED_FORMAT':'csv',
            'FEED_URI' : 'tmp/retailing.csv'
   }

    
    def parse(self, response):
        
        articles = response.xpath('//div[@class="middleArticle"]')
        
 
        for article in articles:
            
            links = 'http://drinksretailingnews.co.uk'+ article.css('h2>a *::attr(href)').extract_first()
            
            yield Request(links,callback=self.parse_item)
                
    
    def parse_item(self, response):
        
        item = NewDrinksItem()
        goose = Goose({'enable_image_fetching': True,'browser_user_agent': 'Mozilla'})
        raw_html = response.text
        txt = goose.extract(raw_html=raw_html)
        
        item['text'] = txt.cleaned_text
        item['abstract']=txt.meta_description
        item['title'] = response.css('.headline::text').extract_first()
        item['link'] = response.url
        date = response.css('.publication_date::text').extract_first()
        item['date_published'] = date.split('|')[1].strip()
        item['image_link'] = txt.top_image.src
        yield item          
              


#####################################################################################
        
        
class Drinks_bulletin(scrapy.Spider):
    name = 'drinks_bulletin'
    allowed_domains = ['drinksbulletin.com.au']
    start_urls = [
            'http://www.drinksbulletin.com.au/latest-news?Page=1',
            'http://www.drinksbulletin.com.au/latest-news?Page=2',
            'http://www.drinksbulletin.com.au/latest-news?Page=3'
            ]

# =============================================================================
#     rules = [
#             Rule(LinkExtractor(restrict_xpaths=['//div[@class="pageLinks"]']), callback='parse_listings', follow=True),
#     ]
# =============================================================================
    custom_settings = {
            'FEED_FORMAT':'csv',
            'FEED_URI' : 'tmp/drinks_bulletin.csv'
   }

    
    
    def parse(self, response):
        
        
        articles = response.xpath('//article[@class="item-list item_1"]')
         
        
 
        for article in articles:
            
            links = article.css('h2>a::attr(href)').extract_first()
            
            yield Request(links,callback=self.parse_item)
                
     
    def parse_item(self, response):
        
        item = NewDrinksItem()
        goose = Goose({'enable_image_fetching': True,'browser_user_agent': 'Mozilla'})
        raw_html = response.text
        txt = goose.extract(raw_html=raw_html)
       
        item['text'] = txt.cleaned_text
        item['abstract']=txt.meta_description
        item['title'] = txt.title
        item['link'] = response.url
        item['date_published'] = response.css('p>span.tie-date::text').extract_first()
        item['image_link'] = txt.top_image.src
 
        yield item

     
        
        
#########################################################################################        



class Food_and_Bev(scrapy.Spider):
    name = 'food_and_bev'
    allowed_domains = ['foodmag.com.au']
    start_urls = [
            'https://www.foodmag.com.au/category/news/page/1',
            'https://www.foodmag.com.au/category/news/page/2'
            ]

# =============================================================================
#     rules = [
#             Rule(LinkExtractor(restrict_xpaths=['//div[@class="wp-pagenavi"]']), callback='parse_listings', follow=True),
#     ]
# =============================================================================
    custom_settings = {
            'FEED_FORMAT':'csv',
            'FEED_URI' : 'tmp/foodmag.csv'
   }

    
    
    def parse(self, response):
        
        
        articles = response.xpath('//div[@class="news-con"]/ul/li')
         
 
        for article in articles:
            
            links = article.css('h2>a::attr(href)').extract_first()
            
            yield Request(links,callback=self.parse_item)
                
    
  
    def parse_item(self, response):
        
        item = NewDrinksItem()
        goose = Goose({'enable_image_fetching': True,'browser_user_agent': 'Mozilla'})
        raw_html = response.text
        txt = goose.extract(raw_html=raw_html)
       
        item['text'] = txt.cleaned_text
        item['abstract']=txt.meta_description
        text = txt.title
        item['title'] = text.split('|')[0].strip()
        item['link'] = response.url
        item['date_published'] = response.css('time.entry-date::text').extract_first()
        item['image_link'] = txt.top_image.src
        yield item



###################################################################################
        
class DrinkStuff(scrapy.Spider):
    name = 'drinkstuff'
    allowed_domains = ['drinkstuff-sa.co.za']
    start_urls = [
            'https://www.drinkstuff-sa.co.za/sa-drinks-stuff/page/1'
            ]

# =============================================================================
#     rules = [
#             Rule(LinkExtractor(restrict_xpaths=['//ul[@class="uk-pagination"]']), callback='parse_listings', follow=True),
#     ]
# =============================================================================
    custom_settings = {
            'FEED_FORMAT':'csv',
            'FEED_URI' : 'tmp/drinkstuff.csv'
   }

    
    
    def parse(self, response):
        
        
        articles = response.xpath('//article')
         
 
        for article in articles:
            
            links = article.css('h3>a::attr(href)').extract_first()
            
            yield Request(links,callback=self.parse_item)
                
    
  
    def parse_item(self, response):
        
        item = NewDrinksItem()
        goose = Goose({'enable_image_fetching': True,'browser_user_agent': 'Mozilla'})
        raw_html = response.text
        txt = goose.extract(raw_html=raw_html)
       
        item['text'] = txt.cleaned_text
        item['abstract']=txt.meta_description
        text = txt.title
        item['title'] = text.split('»')[0].strip()
        item['link'] = response.url
        item['date_published'] = response.css('time::text').extract_first()
        item['image_link'] = txt.top_image.src
        yield item        
     
        
        
################################################################################################

class CiderUK(scrapy.Spider):
    name = 'cideruk'
    allowed_domains = ['cideruk.com']
    start_urls = [
            'http://cideruk.com/cider-news/page/1',
            'http://cideruk.com/cider-news/page/2',
            'http://cideruk.com/cider-news/page/3'
            ]

# =============================================================================
#     rules = [
#             Rule(LinkExtractor(restrict_xpaths=['//div[@class="pagination clearfix"]']), callback='parse_listings', follow=True),
#     ]
# =============================================================================
    custom_settings = {
            'FEED_FORMAT':'csv',
            'FEED_URI' : 'tmp/cideruk.csv'
   }

    
    
    def parse(self, response):
        
        
        articles = response.xpath('//article')
         
 
        for article in articles:
            
            links = article.css('h2>a::attr(href)').extract_first()
            
            yield Request(links,callback=self.parse_item)
                
    
  
    def parse_item(self, response):
        
        item = NewDrinksItem()
        goose = Goose({'enable_image_fetching': True,'browser_user_agent': 'Mozilla'})
        raw_html = response.text
        txt = goose.extract(raw_html=raw_html)
       
        item['text'] = txt.cleaned_text
        item['abstract']=txt.meta_description
        item['title'] = response.css('div>h1::text').extract_first()
        item['link'] = response.url
        item['date_published'] = response.css('p>span::text').extract_first()
        item['image_link'] = txt.top_image.src
        yield item




########################################################################################


process = CrawlerProcess()
crawler_settings = Settings()
crawler_settings.setmodule(my_settings)
process = CrawlerProcess(settings=crawler_settings)

process.crawl(CiderUK)
process.crawl(DrinkStuff)
process.crawl(Food_and_Bev)
process.crawl(Drinks_bulletin)
process.crawl(BevIndustrySpider)
process.crawl(FoodbevSpider)
process.crawl(TheSpritBusinessSpider)
process.crawl(BevDailySpider)
process.crawl(BevNetSpider)
process.crawl(BevSoftSpider)
process.crawl(DrinkSpider)
process.crawl(DrinkpreneurSpider)
process.crawl(DrinksInsightSpider)
process.crawl(RetailingSpider)
process.start()