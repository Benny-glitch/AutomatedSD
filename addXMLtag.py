import os
import xml.etree.ElementTree as ET

import pydrill
import utils


def add_xml_spotbugs_tag(build_xml_path):
    try:
        # Parsing del file build.xml
        tree = ET.parse(build_xml_path)
        root = tree.getroot()

        # Aggiunta del taskdef
        taskdef_element = ET.Element("taskdef")
        taskdef_element.set("resource", "edu/umd/cs/findbugs/anttask/tasks.properties")
        taskdef_element.set("classpath", f"{utils.ANT_LIB_PATH}/spotbugs-ant.jar")
        root.append(taskdef_element)

        # Aggiunta della proprietà spotbugs.home
        property_element = ET.Element("property")
        property_element.set("name", "spotbugs.home")
        property_element.set("value", f"{utils.TOOL_PATH}")
        root.append(property_element)

        # Aggiunta del target spotbugs
        target_element = ET.Element("target")
        target_element.set("name", "spotbugs")
        target_element.set("depends", "jar")

        spotbugs_element = ET.Element("spotbugs")
        spotbugs_element.set("home", "${spotbugs.home}")
        spotbugs_element.set("output", "xml")

        build_logs_dir = utils.XML_DIR
        new_log_file_name = "new_file_log.xml"
        old_log_file_name = "old_file_log.xml"

        # Lista tutti i file nella cartella build_logs
        files_in_build_logs = os.listdir(build_logs_dir)

        if len(files_in_build_logs) == 0:
            spotbugs_element.set("outputFile", f"{utils.XML_DIR}/{new_log_file_name}")
        else:
            # Controlla se esiste un nuovo file XML
            if new_log_file_name in files_in_build_logs:
                if os.path.exists(os.path.join(build_logs_dir, old_log_file_name)):
                    os.remove(os.path.join(build_logs_dir, old_log_file_name))
                # Rinomina il file log.xml attivo come old_file_log.xml
                os.rename(os.path.join(build_logs_dir, new_log_file_name),os.path.join(build_logs_dir, old_log_file_name))

                # Rinomina il nuovo file XML come log.xml
                spotbugs_element.set("outputFile", f"{utils.XML_DIR}/{new_log_file_name}")

        auxClasspath_element = ET.Element("auxClasspath")
        auxClasspath_element.set("path", "${basedir}/lib/Regex.jar")
        sourcePath_element = ET.Element("sourcePath")
        sourcePath_element.set("path", "${basedir}/src")

        class_element = ET.Element("class")
        class_element.set("location", "${basedir}/build/classes")

        spotbugs_element.append(auxClasspath_element)
        spotbugs_element.append(sourcePath_element)
        spotbugs_element.append(class_element)

        target_element.append(spotbugs_element)
        root.append(target_element)

        # Salva le modifiche nel file XML
        tree.write(build_xml_path)
    except Exception as e:
        print("Non è stato trovato il file build.xml\nerrore:", e)
        return False

    try:
        os.chdir(utils.REPO_PATH)
        response = os.system(f"ant spotbugs")
        if int(response) == 256:
            pydrill.reset_logs()
            raise Exception
    except Exception as e:
        print("La build non è andata a buon fine")
        return False

    return True
