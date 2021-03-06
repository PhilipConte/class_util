import itertools

from django.db.models import Q
from django import forms
from .models import Course, Section, Pathway
from django_filters import rest_framework as filters

def form_control(placeholder):
    return forms.TextInput(attrs={'placeholder': placeholder, 'class': 'form-control'})

class CourseFilter(filters.FilterSet):
    average_GPA = filters.NumberFilter(field_name='average_GPA', label='Average GPA ≥', lookup_expr='gte')
    pathways = filters.ModelChoiceFilter(queryset=Pathway.objects.all())

    class Meta:
        model = Course
        fields = {
            'department': ['iexact'],
            'number': ['gt', 'lt'],
            'title': ['icontains'],
            'hours': ['exact'],
        }

class GroupedSectionFilter(filters.FilterSet):
    instructor = filters.CharFilter(
        field_name='instructor',
        label='',
        lookup_expr='icontains',
        widget= form_control('filter by instructor...')
    )


class CourseFilterMulti(filters.FilterSet):
    multi = filters.CharFilter(
        label='',
        method='filter_multi',
        widget= form_control('search all courses...')
    )
    search_fields = ['department', 'number', 'title']

    def filter_multi(self, qs, name, value):
        if value:
            q_parts = value.split()
            q_totals = Q()

            combinatorics = itertools.product([True, False], repeat=len(q_parts) - 1)
            possibilities = []
            for combination in combinatorics:
                i = 0
                one_such_combination = [q_parts[i]]
                for slab in combination:
                    i += 1
                    if not slab: # there is a join
                        one_such_combination[-1] += ' ' + q_parts[i]
                    else:
                        one_such_combination += [q_parts[i]]
                possibilities.append(one_such_combination)

            for p in possibilities:
                list1=self.search_fields
                list2=p
                perms = [zip(x,list2) for x in itertools.permutations(list1,len(list2))]

                for perm in perms:
                    q_part = Q()
                    for p in perm:
                        q_part = q_part & Q(**{p[0]+'__icontains': p[1]})
                    q_totals = q_totals | q_part

            qs = qs.filter(q_totals)

        return qs

    class Meta:
        model = Course
        fields = ['multi']
