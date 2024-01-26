from django.db import models

from tinymce import models as tinymce_models

# Create your models here.

class Grade(models.Model):
    grade = models.IntegerField(unique=True)

    to_scrape = models.BooleanField(default=False)

    def __str__(self):
        return f'class {self.grade}' 

class Publication(models.Model):
    author = models.CharField(max_length=255, unique=True)
    hyperlink = models.URLField()
    available = models.BooleanField(default=True)

    to_scrape = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author} {self.to_scrape} {self.available}"
    
class Subject(models.Model):
    shaalaa_id = models.IntegerField(blank=True)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    descriptive_name = models.CharField(max_length=255)
    url = models.URLField(blank=True)

    to_scrape = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.grade} {self.name} {self.publication}"


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
    

class Question(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    type = models.ForeignKey(QuestionType, on_delete=models.CASCADE, blank=False)
    question = tinymce_models.HTMLField()
    url = models.URLField(blank=True)
    solution_url = models.URLField(max_length=555)
    review_required = models.BooleanField(default=False)
    meta = models.CharField(max_length=255)

    def __str__(self):
        return f" {self.chapter.subject.grade} {self.chapter.subject.name} {self.chapter.name} {self.type}"
    
class Solution(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    solution = tinymce_models.HTMLField()

    def __str__(self):
        return self.solution

class QuestionResource(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    resource = models.URLField()
    meta = models.TextField()

class SolutionResource(models.Model):
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
    resource = models.URLField()
    meta = models.TextField()
    


