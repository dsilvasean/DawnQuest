from django.db import models

class Grade(models.Model):
    grade = models.IntegerField(unique=True)

    def __str__(self):
        return f'class {self.grade}' 

class Board(models.Model):
    SITES = (
        (1, 'Maharashtra'),
    )
    board = models.IntegerField(choices=SITES,)

    def __str__(self):
        return self.get_board_display()

class Subject(models.Model):
    SITES = (
        (1, 'Mathematics'),
    )
    subject = models.IntegerField(choices=SITES,)

    def __str__(self):
        return f'{self.subject}'

class Spider(models.Model):
    SITES = (
        (1, 'EBalbharti'),
        (2, "shaalaa"),

    )
    site = models.IntegerField(choices=SITES,)

    def __str__(self):
        return f'{self.get_site_display()}'

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

