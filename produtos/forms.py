from django import forms
from .models import Produto, Marca, Fabricante, Grupo, TipoEntrada, TipoSaida

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'
        widgets = {
            'data_ultima_compra': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'situacao': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            css_class = 'form-control'
            if self.errors.get(field_name):
                css_class += ' is-invalid'

            # Campos tipo select
            if field.widget.__class__.__name__ == 'Select':
                field.widget.attrs.update({'class': 'form-select'})
            elif field_name == 'descricao':
                field.widget.attrs.update({'class': css_class, 'rows': 4})
            elif field_name != 'data_ultima_compra':
                field.widget.attrs.update({'class': css_class})

        # Defina se quer tornar algum desses campos não obrigatórios
        self.fields['grupo'].required = False
        self.fields['fabricante'].required = False
        self.fields['marca'].required = False

class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nome']

class FabricanteForm(forms.ModelForm):
    class Meta:
        model = Fabricante
        fields = ['nome']

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['nome']


class TipoEntradaForm(forms.ModelForm):
    class Meta:
        model = TipoEntrada
        fields = ['nome']

class TipoSaidaForm(forms.ModelForm):
    class Meta:
        model = TipoSaida
        fields = ['nome']