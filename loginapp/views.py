from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import render,redirect 
from django.contrib.auth import login, authenticate

class CustomLoginView(LoginView):
    template_name = 'loginapp/login.html'  # Create this template later

    def get_success_url(self):
        return '/dashboard/' 

def logout_view(request):
    # Perform logout logic here
    logout(request)
    # Redirect to the logout success page or render a template
    return render(request, 'loginapp/logout.html')

'''def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to your dashboard or another page
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')

    return render(request, 'loginapp/login.html')'''