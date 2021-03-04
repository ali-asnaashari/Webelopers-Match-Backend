from django import forms


class ContactUsForm(forms.Form):
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'title'}))
    email = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'email'}))
    text = forms.CharField(required=True, min_length=10, max_length=250, widget=forms.Textarea(attrs={'id': 'text'}))

    class Meta:
        # model = User
        fields = ('title', 'email', 'text')
