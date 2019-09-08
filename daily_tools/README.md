# abspath
根据输入的相对路径输出绝对路径

# stamp

## 简介
根据文件后缀名给已经存在的可执行脚本自动加上`#!/bin/bash`等解释器信息以及创建时间，作者等等。添加的作者名可以在脚本中进行修改。如果文件不存在，则会新建该名称的文件。

## 用法

```bash
stamp <文件名>
```

## 选项

目前不支持选项

# journal

## 简介

生成一个以当前日期命名和输入标题命名的markdown文件

## 用法

```bash
journal
```

## 选项

目前不支持选项

# create_entry

## 简介

用于建立一个`.desktop`文件

# 用法

```bash
create_entry <软件名称> [选项]
# 软件名称中空格会被下划线替代后生成.desktop文件的文件名
```

## 选项

-s <start_cmd>

-i <icon_path>

-t <type> type一般为Application，还可以Link和Directory

-T <is_in_terminal> 该选项的参数只能是true或者false

# setup
用于在重装系统后完成自动配置

# backup2oss
用于打包一个目录并上传到阿里云oss