# python 多线程实例—简易的m3u8下载器

## 介绍

这个是上篇帖子的实际应用 [简易封装的python多线程类 - 『编程语言讨论求助区』 - 吾爱破解 - LCG - LSG |安卓破解|病毒分析|www.52pojie.cn](https://www.52pojie.cn/thread-1615108-1-1.html)

主要用来多线程下载文件，对m3u8链接进行了 解析、下载、解密（暂无）、合并、删除等操作

## 文件内容：

m3u8download_hecoter

​		__init__.py

​		decrypt.py

​		delFile.py

​		download.py

​		merge.py

​		parser.py

## __init__.py

识别为 python 程序，向里面插入代码也可以在外部直接引用

```

```

## decrypt.py

支持 AES_128、SAMPLE-AES-CTR、KOOLEARN-ET、Widevine

```

```

## parser.py

解析 m3u8 链接，方便后面传入下载模块

```

```

## download.py

实际多线程下载部分，另配有简易进度条

```

```

## 	merge.py

下载完成合并部分，有3种合并方式，二进制合并，先二进制合并再 ffmpeg 转码，直接 ffmpeg 合并，默认第三种，其他可自行选择

```

```

## delFile.py

删除多余文件

```

```

## 使用方法

下载完整代码：https://github.com/hecoter/m3u8download_hecoter 直接调用

```
from m3u8download_hecoter import m3u8download

m3u8url = 'https://defaultts.tc.qq.com/AfOx6zHHnDOlZi-1ib1P4wWLaqTVFSR8HUAL5zOLviKI/uwMROfz2r55goaQXGdGnC2de64gtX89GT746tcTJVnDpJgsD/svp_50112/6sxUTJMEy1aAvt2kNwrxNLM-fJtbUJIh5nq25C1f3zXCLEaprNxWVtvjEFKpH0RyQ7WL2Yy1EK7se8x2imryJ03VDTVu6Qifex1O2xlxCwJj1fNTvjkyV70CEUSFqiV2jxytAOk-W_zQSjHwWZzZwjSQTz0benSgbMNLcqDEo06HX2CGIwwY5Q/gzc_1000102_0b53kaabyaaabeahf5ymrfrmaugddroaagca.f321004.ts.m3u8?ver=4'

m3u8download(m3u8url,title='')
```

