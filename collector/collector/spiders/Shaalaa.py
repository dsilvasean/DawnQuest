import scrapy, json, re
from asgiref.sync import sync_to_async
from urllib.parse import quote
from django.utils.text import slugify

from collector.items import ShaalaaPublication

from collector.spiders.Utils import DatabaseHelper

class ShaalaaSpider(scrapy.Spider):
    q_count = 0
    name = "ShaalaaSpider"
    database_helpter = DatabaseHelper(spider_name=name)
    allowed_domains = ["shaalaa.com"]
    start_urls = ["https://www.shaalaa.com/textbook-solutions"]
    root_url = "https://www.shaalaa.com"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    custom_settings = {
        'ITEM_PIPELINES': {
            'collector.pipelines.ShaalaaPipeline': 400
        }}


    async def parse(self, response):
        available_publications= response.xpath("//div[contains(@class, 'block') and not(contains(@class, ' '))][2]//a")
        publication_count = await sync_to_async(self.database_helpter.get_publications_info)(count=True)
        publications = [ShaalaaPublication(author=publication.xpath("./text()").extract_first(), hyperlink=f"{self.root_url}{publication.xpath('./@href').extract_first()}", available=True,)
                        for publication in available_publications]
        
        if publication_count is not None and (len(available_publications) != publication_count):
            for publication in publications:
                yield {"item_data": publication, "item_type":"publication"}
            
            
        publications_to_scrape = await sync_to_async(self.database_helpter.get_publications_info)()
        for publication in publications_to_scrape:
            print(publication)
            yield scrapy.Request(publication, callback=self.parse_publication)

    async def parse_publication(self,response):
        available_grades = []
        grades_ = await sync_to_async(self.database_helpter.get_grades_info)()
        _available_grades_ = response.xpath(f"//div[contains(@class, 'unit_solutions')]")
        products_units_url = await sync_to_async(self.database_helpter.get_meta_info)(name="product_unit_url", attribute_name="get_products_units", attribute_extra_name="url")
        for _grade_ in _available_grades_:
            grade_t = _grade_.xpath('./text()').re_first(r'Class (\w+)')
            if grade_t and int(grade_t) in grades_:
                g = {}
                g["grade"] = grade_t
                g["id"] = _grade_.xpath(".//@data-author_course_unit_id").extract_first()
                available_grades.append(g)

        for grade in available_grades:
            product_url = f"{products_units_url}?id={int(grade['id'])}"
            yield scrapy.Request(product_url, callback=self.parse_grades_url, cb_kwargs={"grade": grade})
        

    def parse_grades_url(self,response, grade):
        json_response = json.loads(response.text).get('content').get('data')[0]
        url_ = f"{self.root_url}{json_response.get('url2')}"
        yield scrapy.Request(url_, callback=self.parse_grade, cb_kwargs={"course_id": json_response.get("unit_id"), "grade": grade} ) 
    
    async def parse_grade(self,response, course_id,grade):
        subjects = []
       
        subjects_ = response.xpath("//input[contains(@class,'qp_filter')]")
        chapters_url = await sync_to_async(self.database_helpter.get_meta_info)(name="chapters_url", attribute_name="get_products_units", attribute_extra_name="url_chapters")

        for subject in subjects_:
            subject_ = {}
            subject_["name"] = subject.xpath(".//@data-url").extract_first()
            subject_["id"] = subject.xpath(".//@data-value").extract_first()
            subjects.append(subject_)
            
        chapter_index_param = {
            "subjects":[str(s_['id']) for s_ in subjects],
            "id":int(course_id),
            "getTotal":True
        }
        print(chapter_index_param)
        params_= quote(json.dumps(chapter_index_param))
        yield scrapy.Request(f"{chapters_url}?type=textbookSolutions&content-type=course&params={params_}", callback=self.parse_subjects, cb_kwargs={"grade":grade})


    async def parse_subjects(self, response, grade):
        json_response = json.loads(response.text).get("content").get("data")
        pub_name = json_response.get("data")[0].get("author_names")[0]
        subjects_and_lessons_scrape = await sync_to_async(self.database_helpter.get_meta_info)(name="collected_subjects_before", attribute_name=f"subjects_scraped_grade_{grade['grade']}", attribute_extra=pub_name)
        subjects_scrape = []

        if not subjects_and_lessons_scrape:
            publication_id = await sync_to_async(self.database_helpter.get_publications_info)(name=pub_name)
            grade_id = await sync_to_async(self.database_helpter.get_grades_info)(grade=grade['grade'])
            for _sub_ in json_response.get("data"):
                export_data = {}
                subject_info = {}
                chapters = []
                subject_info["name"] = _sub_.get("subject_name")
                subject_info["sub_id"] = _sub_.get("id")
                subject_info["descriptive_name"] = _sub_.get("name")
                subject_info["url"] = f"{self.root_url}{_sub_.get('url2')}"
                subject_info["publication_id"] = publication_id
                subject_info["grade_id"] = grade_id
                for chap in _sub_.get("products")[0].get("chapters"):
                    chapters.append(chap)
                export_data = {"subject" : subject_info, "chapters": chapters}
                subjects_scrape.append(export_data)
                # print(export_data)
                # return
                yield {"item_data": export_data, "item_type":"subjects_and_chapters"}

        else:
            print("Publication lessons and chapters already collected check Meta.subjects_scraped_-grade- value")

        subjects_to_scrape = await sync_to_async(self.database_helpter.get_subjects_info)(grade=grade["grade"],publication=pub_name)
        for subject in subjects_to_scrape:
            yield scrapy.Request(subject["url"], callback=self.parse_subject, cb_kwargs={"subject": subject["shaalaa_id"]})
            
            
    async def parse_subject(self, response, subject):
        print("aa",response)
        available_chapters_ =await sync_to_async(self.database_helpter.get_chapters_info)(subject=subject)
        available_chapters = [{ "chapter_name":f'{slugify(c.name)}', "id": c.id }
                               for c in  available_chapters_]
        # print(available_chapters)
        # chapters_in_dom =  response.xpath(f"//div[contains(@class, 'block')]//a[contains(@href, 'chapter') and contains(normalize-space(), 'Chapter')]/@href").extract()
        chapters_in_dom_ =  response.xpath(f"//div[contains(@class, 'block')]//a[contains(@href, 'chapter') and contains(normalize-space(), 'Chapter')]")
        chapters_in_dom =[{"href":chap.xpath("./@href").get(), "name": slugify(chap.xpath("./text()").get())}
                            for chap in chapters_in_dom_
                            ]
        # print("chap in dom", chapters_in_dom)
        # return
        print(chapters_in_dom)
        _chapters_ = [{"chapter_url": f"{self.root_url}{c['href']}", "_chapter": avc}
                      for avc in available_chapters 
                      for c in chapters_in_dom 
                      if re.search(re.escape(avc["chapter_name"]), c['name'])]  
        # export_data = {"chapters":_chapters_, "subject":subject}
        # yield {"item_type":"chapters_url_update", "item_data":export_data}
        for chapter in _chapters_:
            print(f"ccccc {chapter}")
            yield scrapy.Request(chapter["chapter_url"], callback=self.parse_chapter, cb_kwargs={"chapter_":chapter["_chapter"]["id"]})

        # available_chapters =  response.xpath(f"//div[contains(@class, 'block')]//a[contains(@href, 'chapter') and contains(normalize-space(), 'Chapter')]/@href").extract()[0:1]
        # for chapter in available_chapters:
        #     chapter_url = f"{self.root_url}{chapter}"
        #     yield scrapy.Request(chapter_url, callback=self.parse_chapter)


    def parse_chapter(self, response, chapter_):
        print("parse chapter was callled")
        questions_block = response.xpath(f"//div[contains(@class, 'qp_result_data')][@data-id]")
        # print(questions_block)
        # return
        self.q_count += len(questions_block)
        for i, question_block in enumerate(questions_block):
            review_required= False
            question_extra_content = None
            solution_href = question_block.xpath(f".//a[contains(@class, 'view_solution')]/@href").extract()
            question_type_text = question_block.xpath(f".//div[contains(@class, 'html_text')]//strong/text()").extract()
            if not question_type_text:
                question_type_text = questions_block[i-1].xpath(f".//div[contains(@class, 'html_text')]//strong/text()").extract()
            
            question_meta = question_block.xpath(f".//div[contains(@class, 'qp_result_data_data_meta')]/text()").extract()
            # question_ = question_block.xpath(f".//div[contains(@class, 'html_text')]//p[not(@class)]/text()").extract()
            question_ = question_block.xpath(f".//div[contains(@class, 'html_wrap')]/*").extract()
            
            print(question_)
            if not question_:
                question_ = question_block.xpath(f".//div[contains(@class, 'html_text')]/*[not(self::p[.//strong])]").extract()
                review_required = True
            imgs =  question_block.xpath(f".//div[contains(@class, 'html_text')]/*[not(self::p[.//strong])]//img/@src").extract()
            if imgs:
                question_extra_content = f"{self.root_url}{' '.join(imgs)}"
            if solution_href:
                solution_href = f"{self.root_url}{' '.join(solution_href)}"
            
            _question_ = {
                'chapter_id': chapter_,
                'review_required':review_required,
                'question_type_text':question_type_text,
                'question_meta':question_meta,
                'question_': question_,
                'question_extra_content': question_extra_content,
                'solution_url': solution_href
            }

            if len(solution_href) > 4:
                # print(_question_)
                yield scrapy.Request(solution_href, callback=self.parse_solution, priority=1, cb_kwargs={'_question_':_question_})
                # print(_question_['question_'])
    
    def parse_solution(self, response, _question_):
        _question_ = _question_
        _solution_ = {}
        question_type_div = response.xpath("//div[contains(@class, 'qbq_q_type')]/text()") or None
        if question_type_div is not None:
            questions_type = question_type_div.extract()
        # question_type = question_type_div.extract_first() or None
        # question_type_sub_type = response.xpath("//div[contains(@class, 'qbq_q_type')]/text()").extract()[-1] if len(question_type_div) > 1 else None
        # print(question_type, question_type_sub_type)
        # solution_block  = response.xpath("//div[contains(@id, 'answer')]/*") or None
        solution_block  = response.xpath("//div[contains(@id, 'answer')]") or None
        # sol_raw = ''
        # for child_node in solution_block:
        #     child_html = child_node.extract()
        #     sol_raw =sol_raw+ child_html
        # print(sol_raw)
        # print(solution_block.get())
        # sol_ = None
        # for sol in solution_block.xpath(".//descendant::*"):
        #     sol_ += sol.xpath()
        if solution_block is not None:
            # solution_raw_html = ''
            # for child_node in solution_block:
            #     solution_raw_html +=child_node.extract()
            # _solution_["solution_"] = "".join(solution_block.xpath(".//*/text()").extract())
            # _solution_["solution_"] = solution_block.xpath(".//descendant::*").get()
            # _solution_["solution_"] = solution_raw_html
            _solution_["solution_"] = solution_block.extract()
            # _question_['solution_'] = "".join(solution_block.xpath(".//*/text()").extract())
        
        _solution_['extra'] = None
        _solution_['question_type_from_solution'] = questions_type

        # _solution_['question_type_subtype_from_solution'] = question_type_sub_type if question_type_sub_type is not None else None
        
        _question_["_solution_"] = _solution_
        print(_question_)
        yield {"item_data": _question_, "item_type":"question_and_solution"}
        print("Total Questions collected", self.q_count)

    def close(self,spider, reason):
        custom_data = {'question_collected': self.q_count}
        self.crawler.stats.set_value('custom_data', custom_data)
        super().close(spider, reason)
