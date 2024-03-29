# Data-Processing-Toolkit

Data Processing Toolkit (DPT)是一个用来处理计算结束后数据的一个工具包。目前版本为测试版0.8.3，尚未成为正式版，因此如有出现bug、或者想要添加某些功能，可以联系邮箱hanpu-liang@cumt.edu.cn进行反馈。

## 引用

若使用该软件，请引用以下几篇文章：

1. Hanpu Liang, et al. The Journal of Physical Chemistry Letters 12, 10975 (2021). DOI: 10.1021/acs.jpclett.1c03248
2. Hanpu Liang, et al. Nanoscale 13, 11994 (2021). DOI: 10.1039/D1NR02548A

## 环境

shell版本: bash

python版本: python2.7及以后。目前要求有numpy库。

## 获取安装包

利用命令行端输入

```sh
$ wget -N --no-check-certificate https://github.com/HanpuLiang/Data-Processing-Toolkit/tree/master/public/DPT-0.8.3.tar.gz
```

## 安装

解压安装包

```shell
$ tar -zxcf DPT-0.4.tar.gz
```

进入文件夹并修改安装脚本中各路径，如VASP, MPI等

```shell
$ vim install.sh
```

运行安装脚本

```shell
$ cd DPT-0.4
$ sh install.sh
```

若没有报错，则安装成功。重启终端即可运行。

## 运行示例

新建文件夹test/

```shell
$ mkdir test
```

将示例文件复制其中

```shell
$ cp ../DPT-0.4/example/electronic_structure/* . -rf
```

运行软件

```shell
$ DPT -b
$ DPT -d
$ DPT -f
```

## licence

MIT License

Copyright (c) 2019 Hanpu Liang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
