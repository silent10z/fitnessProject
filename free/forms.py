from django import forms
from django_summernote.widgets import SummernoteWidget

from .models import Free

# 새글쓰기 폼
class FreeWriterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FreeWriterForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = '제목'
        self.fields['title'].widget.attrs.update({
            'placeholder': '제목을 입력해주세요.',
            'class': 'form-control',
            'autfocus': 'True',
        })


    class Meta:
        model = Free
        fields = ['title', 'content', 'top_fixed', 'upload_files']
        widgets = {
            'content': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}),
        }
