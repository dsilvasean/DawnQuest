import scrapy

from collections import OrderedDict
from collector.items import BookItem
import re
from googletrans import Translator



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
        for grade in response.css("span[class='spnItem'] input").css("[id^='chk_2']")[5:6]:
            _grade_f = grade.css("::attr(name)").extract_first()
            _grade_n = ''.join([i for i in _grade_f if i.isdigit()])
            # self.grade_ = grade.css("::attr(name)").extract_first()
            # self.grade_numeric = ''.join([i for i in self.grade_ if i.isdigit()])
            page = 1
            form_values = [f"{self.script_manager[0]}|{self.script_manager[0]}", f"{self.script_manager[0]}", f"{_grade_n} {self.medium.get('english')}#{page}",response.css("input[id=__VIEWSTATE]::attr(value)").get(), response.css("input#__VIEWSTATEGENERATOR::attr(value)").get(),response.css("input#__EVENTVALIDATION::attr(value)").get(), "on", f"{_grade_n} {self.medium.get('english')}", "2022","true", ]
            form_ = OrderedDict(zip(self.form_keys, form_values))
            form_.update({f'{_grade_f}': 'on'})
            form_.update({f'chk{self.medium.get("english")}': 'on'})
            
            yield scrapy.FormRequest(self.start_urls[0],
                formdata=form_,
                callback=self.parse_page,
                cb_kwargs={'page': 1, '_grade_n':''.join([i for i in _grade_f if i.isdigit()]), '_grade_s':_grade_f },
                errback= self.err_func  
            )
    
    def parse_page(self, response, page, _grade_n, _grade_s):
        if page == 1:
            pages  = int(response.css("span[id='lblNoOfPages']::text").get())
        else:
            pages = 0
        translator = Translator()

        for book in response.css("div[class='bookDetails1']"):
            book_title = book.css("div[class='divbooknm']::text").get()
            book_title_ = translator.translate(book_title, dest='en', src='mr').text
            book_cover = f"""{self.start_urls[0]}/{book.css("img::attr('src')").get()}"""
            book_pdf = book.css("div[class='button']::attr('onclick')").get().split("(")[1].split(",")[0][1:-1]
            grade = _grade_n
            print(f'this is gradee {_grade_n}')
            book = BookItem(title_orig=book_title,book_cover= book_cover,book_url=book_pdf, grade=_grade_n[-2:], title_eng=book_title_)
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
            form_values = [f"{self.script_manager[1]}|{self.script_manager[1]}", f"{self.script_manager[1]}", f"{_grade_n} {self.medium.get('english')}#{i}",_viewstate_, _viewstate_generator, _eventvalidation_, "on", f"{_grade_n} {self.medium.get('english')}", "2022","true", ]
            form_ = OrderedDict(zip(self.form_keys, form_values))
            form_.update({f'{_grade_s}': 'on'})
            form_.update({f'chk{self.medium.get("english")}': 'on'})
            yield scrapy.FormRequest(self.start_urls[0],
            formdata=form_,
            callback=self.parse_page,
            cb_kwargs={'page': i, '_grade_n':_grade_n, '_grade_s': _grade_s},
            errback=self.err_func
            )

    def err_func(self, resp):
        print(resp.value.response._body)
    

