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

import os, sys
from datetime import date
from django.core.management.base import BaseCommand, CommandError
from pups import settings
from stats.models import Issue

class Command(BaseCommand):
    help = "Backs up a month worth of stats"

    def handle(self, *args, **options):
        if len(args) != 1:
            print "Usage: python manage.py statsbackupmonthly month_as_a_ number"
            sys.exit(0)

        if args[0].isdigit() and int(args[0]) in range(1, 12): 
            backup_stats_report(args[0])
            print "Successfully backed up the report and reset the counters"
            sys.exit(1)
        else:
            print "month range has to be between 1 and 12"
            sys.exit(-1)

def backup_stats_report(month):
    '''
    Dumps a monthly report in a text file on disk and resets
    the frequency counters
    '''

    # Making sure the report file path exists
    if not os.path.exists(settings.CONFIG['stats_reports_path']):
        os.mkdir(settings.CONFIG['stats_reports_path'])

    reports = os.listdir(settings.CONFIG['stats_reports_path'])
    file_name = month + '_' + str(date.today().year)

    # Report already backed up
    if file_name in reports:
        print "Report already backed up"
        sys.exit(-1)

    if not save_report_on_disk(file_name):
        print "Disk error or lack of write permissions"
        sys.exit(-1)

    # Reset frequency in db
    Issue.objects.update(frequency=0)


def save_report_on_disk(file_name):
    try:
        fp = open(settings.CONFIG['stats_reports_path'] + file_name, 'w')
    except IOError:
        return False # Can't open file

    issues = Issue.objects.values_list('text', 'frequency').order_by('-frequency')
    text_list = []
    frequency_list = []

    for i in issues:
        text_list.append(i[0])
        frequency_list.append(i[1])

    longest_str_len = len(max(text_list, key=len))
    longest_freq_len = len(str(max(frequency_list)))
    separator = ' | '
    line_len = longest_str_len + longest_freq_len + len(separator)

    for issue in issues:
        remaining_width = longest_str_len - len(issue[0])
        fp.write(issue[0].encode('utf-8').strip()
                + (" " * remaining_width)
                + separator
                + str(issue[1]) + '\n'
                + '-' * line_len + '\n')
    fp.close()
    return True
