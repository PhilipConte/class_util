from pathlib import Path
from csv import DictReader
from django.core.management import BaseCommand
from distributions.models import Term, Course, Section

ALREADY_LOADED_ERROR_MESSAGE = """
If you need to reload the section data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables\n"""

INVALID_CSV_NAME_ERROR_MESSAGE = """
CSVs must be in the format [fall/spring]YYYY.csv
eg: fall 2018 would be fall2018.csv
non-fall/spring semesters are not supported at this time\n"""

class Command(BaseCommand):
    help = "Loads data from distributions/data/*.csv into the Sections model"

    def handle(self, *args, **options):
        if Section.objects.exists():
            print('Section data already loaded...exiting.')
            print(ALREADY_LOADED_ERROR_MESSAGE)
            return

        duplicates = 0
        print("Loading section data...\n")
        for path in Path('distributions/data').iterdir():
            path_str = str(path).lower()
            if path_str[-4:] != '.csv':
                continue

            filename = path.parts[-1].split('.')[0]
            semester = filename[:-4]
            year = filename[-4:]
            if semester not in ['fall', 'spring']:
                print('invalid semester in csv: ' + path_str)
                print(INVALID_CSV_NAME_ERROR_MESSAGE)
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
