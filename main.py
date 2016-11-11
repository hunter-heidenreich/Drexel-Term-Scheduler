from lxml import html
import requests


def print_courses(courses):
    for course in courses:
        print(course)


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
    return courses


if __name__ == "__main__":
    main_url = 'https://duapp2.drexel.edu/webtms_du/app?component=subjectDetails&page=CollegesSubjects&service=direct&sp=ZH4sIAAAAAAAAAFvzloG1uIhBPjWlVC%2BlKLUiNUcvs6hErzw1qSS3WC8lsSRRLyS1KJcBAhiZGJh9GNgTk0tCMnNTSxhEfLISyxL1iwtz9EECxSWJuQXWPgwcJUAtzvkpQBVCEBU5iXnp%2BsElRZl56TB5l9Ti5EKGOgamioKCEgY2IwNDM2NToJHBBSBVCoGliUVAZQqGZrqG5gCfPyshpgAAAA%3D%3D'
    subjects2017 = {
        'ENGL': '&sp=SAS&sp=SENGL&sp=1'
    }
    print_courses(load_subject(main_url + subjects2017['ENGL']))
