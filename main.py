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


if __name__ == "__main__":
    winter2017 = 'https://duapp2.drexel.edu/webtms_du/app?component=subjectDetails&page=CollegesSubjects&service=direct&sp=ZH4sIAAAAAAAAAFvzloG1uIhBPjWlVC%2BlKLUiNUcvs6hErzw1qSS3WC8lsSRRLyS1KJcBAhiZGJh9GNgTk0tCMnNTSxhEfLISyxL1iwtz9EECxSWJuQXWPgwcJUAtzvkpQBVCEBU5iXnp%2BsElRZl56TB5l9Ti5EKGOgamioKCEgY2IwNDMyNToJHhmXlAaYXA0sQiEG1opmtoDgAb98cdpgAAAA%3D%3D'
    spring2017 = 'https://duapp2.drexel.edu/webtms_du/app?component=subjectDetails&page=CollegesSubjects&service=direct&sp=ZH4sIAAAAAAAAAFvzloG1uIhBPjWlVC%2BlKLUiNUcvs6hErzw1qSS3WC8lsSRRLyS1KJcBAhiZGJh9GNgTk0tCMnNTSxhEfLISyxL1iwtz9EECxSWJuQXWPgwcJUAtzvkpQBVCEBU5iXnp%2BsElRZl56TB5l9Ti5EKGOgamioKCEgY2IwNDM2NToJHBBSBVCoGliUVAZQqGZrqG5gCfPyshpgAAAA%3D%3D'
    subjects = {
        'ENGL': '&sp=SAS&sp=SENGL&sp=1',
        'BUSN': '&sp=SB&sp=SBUSN&sp=1'
    }
    running = ' '
    schedule = []
    while running != 'Q':
        running = print_choices()
        if running == '1':
            add_to_schedule(schedule)

    #print(create_schedule())
    #print_courses(load_subject(winter2017 + subjects['ENGL']))
