#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @name   : find_target.py
# @author : cat
# @date   : 2017/8/2.

import os


def bash_shell(bash_command):
    """
    python 中执行 bash 命令
    :param bash_command:
    :return: bash 命令执行后的控制台输出
    """
    try:
        return os.popen(bash_command).read().strip()
    except:
        return None


def find_target(target_path="./../", key='.git'):
    """
    查找目标目录所在的目录 ： 如 ／aa/bb/.git --> return /aa/bb/
    :param target_path:
    :param key: target
    :return:
    """
    walk = os.walk(target_path)
    for super_dir, dir_names, file_names in walk:
        for dir_name in dir_names:
            if dir_name == key:
                dir_full_path = os.path.join(super_dir, dir_name)
                # print(dir_full_path, super_dir, dir_name, sep=" ## ")
                yield super_dir


if __name__ == '__main__':
    for repo_path in find_target('/Users/cat/Desktop/testGit/a6', key='.repo'):
        print('find repo in -->', repo_path)

    for git_path in find_target('/Users/cat/Desktop/testGit/a6', key='.git'):
        print('find git in -->', git_path)
        # print(bash_shell('git config --global core.filemode false'))
    # test for bash_command
    # print(bash_shell('git init'))
    # print(bash_shell('ls -al'))
    pass
