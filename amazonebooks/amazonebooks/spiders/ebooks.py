import scrapy
from ..items import AmazonebooksItem

class EbooksSpider(scrapy.Spider):
    name = "ebooks"
    custom_settings = {"FEEDS" : {'ebooks/%(name)s/%(name)s_batch_%(batch_id)d.csv': {'format' : 'csv',
                                                                                        'batch_item_count' : 11000,}
                                  }
                       }

    #kindleebooks english
    start_urls = ["https://www.amazon.in/s?i=digital-text&bbn=1634753031&rh=n%3A1634753031%2Cp_n_feature_three_browse-bin%3A11301931031%2Cp_n_feature_nineteen_browse-bin%3A4729244031&dc&ds=v1%3ABw%2B1dOC17Td7qLy8AB12HJOVtViQ4QSzTgnbhP8aXVs&qid=1690095586&rnid=4729243031&ref=sr_nr_p_n_feature_nineteen_browse-bin_1"]

    def parse(self, response):
        all_genre = response.css(".s-navigation-indent-2 span.a-list-item")

        for genre in all_genre:
            genre_url = genre.css("a::attr(href)").get()
            genre_url = "https://www.amazon.in" + genre_url
            genre_name = genre.css(".a-color-base ::text").get()

            yield scrapy.Request(genre_url, callback = self.getlinks, meta={'genre_name':genre_name})#,'genre_url':genre_url})



    def getlinks(self, response):
        dataItem = AmazonebooksItem()

        link_all = response.css(".s-line-clamp-2 .a-link-normal::attr(href)").getall()
        #asin_all = response.css("div.s-asin::attr(data-asin)").getall()
        genre_name = response.meta.get('genre_name')
        
        
        
        for link in link_all:

            book_url = "https://www.amazon.in"+link
            yield scrapy.Request(book_url,callback=self.parse_metadata,meta={'dataItem': dataItem,'genre_name':genre_name})

        next_page = response.css(".s-pagination-next::attr(href)").get()

        if next_page:
            next_page = "https://www.amazon.in"+next_page
            yield response.follow(next_page,callback=self.getlinks,meta={'genre_name':genre_name})#,'genre_url':genre_url}) 

            
            
    def parse_metadata(self, response):
        dataItem = response.meta.get('dataItem')
        
        dataItem['asin'] = response.css("#averageCustomerReviews::attr(data-asin)").get()  #response.meta.get('asin')
        dataItem['genre'] = response.meta.get('genre_name')
        dataItem['book_url'] = response.request.url
        
        
        dataItem['title'] = response.css("#productTitle::text").extract()
        authors_name = response.css("#bylineInfo .a-link-normal::text").extract()
        authors_contribution = response.css(".contribution .a-color-secondary::text").extract()
        authors = []
        for i in range(len(authors_name)):
            authors.append(authors_name[i]+authors_contribution[i])
        dataItem['authors'] =authors
        #take from product detail
        dataItem['publisher'] = response.css("#rpi-attribute-book_details-publisher .rpi-attribute-value span::text").get()
        dataItem['published_date'] = response.css("#rpi-attribute-book_details-publication_date .rpi-attribute-value span::text").get()
        dataItem['description_html'] = response.css("#bookDescription_feature_div div div").get() #check for page with small desc CHECKED!! WORKS FINE YEAY 
        dataItem['average_rating'] = response.css("#acrPopover .a-color-base::text").get()
        dataItem['ratings_count'] = response.css("#acrCustomerReviewText::text").get()
        
        dataItem['print_length'] = response.css("#rpi-attribute-book_details-ebook_pages .a-declarative span::text").get()
        dataItem['price'] = response.css("#kindle-price::text").extract()[1]
        dataItem['image_url'] = response.css("#ebooksImgBlkFront::attr(src)").get()
        reviews_url = response.css("#reviews-medley-footer .a-text-bold::attr(href)").get()
        dataItem['reviews_url'] = "https://www.amazon.in" + reviews_url

        
        yield dataItem
