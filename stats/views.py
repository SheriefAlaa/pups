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


# Status codes
_issueDoesNotExist, _issuesIsLocked, _issueIsNotLocked, \
_failure = range(1,5)


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
    response = get_response(request.POST['id'])

    if response['status_code'] == _issueIsNotLocked:
        Issue.plus_one(request.POST['id'])

    return HttpResponse(json.dumps(response),
                        content_type="application/json")


@login_required
def edit_issue_ajax(request):
    '''
    Attempts to lock issue row in db and reports back if row
    was locked by another user or does not exist.
    '''
    response = get_response(request.POST['id'])

    if response['status_code'] == _issueIsNotLocked:
        Issue.lock(request.POST['id'], request.user.username)

    return HttpResponse(json.dumps(response),
                        content_type="application/json")


@login_required
def save_issue_edit_ajax(request):
    return HttpResponse(json.dumps(Issue.save_edit(
                        request.POST['id'],
                        request.POST['edited_text'],
                        request.user.username)),
                        content_type="application/json")


@login_required
def unlock_issue_ajax(request):
    return HttpResponse(json.dumps(Issue.unlock(request.POST['id'])),
                        content_type="application/json")


@login_required
def delete_issue_ajax(request):
    '''
    Deletes one issue (db row) and gives back feedback in json
    '''
    response = get_response(request.POST['id'])

    if response['status_code'] == _issueIsNotLocked:
        Issue.delete_issue(request.POST['id'])

    return HttpResponse(json.dumps(response),
                        content_type="application/json")


def get_response(id):
    lock_status = Issue.lock_status(int(id))
    response = {}

    if lock_status:
        if lock_status[0] == _issuesIsLocked:
            response['status_code'] = lock_status[0]
            response['locked_by'] = lock_status[1]
            response['expires_in'] = lock_status[2]

        elif lock_status[0] == _issueDoesNotExist:
            response['status_code'] = lock_status[0]

        elif lock_status[0] == _issueIsNotLocked:
            response['status_code'] = lock_status[0]
            response['lock_limit'] = lock_status[1]

    return response
