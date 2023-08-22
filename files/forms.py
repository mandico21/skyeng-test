from django.forms import ModelForm

from files.models import FileUpload


class FileForm(ModelForm):
    class Meta:
        model = FileUpload
        fields = ['filename', 'file']
