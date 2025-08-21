# Utility functions used for spiders

from core.models import Meta, Publication, Subject, Chapter, Grade

class DatabaseHelper:
    def __init__(self, spider_name=None):
        self.spider_name =spider_name 

    def get_meta_info(self,name, attribute_name=None, attribute_extra_name=None, attribute_extra=None):
        meta_objects =Meta.objects.filter(spider__spider_name=self.spider_name)
        if name=="publications_scraped":
            meta_object = meta_objects.filter(attribute_name=attribute_name).first()
            return meta_object.attribute_value if meta_object else None
        elif name=="collected_subjects_before":
            meta_object = meta_objects.filter(attribute_name=attribute_name, attribute_extra__icontains=attribute_extra).first()
            return meta_object.attribute_value if meta_object else None
        elif name=="product_unit_url" or name=="chapters_url":
            meta_object = meta_objects.filter(attribute_name=attribute_name).first()
            return meta_object.attribute_extras.filter(attribute_extra_name=attribute_extra_name).first().attribute_extra_value if meta_object else None
        return None

    def get_publications_info(self,name=None,count=False):
        if count:
            return Publication.objects.filter(site=self.spider_name).count() if not None else None
        if name:
            publications = Publication.objects.filter(available=True, to_scrape=True, author__icontains=name)
            return publications.first().id
        else:
            publications = Publication.objects.filter(available=True, to_scrape=True).all()
            return [pub.hyperlink for pub in publications] if publications else None
    
    def get_subjects_info(self,grade,publication):
        if grade and publication:
            subjects  = Subject.objects.filter(to_scrape=True,grade__grade=grade, publication__author__icontains=publication)
            return [{"url":s.url, "shaalaa_id":s.shaalaa_id} for s in subjects] if subjects else None
    
    def get_chapters_info(self,subject=None, chapter=None):
        if subject and not chapter:
            chapters = Chapter.objects.filter(subject__shaalaa_id=subject, to_scrape=True)
            return [chap for chap in chapters] if chapters else None
    
    def get_grades_info(self, grade=None):
        if grade:
            grade = Grade.objects.filter(to_scrape=True,grade=grade)
            return grade.first().id if grade else None
        else:
            grades = Grade.objects.filter(to_scrape=True)
            return [g.grade for g in grades] if grades else None
    
        
    
