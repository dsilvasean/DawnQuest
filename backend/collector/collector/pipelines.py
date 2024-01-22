# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from core.models import Book, Grade, Subject, Board

from ShaalaaMiner.models import Publication

from asgiref.sync import sync_to_async


class ShaalaaPipeline:
    @sync_to_async  
    def process_item(self,item,spider):
        if spider.name == "ShaalaaSpider":
            if item.get("item_type") == "publication":
                item_ = item.get("item_data")
                _pub_ = Publication(
                    author = item_['author'],
                    hyperlink = item_['hyperlink']
                )
                _pub_.save()
                return item


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
