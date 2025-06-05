from django import forms
from .models import Cliente, Segmento, Atividade

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'data_inclusao': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            css_class = 'form-control'
            if self.errors.get(field_name):
                css_class += ' is-invalid'
            if field_name == 'observacao':
                field.widget.attrs.update({'class': css_class, 'rows': 4})
            elif field_name != 'data_inclusao':
                field.widget.attrs.update({'class': css_class})

        # Remove o empty_label padrão
        self.fields['segmento'].empty_label = None
        self.fields['atividade'].empty_label = None

        # Adiciona o atributo required para forçar validação se quiser
        self.fields['segmento'].required = False
        self.fields['atividade'].required = False


class SegmentoForm(forms.ModelForm):
    class Meta:
        model = Segmento
        fields = ['nome']

class AtividadeForm(forms.ModelForm):
    class Meta:
        model = Atividade
        fields = ['nome']