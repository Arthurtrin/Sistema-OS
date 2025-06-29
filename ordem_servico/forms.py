from django import forms
from .models import OrdemServico, Segmento, Status, Unidade, ProdutoOrdemServico

class ProdutoOrdemServicoForm(forms.ModelForm):
    class Meta:
        model = ProdutoOrdemServico
        fields = ['produto', 'quantidade', 'baixa']
        widgets = {
            'baixa': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Esconde o campo baixa para ser manipulado via JS e campo hidden
        self.fields['baixa'].widget = forms.HiddenInput()

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                css_class = 'form-control'
                if self.errors.get(field_name):
                    css_class += ' is-invalid'
                field.widget.attrs.update({'class': css_class})

        if 'DELETE' in self.fields:
            self.fields['DELETE'].widget.attrs.update({'style': 'display:none;'})

class OrdemServicoForm(forms.ModelForm):
    data_abertura = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d']
    )

    obra_inicio = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d']
    )

    obra_termino = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = OrdemServico
        fields = '__all__'
        widgets = {
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'arquivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            css_class = 'form-control'
            if self.errors.get(field_name):
                css_class += ' is-invalid'
            
            # já tratados no widgets do Meta
            if field_name in ['data_abertura', 'obra_inicio', 'obra_termino', 'descricao', 'arquivo']:
                continue

            field.widget.attrs.update({'class': css_class})



class SegmentoForm(forms.ModelForm):
    class Meta:
        model = Segmento
        fields = ['nome']

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['nome']

class UnidadeForm(forms.ModelForm):
    class Meta:
        model = Unidade
        fields = ['nome']

