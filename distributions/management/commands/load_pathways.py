import json
from pathlib import Path
from django.core.management import BaseCommand
from distributions.models import Course, Pathway

PATHWAY_DICT = {
    'AR01': ['CLE Area 1', 'Writing and Discourse'],
    'AR02': ['CLE Area 2', 'Ideas, Cultural, Traditions, and Values'],
    'AR03': ['CLE Area 3', 'Society and Human Behavior'],
    'AR04': ['CLE Area 4', 'Scientific Reasoning and Discovery'],
    'AR05': ['CLE Area 5', 'Quantitative and Symbolic Reasoning'],
    'AR06': ['CLE Area 6', 'Creativity and Aesthetic Experience'],
    'AR07': ['CLE Area 7', 'Critical Issues in a Global Context '],
    'G01A': ['Pathway 1a', 'Advanced/Applied Discourse'],
    'G01F': ['Pathway 1f', 'Foundational Discourse'],
    'G02': ['Pathway 2', 'Critical Thinking in the Humanities'],
    'G03': ['Pathway 3', 'Reasoning in the Social Sciences'],
    'G04': ['Pathway 4', 'Reasoning in the Natural Sciences'],
    'G05A': ['Pathway 5a', 'Advanced/Applied Quantitative and Computational Thinking'],
    'G05F': ['Pathway 5f', 'Foundational Quantitative and Computational Thinking'],
    'G06A': ['Pathway 6a', 'Critique and Practice in the Arts'],
    'G06D': ['Pathway 6d', 'Critique and Practice in Design'],
    'G07': ['Pathway 7', 'Critical Analysis of Equity and Identity in the United States']
}

class Command(BaseCommand):
    help = "Annotates Courses with Pathways areas"

    def handle(self, *args, **options):
        if Pathway.objects.exists() or not Path('/data/areas.json').is_file():
            return

        with open(Path('/data/areas.json'), 'r') as f:
            data = json.load(f)

            print("Loading pathways...")
            for path_key, arr in PATHWAY_DICT.items():
                pathway = Pathway()
                pathway.name = arr[0]
                pathway.description = arr[1]
                pathway.save()

                for string in data[path_key]:
                    parts, title = string.split('|')[:2]
                    department, number = parts.split(' ')

                    if not number.isnumeric():
                        print('Could not add {} {}: non-numeric number'.format(
                            department, number
                        ))
                        continue

                    courses = Course.objects.filter(
                        department=department,
                        number=number
                    )
                    if not courses.exists():
                        print('No course found for {} {}: {}'.format(
                            department, number, title
                        ))
                        continue

                    pathway.courses.add(*list(courses))
        print('done')
