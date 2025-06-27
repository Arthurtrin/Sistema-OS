from django import forms
from .models import OrdemServico, Segmento, Status, Unidade

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