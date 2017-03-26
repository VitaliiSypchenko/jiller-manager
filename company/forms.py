from django import forms

from company.models import Company


class CreateCompanyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateCompanyForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_name(self):
        cleaned_data = super(CreateCompanyForm, self).clean()
        name = cleaned_data.get('name')
        if not name.isalpha():
            raise forms.ValidationError(
                'Only letters are allowed')
        return name

    class Meta:
        model = Company
        fields = ['name']


