#!/bin/bash

# 监视目录更改
monitor_dir() {
  dir_path=$1
  #set_time=$2
  #recipient_email=$2
  Do_What="inotifywait:monitor_dir"

  inotifywait -m -r --format '%e %w%f' "$dir_path" | while read event file; do
    #echo "$event happened on $file" | send_email  "$recipient_email" &
  # if [ "$event" == "MODIFY" ]; then
  #   echo "File $file was modified."
  # elif [ "$event" == "CREATE" ]; then
  #   echo "File $file was created."
  # elif [ "$event" == "MOVED_FROM" ]; then #delete
  #   echo "File $file was MOVED_FROM."
  # elif [ "$event" == "OPEN" ]; then
  #   echo "File $file was OPEN."
  # fi
    #echo "$event happened on $file"  
    #sleep 10
  if [ "$event" == "MODIFY" ]; then
    echo "File $file was MODIFY." | send_email   "$Do_What"  &
    echo "File $file was MODIFY." | send_notification &

  elif [ "$event" == "MOVED_FROM" ]; then
    echo "File $file was MOVED_FROM." | send_email   "$Do_What" &
    echo "File $file was MOVED_FROM." | send_notification &
  elif [ "$event" == " " ]; then
    cho "$event"
  fi

  done
}

# 监控CPU内存使用情况
monitor_system() {
  fortime=$1
  threshold_mem=70
  #threshold_mem1 ="inotifywait:123"

while true; do
  # 获取当前内存使用情况  
  #mem_usage=$(free | awk '/Mem/ {printf "%d\n", $3/$2 * 100.0}')

  mem_usage=$(free -m | awk 'NR==2{printf "%s\n", $3*100/$2 }')
  # 检查内存使用率是否高于阈值
  if [ "$(echo "$mem_usage >= $threshold_mem" | bc)" -eq 1 ]; then
    echo "检测到内存使用率较高: $mem_usage%" | send_email   "monitor_system" &
    echo "检测到内存使用率较高: $mem_usage%" | send_notification &
  else
    echo "当前内存使用 : $mem_usage%"  | send_email   "monitor_system" &
    echo "当前内存使用 : $mem_usage%"  | send_notification &
  fi

  sleep $fortime
  sleep 60
done
}

# 监控过程状态
monitor_process() {
  process_name=$1
  Do_What="monitor_process"

  while true; do
    if [ -z "$(pidof "$process_name")" ]; then
      echo "$process_name δ����" | send_email   "$Do_What"  &
      echo "$process_name δ����" | send_notification &
      #break
    else
      echo "$process_name ������" | send_email   "$Do_What"  &
      echo "$process_name ������" | send_notification &
    fi

    #time 
    sleep 60
  done
}

# 监控软件版本
monitor_version() {
  process_name=$1
  Do_What="monitor_version"

  while true; do
    local_version=$(dpkg -s "$process_name" | grep "Version" | awk '{print $2}')
    server_version=$(apt-cache policy ${process_name} | awk '/Installed/ {print $2}')

    echo "local_version = $local_version"
    echo "server_version = $server_version"
0
    if [ "$local_version" != "$server_version" ]; then
      echo "${process_name} 版本已过时，当前版本为 ${local_version}, 最新版本为 ${server_version}." | send_email   "$Do_What"  &
      echo "${process_name} 版本已过时，当前版本为 ${local_version}, 最新版本为 ${server_version}." | send_notification &

    else
      echo "${process_name} 版本是最新的，当前版本是 ${local_version}." | send_email   "$Do_What"  &
      echo "${process_name} 版本是最新的，当前版本是 ${local_version}." | send_notification &

    fi
    sleep 3600
  done
}

# 发送邮件通知
send_email() {
  #recipient_email=$1
  recipient_email="1843259704@qq.com"
  email_content=$1
  message=$(cat)
  if [ -n "$recipient_email" ] && [ -n "$message" ]; then
    echo "$email_content:$message"  | s-nail -s "来自某台虚拟机..." $recipient_email
  fi
}

send_notification() {
  #message=$1
  message=$(cat)
  notify-send "$message"
  # 发送邮件
  echo "$message"  
}

usage() {
    echo "Usage(用法功能):"
    echo "args(参数)": ["-m" ,"dirpath" ,"-t" ,"time" ,"-p" ,"processname" ,"-v " ,"processname"]
    exit -1
}
 

if [ $# -lt 2 ]; then
  usage
fi



 
while getopts 'm:t:p:v:a:b:c:i' OPT; do
    case $OPT in
        m) dir_path="$OPTARG";;
        t) monitor_system_time="$OPTARG";;
        p) process_name="$OPTARG";;
        v) version_process_name="$OPTARG";;
        # a) email_address=$OPTARG;;
        # b) email_password=$OPTARG;;
        c) recipient_email=$OPTARG;;
        ?) usage;;
    esac
done



#sh detection.sh -m /root//myq2    -t 10     -p firefox  -v firefox  -c 1843259704@qq.com 

#1.通过命令行参数指定检测某个目录，当目录文件发生改动时，输出变动信息
#sh detection.sh -m /root/linuxstudy/Q2 -c 1843259704@qq.com
if [ -n "$dir_path" ] ; then
monitor_dir "$dir_path" &
fi

#2.定时检测kali系统的CPU温度，内存使用情况，达到阈值，输出提示信息
#sh detection.sh -t 10   (s)
if [ -n "$monitor_system_time" ]; then
echo $monitor_system_time
monitor_system "$monitor_system_time"  &   
fi

#3.通过命令行参数监测某个程序进程，意外结束时，发出警告提醒
#sh detection.sh -p firefox
if [ -n "$process_name" ]; then
monitor_process "$process_name"  &   
fi

# 4.对指定的软件进行版本监控，当本地版本信息与服务端的版本信息不匹配时，输出当前版本和可更新版本
#sh detection.sh -v firefox
if [ -n "$version_process_name" ]; then
monitor_version "$version_process_name" &  
fi


wait