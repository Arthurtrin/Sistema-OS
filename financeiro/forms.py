from django import forms
from .models import Empresa, ContasReceber

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            # Se for checkbox
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                css_class = 'form-control'
                if self.errors.get(field_name):
                    css_class += ' is-invalid'
                field.widget.attrs.update({'class': css_class})

            # Se for Select, adiciona também a classe form-select sem remover as outras
            if isinstance(field.widget, forms.Select):
                current_classes = field.widget.attrs.get('class', '')
                field.widget.attrs.update({'class': f'{current_classes} form-select'})
