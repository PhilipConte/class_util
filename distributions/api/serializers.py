import decimal
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    SlugRelatedField,
    DecimalField,
    CharField,
)

from distributions.models import Term, Section, Course

class TermSerializer(ModelSerializer):
    semester = CharField(source='semester.name', read_only=True)

    class Meta:
        model = Term
        fields = ['year', 'semester']

class SectionBaseSerializer(ModelSerializer):
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
        ]

class CourseBaseSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='distributions-api:course_detail',
        lookup_field='slug'
    )

    class Meta:
        model = Course
        fields = [
            'department',
            'number',
            'title',
            'hours',
            'url',
        ]

class SectionInstructorSerializer(SectionBaseSerializer):
    class Meta:
        model = Section
        fields = [
            'term',
            'CRN',
            'average_GPA',
            'As',
            'Bs',
            'Cs',
            'Ds',
            'Fs',
            'withdrawals',
            'class_size',
        ]

class SectionSerializer(SectionBaseSerializer):
    course = SlugRelatedField(read_only=True, slug_field='slug')
    class Meta:
        model = Section
        fields = [
            'term',
            'course',
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
        ]

class CourseSerializer(CourseBaseSerializer):
    average_GPA = DecimalField(max_digits=None, decimal_places=2, rounding=decimal.ROUND_HALF_UP)
    As = DecimalField(max_digits=None, decimal_places=2, rounding=decimal.ROUND_HALF_UP)
    Bs = DecimalField(max_digits=None, decimal_places=2, rounding=decimal.ROUND_HALF_UP)
    Cs = DecimalField(max_digits=None, decimal_places=2, rounding=decimal.ROUND_HALF_UP)
    Ds = DecimalField(max_digits=None, decimal_places=2, rounding=decimal.ROUND_HALF_UP)
    Fs = DecimalField(max_digits=None, decimal_places=2, rounding=decimal.ROUND_HALF_UP)
    sections = SlugRelatedField(many=True, read_only=True, slug_field='slug')

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
            'sections',
            'url',
        ]
