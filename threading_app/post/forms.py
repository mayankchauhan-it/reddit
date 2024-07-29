from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'attachments', 'category']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'attachments': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_attachments(self):
        attachments = self.cleaned_data.get('attachments')
        if attachments:
            if not attachments.content_type.startswith('image') and not attachments.content_type.startswith('video'):
                raise forms.ValidationError('Only image and video files are allowed.')
        return attachments
