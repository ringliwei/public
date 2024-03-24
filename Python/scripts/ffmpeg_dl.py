import subprocess
import threading

SAVE_PATH = "D:/downloads"


def ffmpeg_dl(real_url, save_path_name):
    ffmpeg_path = "ffmpeg"
    user_agent = ("Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/537.36 ("
                  "KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile "
                  "Safari/537.36")

    analyzeduration = "20000000"
    probesize = "10000000"
    bufsize = "8000k"
    max_muxing_queue_size = "1024"

    ffmpeg_command = [
        ffmpeg_path, "-y",
        "-v", "verbose",
        "-rw_timeout", "30000000",
        "-loglevel", "error",
        "-hide_banner",
        "-user_agent", user_agent,
        "-protocol_whitelist", "rtmp,crypto,file,http,https,tcp,tls,udp,rtp",
        "-thread_queue_size", "1024",
        "-analyzeduration", analyzeduration,
        "-probesize", probesize,
        "-fflags", "+discardcorrupt",
        "-i", real_url,
        "-bufsize", bufsize,
        "-sn", "-dn",
        "-reconnect_delay_max", "60",
        "-reconnect_streamed", "-reconnect_at_eof",
        "-max_muxing_queue_size", max_muxing_queue_size,
        "-correct_ts_overflow", "1",
    ]

    audio_code = "aac"
    segment_format = "mp4"
    split_time = "180000"

    command = [
        "-c:v", "copy",
        "-c:a", audio_code,
        "-map", "0",
        "-f", "mp4",
        # "-segment_time", split_time,
        # "-segment_format", segment_format,
        # "-reset_timestamps", "1",
        save_path_name,
    ]

    ffmpeg_command.extend(command)
    try:
        _output = subprocess.check_output(ffmpeg_command,
                                          stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print(f"错误信息: {e} 发生错误的行数: {e.__traceback__.tb_lineno}")


if __name__ == "__main__":
    i = 0
    def geti():
        global i
        i = i + 1
        return i
    
    url_list = [
        ["https://xx/index.m3u8", f"{SAVE_PATH}/xx{geti()}.mp4"],
    ]
    


    tt = []
    for url, name in url_list:
        thread = threading.Thread(
            target=ffmpeg_dl, args=(url, name), name='ffmpeg_dl')
        thread.start()
        tt.append(thread)

    for t in tt:
        t.join()
