#!/bin/bash
#########################################################################
# File Name: AI_extrapolation.sh
# Nickname: Alice(From Chengdu.China)
# Position: IT.Engineer
# TEL: +86-17313081751
# WeChat: AliceEngineerT
# QQNumber: 489261538
# Telegram: @AliceEngineer
# E-mail(Chinese Mainland): private.profession@foxmail.com
# E-mail(Global): alice.engineer.pro@gmail.com
# Created Time: 2022年07月27日 星期三 10时01分18秒
#########################################################################

# Global Variables
PROJECT_HOME=""
CONDA_ENVIRONMENT_NAME=""

# Change User --> root
static_user() {
  if [ "$(whoami)" = root ]; then
    pass
  else
    {
      su - root
    }
  fi
}

# Change Anaconda --> $(ENVIRONMENT_NAME)
environment_config() {
  if [ "$(conda --version | wc -l)" = 1 ]; then
    conda activate "$CONDA_ENVIRONMENT_NAME"
  else
    {
      local str_a="Error: Not Found Anaconda"
      local str_b="Please install Anaconda or Add Anaconda to the environment variable (User or System)"
      printf "\033[41;37m %s \033[0m\n" "$str_a"
      printf "\033[41;37m %s \033[0m\n" "$str_b"
    }
  fi
}

run_project() {
  mkdir -p "$PROJECT_HOME"/logs
  local str_a="Please check program path"
  cd "$(PROJECT_HOME)" || printf "\033[41;37m Error: Not Found %s \033[0m\n" "$PROJECT_HOME" && printf "\033[41;37m %s \033[0m\n" "$str_a"
  nohup python -u run.py >./logs/run.log 2>&1 &
}

start_project() {
  if [ "$(pgrep run | wc -l)" = 1 ]; then
    pass
  else
    {
      run_project
    }
  fi
}

stop_project() {
  if [ "$(pgrep run | wc -l)" = 1 ]; then
    kill "$(pgrep run)"
  else
    {
      pass
    }
  fi
}

restart_project() {
  stop_project
  start_project
}

# main
set -- "$(getopt -o h --long start,stop,restart -- "$@")"
while true;
#while getopts ":a:b:c:" n;
do
  case $1 in
  --start)
    start_project;
    shift
    ;;
  --stop)
    stop_project;
    shift
    ;;
  --restart)
    restart_project;
    shift
    ;;
  -h | --help)
    printf "Usage: \n--start    Start Service\n--stop    Stop Service\n-h, --help    display this help and exit\n";
    return 0;
    shift;
    ;;
  --)
    shift;
    break
    ;;
  *)
    options_error="Invalid option"
    printf "\033[41;37m %s \033[0m\n" "$options_error"
    ;;
  esac
done

for param in "$@"; do
  echo "Param: $param"
done
