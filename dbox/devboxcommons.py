from subprocess import call, check_output
import sys
import os
import logging

class OS:

    def __init__(self, dist_name, version):
        self.dist_name = dist_name
        self.version = version

class OSUtils:

    def __init__(self, log):
        self.log = log

    def execute(self, to_execute):
        self.log.info("executing: %s" % (to_execute))
        result = call(to_execute, shell=True)
        if result > 0:
            self.log.error("execution resulted in a result greater than 0. exiting")
            sys.exit(1)

    def execute_with_output(self, command):
        return check_output(command, shell=True, stderr=None).decode("utf-8")
        
    def get_os_version(self):
        result = self.execute_with_output('cat /etc/*-release')
        dist_name = ""
        version = ""
        for line in result.splitlines(True):
            line = line.strip()
            parts = line.split('=')
            if len(parts) == 2:
                if parts[0].strip() == 'ID':
                    dist_name = parts[1].strip().lower()
                elif parts[0].strip() == 'VERSION_ID':
                    version = parts[1].strip().lower().strip('"')
        return OS(dist_name, version)

    def delete(self, file_to_delete):
        self.log.info("deleting: %s" % (file_to_delete))
        self.execute("rm -r %s" % file_to_delete)

    def ensure_exists(self, path_to_file):
        if not os.path.exists(path_to_file):
            self.log.error("the file or dir does not exist: '{0}'".format(path_to_file))
            sys.exit(1)

    def exists(self, path_to_file):
        return os.path.exists(path_to_file)

    def mkdirs(self, path):
        self.log.info("creating dir '%s'", path)
        os.makedirs(path)

    def read_file(self, file_name):
        f = open(file_name, 'r')
        contents = f.read()
        f.close()
        return contents

    def write_file(self, file_name, contents):
        f = open(file_name, 'w')
        f.write(contents)
        f.close()


class Logger:

    def __init__(self, application_name):
        self.log = logging.getLogger()
        self.log.setLevel(logging.DEBUG)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(levelname)s] - %(asctime)s - %(name)s - %(message)s')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)
        self.log.name = application_name

    def info(self, msg, *args, **kwargs):
        self.log.info(msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self.log.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.log.error(msg, *args, **kwargs)
