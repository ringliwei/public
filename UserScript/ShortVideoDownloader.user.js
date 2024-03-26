// ==UserScript==
// @name              短视频下载助手，为抖音、快手、小红书等提供无水印高清下载功能
// @namespace         huahuacat_nowater_downloader
// @version           1.0.3
// @description       视频下载助手：1、支持抖音短视频下载：为首页、搜索结果、用户主页等提供无水印视频下载功能；2、快手短视频下载：为视频详情页提供无水印视频下载功能；其他平台持续开发中【脚本长期维护更新，完全免费，无广告】
// @author            爱画画的猫,潮玩天下
// @include           https://www.douyin.com/*
// @include           https://www.kuaishou.com/*
// @connect           www.iesdouyin.com
// @grant             unsafeWindow
// @grant             GM_openInTab
// @grant             GM.openInTab
// @grant             GM_xmlhttpRequest
// @grant             GM.xmlHttpRequest
// @license           AGPL License
// @charset		      UTF-8
// @original-author   爱画画的猫
// @original-license  AGPL License
// @original-script   https://greasyfork.org/zh-CN/scripts/418804
// @run-at            document-idle
// @downloadURL https://update.greasyfork.org/scripts/452660/%E7%9F%AD%E8%A7%86%E9%A2%91%E4%B8%8B%E8%BD%BD%E5%8A%A9%E6%89%8B%EF%BC%8C%E4%B8%BA%E6%8A%96%E9%9F%B3%E3%80%81%E5%BF%AB%E6%89%8B%E3%80%81%E5%B0%8F%E7%BA%A2%E4%B9%A6%E7%AD%89%E6%8F%90%E4%BE%9B%E6%97%A0%E6%B0%B4%E5%8D%B0%E9%AB%98%E6%B8%85%E4%B8%8B%E8%BD%BD%E5%8A%9F%E8%83%BD.user.js
// @updateURL https://update.greasyfork.org/scripts/452660/%E7%9F%AD%E8%A7%86%E9%A2%91%E4%B8%8B%E8%BD%BD%E5%8A%A9%E6%89%8B%EF%BC%8C%E4%B8%BA%E6%8A%96%E9%9F%B3%E3%80%81%E5%BF%AB%E6%89%8B%E3%80%81%E5%B0%8F%E7%BA%A2%E4%B9%A6%E7%AD%89%E6%8F%90%E4%BE%9B%E6%97%A0%E6%B0%B4%E5%8D%B0%E9%AB%98%E6%B8%85%E4%B8%8B%E8%BD%BD%E5%8A%9F%E8%83%BD.meta.js
// ==/UserScript==

(function () {
    /**
     * 此工具方法来自画画的猫
     * 脚本地址:https://greasyfork.org/zh-CN/scripts/418804
     */
    //共有方法，全局共享
    function commonFunction() {
        this.GMgetValue = function (name, value = null) {
            let storageValue = value;
            if (typeof GM_getValue === "function") {
                storageValue = GM_getValue(name, value);
            } else if (typeof GM.setValue === "function") {
                storageValue = GM.getValue(name, value);
            } else {
                var arr = window.localStorage.getItem(name);
                if (arr != null) {
                    storageValue = arr;
                }
            }
            return storageValue;
        };
        this.GMsetValue = function (name, value) {
            if (typeof GM_setValue === "function") {
                GM_setValue(name, value);
            } else if (typeof GM.setValue === "function") {
                GM.setValue(name, value);
            } else {
                window.localStorage.setItem(name, value);
            }
        };
        this.GMaddStyle = function (css) {
            var myStyle = document.createElement("style");
            myStyle.textContent = css;
            var doc = document.head || document.documentElement;
            doc.appendChild(myStyle);
        };
        this.GMopenInTab = function (url, options = { active: true, insert: true, setParent: true }) {
            if (typeof GM_openInTab === "function") {
                GM_openInTab(url, options);
            } else {
                GM.openInTab(url, options);
            }
        };
        this.addScript = function (url) {
            var s = document.createElement("script");
            s.setAttribute("src", url);
            document.body.appendChild(s);
        };
        this.randomNumber = function () {
            return Math.ceil(Math.random() * 100000000);
        };
        this.request = function (mothed, url, param) {
            //网络请求
            return new Promise(function (resolve, reject) {
                GM_xmlhttpRequest({
                    url: url,
                    method: mothed,
                    data: param,
                    onload: function (response) {
                        var status = response.status;
                        var playurl = "";
                        if (status == 200 || status == "200") {
                            var responseText = response.responseText;
                            resolve({ result: "success", data: responseText });
                        } else {
                            reject({ result: "error", data: null });
                        }
                    },
                });
            });
        };
        this.addCommonHtmlCss = function () {
            var cssText = `
				@keyframes fadeIn {
				    0%    {opacity: 0}
				    100%  {opacity: 1}
				}
				@-webkit-keyframes fadeIn {
				    0%    {opacity: 0}
				    100%  {opacity: 1}
				}
				@-moz-keyframes fadeIn {
				    0%    {opacity: 0}
				    100%  {opacity: 1}
				}
				@-o-keyframes fadeIn {
				    0%    {opacity: 0}
				    100%  {opacity: 1}
				}
				@-ms-keyframes fadeIn {
				    0%    {opacity: 0}
				    100%  {opacity: 1}
				}
				@keyframes fadeOut {
				    0%    {opacity: 1}
				    100%  {opacity: 0}
				}
				@-webkit-keyframes fadeOut {
				    0%    {opacity: 1}
				    100%  {opacity: 0}
				}
				@-moz-keyframes fadeOut {
				    0%    {opacity: 1}
				    100%  {opacity: 0}
				}
				@-o-keyframes fadeOut {
				    0%    {opacity: 1}
				    100%  {opacity: 0}
				}
				@-ms-keyframes fadeOut {
				    0%    {opacity: 1}
				    100%  {opacity: 0}
				}
				.web-toast-kkli9{
				    position: fixed;
				    background: rgba(0, 0, 0, 0.7);
				    color: #fff;
				    font-size: 14px;
				    line-height: 1;
				    padding:10px;
				    border-radius: 3px;
				    left: 50%;
				    transform: translateX(-50%);
				    -webkit-transform: translateX(-50%);
				    -moz-transform: translateX(-50%);
				    -o-transform: translateX(-50%);
				    -ms-transform: translateX(-50%);
				    z-index: 999999999999999999999999999;
				    white-space: nowrap;
				}
				.fadeOut{
				    animation: fadeOut .5s;
				}
				.fadeIn{
				    animation:fadeIn .5s;
				}
				`;
            this.GMaddStyle(cssText);
        };
        this.webToast = function (params) {
            //小提示框
            var time = params.time;
            var background = params.background;
            var color = params.color;
            var position = params.position; //center-top, center-bottom
            var defaultMarginValue = 50;

            if (time == undefined || time == "") {
                time = 1500;
            }

            var el = document.createElement("div");
            el.setAttribute("class", "web-toast-kkli9");
            el.innerHTML = params.message;
            //背景颜色
            if (background != undefined && background != "") {
                el.style.backgroundColor = background;
            }
            //字体颜色
            if (color != undefined && color != "") {
                el.style.color = color;
            }

            //显示位置
            if (position == undefined || position == "") {
                position = "center-bottom";
            }

            //设置显示位置，当前有种两种形式
            if (position === "center-bottom") {
                el.style.bottom = defaultMarginValue + "px";
            } else {
                el.style.top = defaultMarginValue + "px";
            }
            el.style.zIndex = 999999;

            document.body.appendChild(el);
            el.classList.add("fadeIn");
            setTimeout(function () {
                el.classList.remove("fadeIn");
                el.classList.add("fadeOut");
                /*监听动画结束，移除提示信息元素*/
                el.addEventListener("animationend", function () {
                    document.body.removeChild(el);
                });
                el.addEventListener("webkitAnimationEnd", function () {
                    document.body.removeChild(el);
                });
            }, time);
        };
        this.queryUrlParamter = function (text, tag) {
            //查询GET请求url中的参数
            if (text.indexOf("?") != -1) {
                //选取?后面的字符串,兼容window.location.search，前面的?不能去掉
                var textArray = text.split("?");
                text = "?" + textArray[textArray.length - 1];
            }
            var t = new RegExp("(^|&)" + tag + "=([^&]*)(&|$)");
            var a = text.substr(1).match(t);
            if (a != null) {
                return a[2];
            }
            return "";
        };
        this.isPC = function () {
            var userAgentInfo = navigator.userAgent;
            var Agents = ["Android", "iPhone", "SymbianOS", "Windows Phone", "iPad", "iPod"];
            var flag = true;
            for (var v = 0; v < Agents.length; v++) {
                if (userAgentInfo.indexOf(Agents[v]) > 0) {
                    flag = false;
                    break;
                }
            }
            return flag;
        };
        this.getBilibiliBV = function () {
            var pathname = window.location.pathname;
            var bv = pathname.replace("/video/", "").replace("/", "");
            return bv;
        };
        this.getSystemOS = function () {
            var u = navigator.userAgent;
            if (!!u.match(/compatible/i) || u.match(/Windows/i)) {
                return "windows";
            } else if (!!u.match(/Macintosh/i) || u.match(/MacIntel/i)) {
                return "macOS";
            } else if (!!u.match(/iphone/i) || u.match(/Ipad/i)) {
                return "ios";
            } else if (!!u.match(/android/i)) {
                return "android";
            } else {
                return "other";
            }
        };
        this.RPCDownloadFile = function (fileName, url, savePath = "D:/", RPCURL = "ws://localhost:16800/jsonrpc", RPCToken = "") {
            const self = this;
            if (!savePath) {
                savePath = "D:/";
            }
            if (!RPCURL) {
                RPCURL = "ws://localhost:16800/jsonrpc";
            }
            let options = {
                //下载配置文件
                dir: savePath,
                "max-connection-per-server": "16",
                header: ["User-Agent:" + navigator.userAgent + "", "Cookie:" + document.cookie + "", "Referer:" + window.location.href + ""],
            };
            if (!!fileName) {
                options.out = fileName;
            }
            let jsonRPC = {
                jsonrpc: "2.0",
                id: "huahuacat",
                method: "aria2.addUri",
                params: [[url], options],
            };
            if (!!RPCToken) {
                jsonRPC.params.unshift("token:" + RPCToken); // 必须要加在第一个
            }
            return new Promise(function (resolve, reject) {
                var webSocket = new WebSocket(RPCURL);
                webSocket.onerror = function (event) {
                    console.log("webSocket.onerror", event);
                    reject("Aria2连接错误，请打开Aria2和检查RPC设置！");
                };
                webSocket.onopen = function () {
                    webSocket.send(JSON.stringify(jsonRPC));
                };
                webSocket.onmessage = function (event) {
                    let result = JSON.parse(event.data);
                    switch (result.method) {
                        case "aria2.onDownloadStart":
                            resolve("Aria2 开始下载【" + fileName + "】");
                            webSocket.close();
                            break;
                        case "aria2.onDownloadComplete":
                            break;
                        default:
                            break;
                    }
                };
            });
        };
        this.getElementObject = function (selector, delay = 200) {
            return new Promise((resolve, reject) => {
                let totalDelay = 0;
                let elementInterval = setInterval(() => {
                    if (totalDelay >= 2500) {
                        reject(false);
                        clearInterval(elementInterval);
                    }
                    let element = document.querySelector(selector);
                    if (element) {
                        resolve(element);
                        clearInterval(elementInterval);
                    } else {
                        totalDelay += delay;
                    }
                }, delay);
            });
        };
    }

    //统一工具
    const commonFunctionObject = new commonFunction();
    commonFunctionObject.addCommonHtmlCss(); //统一html、css元素添加

    /**
     * 短视频去水印下载，与爱画画的猫共同开发维护
     * https://greasyfork.org/zh-CN/scripts/418804
     */
    function shortVideoDownloader() {
        this.douyinVideoDownloader = function () {
            if (window.location.host !== "www.douyin.com") {
                return;
            }
            window.addEventListener("load", function () {
                //这是搜索界面
                if (window.location.href.match(/https:\/\/www\.douyin\.com\/search\/.*?/)) {
                    function downloader() {
                        const videoContainers = document.querySelectorAll(".player-info");
                        videoContainers.forEach((element) => {
                            if (element.getAttribute("dealwith")) {
                                return;
                            }
                            let bottomMenu = element.querySelector("xg-right-grid");
                            if (!bottomMenu) {
                                return;
                            }
                            let playbackSetting = bottomMenu.querySelector(".xgplayer-playback-setting");
                            if (!playbackSetting) {
                                return;
                            }
                            let download = playbackSetting.cloneNode(true); // 拷贝一个节点
                            let downloadText = download.querySelector("div:first-child");
                            let video = element.querySelector("video");
                            downloadText.innerText = "下载";
                            downloadText.style = "font-size:13px";
                            playbackSetting.after(download);
                            element.setAttribute("dealwith", "true");
                            download.addEventListener("click", (e) => {
                                let playerUrl = video.children[0].src;
                                commonFunctionObject.GMopenInTab(playerUrl);
                            });
                        });
                    }
                    downloader();
                    setInterval(function () {
                        downloader();
                    }, 500);
                } else {
                    async function downloader() {
                        try {
                            //延迟加载等到是否完成
                            let videoContainer = await commonFunctionObject.getElementObject(".xg-video-container");
                            if (!videoContainer) {
                                return false;
                            }
                            let bottomMenus = document.querySelectorAll(".xg-right-grid");
                            let bottomMenuLength = bottomMenus.length;
                            let bottomMenu = bottomMenus.length > 1 ? bottomMenus[bottomMenuLength - 2] : bottomMenus[bottomMenuLength - 1];
                            let douyinVideoDownloaderDom = document.querySelector("#douyin-video-downloder");
                            if (douyinVideoDownloaderDom) {
                                douyinVideoDownloaderDom.parentNode.parentNode.removeChild(douyinVideoDownloaderDom.parentNode);
                            }

                            // 拷贝一个节点
                            let playbackSetting = bottomMenu.querySelector(".xgplayer-playback-setting");
                            if (!playbackSetting) {
                                return false;
                            }
                            let download = playbackSetting.cloneNode(true);
                            let downloadText = download.querySelector("div:first-child");
                            downloadText.innerText = "下载";
                            downloadText.style = "font-size:14px";
                            downloadText.setAttribute("id", "douyin-video-downloder");

                            let autoplaySetting = document.querySelector(".xgplayer-autoplay-setting");
                            if (!autoplaySetting) {
                                return false;
                            }
                            autoplaySetting.after(download);
                            let videoPlayers = document.querySelectorAll("video");
                            let videoPlayDom = videoPlayers[videoPlayers.length > 1 ? videoPlayers.length - 2 : videoPlayers.length - 1];
                            document.querySelector("#douyin-video-downloder").addEventListener("click", (e) => {
                                let playerUrl = videoPlayDom.children[0].src;
                                commonFunctionObject.GMopenInTab(playerUrl);
                            });
                        } catch (e) {}
                    }
                    //监听鼠标
                    window.addEventListener("wheel", downloader);
                    window.addEventListener("keydown", function (e) {
                        if (e.code == "ArrowDown" || e.code == "ArrowUp") {
                            downloader();
                        }
                    });
                    //视频改变后触发
                    async function domNodeInserted() {
                        let findVideoInterval = setInterval(function () {
                            let videoElement = document.querySelector("video");
                            if (videoElement) {
                                videoElement.addEventListener("DOMNodeInserted", (e) => {
                                    downloader();
                                });
                                clearInterval(findVideoInterval);
                            }
                        }, 200);
                    }
                    domNodeInserted();
                    downloader();
                    window.addEventListener("click", downloader);
                }
            });
        };
        this.kuaishouVideoDownloader = function () {
            if (window.location.host !== "www.kuaishou.com") {
                return;
            }
            window.addEventListener("load", function () {
                async function downloader() {
                    let kuaishouVideoDownloder = document.querySelector("#kuaishou-video-downloder");
                    if (!kuaishouVideoDownloder) {
                        let downloadDIV = document.createElement("div");
                        downloadDIV.style =
                            "cursor:pointer;width:50px;height:40px;line-height:40px;text-align:center;background-color:#FFF;color:#000;position:fixed;top:200px;left:0px;z-index:999;";
                        downloadDIV.innerText = "下载";
                        downloadDIV.setAttribute("id", "kuaishou-video-downloder");
                        document.body.appendChild(downloadDIV);

                        downloadDIV.addEventListener("click", function (e) {
                            let videoDom = document.querySelector(".player-video");
                            if (!videoDom) {
                                console.log("没有找到DOM");
                                return;
                            }
                            let videoSrc = videoDom.getAttribute("src");
                            if (videoSrc.match(/^blob/)) {
                                console.log("blob视频无法下载");
                                return;
                            }
                            commonFunctionObject.GMopenInTab(videoSrc);
                        });
                    }
                }
                document.querySelectorAll(".switch-item").forEach(function (value) {
                    value.addEventListener("click", function () {
                        downloader();
                    });
                });
                downloader();
                setInterval(function () {
                    let kuaishouVideoDownloder = document.querySelector("#kuaishou-video-downloder");
                    if (kuaishouVideoDownloder) {
                        if (window.location.href.match(/https:\/\/www\.kuaishou\.com\/short-video\/.*?/)) {
                            kuaishouVideoDownloder.style.display = "block";
                        } else {
                            kuaishouVideoDownloder.style.display = "none";
                        }
                    }
                }, 800);
            });
        };
        this.start = function () {
            this.douyinVideoDownloader();
            this.kuaishouVideoDownloader();
        };
    }
    new shortVideoDownloader().start();
})();
