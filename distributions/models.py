from django.db import models

class Section(models.Model):
    #TERM_CHOICES: see management/load_section_data.py, ctrl+f term

    term = models.CharField(max_length=10)
    year = models.PositiveIntegerField()

    department = models.CharField(max_length=8)
    course_number = models.PositiveIntegerField()
    course_title = models.CharField(max_length=50)
    credit_hours = models.PositiveIntegerField()
    
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
