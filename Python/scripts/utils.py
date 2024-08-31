
import subprocess
import os
import sys


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
