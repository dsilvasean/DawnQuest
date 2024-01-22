import scrapy

from collector.items import ShaalaaPublication


class ShaalaaSpider(scrapy.Spider):
    name = "ShaalaaSpider"
    allowed_domains = ["shaalaa.com"]
    start_urls = ["https://www.shaalaa.com/textbook-solutions"]
    root_url = "https://www.shaalaa.com"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    publications_to_scrape = ["balbharati"]
    grades_to_scrape = [6]
    subjects_to_scrape = ["history"]


    def parse(self, response):
        available_publications= response.css("div[class='block']")[1].css("a::attr('href')").getall()

        for publication in self.publications_to_scrape:
            publication_tbs_url = [f'{self.root_url}{href}' for href in available_publications if publication.lower() in href][0]
            yield scrapy.Request(publication_tbs_url, callback=self.parse_publication)
        
    def parse_publication(self,response):
        for grade in self.grades_to_scrape:
            available_subjects = response.xpath(f"//div[span[@id='{grade}th-standard']]//a/@href").extract()
            
            for subject in self.subjects_to_scrape:
                subject_tb_url = [f'{self.root_url}{href}' for href in available_subjects if subject.lower() in href][0]
                yield scrapy.Request(subject_tb_url, callback=self.parse_subject)
        
    def parse_subject(self, response):
        available_chapters =  response.xpath(f"//div[contains(@class, 'block')]//a[contains(@href, 'chapter') and contains(normalize-space(), 'Chapter')]/@href").extract()[0:1]
        for chapter in available_chapters:
            chapter_url = f"{self.root_url}{chapter}"
            yield scrapy.Request(chapter_url, callback=self.parse_chapter)


    def parse_chapter(self, response):
        questions_block = response.xpath(f"//div[contains(@class, 'qp_result_data')][@data-id]")
        for i, question_block in enumerate(questions_block):
            review_required= False
            question_extra_content = None
            solution_href = question_block.xpath(f".//a[contains(@class, 'view_solution')]/@href").extract()
            question_type_text = question_block.xpath(f".//div[contains(@class, 'html_text')]//strong/text()").extract()
            if not question_type_text:
                question_type_text = questions_block[i-1].xpath(f".//div[contains(@class, 'html_text')]//strong/text()").extract()
            
            question_meta = question_block.xpath(f".//div[contains(@class, 'qp_result_data_data_meta')]/text()").extract()
            question_ = question_block.xpath(f".//div[contains(@class, 'html_text')]//p[not(@class)]/text()").extract()
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
                'review_required':review_required,
                'question_type_text':question_type_text,
                'question_meta':question_meta,
                'question_': question_,
                'question_extra_content': question_extra_content,
                'solution_url': solution_href
            }

            if len(solution_href) > 4:
                yield scrapy.Request(solution_href, callback=self.parse_solution, priority=1, cb_kwargs={'_question_':_question_})
                # print(_question_['question_'])
            # print(_question_)
    
    def parse_solution(self, response, _question_):
        _question_ = _question_
        question_type = response.xpath("//div[contains(@class, 'qbq_q_type')]/text()").extract_first() or None
        solution_block  = response.xpath("//div[contains(@id, 'answer')]")

        if solution_block is not None:
            _question_['solution_'] = "".join(solution_block.xpath(".//*/text()").extract())
        
        _question_['solution_extra'] = None
        _question_['question_type_from_solution'] = question_type
        # print(solution_block)
        
        print(_question_)


            
            
            

           
