from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField

from distributions.models import Term, Section, Course

class TermSerializer(ModelSerializer):
    semester = SerializerMethodField()

    class Meta:
        model = Term
        fields = [
            'year',
            'semester',
        ]
    
    def get_semester(self, obj):
        return obj.semester.name

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

class SectionSerializer(SectionBaseSerializer):
    course = CourseBaseSerializer()

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
    average_GPA = SerializerMethodField()
    As = SerializerMethodField()
    Bs = SerializerMethodField()
    Cs = SerializerMethodField()
    Ds = SerializerMethodField()
    Fs = SerializerMethodField()
    sections = SectionBaseSerializer(many=True, read_only=True)

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

    def get_average_GPA(self, obj):
        return round(obj.average_GPA, 2)

    def get_As(self, obj):
        return round(obj.As, 1)
    
    def get_Bs(self, obj):
        return round(obj.Bs, 1)

    def get_Cs(self, obj):
        return round(obj.Cs, 1)
    
    def get_Ds(self, obj):
        return round(obj.Ds, 1)

    def get_Fs(self, obj):
        return round(obj.Fs, 1)
