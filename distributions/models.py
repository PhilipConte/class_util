from django.db import models
from django.urls import reverse
from .utils import sections_stats, quote

class Term(models.Model):
    semester = models.CharField(max_length=10)
    year = models.PositiveIntegerField()

    def __str__(self):
        return '{} {}'.format(self.semester, self.year)

class Course(models.Model):
    department = models.CharField(max_length=8)
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=50)
    hours = models.PositiveIntegerField()

    @property
    def url_args(self):
        return [self.department, self.number, quote(self.title), self.hours]

    def get_absolute_url(self):
        return reverse('course', args=self.url_args)

    @property    
    def sections(self):
        return Section.objects.all().filter(course=self)

    @property
    def stats(self):
        return sections_stats(self.sections)

    @property
    def gpa(self):
        return self.stats['GPA']

    def short(self):
        return '{} {}'.format(self.department, self.number)

    def no_credits(self):
        return self.short() + ': {}'.format(self.title)

    def __str__(self):
        return self.no_credits() + ' ({} credits)'.format(self.hours)

class Section(models.Model):
    term = models.ForeignKey(Term, on_delete=models.CASCADE)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    CRN = models.PositiveIntegerField()
    instructor = models.CharField(max_length=30)
    average_GPA = models.DecimalField(max_digits=4, decimal_places=2)
    As = models.DecimalField(max_digits=4, decimal_places=1)
    Bs = models.DecimalField(max_digits=4, decimal_places=1)
    Cs = models.DecimalField(max_digits=4, decimal_places=1)
    Ds = models.DecimalField(max_digits=4, decimal_places=1)
    Fs = models.DecimalField(max_digits=4, decimal_places=1)
    withdrawals = models.PositiveIntegerField()
    class_size = models.PositiveIntegerField()

    def get_absolute_url(self):
        return reverse('section_id', args=[self.id])

    def __str__(self):
        return '{}: CRN: {} ({})'.format(self.course, self.CRN, self.term)
