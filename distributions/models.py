from django.db import models
from django.db.models import F, Sum, Avg, Count
from django.urls import reverse
from .utils import quote, dict_pop

raw_stats = {'average_GPA': (Avg,'average_GPA'),
            'As': (Avg,'As'), 'Bs': (Avg,'Bs'),
            'Cs': (Avg,'Cs'), 'Ds': (Avg,'Ds'), 'Fs': (Avg,'Fs'),
            'students': (Sum,'class_size'),
            'withdrawals': (Sum,'withdrawals')}
stats_dict = {key: t[0](t[1]) for key, t in raw_stats.items()}

class Semester(models.Model):
    name = models.CharField(max_length=20)
    ordering = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['ordering']

class Term(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()

    def __str__(self):
        return '{} {}'.format(self.semester, self.year)

    class Meta:
        ordering = ['year', 'semester']

class CourseManager(models.Manager):
    def get_queryset(self, **kwargs):
        base_dict = dict_pop(raw_stats, ['students', 'withdrawals'])
        to_annotate = {k: t[0]('sections__'+t[1]) for k, t in base_dict.items()}
        return super().get_queryset(**kwargs).annotate(**to_annotate)

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
        return reverse('course_detail', args=self.url_args)

    @property
    def stats(self):
        return self.sections.stats()

    def short(self):
        return '{} {}'.format(self.department, self.number)

    def no_credits(self):
        return self.short() + ': {}'.format(self.title)

    def __str__(self):
        return self.no_credits() + ' ({} credits)'.format(self.hours)

    class Meta:
        ordering = ['department', 'number', 'title', 'hours']

class SectionQueryset(models.QuerySet):
    def stats(self):
        def safe_round(val):
            return round(val, 2) if (type(val) is float) else val
        
        data = self.aggregate(**stats_dict)
        
        return {key: safe_round(value) for key, value in data.items()}
    
    def group_by_instructor(self):
        stats = dict_pop(stats_dict, 'students')
        stats['sections_taught'] = Count('instructor')
        return self.values('instructor').annotate(**stats)

    def group_by_term(self):
        group = self.values('term').annotate(
            average_GPA=stats_dict['average_GPA'])
        
        for item in group:
            item['average_GPA'] = round(item['average_GPA'], 2)
            item['term'] = Term.objects.get(pk=item['term'])
        
        group = {item['term']: item['average_GPA'] for item in group}
        return group

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
    
    class Meta:
        ordering = ['term', 'course', 'CRN', 'instructor', 'average_GPA']
