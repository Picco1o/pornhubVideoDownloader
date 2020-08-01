import requests
import os
import time
import execjs
import argparse
from lxml import etree
from concurrent.futures import ThreadPoolExecutor, as_completed


parser = argparse.ArgumentParser(description='some args')
parser.add_argument('-u', '--url', required=True, help='pornhub video url')
parser.add_argument('-t', '--thread', help='download threads', default=5, type=int)
args = parser.parse_args()
base_url = args.url
s = requests.Session()
STORAGE_FOLDER = 'video'
download_size = 0
executor = ThreadPoolExecutor(max_workers=args.thread)


def parse():
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
	}
	video_list = []
	try:
		r = s.get(base_url, headers=headers, stream=True)
		html = etree.HTML(r.text)
		js = html.xpath('//*[@id="player"]/script[1]')[0].text
		id = html.xpath('//*[@id="player"]')[0].get('data-video-id')
	except:
		print(r.status_code)
		return (False, video_list)
	ctx = execjs.compile('var playerObjList = {};'+js)
	result = ctx.eval('flashvars_{}'.format(id))
	for i in result['mediaDefinitions']:
		if i['format'] == 'mp4':
			config = {}
			config['quality'] = i['quality'] + 'p'
			config['url'] = i['videoUrl']
			config['filename'] = result['video_title'] + '-' + i['quality']+'p' + '.mp4'
			video_list.append(config)
	return (True, video_list)


def segmentation(video_size):
    limit = int(1024 * 1024)
    end = size = video_size
    start = 0
    while True:
        if limit > end:
            yield (start, size)
            break
        else:
            yield (start, (start+limit))
            end -= limit
            start += (limit+1)


def download(size, config, chunk, file):
    global download_size
    url = config['url']
    headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36 Edg/80.0.361.109',
		'Range': 'bytes={}-{}'.format(chunk[0], chunk[1])
    }
    r = s.get(url, headers=headers)
    download_size += int(r.headers['Content-Length'])
    file.seek(chunk[0])
    file.write(r.content)
    icon = int(50 * download_size / size)
    print('\r' + '[下载进度]:[{}]{:.2f}%'.format(('#' * icon).ljust(50), (download_size / size * 100)), end='')


def create_task(size, file, config):
	for i in segmentation(size):
			task = executor.submit(download, size, config, i, file)
			yield task


def start(config):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
		'Range': 'bytes=0-1'
	}
	filename = '{}/{}'.format(STORAGE_FOLDER, config['filename'])
	if os.path.exists(filename):
		print('文件已存在！')
		return
	else:
		try:
			r = s.get(config['url'], headers=headers, stream=True)
			size = int(r.headers['Content-Range'].split('/')[1])
		except:
			print(r.status_code)
			return
		print('[文件大小]:%0.2fMB' % (size / 1024 / 1024))
		start = time.time()
		with open(filename, 'wb+') as file:
			for future in as_completed(create_task(size, file, config)):
					future.result()
		print('\n下载完成!用时:{:.2f}秒'.format(time.time()-start))



def main():
	if not os.path.exists(STORAGE_FOLDER):
		os.makedirs(STORAGE_FOLDER)
	result = parse()
	if result[0]:
		config = result[1]
		print('# 可用下载')
		for index, value in enumerate(config):
			print('{}:{}'.format(index, value['quality']))
		try:
			id = int(input('# 请输入对应的下载序号：'))
		except:
			print('输入有误！')
			return
		if id+1 > len(config):
			print('未找到对应序号')
		# print(config[id])
		start(config[id])
	else:
		print('请检查输入url及网络！')


if __name__ == '__main__':
	main()