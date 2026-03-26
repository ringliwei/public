
import functools
import os
import subprocess
import sys
import traceback


def check_ffmpeg_existence(ffmpeg_path):
    dev_null = open(os.devnull, 'wb')
    try:
        subprocess.run(['ffmpeg', '--help'], stdout=dev_null, stderr=dev_null, check=True)
    except subprocess.CalledProcessError as e:
        return False
    except FileNotFoundError:
        ffmpeg_file_check = subprocess.getoutput(ffmpeg_path)
        if ffmpeg_file_check.find("run") > -1 and os.path.isfile(ffmpeg_path):
            os.environ['PATH'] += os.pathsep + os.path.dirname(os.path.abspath(ffmpeg_path))
            return True
        else:
            sys.exit(0)
    finally:
        dev_null.close()
    return True


def trace_error_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_line = traceback.extract_tb(e.__traceback__)[-1].lineno
            error_info = f"错误信息: type: {type(e).__name__}, {str(e)} in function {func.__name__} at line: {error_line}"
            return []

    return wrapper
