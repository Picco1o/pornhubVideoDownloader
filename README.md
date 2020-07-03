# pornhubVideoDownloader
多线程pornhub视频下载器

#### python版本
- [x] python3+

#### 使用说明
- 下载项目：

 ```shell
git clone https://github.com/Picco1o/pornhubVideoDownloader.git
```

- 下载依赖：

 ```shell
# linux需先配置node.js或其他javascript运行环境
cd pornhubVideoDownloader
pip install -r requirements.txt
# or
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

- 运行：

 ```python
python downloader.py -u https://cn.pornhub.com/view_video.php?viewkey=xxxxxxxxxxxxxxx
```

- 运行参数说明：

|参数   |是否必填   |说明   |
| ------------ | ------------ | ------------ |
| -u/--url  | 是  | pornhub播放页面url  |
|  -t/-- thread | 否  | 下载线程数，默认为5  |

- 示例：

 ```python
python downloader.py -u https://cn.pornhub.com/view_video.php?viewkey=ph5c0491898480f
```
