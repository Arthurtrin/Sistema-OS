from django import forms
from .models import Cliente, Segmento, Atividade

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'data_inclusao': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'  # <- formato ISO para <input type="date">
            ),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            css_class = 'form-control'
            if self.errors.get(field_name):
                css_class += ' is-invalid'
                
            if field.widget.__class__.__name__ == 'Select':
                class_attr = 'form-select'
                if 'is-invalid' in css_class:
                    class_attr += ' is-invalid'
                field.widget.attrs.update({'class': class_attr})
            else:
                if field_name == 'observacao':
                    field.widget.attrs.update({'class': css_class, 'rows': 4})
                elif field_name != 'data_inclusao':
                    field.widget.attrs.update({'class': css_class})

        self.fields['data_inclusao'].input_formats = ['%Y-%m-%d']
        self.fields['segmento'].empty_label = 'Selecione o Segmento'
        self.fields['atividade'].empty_label = 'Selecione a Atividade'
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
