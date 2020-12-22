from configparser import ConfigParser


def read_db_config(filename='config.ini', section='mysql'):
    """Read database configuration file and return a dictionary object

    Args:
        filename (str, optional): name of the configuration file. Defaults to 'config.ini'.
        section (str, optional): section of database configuration. Defaults to 'mysql'.
    """
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)
    
    # get section, default to mysql
    if parser.has_section(section):
        items = parser.items(section)
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))
    # print(items)
    return dict(items)

if __name__ == "__main__":
    print(read_db_config())
