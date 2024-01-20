# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from core.models import Book, Grade, Subject, Board

from asgiref.sync import sync_to_async



class EBalbhartiPipeline:
    async def process_item(self, item, spider):
        print("pipline init")
        self.title_eng = await self.get_title_eng(item)
        self.grade = await self.get_grade(item)
        self.board = await self.get_board(item)
        self.subject = await self.get_subject(item)
        book_instance = Book(
            title_orig=item['title_orig'],
            title_eng = self.title_eng,
            book_cover = item['book_cover'],
            book_url= item['book_url'],
            grade = self.grade,
            board = self.board,
            subject = self.subject
        )
        await sync_to_async(book_instance.save)()
        return item
    
    async def get_grade(self,item):
        return await sync_to_async(Grade.objects.get)(id=1)
    
    async def get_title_eng(self,item):
        return 'english titile '
    
    async def get_subject(self,item):
        return await sync_to_async(Subject.objects.get)(id=1)
    
    async def get_board(self,item):
        return await sync_to_async(Board.objects.get)(id=1)
        
