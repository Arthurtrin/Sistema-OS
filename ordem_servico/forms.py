from django import forms
from .models import OrdemServico, Segmento, Status, Unidade, ProdutoOrdemServico

class ProdutoOrdemServicoForm(forms.ModelForm):
    dar_baixa = forms.BooleanField(required=False, initial=False, label='Dar baixa no estoque')
    
    class Meta:
        model = ProdutoOrdemServico
        fields = ['produto', 'quantidade', 'dar_baixa']  # Inclua o dar_baixa aqui

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            css_class = 'form-control'
            if self.errors.get(field_name):
                css_class += ' is-invalid'

            # Para checkbox, normalmente a classe é 'form-check-input', então ajuste:
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': css_class})

        if 'DELETE' in self.fields:
            self.fields['DELETE'].widget.attrs.update({'style': 'display:none;'})

class OrdemServicoForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        fields = '__all__'
        widgets = {
            'data_abertura': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'obra_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'obra_termino': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
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

