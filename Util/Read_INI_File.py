from configparser import ConfigParser


def read_config_ini():
    config = ConfigParser()
    conf = "D:\\Work\\Documents\\PythonLLearning\\Python_Flask_Eli\\FlaskTestApp\\Util\\config.ini"
    config.read(conf)
    return config
