#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @name   : find_target.py
# @author : cat
# @date   : 2017/8/2.

import os
import multiprocessing
import time


def bash_shell(bash_command):
    """
    python 中执行 bash 命令
    :param bash_command:
    :return: bash 命令执行后的控制台输出
    """
    try:
        print("bash_command = {}".format(bash_command))
        return os.popen(bash_command).read().strip()
    except Exception:
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
                yield super_dir


def execute(semaphore, msg, command='ls -a', path="./"):
    try:
        semaphore.acquire()
        # print(msg)
        # time.sleep(1)
        print(bash_shell(command))
    finally:
        semaphore.release()


if __name__ == '__main__':
    s_time = time.time()

    s = multiprocessing.Semaphore(10)

    command_path = '/Users/cat/Desktop/testGit/a6'
    # target_path = '/'
    for repo_path in find_target(command_path, key='.repo'):
        os.chdir(repo_path)  # todo: the key code !!!
        msg = 'find repo in -->{}'.format(repo_path)
        p = multiprocessing.Process(target=execute,
                                    args=(s, msg,),
                                    kwargs={'command': 'pwd', 'path': repo_path})
        p.daemon = True
        p.start()
        p.join()
    for git_path in find_target(command_path, key='.git'):
        os.chdir(git_path)
        msg = 'find git in -->{}'.format(git_path)
        p = multiprocessing.Process(target=execute,
                                    args=(s, msg,),
                                    kwargs={'command': 'pwd', 'path': git_path})
        p.daemon = True
        p.start()
        p.join()
    e_time = time.time()

    print("spend time : {:.3f} seconds".format(e_time - s_time))
    print('end ', "#" * 20, " end")
    # print(bash_shell('ls -al'))
    pass
