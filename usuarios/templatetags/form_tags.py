from django import template

register = template.Library()

@register.filter(name='adicionar_classe')
def adicionar_classe(campo, classe_css):
    return campo.as_widget(attrs={"class": classe_css})