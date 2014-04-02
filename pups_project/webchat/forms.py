from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

class ChangePassForm(forms.Form):
    current_pass = forms.CharField(max_length=32, widget=forms.PasswordInput)
    new_pass = forms.CharField(max_length=32, widget=forms.PasswordInput)
    new_pass_confirm = forms.CharField(max_length=32, widget=forms.PasswordInput)

    def change_password(self, request, data):
        if (data['new_pass'] == data['new_pass_confirm'] ) and \
            request.user.check_password(data['current_pass'] ):

            request.user.set_password(data['new_pass'])
            request.user.save()
            return True
        else:
            return False