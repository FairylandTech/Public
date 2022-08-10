# 关于AI_extrapolation.sh脚本文件说明

## Part1: 修改脚本环境变量

```bash
# 修改全局环境变量
# 项目路径
PROJECT_HOME=""
# example:
# PROJECT_HOME="/home/alice/project/ai_obj"
# conda 运行环境的名称
CONDA_ENVIRONMENT_NAME=""
# example:
# CONDA_ENVIRONMENT_NAME="radar_env_ai_obj"

```

## Part2: 脚本运行

```bash
# 启动
AI_extrapolation.sh --start
# 停止
AI_extrapolation.sh --stop
# 重启
AI_extrapolation.sh --restart
# 帮助
AI_extrapolation.sh -h
AI_extrapolation.sh --help
```
