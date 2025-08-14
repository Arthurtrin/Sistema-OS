from django.shortcuts import render

# Create your views here.
def principal(request):
    return render(request, 'financeiro/principal.html')