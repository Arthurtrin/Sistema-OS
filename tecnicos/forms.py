from django import forms
from .models import Tecnico

class TecnicoForm(forms.ModelForm):
    class Meta:
        model = Tecnico
        fields = '__all__'
        widgets = {
            'prc_comissao': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            css_class = 'form-control'
            if self.errors.get(field_name):
                css_class += ' is-invalid'
            
            # campos textareas
            if field_name == 'observacao':
                field.widget.attrs.update({'class': css_class, 'rows': 4})
            elif field_name == 'prc_comissao':
                # já definido no widget NumberInput, só atualiza a classe
                field.widget.attrs.update({'class': css_class})
            else:
                field.widget.attrs.update({'class': css_class})

        # Remove o empty_label padrão do campo 'estado' para forçar seleção
        if 'estado' in self.fields:
            self.fields['estado'].empty_label = None
            self.fields['estado'].required = True
