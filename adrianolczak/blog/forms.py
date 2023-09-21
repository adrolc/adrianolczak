from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=25,
        label="Search",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "query_input",
                "type": "search",
            }
        ),
    )
