from django.db import models
from django.db.models import F, Sum, Avg
from django.urls import reverse
from .utils import quote

class Term(models.Model):
    semester = models.CharField(max_length=10)
    year = models.PositiveIntegerField()

    def __str__(self):
        return '{} {}'.format(self.semester, self.year)

class CourseManager(models.Manager):
    def all(self):
        return self.get_queryset().annotate(average_GPA=Avg('sections__average_GPA'))

class Course(models.Model):
    department = models.CharField(max_length=8)
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=50)
    hours = models.PositiveIntegerField()
    
    objects = CourseManager()

    @property
    def url_args(self):
        return [self.department, self.number, quote(self.title), self.hours]

    def get_absolute_url(self):
        return reverse('course', args=self.url_args)

    @property
    def stats(self):
        return self.sections.stats()

    def short(self):
        return '{} {}'.format(self.department, self.number)

    def no_credits(self):
        return self.short() + ': {}'.format(self.title)

    def __str__(self):
        return self.no_credits() + ' ({} credits)'.format(self.hours)

class SectionQueryset(models.QuerySet):
    def stats(self):
        def safe_round(val):
            return round(val, 2) if (type(val) is float) else val
        
        data = self.aggregate(
            GPA=Avg('average_GPA'),
            A=Avg('As'), B=Avg('Bs'),
            C=Avg('Cs'), D=Avg('Ds'), F=Avg('Fs'),
            students=Sum('class_size'),
            withdrawals=Sum('withdrawals'))
        
        return {key: safe_round(value) for key, value in data.items()}

class Section(models.Model):
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='sections')

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    
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

    objects = SectionQueryset.as_manager()

    def __str__(self):
        return '{}: CRN: {} ({})'.format(self.course, self.CRN, self.term)
