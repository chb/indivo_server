from django import forms
#from django.forms.widgets import RadioFieldRenderer
#from django.utils.safestring import mark_safe
#from django.utils.encoding import force_unicode

#class IndivoRadioFieldRenderer(RadioFieldRenderer):
#    """
#    Extend RadioFieldRenderer to provide a custom renderer
#    """
#    def render(self):
#        """Outputs a <ul> for this set of radio fields."""
#        return mark_safe(u'<ul class="inputs-list">\n%s\n</ul>' % u'\n'.join([u'<li>%s</li>'
#                % force_unicode(w) for w in self]))

class RecordForm(forms.Form):
    full_name = forms.CharField()
    email = forms.EmailField()
    street_address = forms.CharField()
    postal_code = forms.CharField()
    country = forms.CharField(initial='USA')
    phone_number = forms.CharField(required=False)

class AccountForm(forms.Form):
    RADIO_CHOICES = (
        ('owner', "Owner"),
        ('fullShare', "Full Share"),
    )
    full_name = forms.CharField()
    email = forms.EmailField()
    #share_type = forms.ChoiceField(choices=RADIO_CHOICES, widget=forms.RadioSelect(renderer=IndivoRadioFieldRenderer))
