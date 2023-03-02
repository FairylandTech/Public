# encoding=utf8
"""

@author: Bob
@create time: 2021/10/13 17:36
"""
from __future__ import print_function, division

import logging
import os
import shutil
import sys
import time
from glob import glob
from multiprocessing import Pool
from os.path import splitext


def is_zh_han(string):
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
        return False


def compiles(
        work_dir='.',
        filenames: (list, tuple) = None,
        exclude_files: (list, tuple) = None,
        annotation=False,
        numpy_includes=True,
        debug_mode=False,
        rm_src_file=False,
        **kwargs
):
    """

    :param work_dir: 工作目录
    :param filenames: 列表或者元组, 同一个工作目录下的py文件, 没有指定时, 会编译work_dir目录下所有'.pyx', '.py', '.pyw'文件
    :param exclude_files: 编译的文件名, 注意: 是文件名, 而不是一个文件路径
    :param annotation: 是否生产 .html 的文件注释
    :param numpy_includes: 是否包括了numpy
    :param debug_mode: 是否debug模式
    :param rm_src_file: 是否删除原始文件
    :return:
    """
    # 切换当前的工作路径
    work_dir = os.path.abspath(work_dir)
    print('当前处理目录: "%s"' % work_dir)
    os.chdir(work_dir)

    if exclude_files is None:
        exclude_files = []
    exclude_files = list(exclude_files) + [
        '__init__.py',  # __init__.py 无法编译
        os.path.basename(__file__),  # 自身不编译
    ]

    if filenames is None:
        filenames = [
            os.path.join(work_dir, '*.py'),
            os.path.join(work_dir, '*.pyx'),
            os.path.join(work_dir, '*.pyw'),
        ]

    logging.getLogger().setLevel(logging.DEBUG) if debug_mode else logging.getLogger().setLevel(logging.INFO)

    # The filename args are allowed to be globs
    # files = [f for g in filenames for f in glob(g)
    #          if splitext(f)[1].lower() in ['.pyx', '.py', 'pyw']]
    print('Given filenames = ' + '\n\t'.join(filenames))
    print('Current dir contents: \n' + '\n\t'.join(os.listdir('.')))

    # This is a beautiful, beautiful line. This is why I use Python.
    files = [f for g in filenames for f in glob(g)]
    print('Detected files: \n\t' + '\n\t'.join(files))

    # Collect all the extensions to process
    extensions = []
    for f in files:
        base_file_name = os.path.basename(f)
        if (base_file_name in exclude_files) or is_zh_han(base_file_name):
            print('Skip: %s' % f)
            continue
        basename, ext = splitext(f)
        extensions.append((basename, f))

    # No pyx files given.
    if len(extensions) == 0:
        print('Notice: No valid source filenames were supplied in "%s". ' % work_dir)
        return

    # Checking for missing files
    missing = [f for n, f in extensions if not os.path.exists(f)]
    if missing:
        print('** ERROR: These files were missing:')
        for f in missing:
            logging.error('    {}'.format(f))
        logging.error('Aborting.')
        sys.exit(2)

    # Restore distutils command line args
    # TODO: It should be possible to specify these
    # options direction on the objects, rather than
    # hacking the command line.
    print(sys.argv[0])
    sys.argv = [sys.argv[0], 'build_ext', '--inplace']

    from setuptools import setup, Extension
    from Cython.Distutils import build_ext
    from Cython.Build import cythonize
    import Cython.Compiler.Options
    Cython.Compiler.Options.annotate = annotation

    # Create module objects
    ext_modules = []
    for n, f in extensions:
        # The name must be plain, no path
        module_name = os.path.basename(n)
        obj = Extension(module_name,
                        [f],
                        extra_compile_args=["-O2", "-march=native"])
        ext_modules.append(obj)

    # Extra include folders. Mainly for numpy.
    include_dirs = []
    if numpy_includes:
        try:
            import numpy
            include_dirs += [numpy.get_include()]
        except:
            print('** ERROR: Numpy is required, but not found. Please install it')

    setup(
        cmdclass={'build_ext': build_ext},
        include_dirs=include_dirs,
        ext_modules=cythonize(ext_modules),
    )

    # Rename: rename generated pyd files
    time.sleep(1)
    pyd_src_files = glob(os.path.join(work_dir, '*.pyd')) + glob(os.path.join(work_dir, '*.so'))
    for pyd_src_file in pyd_src_files:
        pyd_src_name = os.path.basename(pyd_src_file)
        pyd_target_name = '%s.%s' % (pyd_src_name.split('.')[0], pyd_src_name.split('.')[-1])
        pyd_target_path = os.path.join(work_dir, pyd_target_name)
        os.rename(pyd_src_file, pyd_target_path)

    # Cleanup: delete intermediate C files, py files,  pyx files, and build folder.
    for n, f in extensions:
        if os.path.exists(n + '.c'):
            os.remove(n + '.c')

        if rm_src_file and os.path.exists(f):
            os.remove(f)

        build_dir = os.path.join(os.path.dirname(n), 'build')
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)


def compile_multilevel_dir(source_dir, processes_num: int = 1, rm_src_file=False, **kwargs):

    system = 'windows' if 'win32' in sys.platform else sys.platform
    sub_name = f'{system.lower()}_py{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}'
    target_dir = os.path.join(os.path.dirname(source_dir), f'{os.path.basename(source_dir)}_{sub_name}')

    # 复制整个项目, 存在就先删除
    if os.path.exists(target_dir) and os.path.isdir(target_dir):
        shutil.rmtree(target_dir)
        time.sleep(1)
    shutil.copytree(source_dir, target_dir)
    # 删除复制目录下的本文件
    this_file_path = os.path.join(target_dir, os.path.basename(os.path.abspath(__file__)))
    if os.path.exists(this_file_path):
        os.remove(this_file_path)

    pool = Pool(processes=processes_num) if processes_num > 1 else None
    # 遍历整个项目目录的文件夹, 然后编译
    for root, dirs, files in os.walk(target_dir):
        rname = os.path.basename(root)
        if rname.endswith('__pycache__') or rname.startswith('.'):  # 删除缓存文件, 删除隐藏文件夹(例如.git, .idea等)
            shutil.rmtree(root)
            continue

        kwargs.update(dict(work_dir=root, rm_src_file=rm_src_file))
        if pool:
            pool.apply_async(compiles, kwds=kwargs)
        else:
            compiles(**kwargs)

    if pool:
        pool.close()
        pool.join()


if __name__ == '__main__':
    st = time.time()

    # p_num = 1 if os.cpu_count() < 3 else os.cpu_count() - 2
    p_num = 6

    # print(is_zh_han('北斗.py'))

    # compiles(
    #     work_dir=r'H:\Projects\utils_tmp\aksu',
    #     filenames=['run_analysis.py'],
    #     rm_src_file=False
    # )
    compile_multilevel_dir(
        source_dir=os.path.dirname(os.path.abspath(__file__)),
        exclude_files=['run.py'],
        rm_src_file=True,
        processes_num=p_num,
    )

    print('done! 耗时: ', time.time() - st, 's')
