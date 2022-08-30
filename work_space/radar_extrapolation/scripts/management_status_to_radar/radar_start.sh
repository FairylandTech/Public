#!/bin/bash
# ========================================================================
# FileName: radar_start.sh
# Author: Alice(From Chengdu.China)
# Career: IT.Engineer
# WeChat: AliceEngineerT
# QQNumber: 489261538
# Telegram: @AliceEngineer
# E-mail(Chinese Mainland): alice_engineer@yeah.net
# E-mail(Global): alice.engineer.pro@gmail.com
# Created Time: 2022/8/30 18:18
# ========================================================================
#
#######################################
# description: main
# Globals:
#   ANACONDA_ENVIRONMENT_NAME
#   DEFAULT_COLOR
#   GREEN
#   RED
# Arguments:
#  None
#######################################
main() {
  project_path=""
  local anaconda_environment_name=""
  # color fonts
  red_color='\e[1;31m'
  greed_color='\e[1;32m'
  defalut_color='\e[0m'
  if [ "$(whoami)" = root ]; then
    echo -e "${greed_color}INFO: ${defalut_color}User: $(whoami)"
    if [ "$(conda --version | wc -l)" != 1 ]; then
      echo -e "${red_color}ERROR: ${defalut_color}Check the conda installed or not and conda env path"
      echo -e "${greed_color}INFO: ${defalut_color}Script running End"
    else
      {
        conda activate >/dev/null 2>&1
        conda activate "${anaconda_environment_name}"
        #######################################
        # description run
        # Globals:
        #   defalut_color
        #   greed_color
        #   project_path
        #   red_color
        #   scripts_path
        # Arguments:
        #  None
        #######################################
        run() {
          cd "${project_path}" || echo -e "${red_color}ERROR: ${defalut_color}Not found ${project_path}"
          if [ -a "run.py" ]; then
            local radar_run="radar_run.py"
            cp ./run.py "./${radar_run}"
            nohup ./radar_run.py
          else
            {
              echo -e "${red_color}ERROR: ${defalut_color}Path: ${project_path} not found, Check again"
              echo -e "${greed_color}INFO: ${defalut_color}Script running End"
            }
          fi
          echo -e "${greed_color}INFO: ${defalut_color}Script running End"
        }
        run

      }
    fi
  else
    {
      echo -e "${red_color}ERROR: ${defalut_color}User: $(whoami), Try again using root"
      echo -e "${greed_color}INFO: ${defalut_color}Script running End"
    }
  fi
}

main
