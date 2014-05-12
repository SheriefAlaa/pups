# This file is part of Pups, a django/python project which contains
# web support tools
#
#  Author: Sherief Alaa <sheriefalaa.w@gmail.com>
#
#  Copyright:
#   (c) 2014 Sherief Alaa.
#   (c) 2014 The Tor Project, Inc.
#
# Pups is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pups is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pups.  If not, see <http://www.gnu.org/licenses/>.

from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required
from pups.forms import ChangePassForm
from django.contrib import messages
from pups.feedback import FeedbackMessages as fbm


def custom_login(request):
    '''
    Extends django's built-in login view to support redirecting already
    logged in users so that they can't view login.html if logged in.
    '''
    if request.user.is_authenticated():
        return redirect('/')

    return login(request, 'login.html', 'login')


@login_required
def change_password(request):
    form = ChangePassForm(request.POST or None)

    if form.is_valid():  # If all fields are valid change the password
        if form.change_password(request, form.cleaned_data):
            messages.add_message(request, messages.INFO, fbm.good_pw)
            return redirect('/chpass')

        messages.add_message(request, messages.INFO, fbm.bad_pw)

    return render(request, 'change_password.html', {'form': form})


@login_required
def home(request):
    return render(request, "pups.html")
