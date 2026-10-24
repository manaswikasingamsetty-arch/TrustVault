
from django import forms
from .models import Document


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["title", "file"]

        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Enter document name",
                "class": "form-input",
            }),
            "file": forms.ClearableFileInput(attrs={
                "accept": ".pdf,.jpg,.jpeg,.png",
                "class": "form-input",
            }),
        }

    def clean_file(self):
        uploaded_file = self.cleaned_data.get("file")

        if not uploaded_file:
            raise forms.ValidationError("Please select a file.")

        allowed_types = [
            "application/pdf",
            "image/jpeg",
            "image/png",
        ]

        if uploaded_file.content_type not in allowed_types:
            raise forms.ValidationError(
                "Only PDF, JPG, JPEG and PNG files are allowed."
            )

        if uploaded_file.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                "File size must be less than 5 MB."
            )

        return uploaded_file
