import xml.etree.ElementTree as ET
import xmldiff
import utils
import csv


def find_bugs_by_xml(commit_hash, commit_author, counter):
    tree1 = ET.parse(utils.XML_PATH_NEW)
    tree2 = ET.parse(utils.XML_PATH_OLD)

    root1 = tree1.getroot()
    root2 = tree2.getroot()

    class_names_old = set()
    class_names_new = set()

    for bug_instance in root1.findall('.//BugInstance'):
        class_element = bug_instance.find('Class')
        if class_element is not None:
            class_name = class_element.get('classname')
            class_names_old.add(class_name)

    for bug_instance in root2.findall('.//BugInstance'):
        class_element = bug_instance.find('Class')
        if class_element is not None:
            class_name = class_element.get('classname')
            class_names_new.add(class_name)


    # Trova i bug aggiunti nel secondo file rispetto al primo
    diff = class_names_new.difference(class_names_old)

    introduced_bugs = [{'author': commit_author, 'hash': commit_hash, 'method': diff}]

    output_file = utils.PROJECT_REPO + f"/results/bug_introdotti{int(counter)}.csv"

    with open(output_file, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=['author', 'hash', 'method'])
        writer.writeheader()
        writer.writerows(introduced_bugs)

    print("Bug introdotti scritti in", output_file)
