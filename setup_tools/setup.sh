# script used when reinstalling a Linux system

vscode_link='https://vscode.cdn.azure.cn/stable/c47d83b293181d9be64f27ff093689e8e7aed054/code_1.42.1-1581432938_amd64.deb'
wps_link='https://wdl1.cache.wps.cn/wps/download/ep/Linux2019/8865/wps-office_11.1.0.8865_amd64.deb'
download_dir=~/Download
log='setup.log'
startup_setup_script='./create_startup.sh'
setup_list=(wget gcc g++ pip3 ipython3 java vscode typora wps)

# The default choice is not to exit.
function prompt_exit(){
    read choose
    if [ "$choose" = "n" ];then
        exit 1
    fi
}

function check_fail() {
    if [ $? -ne 0 ]; then
        echo 'failed' >> $log
        echo -n 'An error occurred, should continue?(y/n)'
        prompt_exit
    else
        echo "ok" >> $log
    fi
}

function in_setup_list() {
    if [ -z $1 ];then
        echo "no name specified"
        return 0
    fi
    for item in ${setup_list[@]}
    do
        [ $1 = $item ] && return 0
    done
    return 1
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

if should_install wget;then
    echo 'install wget' | tee $log
    sudo apt install wget > /dev/null
    check_fail
fi

if should_install git;then
    echo 'install git...' | tee $log
    sudo apt install git > /dev/null
    check_fail
fi

if should_install g++;then
    echo 'install g++' | tee $log
    sudo apt install g++ > /dev/null
    check_fail
fi

if should_install pip3;then
    echo 'install pip' | tee $log
    sudo apt install python3-pip > /dev/null
    check_fail
fi

if should_install java;then
    echo 'install jdk' | tee $log
    sudo apt install openjdk-8-jdk > /dev/null
    check_fail
fi

# install non-apt software

echo 'install vscode' | tee $log
wget $vscode_link -O $download_dir/vscode.deb
sudo apt install $download_dir/vscode.deb > /dev/null
check_fail

echo 'install typora' | tee $log
wget -qO - https://typora.io/linux/public-key.asc | sudo apt-key add -
# add Typora's repository
sudo add-apt-repository 'deb https://typora.io/linux ./'
sudo apt update > /dev/null
# install typora
sudo apt install typora > /dev/null
check_fail

echo 'install wps' | tee $log
wget $wps_link -O $download_dir/wps.deb
sudo apt install $download_dir/wps.deb > /dev/null
check_fail

echo 'install TinyTex' | tee $log
wget -qO- "https://yihui.name/gh/tinytex/tools/install-unx.sh" | sh
check_fail

# do some other configuration

echo 'create startup directory' | tee $log
[ -x $startup_setup_script ] && $startup_setup_script
check_fail

echo 'create workplace' | tee $log
mkdir ~/workplace
check_fail
