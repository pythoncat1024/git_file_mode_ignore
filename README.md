# git_file_mode_ignore
通过python脚本对多个git仓库进行文件mode忽略对批处理

* (背景)[http://blog.csdn.net/ducklikejava/article/details/76600869]

* 正文：

** git镇楼：`git config --global core.filemode false`**

* **如何利用`python`执行`bash`脚本？**
* **如何像`cd xxx/`一样任性跳转目录执行`bash`命令？**

**这两个问题解决了，才算是解决了使用`python`脚本执行`bash`命令的全部痛点。**

一一解答：
> 1. 如何利用`python`执行`bash`脚本？
* `os.popen(bash_comand)`即可
> 2. 如何像`cd xxx/`一样任性跳转目录执行`bash`命令？
* `os.chdir(path)`就如同`cd xxx/`一般，可以任性地切换到任意目录

于是，就有了如下代码   ：
   
```
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

```

于是，执行之后的输出如下：

```python

bash_command = pwd
/Users/cat/Desktop/testGit/a6
bash_command = pwd
/Users/cat/Desktop/testGit/a6/frameworks/base
bash_command = pwd
/Users/cat/Desktop/testGit/a6/packages/apps/Email
bash_command = pwd
/Users/cat/Desktop/testGit/a6/packages/apps/Music
bash_command = pwd
/Users/cat/Desktop/testGit/a6/packages/apps/Settings
bash_command = pwd
/Users/cat/Desktop/testGit/a6/vender/customer
spend time : 0.096 seconds
end  ####################  end

Process finished with exit code 0

```

通过输出可以看到，所有的`.repo`以及`.git`目录所在目录是已经找出来了。然后执行`bash_commad(command)`即可在仓库目录执行`git / repo`命令了。
