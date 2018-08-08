# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Git check out batch"""


import os

from time import sleep


class G:
    """Git operation batch"""

    def __init__(self):
        self.diyidan = '~/Documents/diyidan/'

    def cmd(self, command):
        """System command"""
        return os.popen(command).read()

    def get_all_sub_dirs(self, path):
        """Get all module dirs"""
        return (x for x in self.cmd(f"ls {self.diyidan}{path}").split('\n') if x)

    def cd(self, path):
        """cd to path"""
        return self.cmd(f"cd {path}")

    def list_branch(self, path):
        """List the current branch"""
        return self.cmd(f"cd {path} && git br")

    def check_out(self, path, branch):
        """Check out to given branch"""
        return self.cmd(f"cd {path} && git co {branch}")

    def check_all_sub_dirs(self, parent_dir, branch):
        """Check out all sub dirs to given branch"""
        path = parent_dir if parent_dir else 'module'
        branch = branch if branch else 'diyidan-master'
        for x in self.get_all_sub_dirs(path):
            module_dir = os.path.join(self.diyidan, path, x)
            if branch in self.list_branch(module_dir):
                # print('---'*3, x)
                # print(self.list_branch(module_dir))
                print(x)
                self.check_out(module_dir, branch)
                sleep(0.2)
                print()
                # print('==='*3, x)
                # print(self.list_branch(module_dir))

    def check_all_modules(self, branch):
        """Check out all modules to given branch"""
        self.check_all_sub_dirs('module', branch)

    def check_all_servers(self, branch):
        """Check out all servers to given branch"""
        self.check_all_sub_dirs('server', branch)

    def run(self):
        """Run server"""
        branch = 'diyidan-master'
        self.check_all_modules(branch)
        # self.check_all_servers(branch)


def main():
    g = G()
    g.run()


if __name__ == '__main__':
    main()
