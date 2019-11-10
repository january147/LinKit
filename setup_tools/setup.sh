# script used when reinstalling a Linux system

vscode_link='https://go.microsoft.com/fwlink/?LinkID=760868'
wps_link='https://wdl1.cache.wps.cn/wps/download/ep/Linux2019/8865/wps-office_11.1.0.8865_amd64.deb'
download_dir=~/Download
log='setup.log'
startup_setup_script='./create_startup.sh'

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

echo `date +%Y-%m-%d_%H:%M:%S` > $log

echo 'updating source...' >> $log
sudo apt update
check_fail

echo 'install wget' >> $log
sudo apt install wget
check_fail

echo 'install git...' >> $log
sudo apt install git
check_fail

echo 'install g++' >> $log
sudo apt install g++
check_fail

echo 'install pip' >> $log
sudo apt install python3-pip
check_fail

echo 'install jdk' >> $log
sudo apt openjdk-8-jdk
check_fail

echo 'install vscode' >> $log
wget $vscode_link -O $download_dir/vscode.deb
sudo apt install $download_dir/vscode.deb
check_fail

echo 'install typora' >> $log
wget -qO - https://typora.io/linux/public-key.asc | sudo apt-key add -
# add Typora's repository
sudo add-apt-repository 'deb https://typora.io/linux ./'
sudo apt update
# install typora
sudo apt install typora
check_fail

echo 'install wps' >> $log
wget $wps_link -O $download_dir/wps.deb
sudo apt install $download_dir/wps.deb
check_fail

echo 'install TinyTex' >> $log
wget -qO- "https://yihui.name/gh/tinytex/tools/install-unx.sh" | sh
check_fail

echo 'create startup directory' >> $log
$startup_setup_script
check_fail

echo 'create workplace' >> $log
mkdir ~/workplace
check_fail
