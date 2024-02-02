import scrapy, json, re
from asgiref.sync import sync_to_async
from urllib.parse import quote
from django.utils.text import slugify

from core.models import Meta
from core.models import Publication, Grade, Chapter, Subject
from collector.items import ShaalaaPublication


class ShaalaaSpider(scrapy.Spider):
    name = "ShaalaaSpider"
    allowed_domains = ["shaalaa.com"]
    start_urls = ["https://www.shaalaa.com/textbook-solutions"]
    root_url = "https://www.shaalaa.com"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    custom_settings = {
        'ITEM_PIPELINES': {
            'collector.pipelines.ShaalaaPipeline': 400
        }}
    publications_to_scrape = ["balbharati"]
    grades_to_scrape = [6]
    subjects_to_scrape = ["history"]

    def get_meta_stats(self,stat_name, attribute_name=None, attribute_extra_name=None, attribute_extra=None):
        meta_objects =Meta.objects.filter(spider__spider_name=self.name)
        if stat_name=="publications_scraped":
            meta_object = meta_objects.filter(attribute_name=attribute_name).first()
            return meta_object.attribute_value if meta_object else None
        elif stat_name=="collected_subjects_before":
            meta_object = meta_objects.filter(attribute_name=attribute_name, attribute_extra__icontains=attribute_extra).first()
            return meta_object.attribute_value if meta_object else None
        elif stat_name=="product_unit_url" or stat_name=="chapters_url":
            meta_object = meta_objects.filter(attribute_name=attribute_name).first()
            return meta_object.attribute_extras.filter(attribute_extra_name=attribute_extra_name).first().attribute_extra_value if meta_object else None
        return None


    def get_publications_db(self, name=None):
        if name :
            publications_ = Publication.objects.filter(available=True, to_scrape=True, author__icontains=name).all()
            return publications_.first().id
        else:
            publications_ = Publication.objects.filter(available=True, to_scrape=True).all()
        if publications_:
            return [pub_.hyperlink for pub_ in publications_]
        return None

    def get_subjects_db(self,grade, publication):
        if grade:
            subjects = Subject.objects.filter(to_scrape=True,grade__grade=grade, publication__author__icontains=publication)
            return [{"url": s.url, "shaalaa_id": s.shaalaa_id} for s in subjects]
            

    def get_chapters_to_scrape(self,subject):
        if subject:
            chapters = Chapter.objects.filter(subject__shaalaa_id=subject, to_scrape=True).all()
            if chapters:
                return [chap for chap in chapters]
            
    def update_chapter_url(self, chapter, url):
        if chapter and url:
            chapter_ = Chapter.objects.filter(name__icontains=chapter,).update(url=url)
            print("updated" ,chapter_ , chapter)
        if chapter_:
            return True
        return False

    def get_grades(self, grade=None):
        if grade:
            grades = Grade.objects.filter(to_scrape=True, grade=grade).all()
            return grades.first().id
        else:
            grades = Grade.objects.filter(to_scrape=True).all()
            if grades:
                return [g_.grade for g_ in grades]
            return None

    async def parse(self, response):
        collected_publication_before = await sync_to_async(self.get_meta_stats)(stat_name="publications_scraped", attribute_name="publications_scraped")
        if not collected_publication_before:
            # available_publications = response.css("div[class='block']")[1].css("a::attr('href')").getall()
            available_publications_= response.xpath("//div[contains(@class, 'block') and not(contains(@class, ' '))][2]//a")
            for _publication in available_publications_:
                _pub = ShaalaaPublication(author=_publication.xpath("./text()").extract_first(), hyperlink=f"{self.root_url}{_publication.xpath('./@href').extract_first()}", available=True,)
                yield {"item_data": _pub, "item_type":"publication"}
        else:
            publications_to_scrape = await sync_to_async(self.get_publications_db)()
            if publications_to_scrape is None:
                print("No Publications to scrape")
                return 
            
        publications_to_scrape = await sync_to_async(self.get_publications_db)()
        for publication in publications_to_scrape:
            # publication_tbs_url = [f'{self.root_url}{href}' for href in available_publications if publication.lower() in href][0]
            # yield scrapy.Request(publication_tbs_url, callback=self.parse_publication)
            yield scrapy.Request(publication, callback=self.parse_publication)

    async def parse_publication(self,response):
        available_grades = []
        grades_ = await sync_to_async(self.get_grades)()
        _available_grades_ = response.xpath(f"//div[contains(@class, 'unit_solutions')]")
        products_units_url = await sync_to_async(self.get_meta_stats)(stat_name="product_unit_url", attribute_name="get_products_units", attribute_extra_name="url")
        for _grade_ in _available_grades_:
            grade_t = _grade_.xpath('./text()').re_first(r'Class (\w+)')
            if grade_t and int(grade_t) in grades_:
                g = {}
                g["grade"] = grade_t
                g["id"] = _grade_.xpath(".//@data-author_course_unit_id").extract_first()
                # g[grade_t] = _grade_.xpath(".//@data-author_course_unit_id").extract_first()
                available_grades.append(g)

        for grade in available_grades:
            product_url = f"{products_units_url}?id={int(grade['id'])}"
            yield scrapy.Request(product_url, callback=self.parse_grades_url, cb_kwargs={"grade": grade})

        
        # if grades_ and available_grades:
        #     for grade in grades_:
        #         print(available_grades)
        #         if grade in available_grades:
        #             print(grade)
                # available_subjects = response.xpath(f"//div[span[@id='{grade}th-standard']]//a/@href").extract()
                # print(available_subjects)

                # for subject in self.subjects_to_scrape:
                #     subject_tb_url = [f'{self.root_url}{href}' for href in available_subjects if subject.lower() in href][0]
                #     yield scrapy.Request(subject_tb_url, callback=self.parse_subject)
        

    def parse_grades_url(self,response, grade):
        json_response = json.loads(response.text).get('content').get('data')[0]
        url_ = f"{self.root_url}{json_response.get('url2')}"
        yield scrapy.Request(url_, callback=self.parse_grades_new, cb_kwargs={"course_id": json_response.get("unit_id"), "grade": grade} ) 
    
    async def parse_grades_new(self,response, course_id,grade):
        subjects = []
       
        subjects_ = response.xpath("//input[contains(@class,'qp_filter')]")
        chapters_url = await sync_to_async(self.get_meta_stats)(stat_name="chapters_url", attribute_name="get_products_units", attribute_extra_name="url_chapters")

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
        subjects_and_lessons_scrape = await sync_to_async(self.get_meta_stats)(stat_name="collected_subjects_before", attribute_name=f"subjects_scraped_grade_{grade['grade']}", attribute_extra=pub_name)
        subjects_scrape = []

        if not subjects_and_lessons_scrape:
            publication_id = await sync_to_async(self.get_publications_db)(name=pub_name)
            grade_id = await sync_to_async(self.get_grades)(grade=grade['grade'])
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
                yield {"item_data": export_data, "item_type":"subjects_and_chapters"}

                # for subject in subjects_scrape:
                #     yield scrapy.Request(subject["subject"]["url"], callback=self.parse_subject, cb_kwargs={"subject": subject["subject"]["sub_id"]})
        else:
            print("Publication lessons and chapters already collected check Meta.subjects_scraped_-grade- value")

        subjects_to_scrape = await sync_to_async(self.get_subjects_db)(grade=grade["grade"],publication=pub_name)
        for subject in subjects_to_scrape:
            yield scrapy.Request(subject["url"], callback=self.parse_subject, cb_kwargs={"subject": subject["shaalaa_id"]})
            
            # for chap in json_response.get("data")
            # yield {"item_data": _pub, "item_type":"publication"}
            


    async def parse_subject(self, response, subject):
        print(response)
        available_chapters_ =await sync_to_async(self.get_chapters_to_scrape)(subject=subject)
        available_chapters = [{ "chapter_name":f'{slugify(c.name)}', "id": c.id }
                               for c in  available_chapters_]
        print(available_chapters)
        chapters_in_dom =  response.xpath(f"//div[contains(@class, 'block')]//a[contains(@href, 'chapter') and contains(normalize-space(), 'Chapter')]/@href").extract()
        print(chapters_in_dom)
        _chapters_ = [{"chapter_url": f"{self.root_url}{c}", "_chapter": avc}
                      for avc in available_chapters 
                      for c in chapters_in_dom 
                      if re.search(re.escape(avc["chapter_name"]), c)]  
        print(_chapters_)     
        for chapter in _chapters_:
            print(chapter)
            # await sync_to_async(self.update_chapter_url)(chapter=chapter.split("/")[-1], url=chapter)
            yield scrapy.Request(chapter["chapter_url"], callback=self.parse_chapter, cb_kwargs={"chapter_":chapter["_chapter"]["id"]  })

        # available_chapters =  response.xpath(f"//div[contains(@class, 'block')]//a[contains(@href, 'chapter') and contains(normalize-space(), 'Chapter')]/@href").extract()[0:1]
        # for chapter in available_chapters:
        #     chapter_url = f"{self.root_url}{chapter}"
        #     yield scrapy.Request(chapter_url, callback=self.parse_chapter)


    def parse_chapter(self, response, chapter_):
        questions_block = response.xpath(f"//div[contains(@class, 'qp_result_data')][@data-id]")
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
            
            # yield scrapy.Request()

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
                print(_question_)
                yield scrapy.Request(solution_href, callback=self.parse_solution, priority=1, cb_kwargs={'_question_':_question_})
                # print(_question_['question_'])
            # print(_question_)
    
    def parse_solution(self, response, _question_):
        _question_ = _question_
        _solution_ = {}
        question_type = response.xpath("//div[contains(@class, 'qbq_q_type')]/text()").extract_first() or None
        solution_block  = response.xpath("//div[contains(@id, 'answer')]")

        if solution_block is not None:
            # _solution_["solution_"] = "".join(solution_block.xpath(".//*/text()").extract())
            _solution_["solution_"] = solution_block.xpath(".//descendant::*").get()
            # _question_['solution_'] = "".join(solution_block.xpath(".//*/text()").extract())
        
        _solution_['extra'] = None
        _solution_['question_type_from_solution'] = question_type
        _question_["_solution_"] = _solution_
        yield {"item_data": _question_, "item_type":"question_and_solution"}
