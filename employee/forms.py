from django.forms import ModelForm
from employee.models import Employee, Checkin, Query


class AddForm(ModelForm):
   class Meta:
        model = Employee
        fields = ['name', 'birthDay', 'homeTown', 'phone', 'gender', 'educationLevel','avatar']

   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs.update({"id":"imgInp", "type":"file", "onchange":"previewFile(this);","required":True})



class SearchForm(ModelForm):
     class Meta:
          model = Query
          fields = ['avatar',]

     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields['avatar'].widget.attrs.update({"id":"imgQuery", "type":"file", "onchange":"previewFile(this);","required":True})