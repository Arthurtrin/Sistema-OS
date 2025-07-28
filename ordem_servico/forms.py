from django import forms
from .models import OrdemServico, Segmento, Status, Unidade, ProdutoOrdemServico, ServicoOrdemServico


class ServicoOrdemServicoForm(forms.ModelForm):
    class Meta:
        model = ServicoOrdemServico
        fields = [
            'servico',
            'profissional',
            'preco_unitario',
            'preco_total',
            'comissao',
            'comissao_total',
            'quantidade'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            # Aplicar classe para checkboxes (não temos no seu caso)
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                css_class = 'form-control'
                if self.errors.get(field_name):
                    css_class += ' is-invalid'
                field.widget.attrs.update({'class': css_class})

            # Campos Select estilizados
            if field.widget.__class__.__name__ == 'Select':
                field.widget.attrs.update({'class': 'form-select'})

        # Placeholders opcionais
        self.fields['servico'].empty_label = 'Selecione o Serviço'
        self.fields['profissional'].empty_label = 'Selecione o Profissional'

class ProdutoOrdemServicoForm(forms.ModelForm):
    class Meta:
        model = ProdutoOrdemServico
        fields = ['produto', 'quantidade']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ == 'Select':
                field.widget.attrs.update({'class': 'form-select'})

        self.fields['produto'].empty_label = 'Selecione o Produto'
        
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
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = OrdemServico
        exclude = ['digitador']
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
            
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ == 'Select':
                field.widget.attrs.update({'class': 'form-select'})

        self.fields['status'].empty_label = 'Selecione o Status'
        self.fields['n_cliente'].empty_label = 'Selecione o Cliente'
        self.fields['unidade'].empty_label = 'Selecione a Unidade'
        self.fields['segmento'].empty_label = 'Selecione o Segmento'

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

