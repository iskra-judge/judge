from django import forms


class CodeTaskFilterForm(forms.Form):
    def __init__(self, categories, difficulties, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'].choices = [(category.id, category.name) for category in categories]
        self.fields['difficulties'].choices = [(difficulty.id, difficulty.name) for difficulty in difficulties]

    categories = forms.ChoiceField(
        choices=(),
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )

    difficulties = forms.ChoiceField(
        choices=(),
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )
