import os

TOOL_PATH = os.path.dirname(os.path.abspath(__file__)) + '/spotbugs-4.8.3'

ANT_SPOTBUGS_PATH = os.path.dirname(os.path.abspath(__file__)) + '/spotbugs-4.8.3/lib/spotbugs-ant.jar'

XML_LOGS_PATH = os.path.dirname(os.path.abspath(__file__)) + '/xml_logs/'

XML_PATH_OLD = XML_LOGS_PATH + '/old_file_log.xml'

XML_PATH_NEW = XML_LOGS_PATH + '/new_file_log.xml'

XML_DIR = os.path.dirname(os.path.abspath(__file__)) + '/xml_logs'

REPO_PATH = os.path.dirname(os.path.abspath(__file__)) + '/cassandra'

XML_BUILD_PATH = REPO_PATH + '/build.xml'

PROJECT_REPO = os.path.dirname(os.path.abspath(__file__))

JAVA_11_PATH = os.path.dirname(os.path.abspath(__file__)) + '/jdk-11.0.20.jdk/Contents/Home'

JAVA_17_PATH_MAC = os.path.dirname(os.path.abspath(__file__)) + '/jdk-17.0.2.jdk/Contents/Home'

JAVA_17_PATH_LINUX = os.path.dirname(os.path.abspath(__file__)) + '/jdk-17.0.2'

ANT_PATH = os.path.dirname(os.path.abspath(__file__)) + '/apache-ant-1.10.14'

ANT_LIB_PATH = os.path.dirname(os.path.abspath(__file__)) + '/apache-ant-1.10.14/lib'
