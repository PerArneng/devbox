#!/usr/bin/env python

import argparse
import os
from devboxcommons import Logger, OSUtils

class Application:

    application_name = "devbox"
    application_description = "a utility for installing a development box"
    playbook_base_dir = 'playbooks'

    def __init__(self):
        self.log = Logger(self.application_name)
        self.os_utils = OSUtils(self.log)
        self.os = self.os_utils.get_os_version()

    def start(self):

        parser = argparse.ArgumentParser(prog=self.application_name, usage='%(prog)s [options]',
                                        description=self.application_description)
        parser.add_argument('-a', '--ansible-playbooks', required=False ,nargs='?', help='the name of the ansible playbook')
        parser.add_argument('-l', '--list', required=False, action='store_true', help='list ansible playbooks')
        parser.add_argument('-s', '--status', required=False, action='store_true', help='the status of the playbook')
        args = parser.parse_args()

        self.log.info('dist name: %s' % self.os.dist_name)
        self.log.info('dist version: %s' % self.os.version)

        if args.ansible_playbooks is not None:
            self.install_playbooks(args.ansible_playbooks.split(','), args.status)
        elif args.list:
            self.list_playbooks(self.playbook_base_dir)


    def list_playbooks(self, playbook_dir):
        playbooks = []
        for root, subdirs, files in os.walk(playbook_dir):
            for yml_file in files:
                if ".yml" in yml_file:
                    playbook = yml_file.replace('.yml', '')
                    playbooks.append('%s - %s' % (playbook, root))

        for playbook in sorted(playbooks):
            print(playbook)

    def install_playbooks(self, playbooks, simulate):

        file_paths = []

        for playbook in playbooks:
            test_paths = [
                '%s/%s/%s/%s.yml' % (self.playbook_base_dir, self.os.dist_name, self.os.version, playbook),
                '%s/%s/%s.yml' % (self.playbook_base_dir, self.os.dist_name, playbook),
                '%s/%s.yml' % (self.playbook_base_dir, playbook)

            ]

            playbook_path = None
            for path in test_paths:
                if self.os_utils.exists(path):
                    playbook_path = path
            
            if playbook_path is None:
                self.log.error("no playbook file found for playbook %s" % playbook)
                exit(1)
            
            file_paths.append(playbook_path)
            self.log.info('found playbook at: %s' % (playbook_path))

        check_param = ''
        if simulate:
            check_param = '--check'

        paths = " ".join(file_paths)
        print(paths)
        self.os_utils.execute('ansible-playbook --ask-become-pass --become -i "localhost," -c local --extra-vars="hosts=localhost" %s %s' % (check_param, paths))


def main():
    app = Application()
    app.start()

if __name__ == '__main__':
    main()
