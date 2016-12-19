'''
 - Some courses have classes ocurring at different times on different days.
   How should that be handled?
 - Generate visuals for schedules
 - Generate txt files for CRNs of schedules
'''

import copy
from lxml import html
import requests


def load_subject(subject, subject_url):
    page = requests.get(subject_url)
    tree = html.fromstring(page.content)

    courselist = tree.xpath('//tr[@class="even"]/td/text() | //tr[@class="odd"]/td/text()')
    crns = tree.xpath('//tr[@class="even"]/td/p/a/text() | //tr[@class="odd"]/td/p/a/text()')
    capacity = tree.xpath('//tr[@class="even"]/td/p/attribute::title | //tr[@class="odd"]/td/p/attribute::title')
    courses = []
    try:
        if not (subject == 'BIO'):
            for x in range(len(courselist)):
                if x % 11 == 0:
                    courses.append([])
                elif x % 11 == 6:
                    courselist[x] = crns[x // 11]
                elif x % 11 == 9:
                    courselist[x] = capacity[x // 11]
                courses[len(courses) - 1].append(courselist[x])
        else:
            for x in range(446, 1073):
                manip = x - 446
                if manip % 11 == 0:
                    courses.append([])
                elif manip % 11 == 6:
                    courselist[x] = crns[x // 11]
                elif manip % 11 == 9:
                    courselist[x] = capacity[x // 11]
                courses[len(courses) - 1].append(courselist[x])

        for i in range(len(courses)):
            courses[i] = course_to_dict(courses[i])
        return remove_full(courses)
    except IndexError:
        print('This subject is still being finalized for the selected term.')
        return []


def load_course(subject, course, preferences):
    restricted = []
    for sub in subject:
        if sub['COURSE'] == course['COURSE']:
            if sub['TYPE'] == course['TYPE']:
                try:
                    if int(sub['SECTION']) < 300:
                        restricted.append(sub)
                except ValueError:
                    restricted.append(sub)

    return restricted


def print_courses(courses):
    for course in courses:
        print(course)


def course_to_dict(course):
    return {
        'SUBJECT': course[0],
        'COURSE': course[1],
        'TYPE': course[2],
        'STYLE': course[3],
        'SECTION': course[4],
        'TITLE': course[5],
        'CRN': course[6],
        'DAYS': format_days(course[7]),
        'TIMES': format_time(course[8]),
        'CAP': course[9],
        'PROF': course[10]
    }


def format_days(day_string):
    days = [0, 0, 0, 0, 0]
    for char in day_string:
        if char == 'M':
            days[0] = 1
        elif char == 'T':
            days[1] = 1
        elif char == 'W':
            days[2] = 1
        elif char == 'R':
            days[3] = 1
        elif char == 'F':
            days[4] = 1
    return days


def format_time(time):
    n_time = [0, 0]

    if(time != 'TBD'):
        n_time = [time[0:2] + time[3:5], time[11:13] + time[14:16]]

        if time[6:8] == 'pm':
            n_time[0] = int(n_time[0]) + 1200
            if n_time[0] >= 2400:
                n_time[0] -= 1200
        else:
            n_time[0] = int(n_time[0])

        if time[17:19] == 'pm':
            n_time[1] = int(n_time[1]) + 1200
            if n_time[1] >= 2400:
                n_time[1] -= 1200
        else:
            n_time[1] = int(n_time[1])

    return n_time


def remove_full(courses):
    return [c for c in courses if c['CAP'] != 'FULL']


def add_to_schedule(schedule):
    response = 'Y'
    while response == 'Y':
        course = add_course()
        if course.pop('RESPONSE', None) == 'Y':
            schedule.append(course)
        print_schedule(schedule)
        response = input('Add new course? (Y/N) ')
    return schedule


def print_schedule(schedule):
    print()
    print('CURRENT SCHEDULE')
    for course in schedule:
        print(course['SUBJECT'], course['COURSE'], course['TYPE'])
    print()


def add_course():
    course = {}
    course['SUBJECT'] = input('Enter subject: ')
    course['COURSE'] = input('Enter the course number: ')
    course['TYPE'] = input('Enter part of course (Lab, Lecture, etc.): ')
    course['RESPONSE'] = input('Adding "' + course['SUBJECT'] + ' ' + course['COURSE'] + ' ' + course['TYPE'] + '". Correct? [Y/N]: ')
    return course


def remove_from_schedule(schedule):
    removing = ' '
    while removing != 'Q':
        if len(schedule) > 0:
            print()
            print('Select course to remove: ')
            for i in range(len(schedule)):
                print(i, schedule[i]['SUBJECT'], schedule[i]['COURSE'], schedule[i]['TYPE'])
            removing = input('Which to remove? [Q] to quit: ')
            try:
                del schedule[int(removing)]
            except ValueError:
                removing = 'Q'
            except IndexError:
                print('Not a valid choice.')
        else:
            print('No schedule yet.')
            removing = 'Q'

    return schedule


def schedule_preferences(preferences):
    print()
    print('Time of Day Preference')
    print('Times are in 24 hour format (0800 is 8:00 AM)')
    preferences['EARLY_TIME'] = int(input('Enter the earleist hour you wish to start a class: '))
    preferences['LATE_TIME'] = int(input('Enter the latest hour you wish to end a class: '))
    preferences['LUNCH_HOUR'] = int(input('Specify a lunch hour (0 for no lunch hour): '))
    print()
    print('CURRENT TIME PREFERENCES')
    print('Time of Day:', preferences['EARLY_TIME'], '-', preferences['LATE_TIME'])
    print('Lunch Hour:', preferences['LUNCH_HOUR'])
    print()
    print('Day Preferences')
    print('List the amount of classes you want per day. Enter 9 if it doesn\'t matter.')
    if('DAYS' not in preferences.keys()):
        preferences['DAYS'] = [0, 0, 0, 0, 0]
    preferences['DAYS'][0] = int(input('Enter the number of classes for Monday: '))
    preferences['DAYS'][1] = int(input('Enter the number of classes for Tuesday: '))
    preferences['DAYS'][2] = int(input('Enter the number of classes for Wednesday: '))
    preferences['DAYS'][3] = int(input('Enter the number of classes for Thursday: '))
    preferences['DAYS'][4] = int(input('Enter the number of classes for Friday: '))
    print()
    print('CURRENT DAY PREFERENCES')
    print('Day limits (Mon-Fri):', preferences['DAYS'])
    print()
    return preferences

def print_choices():
    print()
    print('Drexel Term Master Scheduler [SPRING 2017]')
    print()
    print('[1] Add courses')
    print('[2] Remove courses')
    print('[3] Specify schedule preferences')
    print('[4] Generate schedules')
    print('[Q]uit')
    print()
    return input('Select choice: ')


def generate_schedules(subjects, schedule, preferences):
    spring2017 = 'https://duapp2.drexel.edu/webtms_du/app?component=subjectDetails&page=CollegesSubjects&service=direct&sp=ZH4sIAAAAAAAAAFvzloG1uIhBPjWlVC%2BlKLUiNUcvs6hErzw1qSS3WC8lsSRRLyS1KJcBAhiZGJh9GNgTk0tCMnNTSxhEfLISyxL1iwtz9EECxSWJuQXWPgwcJUAtzvkpQBVCEBU5iXnp%2BsElRZl56TB5l9Ti5EKGOgamioKCEgY2IwNDM2NToJHBBSBVCoGliUVAZQqGZrqG5gCfPyshpgAAAA%3D%3D'
    selection = []
    for course in schedule:
        if len(subjects[course['SUBJECT']]['courses']) == 0:
            subjects[course['SUBJECT']]['courses'] = load_subject(course['SUBJECT'], spring2017 + subjects[course['SUBJECT']]['link'])
        selection.append(load_course(subjects[course['SUBJECT']]['courses'], course, preferences))
    recursive_generator([], selection.pop(), selection, preferences)


def recursive_generator(schedule, current, leftover, prefs):
    for c in current:
        check_val = True
        if c['TIMES'][0] < prefs['EARLY_TIME'] or c['TIMES'][1] > prefs['LATE_TIME']:
            check_val = False
        if prefs['LUNCH_HOUR'] >= c['TIMES'][0] and prefs['LUNCH_HOUR'] < c['TIMES'][1]:
            check_val = False
        if check_val:
            for s in schedule:
                for x in range(len(c['DAYS'])):
                    if c['DAYS'][x] == 1 and s['DAYS'][x] == 1:
                        if c['TIMES'][0] >= s['TIMES'][0] and c['TIMES'][0] <= s['TIMES'][1]:
                            check_val = False
                        elif c['TIMES'][1] >= s['TIMES'][0] and c['TIMES'][1] <= s['TIMES'][1]:
                            check_val = False
        if check_val:
            for x in range(len(prefs['DAYS'])):
                if prefs['DAYS'][x] < c['DAYS'][x]:
                    check_val = False
        if check_val:
            dupe = copy.deepcopy(schedule)
            dupe.append(c)
            saved_prefs = copy.deepcopy(prefs)
            for x in range(len(c['DAYS'])):
                saved_prefs['DAYS'][x] -= c['DAYS'][x]
            if len(leftover) > 0:
                lefts = copy.deepcopy(leftover)
                recursive_generator(dupe, lefts.pop(), lefts, saved_prefs)
            else:
                print_as_block(dupe)


def print_as_block(schedule):
    days = []
    t = 800
    while t < 2200:
        if not (t % 100 == 0):
            days.append((t - 20))
        else:
            days.append(t)
        t += 50

    full_sched = []
    full_sched.append(days)
    for i in range(1, 6):
        full_sched.append([])
        for x in range(len(days)):
            full_sched[i].append(' ')

    for course in schedule:
        for d in range(len(course['DAYS'])):
            if course['DAYS'][d] == 1:
                time_start = (course['TIMES'][0] // 50) - (800 // 50)
                time_end = (course['TIMES'][1] // 50) - (800 // 50) + 1
                for time in range(time_start, time_end):
                    full_sched[d + 1][time] = course['SUBJECT'] + ' ' + course['COURSE'] + ' ' + course['SECTION']

    print()
    for x in range(len(days)):
        print ("{0:^14} {1:^14} {2:^14} {3:^14} {4:^14} {5:^14}".format(full_sched[0][x], full_sched[1][x], full_sched[2][x], full_sched[3][x], full_sched[4][x], full_sched[5][x]))
    print()


if __name__ == "__main__":
    subjects = {
        'BIO': {
            'link': '&sp=SAS&sp=SBIO&sp=1',
            'courses': []
        },
        'BUSN': {
            'link': '&sp=SB&sp=SBUSN&sp=1',
            'courses': []
        },
        'CS': {
            'link': '&sp=SCI&sp=SCS&sp=5',
            'courses': []
        },
        'ENGL': {
            'link': '&sp=SAS&sp=SENGL&sp=1',
            'courses': []
        },
        'ENGR': {
            'link': '&sp=SE&sp=SENGR&sp=6',
            'courses': []
        },
        'MATH': {
            'link': '&sp=SAS&sp=SMATH&sp=1',
            'courses': []
        },
        'PHYS': {
            'link': '&sp=SAS&sp=SPHYS&sp=1',
            'courses': []
        }

    }
    running = ' '
    schedule = []
    preferences = {
        'EARLY_TIME': 0,
        'LATE_TIME': 2400,
        'LUNCH_HOUR': 0,
        'DAYS': [9, 9, 9, 9, 9]
    }

    while running != 'Q':
        running = print_choices()
        if running == '1':
            schedule = add_to_schedule(schedule)
        elif running == '2':
            schedule = remove_from_schedule(schedule)
        elif running == '3':
            preferences = schedule_preferences(preferences)
        elif running == '4':
            generate_schedules(subjects, schedule, preferences)
