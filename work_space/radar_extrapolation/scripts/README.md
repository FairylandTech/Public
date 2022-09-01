# 关于management_radar脚本文件说明

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
