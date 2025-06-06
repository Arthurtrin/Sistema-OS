# usuarios/validators.py
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import MinimumLengthValidator

class MeuMinimumLengthValidator(MinimumLengthValidator):
    def __init__(self, min_length=8):
        super().__init__(min_length=min_length)
    
    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("Esta senha é muito curta. Ela deve conter pelo menos %(min_length)d caracteres."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )
    
    def get_help_text(self):
        return _("Sua senha deve conter pelo menos %(min_length)d caracteres.") % {'min_length': self.min_length}
