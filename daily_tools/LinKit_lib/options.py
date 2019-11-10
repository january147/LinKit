#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Sun Nov 10 14:00:18 2019
# Author: January

# 读取输入的选项
# deprecated
def get_options():
    import sys
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

# option type
# 1 short option
#   A short option consists of only one letter and starts with "-".Several short options can be jointed together with only one prefix "-".
#   e.g. -a -b -abc -d
# 2 long option
#   A long option consists of several letters and starts with "--".
#   e.g. --input --ouput
# 3 argument
#   Both types of options can have arguments, which should exactly follow the option.
#   e.g. --input input.txt
#        -f file.txt
#         
# option_list
#
#   Put an single ':' in option_list to indicate accepting all options.
#   e.g. [':','a','b', 'c:']('a' and 'b' are useless, but 'c:' suggests option c needs an argument)
#
#   Put an ':' behind an option to indicate that option requires an argument
#   e.g. ['input:', 'output:']
#    
# Note: when one error occurred, get_options will call exit(1) to exit the program.

def get_options_v2(args, option_list:list):
    arg_p = 1
    total_arg = len(args)
    options = {}
    raw_arg = []
    options_with_arg = []
    accpet_all = False
    for i in range(len(option_list)):
        option_description = option_list[i]
        if option_description == ':':
            accpet_all = True
            continue
        if option_description[-1] == ':':
            option = option_description[:-1]
            options_with_arg.append(option)
            option_list[i] = option


    while arg_p < total_arg:
        arg = args[arg_p]
        if arg.startswith('--'):
            name = arg[2:]
            if not accpet_all and name not in option_list:
                print("invalid option '%s', pos '%d'"%(name, arg_p))
                exit(1)
            if name not in options_with_arg:
                options[name] = ''
            else:
                arg_p += 1
                if arg_p >= len(args) or args[arg_p].startswith('-'):
                    print("option '%s' requires an argument, pos %d"%(name, arg_p))
                    exit(1)
                value = args[arg_p]
                options[name] = value
        elif arg.startswith('-'):
            names = arg[1:]
            if len(names) <= 1:
                name_likely_with_arg = names
            else:
                for name in names[:-1]:
                    if not accpet_all and name not in option_list:
                        print("invalid option '%s', pos %d"%(name, arg_p))
                        exit(1)
                    if name in options_with_arg:
                        print("option '%s' requiring an argument can be put between options, pos %d"%(name, arg_p))
                        exit(1)
                    options[name] = ''
                name_likely_with_arg = names[-1]
            if not accpet_all and name_likely_with_arg not in option_list:
                print("invalid option '%s', pos %d"%(name_likely_with_arg, arg_p))
                exit(1)
            if name_likely_with_arg not in options_with_arg:
                options[name_likely_with_arg] = ''
            else:
                arg_p += 1
                if arg_p >= len(args) or args[arg_p].startswith('-'):
                    print("option '%s' requires an argument, pos %d"%(name_likely_with_arg, arg_p))
                    exit(1)
                value = args[arg_p]
                options[name_likely_with_arg] = value
        else:
            raw_arg.append(arg)
        arg_p += 1

    return (raw_arg, options)

def main():
    pass
if __name__ == "__main__":
    main()
