from django import forms
from django.core.validators import RegexValidator

from .models import ClientEnquiry

phone_validator = RegexValidator(
    regex=r"^[0-9+()\-\s]{7,20}$",
    message="Enter a valid phone number (digits, spaces, +, -, and () only).",
)


class ClientEnquiryForm(forms.ModelForm):
    """Public-facing enquiry / lead form.

    Field-level validation is deliberately strict enough to keep the lead
    list clean, but every field except contact essentials stays optional
    so the form doesn't turn away a genuine enquiry.
    """

    phone = forms.CharField(
        required=False,
        validators=[phone_validator],
        widget=forms.TextInput(
            attrs={"placeholder": "+91 98765 43210", "class": "form-control"}
        ),
    )

    class Meta:
        model = ClientEnquiry
        fields = [
            "name",
            "company",
            "email",
            "phone",
            "service_required",
            "budget",
            "project_description",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Your full name", "class": "form-control"}
            ),
            "company": forms.TextInput(
                attrs={"placeholder": "Company (optional)", "class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "you@company.com", "class": "form-control"}
            ),
            "service_required": forms.Select(attrs={"class": "form-select"}),
            "budget": forms.Select(attrs={"class": "form-select"}),
            "project_description": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Tell us briefly about your project, goals, and timeline...",
                    "class": "form-control",
                }
            ),
        }
        labels = {
            "project_description": "Project description",
            "service_required": "Service required",
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter your full name.")
        return name

    def clean_project_description(self):
        description = self.cleaned_data["project_description"].strip()
        if len(description) < 20:
            raise forms.ValidationError(
                "Please add a few more details (at least 20 characters) so we can "
                "understand your project."
            )
        return description
