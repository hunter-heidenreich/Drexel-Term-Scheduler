from lxml import html
import requests


def load_subject(subject_url):
    page = requests.get(subject_url)
    tree = html.fromstring(page.content)

    courselist = tree.xpath('//tr[@class="even"]/td/text() | //tr[@class="odd"]/td/text()')
    crns = tree.xpath('//tr[@class="even"]/td/p/a/text() | //tr[@class="odd"]/td/p/a/text()')
    capacity = tree.xpath('//tr[@class="even"]/td/p/attribute::title | //tr[@class="odd"]/td/p/attribute::title')
    courses = []
    for x in range(len(courselist)):
        if x % 11 == 0:
            courses.append([])
        elif x % 11 == 6:
            courselist[x] = crns[x // 11]
        elif x % 11 == 9:
            courselist[x] = capacity[x // 11]
        courses[len(courses) - 1].append(courselist[x])

    for i in range(len(courses)):
        courses[i] = course_to_dict(courses[i])
    return remove_full(courses)

def load_course(subject, course):
    restricted = []
    for sub in subject:
        if sub['COURSE'] == course:
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
        'DAYS': course[7],
        'TIMES': format_time(course[8]),
        'CAP': course[9],
        'PROF': course[10]
    }


def format_time(time):
    n_time = [0, 0]

    if(time != 'TBD'):
        n_time = [time[0:2] + time[3:5], time[11:13] + time[14:16]]

        if time[6:8] == 'pm':
            n_time[0] = int(n_time[0]) + 1200
        else:
            n_time[0] = int(n_time[0])

        if time[17:19] == 'pm':
            n_time[1] = int(n_time[1]) + 1200
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
        print(course['SUBJECT'], course['COURSE'])
    print()


def add_course():
    course = {}
    course['SUBJECT'] = input('Enter subject: ')
    course['COURSE'] = input('Enter the course number: ')
    course['RESPONSE'] = input('Adding "' + course['SUBJECT'] + ' ' + course['COURSE'] + '". Correct? [Y/N] ')
    return course


def remove_from_schedule(schedule):
    removing = ' '
    while removing != 'Q':
        print()
        print('Select course to remove: ')
        for i in range(len(schedule)):
            print(i, schedule[i]['SUBJECT'], schedule[i]['COURSE'])
        removing = input('Which to remove? [Q] to quit: ')
        if removing != 'Q':
            del schedule[int(removing)]
    return schedule


def schedule_preferences(preferences):
    print()
    print('Week Preferences')
    print('[1] Early in the week')
    print('[2] Late in the week')
    print('[3] Middle of the week')
    print('[4] Alternating days')
    print('[5] Concentrate to 1-3 days of the week')
    print('[6] No preference')
    preferences['WEEK'] = int(input('Select option: '))
    print()
    print('Day Preferences')
    print('[1] Early in the day')
    print('[2] Late in the day')
    print('[3] Middle of the day')
    print('[4] Spread out classes')
    print('[5] Concentrate classes together in the day')
    print('[6] Noon gap (for lunch)')
    print('[7] No preferences')
    preferences['DAY'] = int(input('Select option: '))
    print()
    print('Class Style Preferences')
    print('[1] Normal')
    print('[2] Hybrid')
    print('[3] No preferences')
    preferences['STYLE'] = int(input('Select option: '))
    print()
    print('CURRENT PREFERENCES')
    print('Week:', preferences['WEEK'])
    print('Day:', preferences["DAY"])
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
    for course in schedule:
        sub = load_subject(spring2017 + subjects[course['SUBJECT']])
        print_courses(load_course(sub, course['COURSE']))


if __name__ == "__main__":
    subjects = {
        'BIO': '&sp=SAS&sp=SBIO&sp=1',
        'BUSN': '&sp=SB&sp=SBUSN&sp=1',
        'CS': '&sp=SCI&sp=SCS&sp=5',
        'ENGL': '&sp=SAS&sp=SENGL&sp=1',
        'ENGR': '&sp=SE&sp=SENGR&sp=6',
        'MATH': '&sp=SAS&sp=SMATH&sp=1',
        'PHYS': '&sp=SAS&sp=SPHYS&sp=1'

    }
    running = ' '
    schedule = []
    preferences = {}
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

    #print(create_schedule())
    #print_courses(load_subject(winter2017 + subjects['ENGL']))
