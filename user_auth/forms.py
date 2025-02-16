from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    """
    A form for registering a new user with additional fields for first
    name, last name, and email. Inherits from Django's built-in
    UserCreationForm to handle user authentication and password fields.

    Fields:
        - first_name: The user's first name.
        - last_name: The user's last name.
        - email: The user's email address.
    """
    # Additional fields for first and last name, and email.
    first_name = forms.CharField(max_length=101)
    last_name = forms.CharField(max_length=101)
    email = forms.EmailField()

    class Meta:
        """
        The Meta class specifies the model and fields that the form will
        handle.

        The form will work with the 'User' model, handling the fields:
            - username
            - first_name
            - last_name
            - email
            - password1 (password field for user creation)
            - password2 (password confirmation field)
        """
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1',
                  'password2']


class UserDeletionForm(forms.ModelForm):
    """
    A form to confirm the deletion of a user account. It contains a
    checkbox to confirm that the user wants to delete their account.
    """
    # Boolean field to confirm the deletion action.
    confirm = forms.BooleanField(label='Delete User')

    class Meta:
        """
        The Meta class defines the model being used. This form uses the
        'User' model, but no fields will be displayed because only the
        'confirm' field is required.
        """
        model = User
        fields = []

    def delete_user(self, user):
        """
        Deletes the user if the 'confirm' checkbox is checked.

        Args:
            user: The user instance to be deleted.
        """
        # Check if user confirmed the deletion.
        if self.cleaned_data.get('confirm'):
            user.delete()
