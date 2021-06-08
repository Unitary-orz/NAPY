

# Python 命令行参数模块

[TOC]

## 命令行参数

>在命令行中给运行的脚本加参数就是命令行参数。（即从输入位置角度理解）。



eg:

![mark](http://cdn.youyouorz.top/blog/img/20190509/zEGkhTtCDpAq.png?imageslim)

## sys.argv

> 以列表形式储存命令行参数

测试代码`argv_test.py`
```python
import sys

args = sys.argv
print(args)
```
命令行下
```
$ python argv_test.py
['argv_test.py']
$ python argv_test.py Hello 
['argv_test.py', 'Hello']
$ python argv_test.py Hello Word
['argv_test.py', 'Hello','Word']
```

测试代码`argv_test.py`

```python
import sys

args = sys.argv[1]
print(args)
```

命令行下

```
$ python argv_test.py Hello 
Hello
$ python argv_test.py Word
Word
```

`argv[0]` 脚本名

`argv[1]`第一个参数

`argv[2]`第二参数

[.....]

## argparse

> argparse 是 Python 内置的一个用于命令项选项与参数解析的模块,argparse 将会从 sys.argv 中解析出这些参数，并自动生成帮助和使用信息。也是**Python官方推荐使用的模块**

### 简单示例

定位参数

> 以位置的顺序来决定参数

```python
import argparse

parser = argparse.ArgumentParser() #创建ArgumentParser()对象
parser.add_argument('test')  #调用 add_argument() 方法添加参数
args = parser.parse_args() #使用 parse_args()解析出参数

print(args.test)
```

命令行

```
$ python argparse_test.py Hello
Hello
$ python argparse_test.py -h
usage: argparse_test.py [-h] test

positional arguments:
  test

optional arguments:
  -h, --help  show this help message and exit
```

可选参数

```python
import argparse

parser = argparse.ArgumentParser() #创建ArgumentParser()对象
parser.add_argument('--test')  #调用 add_argument() 方法添加参数
args = parser.parse_args() #使用 parse_args()解析出参数

print(args.test)
```

```
$ python argparse_test.py --test Hello
Hello
$python argparse_test.py -h
usage: argparse_test.py [-h] [--test TEST]

optional arguments:
  -h, --help   show this help message and exit
  --test TEST
```

简写加帮助信息

```python
parser.add_argument('-t','--test',help='This is a test')
```

```
$ python argparse_test.py --t Hello
Hello
$ python argparse_test.py -h
usage: argparse_test.py [-h] [-t TEST]

optional arguments:
  -h, --help            show this help message and exit
  -t TEST, --test TEST  This is a test
```

### 方法说明

**argparse.ArgumentParser()** 

> 创建一个新[ArgumentParser](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser)对象

部分参数

- [usage](https://docs.python.org/3/library/argparse.html#usage) - 描述程序用法的字符串（默认值：从添加到解析器的参数生成）
- [description](https://docs.python.org/3/library/argparse.html#description) - 参数help之前显示的文本（默认值：none）
- [epilog](https://docs.python.org/3/library/argparse.html#epilog) - 参数help后显示的文本（默认值：none）

```python
#!/usr/bin/env python3
# -*- coding:utf-8 -*

import argparse

parser = argparse.ArgumentParser(usage='1',description='2',epilog='3')
parser.add_argument('-t','--test',help='This is a test')

print(parser.parse_args().test)
```

```
python argparse_test.py -h
usage: 1

2

optional arguments:
  -h, --help            show this help message and exit
  -t TEST, --test TEST  This is a test

3
```

**ArgumentParser.add_argument()**

> 定义应如何解析单个命令行参数。

部分参数

- [*name or flags*](https://docs.python.org/3/library/argparse.html#name-or-flags) - 选项字符串的名称或列表，例如`foo` 或。`-f, --foo`
- [action](https://docs.python.org/3/library/argparse.html#action) - 在命令行遇到此参数时要采取的基本操作类型。
- [nargs](https://docs.python.org/3/library/argparse.html#nargs) - 应该使用的命令行参数的数量。
- [const](https://docs.python.org/3/library/argparse.html#const) - 某些[操作](https://docs.python.org/3/library/argparse.html#action)和[nargs](https://docs.python.org/3/library/argparse.html#nargs)选择所需的常量值。
- [default](https://docs.python.org/3/library/argparse.html#default) - 如果命令行中不存在参数，则生成的值。
- [type](https://docs.python.org/3/library/argparse.html#type) - 应转换命令行参数的类型。
- [choices](https://docs.python.org/3/library/argparse.html#choices) - 参数允许值的容器。
- [required](https://docs.python.org/3/library/argparse.html#required) - 是否可以省略命令行选项（仅限选项）。
- [help](https://docs.python.org/3/library/argparse.html#help) - 对参数的作用的简要说明。

- [metavar](https://docs.python.org/3/library/argparse.html#metavar) - 用法消息中参数的名称。
- [dest](https://docs.python.org/3/library/argparse.html#dest) - 要添加到返回的对象的属性的名称 [parse_args()](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.parse_args)。

**action**

在命令行遇到此参数时要采取的基本操作类型。

* `store_true` 参数存在,值为True
* `store_false` 参数存在,值为False

store_true

```python
parser.add_argument('-t','--test',action='store_true',help='This is a test')
```

```
$ python argparse_test.py -t
True
```
store_false
```python
parser.add_argument('-t','--test',action='store_false',help='This is a test')
```

```
$ python argparse_test.py -t
False
```

**nargs**

命令行参数的数量,默认为1

```python
parser.add_argument('-t','--test',nargs=2,help='This is a test')
```



```
$ python argparse_test.py -t 1 2
['1', '2']
```



**default**

默认值

```python
parser.add_argument('-t','--test',default='Hello',help='This is a test')
```

```
$ python argparse_test.py -t 
Hello
```

**choices**

指定参数选择

```python
parser.add_argument('-t','--test',choices=['Hello','Word'],help='This is a test')
```

```
$ python argparse_test.py -t 1
usage: 1
argparse_test.py: error: argument -t/--test: invalid choice: '1' (choose from 'Hello', 'Word')
$ python argparse_test.py -t Hello
a
```

**required**

```python
parser.add_argument('-t','--test',choices=['a','b'],help='This is a test')
```

```
$ python argparse_test.py
usage: 1
argparse_test.py: error: argument -t/--test is required
$ python argparse_test.py -t Hello
Hello
```

[Python argparse.ArgumentParser() Examples](<https://www.programcreek.com/python/example/748/argparse.ArgumentParser>)

**参考**

[argparse - Python 3.7.3 documentation](<https://docs.python.org/3/library/argparse.html>)

## optparse

> 命令行选项的解析器

### 简单示例

```python
import optparse

parser = optparse.OptionParser()
parser.add_option('-t','--test',dest='testname',help = 'This is test')
option,args=parser.parse_args()
print(option)
print(args)
print(option.testname)
```



```
$ python optarse_test.py -t 1
{'testname': '1'}
[]
1
$ python optarse_test.py -t 1 2
{'testname': '1'}
['2']
1
$ python optarse_test.py -h
Usage: optarse_test.py [options]

Options:
  -h, --help            show this help message and exit
  -t TESTNAME, --test=TESTNAME
                        This is test
```

### 方法说明

**optparse.OptionParser()**

> 创建解析器

部分参数

- usage - 描述程序用法的字符串（默认值：脚本名 [options]）
- description - 参数help之前显示的文本（默认值：none）
- epilog - 参数help后显示的文本（默认值：none）



 **OptionParser.add_option()**

>  定义选项属性

* action - 在命令行遇到此参数时要采取的基本操作类型。
* nargs - 应该使用的命令行参数的数量。
* const - 某些操作和nargs选择所需的常量值。
* default - 如果命令行中不存在参数，则生成的值。
* type - 应转换命令行参数的类型。
* choices - 参数允许值的容器。
* help - 对参数的作用的简要说明。
* metavar - 用法消息中参数的名称。 
* dest - 要添加到返回的对象的属性的名称 parse_args()。



**parse_args()** 

返回两个值

* options -  一个包含所有选项值的对象

* args - 解析选项后剩余的位置参数列表



**参考**

 [optparse - Python 3.7.3 documentation](https://docs.python.org/3/library/optparse.html)

## getopt

> 命令行选项的C语言风格解析器



**getopt.getopt（args，shortopts，longopts = [] ）**

> 返回两个值,第一个选项值列表,第二个剩下的参数列表

* args - 是要解析的参数列表
* shortopts - 短选项 eg:h
* longopts - 长选项 eg:help

当短选项需要接受值是后面加`:` 

```python
opts, args = getopt.getopt(sys.argv[1:], "h:")
```

当长选项需要接受值是后面加`=`

```python
opts, args = getopt.getopt(sys.argv[1:], "h:", ["help="])
```

**getopt.GetoptError**

> 当在参数列表中找到无法识别的选项或者没有给出需要参数的选项时，会引发此问题。

**示例**

```python
import getopt,sys

try:
    opt,args = getopt.getopt(sys.argv[1:],'t:h',['test=','help'])
except getopt.GetoptErrot as err:
    print(err)
    sys.exit(2) #2 表示shell命令错误
for o,a in opt:
    if o in ('-h','--help'):
        print('eg: -t Hello')
    elif o in ('-t','--test'):
        test = a
print(a)
```

```
$ python getopt_test.py -t Hello
Hello
$ python getopt_test.py -h
eg: -t Hello
```

