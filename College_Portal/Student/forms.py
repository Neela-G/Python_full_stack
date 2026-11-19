from django import forms
class Student_form_data(forms.form):
    reg_no1=forms.IntegerField()
    name1=forms.CharField()
    email1=forms.EmailField()
