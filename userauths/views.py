from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from userauths.forms import UserRegisterForm
from userauths.models import User, Profile

def RegisterView(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in.")
        return redirect('/')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=True)
            full_name = form.cleaned_data['full_name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            new_user = authenticate(email=email, password=password)
            login(request, new_user)

            messages.success(request, f"New account created for {full_name} successfully.")

            try:
                profile = Profile.objects.get(user=new_user)
            except Profile.DoesNotExist:
                profile = Profile.objects.create(user=new_user)
            profile.full_name = full_name
            profile.phone = phone
            profile.save()

            return redirect('hotel:index')

    else:
        form =  UserRegisterForm()

    context = {'form': form}
    return render(request, "userauths/sign-up.html", context)

def LoginView(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in.")
        return redirect('hotel:index')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_query = User.objects.get(email=email)
            user_auth = authenticate(request, email=email, password=password)

            if user_query is not None:
                login(request, user_auth)
                messages.success(request, f"Logged in successfully.")
                next_url = request.GET.get("next", "hotel:index")
                return redirect(next_url)
            else:
                messages.error(request, "Username or Password does not exist.")
                return redirect("hotel:index")
                
        except User.DoesNotExist:
            messages.warning(request, f'User does not exist. Create an account.')
            return redirect("userauths:sign-in")

    return render(request, 'userauths/sign-in.html')

def LogoutView(request):

    logout(request)
    messages.info(request, "You have been logged out.") 

    return redirect('userauths:sign-in')
