import scrapy

from collections import OrderedDict
from collector.collector.items import BookItem
import re


class EbalbhartiSpider(scrapy.Spider):
    name = "EBalbharti"
    allowed_domains = ["books.ebalbharati.in"]
    start_urls = ["https://books.ebalbharati.in"]

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    grade_ = ""
    grade_numeric = 0
    script_manager = ["upBtn", "upMain"]
    medium = {"english": "303"}
    form_keys = ["ScriptManager1","__EVENTTARGET","__EVENTARGUMENT", "__VIEWSTATE", "__VIEWSTATEGENERATOR", "__EVENTVALIDATION", "rdbYear", "txtSelected", "txtyear", "__ASYNCPOST" ]



    def parse(self, response):
        print(f"asas {self.settings.get('ITEM_PIPELINES').__dict__}")
        for grade in response.css("span[class='spnItem'] input").css("[id^='chk_2']")[9:10]:
            self.grade_ = grade.css("::attr(name)").extract_first()
            self.grade_numeric = ''.join([i for i in self.grade_ if i.isdigit()])
            page = 1
            form_values = [f"{self.script_manager[0]}|{self.script_manager[0]}", f"{self.script_manager[0]}", f"{self.grade_numeric} {self.medium.get('english')}#{page}",response.css("input[id=__VIEWSTATE]::attr(value)").get(), response.css("input#__VIEWSTATEGENERATOR::attr(value)").get(),response.css("input#__EVENTVALIDATION::attr(value)").get(), "on", f"{self.grade_numeric} {self.medium.get('english')}", "2022","true", ]
            form_ = OrderedDict(zip(self.form_keys, form_values))
            form_.update({f'{self.grade_}': 'on'})
            form_.update({f'chk{self.medium.get("english")}': 'on'})
            
            yield scrapy.FormRequest(self.start_urls[0],
                formdata=form_,
                callback=self.parse_page,
                cb_kwargs={'page': 1},
                errback= self.err_func  
            )
    
    def parse_page(self, response, page):
        if page == 1:
            pages  = int(response.css("span[id='lblNoOfPages']::text").get())
        else:
            pages = 0
        
        for book in response.css("div[class='bookDetails1']"):
            book_title = book.css("div[class='divbooknm']::text").get()
            book_cover = book.css("img::attr('src')").get()
            book_pdf = book.css("div[class='button']::attr('onclick')").get().split("(")[1].split(",")[0][1:-1]
            book = BookItem(title_orig=book_title,book_cover= book_cover,book_url=book_pdf,)
            print("yield called")
            print(f"This {book}")
            yield book  

        body_ = response.body.decode('utf-8')
        pattern = re.compile(r"__VIEWSTATE\|([^|]+)\|")
        match = pattern.search(body_)
        _viewstate_ = re.compile(r"__VIEWSTATE\|([^|]+)\|").search(body_).group(1)
        _viewstate_generator =  re.compile(r"__VIEWSTATEGENERATOR\|([^|]+)\|").search(body_).group(1)
        _eventvalidation_ =  re.compile(r"__EVENTVALIDATION\|([^|]+)\|").search(body_).group(1)

        for i in range(2,pages+1):
            print('page')
            print(i)
            form_values = [f"{self.script_manager[1]}|{self.script_manager[1]}", f"{self.script_manager[1]}", f"{self.grade_numeric} {self.medium.get('english')}#{i}",_viewstate_, _viewstate_generator, _eventvalidation_, "on", f"{self.grade_numeric} {self.medium.get('english')}", "2022","true", ]
            form_ = OrderedDict(zip(self.form_keys, form_values))
            form_.update({f'{self.grade_}': 'on'})
            form_.update({f'chk{self.medium.get("english")}': 'on'})
            yield scrapy.FormRequest(self.start_urls[0],
            formdata=form_,
            callback=self.parse_page,
            cb_kwargs={'page': i},
            errback=self.err_func
            )

    def err_func(self, resp):
        print(resp.value.response._body)
    

