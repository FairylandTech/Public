# 关于radar_management脚本文件说明

[![author](https://img.shields.io/badge/Author-Alice-orange)](https://res.abeim.cn/api/qq/?qq=489261538) [![github](https://img.shields.io/badge/Github-AliceEngineerPro-green)](https://github.com/AliceEngineerPro) [![type](https://img.shields.io/badge/Type-Script-blue)](#) [![editor](https://img.shields.io/badge/Editor-Pycharm-yellow)](#) [![file](https://img.shields.io/badge/File-Shell-orange)](#) [![version](https://img.shields.io/badge/Version-1.0.0_beta-blue)](#) [![docs](https://img.shields.io/badge/Docs-Passing-brightgreen)](#) [![](https://img.shields.io/badge/%E7%AD%89%E6%88%91%E4%BB%A3%E7%A0%81%E7%BC%96%E6%88%90-%E5%A8%B6%E4%BD%A0%E4%B8%BA%E5%A6%BB%E5%8F%AF%E5%A5%BD-red)](#)

## Part1: 修改脚本环境变量

```bash
# 修改全局环境变量
# 项目路径
PROJECT_HOME=""
# e.g:
# PROJECT_HOME="/home/alice/project/ai_obj"
# conda 运行环境的名称
CONDA_ENVIRONMENT_NAME=""
# e.g:
# CONDA_ENVIRONMENT_NAME="radar_env_ai_obj"

```

## Part2: 脚本运行

```bash
# 启动
management_radar.sh --start
# 停止
management_radar.sh --stop
# 重启
management_radar.sh --restart
# 帮助
management_radar.sh -h
management_radar.sh --help
```

## 脚本预览

```shell
#!/bin/bash
# @File: radar_management
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
      printf "\m[41;37m %s \m[0m\n" "$str_a"
      printf "\m[41;37m %s \m[0m\n" "$str_b"
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
      printf "\m[41;37mInsufficient Permissions, Use root Privileges\m[0m\n"
      exit 1
    }
  fi
}

run_project() {
  static_user
  mkdir -p "${project_home}/logs"
  local str_a="Please check program path"
  cd "${project_home}" || printf "\m[41;37m Error: Not Found %s \m[0m\n" "${project_home}" && printf "\m[41;37m %s \m[0m\n" "$str_a"
  cp run.py radar_run.py
  nohup python -u radar_run.py >./logs/radar_run.log 2>&1 &
  printf "Output log file to: %s/logs/run.log" "$project_home"
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
    printf "\m[41;37m %s \m[0m\n" "$options_error"
    break
    ;;
  esac
done

#for param in "$@"; do
#  echo "Param: $param"
#done

```
