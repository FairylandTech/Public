# coding: utf-8

import os
import logging

# work_path = os.getcwd()
work_path = input(f'路径: ')
files_path_list = []

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s: %(msg)s')


def f_path(path):
    files_path = os.listdir(path)
    for file_path in files_path:
        if file_path.startswith('.'):
            logging.warning(msg=os.path.join(path, file_path))
        else:
            file_path = os.path.join(path, file_path)
            if os.path.isdir(file_path):
                f_path(file_path)
            else:
                files_path_list.append(file_path)
    return files_path_list


def f_change():
    try:
        for file_path in f_path(path=work_path):
            if os.path.isfile(file_path):
                f = open(file=file_path, mode='r', encoding='utf-8')
                read_str = f.read()
                read_str.replace(r'\r\n', r'\n')
                read_str.replace(r'\r', r'\n')
                f.close()
                f = open(file=file_path, mode='wb')
                f.write(read_str.encode(encoding='utf-8'))
                f.close()
                logging.info(msg=f'{file_path}  --  Successfully changed')
            else:
                logging.warning(msg=file_path)
                pass
        return True
    except Exception as error:
        return error


if __name__ == '__main__':
    print(f_change())
