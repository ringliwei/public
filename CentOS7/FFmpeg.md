# FFmpeg

- [FFmpeg](#ffmpeg)
  - [快速入门](#快速入门)
  - [资源](#资源)

## 快速入门

FFmpeg 的命令行参数非常多，可以分成五个部分。

```bash
ffmpeg {1} {2} -i {3} {4} {5}
```

上面命令中，五个部分的参数依次如下。

1. 全局参数
2. 输入文件参数
3. `输入文件`
4. 输出文件参数
5. 输出文件

参数太多的时候，为了便于查看，ffmpeg 命令可以写成多行。

```bash
ffmpeg \
[全局参数] \
[输入文件参数] \
-i [输入文件] \
[输出文件参数] \
[输出文件]
```

下面是一个例子。

```bash
ffmpeg \
-y \ # 全局参数
-c:a libfdk_aac -c:v libx264 \ # 输入文件参数
-i input.mp4 \ # 输入文件
-c:v libvpx-vp9 -c:a libvorbis \ # 输出文件参数
output.webm # 输出文件
```

上面的命令将 mp4 文件转成 webm 文件，这两个都是容器格式。输入的 mp4 文件的音频编码格式是 aac，视频编码格式是 H.264；输出的 webm 文件的视频编码格式是 VP9，音频格式是 Vorbis。

## 资源

- [DouyinLiveRecorder](https://github.com/ihmily/DouyinLiveRecorder)
  - [FFmpeg](https://ffmpeg.org/)
  - [HTTP Live Streaming](https://www.rfc-editor.org/rfc/rfc8216) m3u8
  - [ffmpeg_dl.py](../Python/scripts/ffmpeg_dl.py)
  - [hls.js](https://github.com/video-dev/hls.js) is a JavaScript library that plays HLS in browsers with support for MSE.
  - [flv.js](https://github.com/Bilibili/flv.js) HTML5 FLV Player.
    - [mpegts.js](https://github.com/xqq/mpegts.js) HTML5 MPEG2-TS / FLV Stream Player.
- [webvideo-downloader](https://github.com/jaysonlong/webvideo-downloader)
  - [CommonHlsDownloader.user.js](../UserScript/CommonHlsDownloader.user.js)
  - [WebVideoDownloader.user.js](../UserScript/WebVideoDownloader.user.js)
- [tampermonkey](https://www.tampermonkey.net/)

  - [CommonHlsDownloader.user.js](../UserScript/CommonHlsDownloader.user.js)
  - [WebVideoDownloader.user.js](../UserScript/WebVideoDownloader.user.js)
  - [ShortVideoDownloader.user.js](../UserScript/ShortVideoDownloader.user.js)
  - [Intercept browser requests for resources](https://stackoverflow.com/questions/26516358/intercept-browser-requests-for-resources)
  - [油猴脚本编写快速入门](https://www.cnblogs.com/mq0036/p/17509937.html)

- [FFmpeg 视频处理入门教程](https://ruanyifeng.com/blog/2020/01/ffmpeg.html)
- [如何用 FFMpeg 生成视频](https://zhuanlan.zhihu.com/p/465418866)
- [基于 Nginx 搭建 RTMP-HLS 视频直播服务器（推流+拉流）](https://blog.csdn.net/Harry_z666/article/details/114984077)
  - [NGINX-based Media Streaming Server](https://github.com/arut/nginx-rtmp-module)
- [Nginx 配置搭建 m3u8 格式的视频播放服务](https://www.cnblogs.com/liuyangjava/p/17514580.html)
- [使用 nginx 搭建 HTTP FLV 流媒体服务器](https://blog.csdn.net/water1209/article/details/128708318)
  - [nginx-rtmp-module](https://github.com/arut/nginx-rtmp-module) NGINX-based Media Streaming Server
  - [nginx-http-flv-module](https://github.com/winshining/nginx-http-flv-module)
- [FFmpeg+Nginx+RTMP/HLS 快速搭建直播网站](https://www.cnblogs.com/crazymagic/articles/14101332.html)
- [rtmp-hls-server](https://github.com/TareqAlqutami/rtmp-hls-server) a docker file to create a streaming server that supports RTMP, HLS and DASH content based on nginx and nginx-rtmp-module.
  - [HLS-搭建 Nginx 流媒体点播服务(SaaS docker)](https://blog.csdn.net/ysf465639310/article/details/104700147)
- [FFmpeg 快速入门：命令行详解、工具、教程、电子书](https://blog.mzh.ren/zh/posts/2022/10/ffmpeg-quickstart/)
