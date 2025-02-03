from django import forms
from .models import Topic, Slide

class TopicWithSlidesForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['class_obj', 'title', 'description']

class SlideFormSet(forms.ModelForm):
    class Meta:
        model = Slide
        fields = ['title', 'content', 'image', 'video', 'order']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }
