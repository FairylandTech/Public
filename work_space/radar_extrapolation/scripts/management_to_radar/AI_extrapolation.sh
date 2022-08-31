#!/bin/bash
#########################################################################
# File Name: management_to_radar.sh
# Nickname: Alice(From Chengdu.China)
# Position: IT.Engineer
# TEL: +86-17313081751
# WeChat: AliceEngineerT
# QQNumber: 489261538
# Telegram: @AliceEngineer
# E-mail(Chinese Mainland): alice_engineer@yeah.net
# E-mail(Global): alice.engineer.pro@gmail.com
# Created Time: 2022年07月27日 星期三 10时01分18秒
#########################################################################

# Global Variables
PROJECT_HOME=""
CONDA_ENVIRONMENT_NAME=""

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
      exit 1
    }
  fi
}

# Change User --> root
static_user() {
  if [ "$(whoami)" = root ]; then
    environment_config
  else
    {
      printf "\033[41;37mInsufficient Permissions, Use root Privileges\033[0m\n"
      exit 1
    }
  fi
}

run_project() {
  static_user
  mkdir -p "${PROJECT_HOME}/logs"
  local str_a="Please check program path"
  cd "${PROJECT_HOME}" || printf "\033[41;37m Error: Not Found %s \033[0m\n" "${PROJECT_HOME}" && printf "\033[41;37m %s \033[0m\n" "$str_a"
  cp run.py radar_run.py
  nohup python -u radar_run.py >./logs/radar_run.log 2>&1 &
  printf "Output log file to: %s/logs/run.log" "$PROJECT_HOME"
}

start_project() {
  if [ "$(pgrep radar_run | wc -l)" = 1 ]; then
    printf "Running\n"
  else
    {
      run_project
    }
  fi
}

stop_project() {
  if [ "$(pgrep radar_run | wc -l)" = 1 ]; then
    sudo kill "$(pgrep radar_run)"
  else
    {
      printf "Please execute start\n"
    }
  fi
}

restart_project() {
  stop_project
  printf "wait 10s\n"
  sleep 10
  start_project
}

# main
while true; do
  case $1 in
  --start)
    start_project
    break
    ;;
  --stop)
    stop_project
    break
    ;;
  --restart)
    restart_project
    break
    ;;
  -h | --help)
    printf "
    Usage: 
          --start         Start Service
          --stop          Stop Service
          --restart       Restart Service
          -h, --help      display this help and exit\n"
    break
    ;;
  *)
    options_error="Invalid option, Please execute -h or --help"
    printf "\033[41;37m %s \033[0m\n" "$options_error"
    break
    ;;
  esac
done

#for param in "$@"; do
#  echo "Param: $param"
#done
