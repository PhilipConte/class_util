from django.db import models
from django.urls import reverse

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

    def get_absolute_url(self):
        return reverse('course', args=[self.department, self.number, self.title, self.hours])

    def __str__(self):
        return '{} {}: {} ({} credits)'.format(
            self.department, self.number,
            self.title, self.hours)

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
