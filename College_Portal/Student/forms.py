from django import forms

class Student_form_data(forms.Form):
    reg_no1 = forms.IntegerField(label="Register Number")
    name1 = forms.CharField(max_length=100, label="Student Name")
    email1 = forms.EmailField(label="Email")
    marks1 = forms.DecimalField(max_digits=6, decimal_places=2, label="Marks")
    dob1 = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={'type': 'date'})
    )