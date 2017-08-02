# git_file_mode_ignore
通过python脚本对多个git仓库进行文件mode忽略对批处理

* (背景)[http://blog.csdn.net/ducklikejava/article/details/76600869]

* 正文：

最近公司将源码从`svn`切换到`git`上去管理了。但是不幸的是，貌似`git`没有配置好，没有忽略文件的`mode`。

这样一来就麻烦了，一旦你修改了文件权限，`git`就会认为你修改了该文件。这样，你就得回退，或者提交很多无关文件。

**正确的姿势是：`git config --global core.filemode false`**

但是源码下面的`.git`仓库很多，如果要一个个找到，然后一个个修改是很麻烦的事情。于是，想到使用脚本去执行这个事情。

> *原本是想使用shell去做这件事情的，但是对shell的语法完全不熟悉，看了一会感觉很像windows下的.bat脚本的语法。于是放弃了，因为表达力不足。*

思来想去，虽然`java`最熟悉，但是，怎么把`java`当成脚本使用倒是不会。还是使用`python`吧，反正这种`python`脚本应该很容易实现。

于是，就有了如下代码：

```python
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
        print(bash_shell('git config --global core.filemode false'))
    # test for bash_command
    # print(bash_shell('git init'))
    # print(bash_shell('ls -al'))
    pass

```

> 为了验证代码的正确性，我在本地大致模拟了一些源码的目录结构：
```tree
catde:a6 cat$ tree -a
.
├── .repo
├── frameworks
│   └── base
│       ├── .git
│       ├── core
│       └── libs
├── out
├── packages
│   ├── .gitignore
│   ├── android.mk
│   └── apps
│       ├── Email
│       │   ├── .git
│       │   ├── bin
│       │   ├── res
│       │   └── src
│       │       └── HelloWorld.java
│       ├── Music
│       │   ├── .git
│       │   ├── bin
│       │   ├── res
│       │   └── src
│       │       └── HelloWorld.java
│       └── Settings
│           ├── .git
│           ├── aaa.xds
│           ├── byd
│           └── readme.txt
└── vender
    └── customer
        └── .git

25 directories, 6 files

catde:a6 cat$ pwd
/Users/cat/Desktop/testGit/a6
```

于是，执行之后的输出如下：

```python
find repo in --> /Users/cat/Desktop/testGit/a6
find git in --> /Users/cat/Desktop/testGit/a6/frameworks/base
find git in --> /Users/cat/Desktop/testGit/a6/packages/apps/Email
find git in --> /Users/cat/Desktop/testGit/a6/packages/apps/Music
find git in --> /Users/cat/Desktop/testGit/a6/packages/apps/Settings
find git in --> /Users/cat/Desktop/testGit/a6/vender/customer

```

通过输出可以看到，所有的`.repo`以及`.git`目录所在目录是已经找出来了。然后执行`bash_commad(command)`即可完成对文件`mode`的忽略。
