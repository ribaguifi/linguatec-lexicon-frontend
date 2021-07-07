from django import forms


class ConjugatorForm(forms.Form):
    GRAFIA_CHOICES = (
        ('DGPL', 'DGPL 2017'),
        ('EFA', 'EFA 2010'),
        ('SLA', 'SLA 2006'),
        ('CFA', 'CFA 1987')
    )
    REMATANZA_CHOICES = (
        ('au', '-au / -iu'),
        ('ato', '-ato / -ito')
    )
    PASAUS_CHOICES = (
        ('sintetico', 'Sintético'),
        ('perifrastico', 'Perifrástico'),
        ('sintetico_y_perifrastico', 'Sintético y perifrástico')
    )
    PRIM_PERS_PLURAL_CHOICES = (
        ('completa', 'completa (rematada en -os)'),
        ('apocopada', 'apocopada (no rematada en -os)')
    )
    CHERUNDIO_CHOICES = (
        ('completa', 'completa (rematada en -o)'),
        ('apocopada', 'apocopada (no rematada en -o)')
    )

    grafia = forms.ChoiceField(
        label="Grafía", choices=GRAFIA_CHOICES, widget=forms.RadioSelect
    )
    participio = forms.ChoiceField(
        label="Rematanza d'os participios", choices=REMATANZA_CHOICES, widget=forms.RadioSelect
    )
    tiempo_pasau = forms.ChoiceField(
        label="Tiempos d'os pasaus perfecto simple y anterior", choices=PASAUS_CHOICES, widget=forms.RadioSelect
    )
    primer_plural = forms.ChoiceField(
        label="Forma d'a primer persona plural", choices=PRIM_PERS_PLURAL_CHOICES, widget=forms.RadioSelect
    )
    cherundio = forms.ChoiceField(
        label="Forma d'o cherundio", choices=CHERUNDIO_CHOICES, widget=forms.RadioSelect
    )
    auxiliar_ser = forms.BooleanField(label="Conchugar con o verbo estar como auxiliar si ye posible")
    incoativo = forms.BooleanField(label="Conchugar con a forma incoativa si ye posible")

