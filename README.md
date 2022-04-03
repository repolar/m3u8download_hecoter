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
import json
import time

from m3u8download_hecoter import parser,download,merge,delFile

def m3u8download(m3u8url,title=''):
    # 构造m3u8下载信息
    # m3u8url = 'https://defaultts.tc.qq.com/AfOx6zHHnDOlZi-1ib1P4wWLaqTVFSR8HUAL5zOLviKI/uwMROfz2r55goaQXGdGnC2de64gtX89GT746tcTJVnDpJgsD/svp_50112/6sxUTJMEy1aAvt2kNwrxNLM-fJtbUJIh5nq25C1f3zXCLEaprNxWVtvjEFKpH0RyQ7WL2Yy1EK7se8x2imryJ03VDTVu6Qifex1O2xlxCwJj1fNTvjkyV70CEUSFqiV2jxytAOk-W_zQSjHwWZzZwjSQTz0benSgbMNLcqDEo06HX2CGIwwY5Q/gzc_1000102_0b53kaabyaaabeahf5ymrfrmaugddroaagca.f321004.ts.m3u8?ver=4'

    title,durations,count,temp_dir,data = parser.Parser(m3u8url,title='').run()
    tm = time.strftime("%H:%M:%S", time.gmtime(durations))
    print(title,tm)
    segments = json.loads(data)['segments']

    infos = []
    for segment in segments:
        name = segment['title'] + '.ts'
        uri = segment['uri']
        info1 = {
            'title': temp_dir +'/video/'+name,
            'link': uri
        }
        infos.append(info1)

    download.FastRequests(infos).run() # 下载

    # 下载完成，开始合并
    merge.Merge(temp_dir)
    # 删除多余文件
    delFile.del_file(temp_dir)

if __name__ == '__main__':
    m3u8url = 'https://defaultts.tc.qq.com/AfOx6zHHnDOlZi-1ib1P4wWLaqTVFSR8HUAL5zOLviKI/uwMROfz2r55goaQXGdGnC2de64gtX89GT746tcTJVnDpJgsD/svp_50112/6sxUTJMEy1aAvt2kNwrxNLM-fJtbUJIh5nq25C1f3zXCLEaprNxWVtvjEFKpH0RyQ7WL2Yy1EK7se8x2imryJ03VDTVu6Qifex1O2xlxCwJj1fNTvjkyV70CEUSFqiV2jxytAOk-W_zQSjHwWZzZwjSQTz0benSgbMNLcqDEo06HX2CGIwwY5Q/gzc_1000102_0b53kaabyaaabeahf5ymrfrmaugddroaagca.f321004.ts.m3u8?ver=4'

    m3u8download(m3u8url,title='123')

```

## decrypt.py

解密，暂时没写

```

```

## parser.py

解析 m3u8 链接，方便后面传入下载模块

```
import m3u8
import os,re,json
from time import strftime,gmtime

class Parser:
    def __init__(
            self,m3u8url,title='',work_dir='./Downloads',headers={
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63030532) Edg/100.0.4896.60',
                'Cookie':''
            }
                 ):

        if not os.path.exists(work_dir):
            os.makedirs(work_dir)


        if title == '':
            title = m3u8url.split('?')[0].split('/')[-1].replace('.m3u8', '')
        self.title = self.check_title(title)
        self.temp_dir = work_dir+'/'+title
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        if not os.path.exists(self.temp_dir + '/video'):
            os.makedirs(self.temp_dir + '/video')
        if not os.path.exists(self.temp_dir + '/audio'):
            os.makedirs(self.temp_dir + '/audio')

        self.m3u8url = m3u8url
        self.headers = headers
        self.work_dir = work_dir
        self.durations = 0
        self.count = 0


    def run(self):
        m3u8obj = m3u8.load(uri=self.m3u8url, verify_ssl=False, headers=self.headers)


        segments = m3u8obj.data['segments']
        self.count = len(segments)
        for i, segment in enumerate(segments):
            # 计算时长
            if 'duration' in segment:
                self.durations += segment['duration']

            if 'http' != segment['uri'][:4]:
                if segment['uri'][:2] == '//':
                    segment['uri'] = 'https:' + segment['uri']
                else:
                    segment['uri'] = m3u8obj.base_uri + segment['uri']

                segments[i]['uri'] = segment['uri']
            segment['title'] = str(i).zfill(6)
            segments[i]['title'] = segment['title']

        data = json.dumps(m3u8obj.data, indent=4)

        with open(f'{self.work_dir}/{self.title}/meta.json', 'w', encoding='utf-8') as f:
            f.write(data)
        # 写入raw.m3u8
        raw = m3u8obj.dumps()
        with open(self.work_dir + '/' + self.title + '/' + 'raw.m3u8', 'w', encoding='utf-8') as f:
            f.write(raw)

        return self.title,self.durations,self.count,self.temp_dir,data

    def check_title(self,title):
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_title = re.sub(rstr, "_", title)  # 替换为下划线
        return new_title
```

## download.py

实际多线程下载部分，另配有简易进度条

```
import os
import re

import requests
from threading import Thread
from queue import Queue
import time

q = Queue(100000)
ALL_COUNT = 0
DONE_COUNT = 0

ALL_SIZE = 0
DONE_SIZE = 0


class FastRequests:
    def __init__(
            self,infos,threads=20,headers={
            'User-Agent':'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320 Edg/99.0.4844.74',
            'Cookie':''
        }
    ):
        self.threads = threads # 线程数 20
        global ALL_COUNT
        ALL_COUNT = len(infos)
        self.all_count = len(infos)
        for info in infos:
            q.put(info)
        self.headres = headers

    def run(self):
        for i in range(self.threads):
            t = Consumer(self.headres)
            t.start()

        while DONE_COUNT < ALL_COUNT:
            time.sleep(0.01)


class Consumer(Thread):
    def __init__(self,headers):
        Thread.__init__(self)
        self.headers = headers
        self.retry_times = 16


    def run(self):
        while True:
            if q.qsize() == 0:
                break
            self.download(q.get())

    def sizeFormat(self, size, is_disk=False, precision=2):

        formats = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
        unit = 1000.0 if is_disk else 1024.0
        if not (isinstance(size, float) or isinstance(size, int)):
            raise TypeError('a float number or an integer number is required!')
        if size < 0:
            raise ValueError('number must be non-negative')
        for i in formats:
            size /= unit
            if size < unit:
                return f'{round(size, precision)}{i}'
        return f'{round(size, precision)}{i}'

    def download(self,info):
        global DONE_SIZE
        title = info['title']
        link = info['link']

        if not os.path.exists(title):
            for i in range(self.retry_times):
                response = requests.get(url=link, headers=self.headers, stream=True)
                ts = response.content
                DONE_SIZE += ts.__sizeof__()
                with open(title, 'wb') as f:
                    f.write(ts)
                    f.close()
                if response.status_code == 200:
                    break


        global DONE_COUNT
        DONE_COUNT += 1
        # 简化的进度条
        print(f'\r[{DONE_COUNT}/{ALL_COUNT}] [{self.sizeFormat(DONE_SIZE)}/{self.sizeFormat((DONE_SIZE/DONE_COUNT)*ALL_COUNT)}] {round((DONE_COUNT/ALL_COUNT)*100,2)}%',end='')
```

## 	merge.py

下载完成合并部分，有3种合并方式，二进制合并，先二进制合并再 ffmpeg 转码，直接 ffmpeg 合并，默认第三种，其他可自行选择

```
import os
from shutil import rmtree
import subprocess

class Merge:
    def __init__(self,temp_dir:str,mode=3):
        self.temp_dir = temp_dir

        self.file_list = []
        for root, dirs, files in os.walk(temp_dir+r'\video'):
            for f in files:
                file = os.path.join(root, f)
                if os.path.isfile(file):
                    self.file_list.append(file)

        if mode == 1:
            self.mode1()
        elif mode == 2:
            self.mode2()
        elif mode == 3:
            self.mode3()
        else:
            print('合并方式输入错误！进行二进制合并中……')

    # 直接二进制合并
    def mode1(self):
        with open(self.temp_dir+'.mp4','wb') as f1:
            for i in self.file_list:
                with open(i,'rb') as f2:
                    f1.write(f2.read())
                    f2.close()
            f1.close()


    # 先二进制合并再 ffmpeg 转码
    def mode2(self):
        if not os.path.exists(self.temp_dir + "_ffmpeg.mp4"):
            self.mode1()
            try:
                cmd = 'ffmpeg -loglevel panic'
                os.system(cmd)

                cmd = f'ffmpeg -i {self.temp_dir + ".mp4"} -c copy {self.temp_dir + "_ffmpeg.mp4"} -loglevel panic'
                os.system(cmd)

            except:
                print('未找到 ffmpeg ')

    # 直接 ffmpeg 合并
    def mode3(self):
        if not os.path.exists(self.temp_dir + ".mp4"):
            try:
                cmd = 'ffmpeg -loglevel panic'
                os.system(cmd)
                filelist = [f"file './video/{str(i).zfill(6)}.ts'" for i in range(len(self.file_list))]
                with open(self.temp_dir + '/filelist.txt','w') as f:
                    for i in filelist:
                        f.write(i)
                        f.write('\n')
                    f.close()
                cmd = f"ffmpeg -f concat -safe 0 -i {self.temp_dir + '/filelist.txt'} -c copy {self.temp_dir + '.mp4'} -loglevel panic"
                os.system(cmd)

            except:
                print('未找到 ffmpeg ')
```

## delFile.py

删除多余文件

```
from shutil import rmtree

def del_file(temp_dir):
    rmtree(rf'{temp_dir}', ignore_errors=True)
```

## 使用方法

下载完整代码：https://github.com/hecoter/m3u8download_hecoter 直接调用

```
from m3u8download_hecoter import m3u8download

m3u8url = 'https://defaultts.tc.qq.com/AfOx6zHHnDOlZi-1ib1P4wWLaqTVFSR8HUAL5zOLviKI/uwMROfz2r55goaQXGdGnC2de64gtX89GT746tcTJVnDpJgsD/svp_50112/6sxUTJMEy1aAvt2kNwrxNLM-fJtbUJIh5nq25C1f3zXCLEaprNxWVtvjEFKpH0RyQ7WL2Yy1EK7se8x2imryJ03VDTVu6Qifex1O2xlxCwJj1fNTvjkyV70CEUSFqiV2jxytAOk-W_zQSjHwWZzZwjSQTz0benSgbMNLcqDEo06HX2CGIwwY5Q/gzc_1000102_0b53kaabyaaabeahf5ymrfrmaugddroaagca.f321004.ts.m3u8?ver=4'

m3u8download(m3u8url,title='')
```

