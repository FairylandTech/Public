#!/bin/bash
# @File: radar_management.sh
# @Editor: PyCharm
# @Author: Alice(From Chengdu.China)
# @HomePage: https://github.com/AliceEngineerPro
# @CreatedTime: 2023/1/5 19:49

# Global Variables
project_home=""
conda_environment_name=""

# Change Anaconda --> $(ENVIRONMENT_NAME)
environment_config() {
  if [ "$(conda --version | wc -l)" = 1 ]; then
    conda activate "$conda_environment_name"
  else
    {
      local str_a="Error: Not Found Anaconda"
      local str_b="Please install Anaconda or Add Anaconda to the environment variable (User or System)"
      printf "\033[31m%s\n \033[0m" "$str_a"
      printf "\033[31m%s\n \033[0m" "$str_b"
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
      printf "\033[31mInsufficient Permissions, Use root Privileges\n \033[0m"
      exit 1
    }
  fi
}

run_project() {
  static_user
  mkdir -p "${project_home}/logs"
  local str_a="Please check program path"
  cd "${project_home}" || printf "\033[31mError: Not Found %s\n \033[0m" "${project_home}" && printf "\033[31m %s \033[0m" "$str_a"
  cp run.py radar_run.py
  nohup python -u radar_run.py >./logs/radar_run.log 2>&1 &
  printf "Output log file to: %s/logs/run.log\n" "$project_home"
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
      exit 1
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
  start)
    start_project
    break
    ;;
  stop)
    stop_project
    break
    ;;
  restart)
    restart_project
    break
    ;;
  -h | help)
    printf "
    Usage: 
          start         -Start Service
          stop          -Stop Service
          restart       -Restart Service
          -h, help      -display this help and exit\n"
    break
    ;;
  *)
    options_error="Invalid option, Please execute -h or --help"
    printf "\033[31m%s\n \033[0m" "$options_error"
    break
    ;;
  esac
done

#for param in "$@"; do
#  echo "Param: $param"
#done
