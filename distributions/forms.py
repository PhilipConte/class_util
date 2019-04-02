from django import forms

css_classes = 'form-control bulk-input'

class CSSForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update({'class': css_classes})
