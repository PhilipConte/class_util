from pathlib import Path
from csv import reader
from django.core.management import BaseCommand
from distributions.models import Term, Course, Section, Semester
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

SEMESTER = [ # True if in first year, false if in second
    ('Winter', False),
    ('Spring', False),
    ('Summer I', True),
    ('Summer II', True),
    ('Fall', True)
]


class Command(BaseCommand):
    help = "Loads data from distributions/data/*.csv into the Sections model"

    def handle(self, *args, **options):
        path = Path('/data/Grade Distribution.csv')
        if Semester.objects.exists() or not path.is_file():
            return

        for idx, (name, _) in enumerate(SEMESTER):
            semester = Semester()
            semester.name = name
            semester.ordering = idx + 1
            semester.save()

        print("Loading section data...")
        with open(path, encoding='utf-8-sig') as file:
            next(file) # skip horrible header
            for row in reader(file):
                is_first = next(i[1] for i in SEMESTER if i[0]==row[1])
                year = row[0][2:4] if is_first else row[0][-2:]
                year = int('20' + year) # Y2K FTW

                semester = Semester.objects.get(name=row[1])
                term, _ = Term.objects.get_or_create(semester=semester, year=year)

                section = Section()
                section.term = term
                section.course, _ = Course.objects.get_or_create(
                    department = row[2],
                    number = row[3],
                    title = row[4],
                    hours = int(row[15]))
                section.CRN = row[14]
                section.instructor = row[5]
                section.average_GPA = row[6]
                section.As = row[7]
                section.Bs = row[8]
                section.Cs = row[9]
                section.Ds = row[10]
                section.Fs = row[11]
                section.withdrawals = row[12]
                section.class_size = row[13]
                section.save()
        print('done')
