import os
import sys
import addXMLtag
import find_bugs
import pydrill
import utils


def print_option():
    print('BENVENUTO')
    print('1. INZIA')
    print('0. ESCI')


def choice(selected_choice):
    if selected_choice == '1':
        start()
    else:
        sys.exit()


def commit_divisor():
    print('Inserisci da che numero vuoi iniziare a analizzare: ')
    return input()


def start():
    pydrill.repo_reset_and_download()
    pydrill.reset_logs()
    pydrill.download_java_and_ant_version()
    print('Inserisci da che numero vuoi iniziare a analizzare: ')
    start_commit = input()
    print("Inserisci da che numero vuoi finire l'analizzazione: ")
    end_commit = input()

    commit_iterator_head = pydrill.get_commit_iterator(utils.REPO_PATH, start_commit, end_commit)
    counter = int(start_commit)
    commit = next(commit_iterator_head)
    pydrill.change_repo_to_commit(commit.hash)
    prev_commit = commit

    while True:
        print(f"Commit numero: {counter}")
        try:
            if os.path.exists(utils.XML_PATH_OLD) and not os.path.getsize(utils.XML_PATH_OLD) == 0 and os.path.exists(utils.XML_PATH_NEW) and not os.path.getsize(utils.XML_PATH_NEW) == 0:
                find_bugs.find_bugs_by_xml(prev_commit.hash, prev_commit.author.name, counter)
                os.remove(os.path.join(utils.XML_DIR, "old_file_log.xml"))
            if addXMLtag.add_xml_spotbugs_tag(utils.XML_BUILD_PATH):
                prev_commit = commit
                commit = next(commit_iterator_head)
                pydrill.change_repo_to_commit(commit.hash)
            else:
                pydrill.reset_logs()
                pydrill.change_repo_to_commit(next(commit_iterator_head).hash)
                print("Non è stato possibile compliare la repo")
                print("------------------------------------------\n")
        except StopIteration:
            # Uno degli iteratori ha raggiunto la fine dei commit disponibili
            print("Commit finiti")
            break
        counter += 1


if __name__ == "__main__":
    print_option()
    c_selected = input("Inserisci la scelta: ")
    choice(c_selected)
