from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Chave_Gerenciador, Perfil

TIPOS_USUARIO = [
    ('normal', 'Usuário Normal'),
    ('supervisor', 'Supervisor'),
    ('gerenciador', 'Gerenciador'),
]

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='E-mail', required=True)
    tipo_usuario = forms.ChoiceField(choices=TIPOS_USUARIO, label='Tipo de usuário')
    chave_acesso = forms.CharField(label='Chave de Acesso', required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'tipo_usuario', 'chave_acesso', 'password1', 'password2')
        labels = {
            'username': 'Nome de usuário',
            'password1': 'Senha',
            'password2': 'Confirmação de senha',
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo_usuario')
        chave = cleaned_data.get('chave_acesso')

        if tipo in ['supervisor', 'gerenciador']:
            if not chave:
                self.add_error('chave_acesso', 'Chave de acesso é obrigatória para esse tipo de usuário.')
            else:
                if not Chave_Gerenciador.objects.filter(chave=chave).exists():
                    self.add_error('chave_acesso', 'Chave de acesso incorreta.')

        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.email = self.cleaned_data['email']
        if commit:
            usuario.save()
            from .models import Perfil  # Evita import circular
            tipo = self.cleaned_data['tipo_usuario']
            Perfil.objects.create(usuario=usuario, tipo=tipo)
        return usuario


class EditarUsuarioForm(forms.ModelForm):
    tipo_usuario = forms.ChoiceField(
        choices=Perfil.TIPOS_USUARIO,
        label="Tipo de Usuário"
    )
    
    class Meta:
        model = User
        fields = ['username', 'email']
    
    def __init__(self, *args, **kwargs):
        perfil = kwargs.pop('perfil', None)
        super().__init__(*args, **kwargs)
        if perfil:
            self.fields['tipo_usuario'].initial = perfil.tipo

