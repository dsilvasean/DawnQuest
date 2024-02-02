from django.db import models

from tinymce import models as tinymce_models

# Abstract Models

class TimeStampAbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract= True

class MetaAbstarctModel(models.Model): 
    meta = models.CharField(max_length=555,blank=True, null=True)

    class Meta:
        abstract= True


class QuestionAbstractModel(TimeStampAbstractModel, MetaAbstarctModel):
    question =  tinymce_models.HTMLField()
    url = models.URLField(blank=True, null=True)
    review_required = models.BooleanField(default=False)

    class Meta:
        abstract= True

class SolutionAbstractModel(TimeStampAbstractModel, MetaAbstarctModel):
    solution = tinymce_models.HTMLField()

    class Meta:
        abstract= True



# Concrete Models
class Grade(models.Model):
    grade = models.IntegerField(unique=True)

    to_scrape = models.BooleanField(default=False)

    def __str__(self):
        return f'class {self.grade}' 

class Board(models.Model):
    SITES = (
        (1, 'Maharashtra'),
    )
    board = models.IntegerField(choices=SITES,)

    def __str__(self):
        return self.get_board_display()


class Spider(models.Model):
    SITES = (
        (1, 'EBalbharti'),
        (2, "shaalaa"),

    )
    site_name = models.IntegerField(choices=SITES,)
    url = models.URLField(blank=True)
    spider_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.get_site_name_display()}'

class Meta(models.Model):
    spider = models.ForeignKey(Spider, on_delete=models.CASCADE)
    attribute_name = models.CharField(max_length=255)
    attribute_value = models.BooleanField()
    attribute_extra = models.CharField(max_length=255, blank=True)
    attribute_user_meata = models.TextField(blank=True)

    def __str__(self):
        return f"{self.spider} {self.attribute_name} {self.attribute_value}"
    

class MetaAttributeExtra(models.Model):
    meta = models.ForeignKey(Meta, on_delete=models.CASCADE, related_name="attribute_extras")
    attribute_extra_name = models.CharField(max_length=255)
    attribute_extra_value = models.TextField()

    def __str__(self):
        return f"{self.meta.spider} {self.meta.attribute_name} {self.attribute_extra_name}"
    
class Publication(models.Model):
    board = models.ForeignKey(Board, blank=True, null=True, on_delete=models.CASCADE)
    author = models.CharField(max_length=255,)
    name = models.CharField(max_length=255,)
    hyperlink = models.URLField(blank=True, null=True)
    available = models.BooleanField(default=True)

    to_scrape = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author} {self.to_scrape} {self.available}"
    
    # class Meta:
    #     unique_together = ('author', 'name')
    

class Subject(models.Model):
    # SUBJECTS = (
    #     (1, 'Mathematics'),
    # )
    # subject = models.IntegerField(choices=SUBJECTS,)
    shaalaa_id = models.IntegerField(blank=True, null=True)
    publication = models.ForeignKey(Publication, blank=True, null=True, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, blank=True, null=True, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    descriptive_name = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    to_scrape = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.grade} {self.name} {self.publication}"

class Book(models.Model):
    title_orig = models.CharField(max_length=255, blank=False)
    title_eng = models.CharField(max_length=255, blank=True)
    book_cover = models.URLField()
    book_url = models.URLField()
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    subject =  models.ForeignKey(Subject, on_delete=models.CASCADE)

    to_scrape = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.grade} {self.board} {self.subject} {self.title_eng}'
    


class Chapter(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    url = models.URLField(blank=True)

    to_scrape = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} {self.name}"

class QuestionType(models.Model):
    question_type = models.CharField(max_length=255)
    
    def __str__(self):
        return self.question_type

class Question(QuestionAbstractModel):
    chapter = models.ForeignKey(Chapter, blank=True, null=True, on_delete=models.CASCADE)
    type = models.ForeignKey(QuestionType, on_delete=models.CASCADE, blank=False)
    solution_url = models.URLField(max_length=555, blank=True)
    
    def __str__(self):
        return f" {self.chapter.subject.grade} {self.chapter.subject.name} {self.chapter.name} {self.type}"
    

class Solution(SolutionAbstractModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.solution

class QuestionResource(MetaAbstarctModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    resource = models.URLField()

class SolutionResource(MetaAbstarctModel):
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
    resource = models.URLField()
   
    
    
