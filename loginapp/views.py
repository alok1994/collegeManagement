from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'loginapp/login.html'  # Create this template later
