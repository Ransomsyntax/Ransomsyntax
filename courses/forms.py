from django import forms
from .models import Enquiry, Video, Course


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['name', 'email', 'phone', 'course_interested', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'course_interested': forms.Select(attrs={'class': 'form-select'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell us what you would like to learn...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course_interested'].queryset = Course.objects.filter(is_active=True)
        self.fields['course_interested'].required = False


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['course', 'title', 'description', 'video_file', 'external_url', 'is_free', 'order']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Video Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short description'}),
            'video_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'external_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://youtube.com/... (optional)'}),
            'is_free': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        if teacher is not None:
            self.fields['course'].queryset = Course.objects.filter(teachers=teacher, is_active=True)

    def clean(self):
        cleaned_data = super().clean()
        video_file = cleaned_data.get('video_file')
        external_url = cleaned_data.get('external_url')
        if not video_file and not external_url:
            raise forms.ValidationError("Please either upload a video file or provide an external video URL.")
        return cleaned_data


class StudentAssignForm(forms.Form):
    """Used by a teacher to grant ('unlock') a student's access to one of their own courses."""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student username'})
    )
