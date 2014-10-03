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

import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from stats.models import Issue
from pups import settings



@login_required
def stats_page(request):
    return render(request, 'stats.html')


@login_required
def stats_data_ajax(request):
    return HttpResponse(json.dumps(Issue.get_issues_json()),
                        content_type="application/json")


@login_required
def create_issue(request):

    Issue.create_issue(request.user.username, request.POST['new_issue_text'])
    return redirect("/stats")


@login_required
def plus_one_ajax(request):
    '''
    This method increases an issue by one in the db
    '''
    response_data = {}
    response_data['status'] = 'failure'

    if Issue.plus_one(request.POST['id']):
        response_data['status'] = 'success'

    return HttpResponse(json.dumps(response_data),
                        content_type="application/json")


@login_required
def edit_issue_ajax(request):
    '''
    Attempts to lock issue row in db and reports back if row
    was locked by another user or does not exist.
    '''
    response_data = {}
    lock_status = Issue.lock(request.POST['id'], request.user.username)

    if lock_status is True:
        response_data['lock_status'] = 'lock_success'
        response_data['lock_limit'] = settings.CONFIG['edit_lock_expiration']
    elif lock_status is False:
        response_data['lock_status'] = 'does_not_exist'
    elif type(lock_status) is dict:
        response_data['locked_by'] = lock_status['locked_by']
        response_data['expires_in'] = lock_status['expires_in']

    return HttpResponse(json.dumps(response_data),
                        content_type="application/json")


@login_required
def save_issue_edit_ajax(request):

    response_data = {}
    response_data['status'] = 'failure'

    if Issue.save_edit(request.POST['id'],
                       request.POST['edited_text'],
                       request.user.username):

        response_data['status'] = 'success'

    return HttpResponse(json.dumps(response_data),
                        content_type="application/json")


@login_required
def unlock_issue_ajax(request):

    response_data = {}
    response_data['status'] = 'failure'

    if Issue.unlock(request.POST['id']):
        response_data['status'] = 'success'

    return HttpResponse(json.dumps(response_data),
                        content_type="application/json")


@login_required
def delete_issue_ajax(request):
    '''
    Deletes one issue (db row) and gives back feedback in json
    '''

    response_data = {}
    response_data['status'] = 'failure'

    if Issue.delete_issue(request.POST['id']):
        response_data['status'] = 'success'

    return HttpResponse(json.dumps(response_data),
                        content_type="application/json")
