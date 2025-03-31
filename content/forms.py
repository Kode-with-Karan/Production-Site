from django import forms
from .models import Content, Collaborate, PromotedContent
from django.utils import timezone
from datetime import timedelta

class ContentUploadForm(forms.ModelForm):
    promote = forms.BooleanField(required=False, label="Promote this content?")
    # promotion_days = forms.ChoiceField(
    #     choices=[(1, "1 Day - $5"), (3, "3 Days - $12"), (7, "7 Days - $25")],
    #     required=False,
    #     label="Promotion Duration"
    # )
    promotion_duration = forms.ChoiceField(
        choices=[(1, "1 Day - $5"), (3, "3 Days - $12"), (7, "7 Days - $25")],
        required=False,
        label="Promotion Duration"
    )


    class Meta:
        model = Content
        fields = ['title', 'country', 'duration', 'genre','age_rating', 'cast', 'description', 'content_type', 'file', 'thumbnail', 'promote', 'promotion_duration']
    
    country = forms.CharField(required=False) 
    duration = forms.CharField(required=False) 
    genre = forms.CharField(required=False) 
    cast = forms.CharField(widget=forms.Textarea, required=False)

    def save(self, commit=True, user=None):
        content = super().save(commit=False)
        if commit:
            content.save()
            if self.cleaned_data.get("promote"):
                days = int(self.cleaned_data.get("promotion_days"))
                PromotedContent.objects.create(
                    creator=user,
                    content=content,
                    promotion_end=timezone.now() + timedelta(days=days),
                    amount_paid=days * 5,  # Example: $5 per day
                )
        return content
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('promote') and not cleaned_data.get('promotion_duration'):
            raise forms.ValidationError("Please select a promotion duration.")
        return cleaned_data

# class ContentImageForm(forms.ModelForm):
#     images = forms.FileField(required=False)

class CollaborateUploadForm(forms.ModelForm):
    class Meta:
        model = Collaborate
        fields = ['name', 'email', 'idea_description', 'content_type']
