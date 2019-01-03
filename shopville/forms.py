from django import forms

# Register your forms here
from shopville.models import Buyer


class NewBuyerForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = "__all__"
