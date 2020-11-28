from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('create/', views.UserRegisterView.as_view(), name="create"),
    path('', views.IndexView.as_view(), name="index"),
    path('agreement/', views.AgreementView.as_view(), name="agreement"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('recovery/email/', views.RecoveryEmailView.as_view(), name="recovery_email"),
    path('profile/password/', views.password_edit_view, name='password_edit'),
    path('profile/', views.profile_view, name="profile"),
    path('profile/delete/', views.profile_delete_view, name="delete")

]