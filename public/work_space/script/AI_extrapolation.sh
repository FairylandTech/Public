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
      printf "Insufficient Permissions, Use root Privileges\n"
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
  static_user
  if [ "$(pgrep run | wc -l)" = 1 ]; then
    printf "Running\n"
  else
    {
      run_project
    }
  fi
}

stop_project() {
  static_user
  if [ "$(pgrep run | wc -l)" = 1 ]; then
    kill "$(pgrep run)"
  else
    {
      printf "Please execute start\n"
    }
  fi
}

restart_project() {
  stop_project
  sleep 10
  printf "wait 10s\n"
  start_project
}

# main
while true;
do
  case $1 in
  --start)
    start_project;
    break;
    ;;
  --stop)
    stop_project;
    break;
    ;;
  --restart)
    restart_project;
    break;
    ;;
  -h | --help)
    printf "\t\t\tUsage: \n\t\t\t\t--start\t\t\tStart Service\n\t\t\t\t--stop\t\t\tStop Service\n\t\t\t\t-h, --help\t\tdisplay this help and exit\n";
    break;
    ;;
  *)
    options_error="Invalid option, Please execute -h or --help";
    printf "\033[41;37m %s \033[0m\n" "$options_error";
    break
    ;;
  esac
done

#for param in "$@"; do
#  echo "Param: $param"
#done
