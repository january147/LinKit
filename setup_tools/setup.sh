#!/bin/bash

# script used when reinstalling a Linux system
vscode_link='https://vscode.cdn.azure.cn/stable/c47d83b293181d9be64f27ff093689e8e7aed054/code_1.42.1-1581432938_amd64.deb'
wps_link='https://wdl1.cache.wps.cn/wps/download/ep/Linux2019/8865/wps-office_11.1.0.8865_amd64.deb'
tinytex='https://yihui.name/gh/tinytex/tools/install-unx.sh'
sogopinyin_link='http://cdn2.ime.sogou.com/dl/index/1571302197/sogoupinyin_2.3.1.0112_amd64.deb?st=dFOGMcxat_CQa76fnrZdhg&e=1583505695&fn=sogoupinyin_2.3.1.0112_amd64.deb'
chrome_link='https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'

download_dir=~/Downloads
log='setup.log'
startup_setup_script="./creat_startup.sh"

# put a ":" before a name to skip it
# !!!DO NOT remove the backslash after "="!!!
apt_setup_list_cmd=\
(
    :wget 
    gcc 
    g++ 
    pip3 
    ipython3 
    java 
    hexedit
)
apt_setup_list=(wget gcc g++ python3-pip ipython3 openjdk-8-jdk hexedit)

# download deb files and use apt to install them
deb_name_list=\
(
    :chrome 
    :vscode 
    :wps 
    :sogopinyin
)

deb_download_link=("$chrome_link" "$vscode_link" "$wps_link" "$sogopinyin_link")

# download installers and run them to install applications
installer_list=()
installer_download_link=()

# download seperate executable files(e.g. tar.gz) and put them to $HOME/app
binary_list=()
binary_download_link=()

# The default choice is not to exit.
# param: <default choose>
function prompt_exit(){
    read input
    [ -n "$1" ] && choose="$1"
    [ -n "$input" ] && choose="$input"
    [ -z "$choose" ] && choose="y"
    if [ "$choose" != "n" ];then
        exit 1
    fi
}

function prompt_continue(){
    read input
    [ -n "$1" ] && choose="$1"
    [ -n "$input" ] && choose="$input"
    [ -z "$choose" ] && choose="y"
    if [ "$choose" != "y" ];then
        exit 1
    fi
}

function check_fail() {
    if [ $? -ne 0 ]; then
        echo 'failed' >> $log
        echo -n 'An error occurred, continue?(y/n)(default y)'
        prompt_continue y
    else
        echo "ok" >> $log
    fi
}

function should_install() {
    if [ -z "$1" ];then
        echo "no name specified"
        return 0
    fi
    # test command
    type $1 > /dev/null 2>&1
    if [ $? -eq 0 ];then
        echo "$1 already installed"
        return 1
    else
        return 0
    fi
}

echo `date +%Y-%m-%d_%H:%M:%S` > $log

# echo 'updating source...' | tee $log
# sudo apt update > /dev/null
# check_fail

echo "################apt install##################"
for i in ${!apt_setup_list_cmd[@]}
do
    cmd_name=${apt_setup_list_cmd[i]}
    package_name=${apt_setup_list[i]}
    if [[ $cmd_name == :* ]];then
        continue
    fi
    if should_install $cmd_name;then
        echo "install $cmd_name($package_name)" | tee $log
        sudo apt install $package_name
        check_fail
    fi
done
echo "#############finish apt install###############"

echo "################download deb##################"
for i in ${!deb_download_link[@]}
do
    link=${deb_download_link[i]}
    name=${deb_name_list[i]}.deb
    if [[ $name == :* ]];then
        continue
    fi
    if [ -f $download_dir/$name ];then
        echo "$name already exists"
        continue
    fi
    echo "start download $name"
    #wget $link -O $download_dir/$name
    check_fail
done
echo "#############finish download##################"

echo "################install deb###################"
for i in ${!deb_name_list[@]}
do
    name=${deb_name_list[i]}.deb
    if [[ $name == :* ]];then
        continue
    fi
    if [ ! -f $download_dir/$name ];then
        echo "No such file [$name], can't install"
        continue
    fi
    echo "start install $name"
    sudo apt install $download_dir/$name
    check_fail
done
echo "############finish install deb################"



# echo 'install typora' | tee $log
# wget -qO - https://typora.io/linux/public-key.asc | sudo apt-key add -
# # add Typora's repository
# sudo add-apt-repository 'deb https://typora.io/linux ./'
# sudo apt update > /dev/null
# # install typora
# sudo apt install typora > /dev/null
# check_fail

# echo 'install TinyTex' | tee $log
# wget -qO- "https://yihui.name/gh/tinytex/tools/install-unx.sh" | sh
# check_fail

# do some other configuration

echo 'create startup directory' | tee $log
[ -x $startup_setup_script ] && $startup_setup_script
check_fail

echo 'create workplace' | tee $log
[ -e ~/workplace ] || mkdir ~/workplace
check_fail
