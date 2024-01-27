import platform
import shutil
import subprocess
import tarfile
import requests
from pydriller import Repository
import os
import git
import utils


def download_spotbugs(target_directory=utils.PROJECT_REPO):
    target_path = os.path.join(target_directory, "spotbugs.tar.gz")
    spotbugs_url = f'https://github.com/spotbugs/spotbugs/releases/download/4.8.3/spotbugs-4.8.3.tgz'
    response_spotbugs = requests.get(spotbugs_url, stream=True)

    if not os.path.exists('spotbugs-4.8.3') and not os.path.isdir('spotbugs-4.8.3'):
        if response_spotbugs.status_code == 200:
            # Scrivi il contenuto della risposta nel file di destinazione
            with open(target_path, 'wb') as file:
                shutil.copyfileobj(response_spotbugs.raw, file)
            print(f"Download completato: {target_path}")

            # Ora puoi procedere con l'installazione del file scaricato
            # (il metodo dipende dal formato del file, ad esempio, potresti dover decomprimere un archivio)

            # Esempio: decomprimi un file .tar.gz (da adattare se il formato è diverso)
            with tarfile.open(target_path, 'r:gz') as tar:
                tar.extractall(target_directory)

            os.remove(target_directory + "/spotbugs.tar.gz")
        else:
            print(f"Errore durante il download. Codice di stato: {response_spotbugs.status_code}")



def repo_reset_and_download():
    # Se la directory di destinazione esiste, eliminala
    if os.path.exists(utils.REPO_PATH):
        shutil.rmtree(utils.REPO_PATH)
    try:
        # Clona la repository
        print("Scaricando la repository...")
        git.Repo.clone_from("https://github.com/apache/cassandra.git", utils.REPO_PATH)
        print(f'Repository clonata in: {utils.REPO_PATH}')
    except git.GitCommandError as e:
        print(f'Errore durante il clone della repository: {e}')


def download_java_and_ant_version(target_directory=utils.PROJECT_REPO):
    os_type = platform.system()
    target_path = os.path.join(target_directory, "java.tar.gz")
    target_path_ant = os.path.join(target_directory, "ant.tar.gz")

    # Mappa l'architettura di Python a quella di Java
    if os_type == "Darwin":
        os_arch = "macos-aarch64"
    else:
        os_arch = "linux-x64"

    # Costruisci l'URL del file Java
    java_url = f'https://download.java.net/java/GA/jdk17.0.2/dfd4a8d0985749f896bed50d7138ee7f/8/GPL/openjdk-17.0.2_{os_arch}_bin.tar.gz'
    ant_url = f'https://dlcdn.apache.org//ant/binaries/apache-ant-1.10.14-bin.tar.gz'

    response_ant = requests.get(ant_url, stream=True)
    # Genera la response
    response_java = requests.get(java_url, stream=True)

    if not os.path.exists('jdk-17.0.2.jdk') and not os.path.isdir('jdk-17.0.2.jdk') and os_type == "Darwin":
        if response_java.status_code == 200:
            # Scrivi il contenuto della risposta nel file di destinazione
            with open(target_path, 'wb') as file:
                shutil.copyfileobj(response_java.raw, file)
            print(f"Download completato: {target_path}")

            # Ora puoi procedere con l'installazione del file scaricato
            # (il metodo dipende dal formato del file, ad esempio, potresti dover decomprimere un archivio)

            # Esempio: decomprimi un file .tar.gz (da adattare se il formato è diverso)
            with tarfile.open(target_path, 'r:gz') as tar:
                tar.extractall(target_directory)

            os.remove(utils.PROJECT_REPO + "/java.tar.gz")
        else:
            print(f"Errore durante il download. Codice di stato: {response_java.status_code}")

    if not os.path.exists('jdk-17.0.2') and not os.path.isdir('jdk-17.0.2') and os_type != "Darwin":
        if response_java.status_code == 200:
            # Scrivi il contenuto della risposta nel file di destinazione
            with open(target_path, 'wb') as file:
                shutil.copyfileobj(response_java.raw, file)
            print(f"Download completato: {target_path}")

            # Ora puoi procedere con l'installazione del file scaricato
            # (il metodo dipende dal formato del file, ad esempio, potresti dover decomprimere un archivio)

            # Esempio: decomprimi un file .tar.gz (da adattare se il formato è diverso)
            with tarfile.open(target_path, 'r:gz') as tar:
                tar.extractall(target_directory)

            os.remove(utils.PROJECT_REPO + "/java.tar.gz")
        else:
            print(f"Errore durante il download. Codice di stato: {response_java.status_code}")

    if not os.path.exists('apache-ant-1.10.14') and not os.path.isdir('apache-ant-1.10.14'):
        if response_ant.status_code == 200:
            with open(target_path_ant, 'wb') as file:
                shutil.copyfileobj(response_ant.raw, file)
            print(f"Download completato: {target_path_ant}")

            # Ora puoi procedere con l'installazione del file scaricato

            # Decomprimi un file .tar.gz (da adattare se il formato è diverso)
            with tarfile.open(target_path_ant, 'r:gz') as tar:
                tar.extractall(target_directory)

            os.remove(utils.PROJECT_REPO + "/ant.tar.gz")
        else:
            print(f"Errore durante il download. Codice di stato: {response_ant.status_code}")

    # Verifica che la richiesta sia andata a buon fine (codice 200)

    if os_type == "Darwin":
        os.environ['PATH'] = f'{utils.JAVA_17_PATH_MAC}/bin:{os.environ["PATH"]}'
        os.environ['JAVA_HOME'] = utils.JAVA_17_PATH_MAC
    else:
        os.environ['PATH'] = f'{utils.JAVA_17_PATH_LINUX}/bin:{os.environ["PATH"]}'
        os.environ['JAVA_HOME'] = utils.JAVA_17_PATH_LINUX

    # Aggiungi la directory bin di Java al PATH
    os.environ['ANT_HOME'] = utils.ANT_PATH
    os.environ['PATH'] = f'{utils.ANT_PATH}/bin:{os.environ["PATH"]}'

    os.system("java -version")
    os.system("ant -version")
    copy_spotbugs_ant()


def get_commit_iterator(repo_path, commit_num_start, commit_num_end):
    commits_stack = list(Repository(repo_path, only_in_branch='trunk').traverse_commits())
    iter(commits_stack)
    return iter(commits_stack[int(commit_num_start):int(commit_num_end)])


def change_repo_to_commit(commit_hash):
    repo = git.Repo(utils.REPO_PATH)

    try:
        os.chdir(utils.REPO_PATH)
        command = "git clean -xfd"
        # Esegui il comando utilizzando subprocess
        try:
            subprocess.run(command, shell=True, check=True)
            print("Pulizia completata con successo.")
        except subprocess.CalledProcessError as e:
            print(f"Errore durante la pulizia: {e}")
        # Cambia la directory di lavoro alla commit
        repo.git.checkout(commit_hash, force=True)
        print(f"Repository cambiata alla commit con hash: {commit_hash}")
    except git.GitCommandError as e:
        print(f"Errore: Commit con hash {e.stdout} non trovato nella repository")


def copy_spotbugs_ant():
    try:
        shutil.copy(utils.ANT_SPOTBUGS_PATH, utils.ANT_LIB_PATH)
        print(f"File '{utils.ANT_SPOTBUGS_PATH}' copiato con successo in '{utils.ANT_LIB_PATH}'.")
    except IOError as e:
        print(f"Errore durante la copia del file: {e}")


def reset_logs():
    try:
        shutil.rmtree(utils.XML_DIR)
    except Exception as e:
        pass
    os.makedirs(utils.XML_DIR)
