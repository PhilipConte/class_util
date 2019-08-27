from django.db import models
from django.db.models import F, Sum, Avg, Count, Func
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.dispatch import receiver
from django.utils.safestring import SafeString

from .utils import dict_pop


class Round(Func):
    function = 'ROUND'
    arity = 2
    # Only works as the arity is 2
    arg_joiner = '::numeric, '

    def as_sqlite(self, compiler, connection, **extra_context):
        return super().as_sqlite(compiler, connection, arg_joiner=", ", **extra_context)


raw_stats = {'average_GPA': (Avg,'average_GPA'),
            'As': (Avg,'As'), 'Bs': (Avg,'Bs'),
            'Cs': (Avg,'Cs'), 'Ds': (Avg,'Ds'), 'Fs': (Avg,'Fs'),
            'students': (Sum,'class_size'),
            'withdrawals': (Sum,'withdrawals')}
stats_dict = {key: Round(t[0](t[1]), 2) for key, t in raw_stats.items()}

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
        to_annotate = {k: Round(t[0]('sections__'+t[1]), 2) for k, t in base_dict.items()}
        return super().get_queryset(**kwargs).annotate(**to_annotate)

class Course(models.Model):
    department = models.CharField(max_length=8)
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    hours = models.PositiveIntegerField()

    slug = models.SlugField(unique=True, max_length=200)
    
    objects = CourseManager()

    def get_absolute_url(self):
        return reverse('distributions:course_detail', args=[self.slug])

    @property
    def stats(self):
        return self.sections.stats()

    def short(self):
        return '{} {}'.format(self.department, self.number)

    def no_credits(self):
        return self.short() + ': {}'.format(self.title)

    def __str__(self):
        return self.no_credits() + ' ({} credits)'.format(self.hours)

    def html(self):
        title_parts = str(self).split(':')
        return ('<strong>'+title_parts[0]+'</strong>: '+title_parts[1])

    class Meta:
        ordering = ['department', 'number', 'title', 'hours']

class Pathway(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course, related_name='pathways')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', 'description',)

class SectionQueryset(models.QuerySet):
    def stats(self):
        return self.aggregate(**stats_dict)
    
    def group_by_instructor(self):
        stats = dict_pop(stats_dict, ['students'])
        stats['sections_taught'] = Count('instructor')
        return self.values('instructor').annotate(**stats).order_by('instructor')

    def group_by_term(self):
        semesters = self.values('term').annotate(average_GPA=stats_dict['average_GPA'])
        return {str(Term.objects.get(pk=sem['term'])): sem['average_GPA'] for sem in semesters}

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

    slug = models.SlugField(unique=True, max_length=200)

    objects = SectionQueryset.as_manager()

    def get_absolute_url(self):
        return reverse('distributions:course_instructor_detail', args=[self.course.slug, self.instructor])

    def __str__(self):
        return '{} | {} | {} | {}'.format(self.CRN, self.instructor, self.term, self.course.short())
    
    class Meta:
        ordering = ['term', 'course', 'CRN', 'instructor', 'average_GPA']

@receiver(pre_save, sender=Course)
def pre_save_course_receiver(sender, instance, *args, **kwargs):
    def create_slug(instance, new_slug=None):
        slug = slugify('_'.join([instance.department, instance.number, instance.title, instance.hours]))
        if new_slug is not None:
            slug = new_slug
        qs = sender.objects.filter(slug=slug).order_by("-id")
        if qs.exists():
            new_slug = '{}-{}'.format(slug, qs.first().id)
            return create_slug(instance, new_slug=new_slug)
        return slug
    
    if not instance.slug:
        instance.slug = create_slug(instance)

@receiver(pre_save, sender=Section)
def pre_save_section_receiver(sender, instance, *args, **kwargs):
    def create_slug(instance, new_slug=None):
        slug = slugify('_'.join([str(instance.term), instance.course.short(), instance.instructor, str(instance.CRN)]))
        if new_slug is not None:
            slug = new_slug
        qs = sender.objects.filter(slug=slug).order_by("-id")
        if qs.exists():
            new_slug = '{}-{}'.format(slug, qs.first().id)
            return create_slug(instance, new_slug=new_slug)
        return slug
    
    if not instance.slug:
        instance.slug = create_slug(instance)
