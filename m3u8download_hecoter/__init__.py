import json,sys,os
import time,base64

from m3u8download_hecoter import parser,download,merge,delFile

def m3u8download(m3u8url,title=''):
    # 构造m3u8下载信息
    # m3u8url = 'https://defaultts.tc.qq.com/AfOx6zHHnDOlZi-1ib1P4wWLaqTVFSR8HUAL5zOLviKI/uwMROfz2r55goaQXGdGnC2de64gtX89GT746tcTJVnDpJgsD/svp_50112/6sxUTJMEy1aAvt2kNwrxNLM-fJtbUJIh5nq25C1f3zXCLEaprNxWVtvjEFKpH0RyQ7WL2Yy1EK7se8x2imryJ03VDTVu6Qifex1O2xlxCwJj1fNTvjkyV70CEUSFqiV2jxytAOk-W_zQSjHwWZzZwjSQTz0benSgbMNLcqDEo06HX2CGIwwY5Q/gzc_1000102_0b53kaabyaaabeahf5ymrfrmaugddroaagca.f321004.ts.m3u8?ver=4'

    # list: m3u8url = [{'m3u8url':m3u8url,'title':title},{'m3u8url':m3u8url,'title':title}]
    if type(m3u8url) == list:
        for info in m3u8url:
            print(info)
            m3u8download(m3u8url=info['m3u8url'],title=info['title'])
        sys.exit(0)
    # dir: m3u8url = r'c:\windows\'
    if os.path.isdir(m3u8url):
        for root, dirs, files in os.walk(m3u8url):
            for f in files:
                file = os.path.join(root, f)
                if os.path.isfile(file):
                    if file.split('.')[-1] == 'm3u8':
                        m3u8download(m3u8url=file)
        sys.exit(0)
    title,durations,count,temp_dir,data,method = parser.Parser(m3u8url,title).run()
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
        if 'key' in segment:
            info1['method'] = method
            info1['key'] = base64.b64decode(segment['key']['uri'])
            info1['iv'] = bytes.fromhex(segment['key']['iv'])

        infos.append(info1)

    download.FastRequests(infos).run() # 下载

    # 下载完成，开始合并
    merge.Merge(temp_dir)
    # 删除多余文件
    delFile.del_file(temp_dir)



if __name__ == '__main__':
    m3u8url = 'https://apd-b1924eab69f4e728bd6e28684186fb71.v.smtcdns.com/vipts.tc.qq.com/Anj2gsQ3IeiDU0qrEG0-qLWeZAT8u2b8VwK6a2Sh17zA/uwMROfz2r57AoaQXGdGnC2de64-aQGMBaghPzSlG8CDdub8-/svp_50112/WhAvXfzicpP6Io4AStHy4eWRa8Wb9zTu-bVSGL1twfSP9Gl-iYVlBjzrO9bC8TCp_ere2MjUGqCu1-iA8kGDclx9rHaBF6JDM3R7XXi96DK5OEOt_iDp5L0nc5Ss8C3WEEtM8_afpbl4D1785wL35tac6ufERqZitOeP130huyRBKV2VT2vbrA/0385_gzc_1000102_0b53vyabuaaabqaak4rhe5rmblwddkraahsa.f321003.ts.m3u8?ver=4'
    m3u8download(m3u8url)
