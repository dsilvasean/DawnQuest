# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from core.models import Book, Grade, Subject, Board, Chapter, QuestionType, Question, Solution

# from ShaalaaMiner.models import Question, Solution, QuestionType, QuestionResource

from core.models import Publication

from core.models import Subject as ShaalaaSubject
from asgiref.sync import sync_to_async

from bs4 import BeautifulSoup


class ShaalaaPipeline:
    root_url = "https://www.shaalaa.com"

    @sync_to_async  
    def process_item(self,item,spider):
        if spider.name == "ShaalaaSpider":
            if item.get("item_type") == "publication":
                item_ = item.get("item_data")
                _pub_ = Publication(
                    author = item_['author'],
                    name = item_['author'],
                    hyperlink = item_['hyperlink']
                )
                _pub_.save()
                return item
            elif item.get("item_type") == "subjects_and_chapters":
                item_ =item.get("item_data")
                subject_info = item_.get("subject")
                chapters = item_.get("chapters")
                print(subject_info)
                sub_ = ShaalaaSubject(shaalaa_id=subject_info["sub_id"], publication_id=subject_info["publication_id"], grade_id=subject_info["grade_id"], name=subject_info["name"], descriptive_name=subject_info["descriptive_name"], url=subject_info["url"])
                sub_.save()
                chapters_ = [Chapter(subject=sub_, name=chapter) for chapter in chapters]
                Chapter.objects.bulk_create(chapters_)
                return "Item Received"

            elif item.get("item_type") == "question_and_solution":
                item_ =item.get("item_data")
                solution_ = item_['_solution_']
                print("question_pipeline")
                question_p= self.pre_process_item("question", item_['question_'])
                solution_p = self.pre_process_item("solution", solution_["solution_"])
                types_list = solution_["question_type_from_solution"] 
                # types_list = ["MCQ", "Odd MAN OUT", "A", "A", "A"]
                type_ = self.get_or_create_question_type(types_list=types_list)
                q_= Question.objects.create(chapter=Chapter.objects.get(id=item_["chapter_id"]), type=type_, question =question_p, solution_url=item_["solution_url"], review_required=item_["review_required"], meta="".join(item_["question_meta"]))

                s_ = Solution.objects.create(question=q_, solution=solution_p)

    def pre_process_item(self, type, data):
        if type == "question" or type == "solution":
            data="".join(data)
            if "img" and "src" in data:
                soup = BeautifulSoup(data, 'html.parser')
                img_tags = soup.find_all("img")
                for img in img_tags:
                    img['src'] = self.root_url + img['src']
                data = str(soup)
            return data
    
    def get_or_create_question_type(self, types_list):
        root_value = types_list[0]
        same_node_count = QuestionType.objects.filter(name=root_value, depth=1).count()

        if same_node_count ==0:
            current_node = QuestionType.add_root(name=root_value)
        else:
            current_node = QuestionType.objects.get(name=root_value, depth=1)

        
        for type_value in types_list[1:]:
            try:
                current_node = current_node.get_children().get(name=type_value)
            except ObjectDoesNotExist:
                current_node = current_node.add_child(name=type_value)
        
        return current_node

       



class EBalbhartiPipeline:
    def __init__(self):
        self.books_to_save = []
        
    async def process_item(self, item, spider):
        print("pipline init")
        # self.title_eng = await self.get_title_eng(item)
        self.grade = await self.get_grade(item)
        self.board = await self.get_board(item)
        self.subject = await self.get_subject(item)
        book_instance = Book(
            title_orig=item['title_orig'],
            title_eng = item['title_eng'],
            book_cover = item['book_cover'],
            book_url= item['book_url'],
            grade = self.grade,
            board = self.board,
            subject = self.subject
        )
        await sync_to_async(book_instance.save)()
        return item
    
    async def get_grade(self,item):
        return await sync_to_async(Grade.objects.get)(grade=int(item['grade']))
    
    # async def get_title_eng(self, item):
    #     translation = await self.translate(item['title_orig'])
    #     return translation.text if translation else ''

    async def get_subject(self,item):
        return await sync_to_async(Subject.objects.get)(id=1)
    
    async def get_board(self,item):
        return await sync_to_async(Board.objects.get)(id=1)

    # async def translate(self, text):
    #     translator = Translator()
    #     return await sync_to_async(translator.translate)(text, dest='en')


# class Utils:
#     def get_or_create_root(self, model, name):

def generate_data_from_list(list_):
    root = {'data': {'name': list_[0]}, 'children': []}
    current_node = root

    for item in list_[1:]:
        new_node = {'data': {'name': item}, 'children': []}
        current_node['children'].append(new_node)
        current_node = new_node

    return [root]