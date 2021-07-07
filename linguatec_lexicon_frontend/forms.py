from django import forms


class ConjugatorForm(forms.Form):
    GRAFIA_CHOICES = (
        ('dgpl_2017', 'DGPL 2017'),
        ('efa_2010', 'EFA 2010'),
        ('sla_2006', 'SLA 2006'),
        ('cfa_1987', 'CFA 1987')
    )
    REMATANZA_CHOICES = (
        ('au_iu', '-au / -iu'),
        ('ato_ito', '-ato / -ito')
    )
    PASAUS_CHOICES = (
        ('sintetico', 'Sintético'),
        ('perifrastico', 'Perifrástico'),
        ('sint_perif', 'Sintético y perifrástico')
    )
    PRIM_PERS_PLURAL_CHOICES = (
        ('completa', 'completa (rematada en -os)'),
        ('apocapada', 'apocopada (no rematada en -os)')
    )
    CHERUNDIO_CHOICES = (
        ('completa', 'completa (rematada en -o)'),
        ('apocapada', 'apocopada (no rematada en -o)')
    )

    grafia = forms.ChoiceField(
        label="Grafía", choices=GRAFIA_CHOICES, widget=forms.RadioSelect
    )
    rematanza = forms.ChoiceField(
        label="Rematanza d'os participios", choices=REMATANZA_CHOICES, widget=forms.RadioSelect
    )
    pasaus = forms.ChoiceField(
        label="Tiempos d'os pasaus perfecto simple y anterior", choices=PASAUS_CHOICES, widget=forms.RadioSelect
    )
    prim_pers_plural = forms.ChoiceField(
        label="Forma d'a primer persona plural", choices=PRIM_PERS_PLURAL_CHOICES, widget=forms.RadioSelect
    )
    cherundio = forms.ChoiceField(
        label="Forma d'o cherundio", choices=CHERUNDIO_CHOICES, widget=forms.RadioSelect
    )
    estar_auxiliar = forms.BooleanField(label="Conchugar con o verbo estar como auxiliar si ye posible")
    incoativa = forms.BooleanField(label="Conchugar con a forma incoativa si ye posible")

