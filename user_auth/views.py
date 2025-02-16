from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from .forms import UserRegistrationForm, UserDeletionForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import logout

# Create your views here.


def user_login(request):
    """
    Render the login page for the user.

    This view is responsible for displaying the login form to the user.
    """
    return render(request, 'authentication/login.html')


def user_logout(request):
    """
    Log the user out of the application.

    This view handles logging out the current authenticated user and
    renders a logout confirmation page.
    """
    logout(request)
    return render(request, 'registration/logout.html')


def authenticate_user(request):
    """
    Authenticate a user using the provided username and password.

    This view checks if the provided credentials (username and password)
    match a user in the database. If the user exists and credentials are
    valid, the user is logged in and redirected to their profile page.
    Otherwise, they are redirected back to the login page.
    """
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    # Redirect back to the login page if authentication fails.
    if user is None:
        return HttpResponseRedirect(reverse('user_auth:login'))
    else:
        # Log the user in and redirect to the user profile page.
        login(request, user)
        return HttpResponseRedirect(reverse('user_auth:show_user'))


def show_user(request):
    """
    Show the logged-in user's details.

    This view displays the logged-in user's username and password.
    It is typically shown after a successful login.
    """
    return render(request, 'authentication/user.html', {
        "username": request.user.username,
        "password": request.user.is_active
        })


def register(request):
    """
    Handle user registration.

    This view handles both displaying the registration form and
    processing the form data when the user submits the registration. If
    the form is valid, a new user is created, and the user is redirected
    to the login page with a success message.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user to the database.

            # Show success message on successful registration.
            messages.success(request, f'Your account has been created.'
                             f' You can log in now!')
            return redirect('user_auth:user_list')
    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'authentication/register.html', context)


def delete_user(request, user_id):
    """
    Delete a user from the system.

    This view is responsible for deleting a user. The user is first retrieved
    by their ID. If the form is submitted and valid, the user is deleted and
    a success message is displayed.
    """
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserDeletionForm(request.POST)
        if form.is_valid():
            form.delete_user(user)
            messages.success(request, "User deleted successfully.")
            return redirect("/")
    else:
        form = UserDeletionForm()  # Empty form for confirmation.
    return render(request, "authentication/delete_user.html",
                  {"form": form, "user": user})


def user_list(request):
    """
    Show a list of all users and their activity status.

    This view retrieves all users from the database and displays them in a list.
    Each user will show their username and whether they are active or not.
    """
    users = User.objects.all()  # Get all users from the User model.
    return render(request, "authentication/user_list.html", {"users": users})


def edit_user(request, user_id):
    """
    Edit a user's status (active/inactive).

    This view allows an admin or authorized user to update the status (active/inactive)
    of a user by modifying their `is_active` field. After updating, the user is redirected
    back to the user list page.
    """
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        is_active = request.POST.get("is_active") == "true"
        user.is_active = is_active
        user.save()
        return redirect("user_auth:user_list")

    return render(request, "authentication/edit_user.html", {"user": user})
