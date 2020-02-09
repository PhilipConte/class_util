from pathlib import Path
from csv import DictReader
from django.core.management import BaseCommand
from distributions.models import Term, Course, Section, Semester
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

SEMESTER_DICT = {'winter': 1, 'spring': 2, 'summer1': 3, 'summer2': 4, 'fall': 5}

INVALID_CSV_NAME_ERROR_MESSAGE = """
CSVs must be in the format YYYY_SEMESTER.csv
ie: fall 2018 would be 2018_fall.csv
valid semesters are defined by the SEMESTER_DICT constant
(defined in load_section_data.py)\n"""

INVALID_SEMESTER_DICT_ERROR_MESSAGE = """
Semester names must be unique in the current implementation\n"""

class Command(BaseCommand):
    help = "Loads data from distributions/data/*.csv into the Sections model"

    def handle(self, *args, **options):
        if Section.objects.exists():
            return

        for name, ordering in SEMESTER_DICT.items():
            semester = Semester()
            semester.name = name
            semester.ordering = ordering
            semester.save()

        print("Loading section data...\n")
        for path in Path('data').iterdir():
            path_str = str(path).lower()
            if path_str[-4:] != '.csv':
                continue

            print('loading ' + path_str)

            filename = path.parts[-1].split('.')[0]
            year = filename.split('_')[0]
            semester = filename.split('_')[1]

            try:
                semester = Semester.objects.get(name=semester)
            except ObjectDoesNotExist:
                print('invalid semester in csv: ' + path_str)
                print(INVALID_CSV_NAME_ERROR_MESSAGE)
                continue
            except MultipleObjectsReturned:
                print('invalid semester in csv: ' + path_str)
                print(INVALID_SEMESTER_DICT_ERROR_MESSAGE)
                continue

            if year.isdigit():
                year = int(year)
            else:
                print('invalid year in csv: ' + path_str)
                print(INVALID_CSV_NAME_ERROR_MESSAGE)
                continue

            term = Term()
            term.semester = semester
            term.year = year
            term.save()

            table = []
            with open(path, encoding='utf-8-sig') as file:
                for row in DictReader(file):
                    table.append(row)

            for row in table:
                section = Section()

                section.term = term

                section.course, created = Course.objects.get_or_create(
                    department = row['department'],
                    number = row['course_number_1'],
                    title = row['course_title'],
                    hours = row['credit_hours'])

                section.CRN = row['course_ei']
                section.instructor = row['faculty']
                section.average_GPA = row['qca']
                section.As = row['As']
                section.Bs = row['Bs']
                section.Cs = row['Cs']
                section.Ds = row['Ds']
                section.Fs = row['Fs']
                section.withdrawals = row['Textbox10']
                section.class_size = row['number']
                section.save()
        print('done')

