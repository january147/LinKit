#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Sun Sep 15 15:33:53 2019
# Author: January

import re
import sys

usage = '''There are two usages.
1. translate normal math block format to youdao note math block format:
trans_md -n <normal format markdown>
2. translate youdao note math block to normal math block format
trans_md -y <youdao note format markdown>
Note: trans_md won't delete the original file and the newly generated file will be named as the original filename with a "new_" prefix.
'''

# 读取输入的选项
def get_options():
    options = dict()
    option_name = ''
    no_name_options_count = 0
    waiting_for_value = False
    for item in sys.argv[1:]:
        if(item.startswith('-')):
            option_name = item
            waiting_for_value = True
            options[option_name] = ''
        else:
            if waiting_for_value is True:
                options[option_name] = item
            else:
                options[no_name_options_count] = item
                no_name_options_count = no_name_options_count + 1
    return options

def inline_trans(op, line):
    result=[]
    if op == '-y':
        start_pos = -1
        state = 0
        escape = False
        for letter in line:
            if escape:
                escape = False
            elif letter == '\\':
                escape = True
            elif state == 0:
                if letter == '`':
                    state = 1
                    start_pos = len(result)
            elif state == 1:
                if letter == '$':
                    state = 2
                else:
                    state = 0
            elif state == 2:
                if letter == '$':
                    state = 3
                if letter == '`':
                    state = 0
            elif state == 3:
                if letter == '`':
                    if start_pos != -1:
                        # 清空前面的`号
                        result[start_pos] = ' '
                    state = 0
                    # 去掉`号
                    continue
            result.append(letter)
    elif op == '-n':
        start_pos = -1
        state = 0
        escape = False
        for letter in line:
            if escape:
                escape = False
            elif letter == '\\':
                escape = True
            elif state == 0:
                if letter == '$':
                    result.append('`')
                    state = 2
                elif letter == '`':
                    state = 1
            elif state == 1:
                state = 0
            elif state == 2:
                if letter == '$':
                    state = 3
            elif state == 3:
                if letter != '`':
                    result.append('`')
                    state = 0
            result.append(letter)

    return ''.join(result)


def main():
    youdao_format_start = '```math\n'
    youdao_format_end = '```\n'
    normal_format_start = '$$\n'
    normal_format_end = '$$\n'
    options = get_options()

    if '-y' in options.keys():
        filename = options['-y']
        search_s = youdao_format_start
        search_e = youdao_format_end
        replace_s = normal_format_start
        replace_e = normal_format_end
        op = '-y'
    elif '-n' in options.keys():
        filename = options['-n']
        search_s = normal_format_start
        search_e = normal_format_end
        replace_s = youdao_format_start
        replace_e = youdao_format_end
        op = '-n'
    else:
        print(usage)
        exit(1)

    file = open(filename, 'r')
    new_file = open('new_' + filename, 'w')
    math_start = False
    lines = file.readlines()
    for line in lines:
        if (not math_start) and line.strip(' ') == search_s:
            math_start = True
            new_file.write(replace_s)
        elif math_start and line.strip(' ') == search_e:
            math_start = False
            new_file.write(replace_e)
        else:
            new_file.write(inline_trans(op, line))
    file.close()
    new_file.close()

if __name__ == '__main__':
    main()
