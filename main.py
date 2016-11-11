from lxml import html
import requests


if __name__ == "__main__":
    page = requests.get('https://duapp2.drexel.edu/webtms_du/app?component=subjectDetails&page=CollegesSubjects&service=direct&sp=ZH4sIAAAAAAAAAFvzloG1uIhBPjWlVC%2BlKLUiNUcvs6hErzw1qSS3WC8lsSRRLyS1KJcBAhiZGJh9GNgTk0tCMnNTSxhEfLISyxL1iwtz9EECxSWJuQXWPgwcJUAtzvkpQBVCEBU5iXnp%2BsElRZl56TB5l9Ti5EKGOgamioKCEgY2IwNDM2NToJHBBSBVCoGliUVAZQqGZrqG5gCfPyshpgAAAA%3D%3D&sp=SAS&sp=SENGL&sp=1')
    tree = html.fromstring(page.content)
    #This will create a list of buyers:
    evens = tree.xpath('//tr[@class="even" | @class="odd"]/td/text()')
    courses = []
    for x in range(len(evens)):
        if x % 11 == 0:
            courses.append([])
        #elif x % 11 == 6:
        #    print(tree.xpath('//tr[@class="even"]/td/p/a/text()'))
        courses[len(courses) - 1].append(evens[x])
    for course in courses:
        print(course)
