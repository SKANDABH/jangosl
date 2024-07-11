
from .forms import LoginForm
from django.shortcuts import render, redirect
from .forms import PatientSignUpForm, DoctorSignUpForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import PatientSignUpForm, DoctorSignUpForm, LoginForm


def patient_signup(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to patient dashboard
            return redirect('patient_dashboard')
    else:
        form = PatientSignUpForm()
    return render(request, 'patient_signup.html', {'form': form})


def doctor_signup(request):
    if request.method == 'POST':
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Redirect to doctor dashboard
            return redirect('doctor_dashboard', username=username)
    else:
        form = DoctorSignUpForm()
    return render(request, 'doctor_signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        # print("hi")

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print("hi")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                print("hi")
                login(request, user)
                if user.is_patient:
                    return redirect('patient_dashboard', username=username)
                elif user.is_doctor:
                    return redirect('doctor_dashboard', username=username)
                else:
                    # Redirect to login page if not patient or doctor
                    return redirect('login')
            else:
                print(f"Authentication failed for user: {username}")
                form.add_error(None, 'Invalid username or password')

    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def patient_dashboard(request, username):
    return render(request, 'patient_dashboard.html', {'username': username, 'user': request.user})


def doctor_dashboard(request, username):
    return render(request, 'doctor_dashboard.html', {'username': username, 'user': request.user})
