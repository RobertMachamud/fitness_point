from django import forms
from .models import Offer, Category


class OfferForm(forms.ModelForm):

    class Meta:
        model = Offer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        user_friendly = [
            (c.id, c.get_user_friendly_name()) for c in categories]

        self.fields['category'].choices = user_friendly
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
            # !!!
