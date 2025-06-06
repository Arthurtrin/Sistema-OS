# usuarios/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login_root'),
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('senha/resetar/', auth_views.PasswordResetView.as_view(template_name='usuarios/senha_reset.html'), name='password_reset'),
    path('senha/enviado/', auth_views.PasswordResetDoneView.as_view(template_name='usuarios/senha_enviada.html'), name='password_reset_done'),
    path('senha/confirmar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='usuarios/senha_confirmar.html'), name='password_reset_confirm'),
    path('senha/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='usuarios/senha_completa.html'), name='password_reset_complete'),
    path('editar_usuario/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('excluir_usuario/<int:id>/', views.excluir_usuario, name='excluir_usuario'),
]