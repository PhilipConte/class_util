import decimal
from rest_framework.serializers import ModelSerializer, DecimalField, CharField, IntegerField
from distributions.models import Term, Section, Course


class TermSerializer(ModelSerializer):
    semester = CharField(source='semester.name', read_only=True)

    class Meta:
        model = Term
        fields = ['year', 'semester']


class GroupedSectionSerializer(ModelSerializer):
    sections_taught = IntegerField()

    class Meta:
        model = Section
        fields = [
            'instructor',
            'sections_taught',
            'withdrawals',
            'average_GPA',
            'As',
            'Bs',
            'Cs',
            'Ds',
            'Fs',
        ]


class SectionSerializer(ModelSerializer):
    term = TermSerializer()

    class Meta:
        model = Section
        fields = [
            'term',
            'CRN',
            'instructor',
            'average_GPA',
            'As',
            'Bs',
            'Cs',
            'Ds',
            'Fs',
            'withdrawals',
            'class_size',
            'slug',
        ]

class CourseSerializer(ModelSerializer):
    average_GPA = DecimalField(max_digits=None, decimal_places=2, rounding=decimal.ROUND_HALF_UP)
    As = DecimalField(max_digits=None, decimal_places=2, rounding=decimal.ROUND_HALF_UP)
    Bs = DecimalField(max_digits=None, decimal_places=2, rounding=decimal.ROUND_HALF_UP)
    Cs = DecimalField(max_digits=None, decimal_places=2, rounding=decimal.ROUND_HALF_UP)
    Ds = DecimalField(max_digits=None, decimal_places=2, rounding=decimal.ROUND_HALF_UP)
    Fs = DecimalField(max_digits=None, decimal_places=2, rounding=decimal.ROUND_HALF_UP)

    class Meta:
        model = Course
        fields = [
            'department',
            'number',
            'title',
            'hours',
            'average_GPA',
            'As',
            'Bs',
            'Cs',
            'Ds',
            'Fs',
            'slug',
        ]
