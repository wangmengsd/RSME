# -*- coding: UTF-8 -*-
'''
download images and scale
'''
import argparse
from PIL import Image
import requests
import os
import _thread


def parse_args():
    """
    parase args
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--threads_num',default=5,type=int)
    parser.add_argument('--image_num', default=3)
    parser.add_argument('--entLinks', default='ent_links')
    parser.add_argument('--output_dir', default='wn8')
    args = parser.parse_args()                                       # 步骤三
    return args

def is_valid(file):
    '''
    is valid image file?
    :param file:
    :return:
    '''
    valid = True
    try:
        Image.open(file).load()
    except OSError:
        valid = False
    return valid


def download_img(img_urls, name,args):
    '''
    download images
    :param img_urls:
    :param name: entity ID
    :return:
    '''
    succ_cnt=0
    for img_url in img_urls:
        header = {"User-Agent":'Mozilla/5.0 (Macintosh; '
                               'Intel Mac OS X 10_15_7) '
                               'AppleWebKit/537.36 (KHTML,'
                               ' like Gecko) Chrome/88.0.4324.192'
                               ' Safari/537.36'}
        try:
            r = requests.get(img_url, headers=header,timeout=10)
        except Exception as e:
            print(e)
            continue
        if r.status_code == 200:
            f=open(args.output_dir+'/{0}/{1}.JPEG'.format(name,name+'_'+str(succ_cnt)), 'wb')
            f.write(r.content)
            f.flush()
            f.close()
            if not is_valid(args.output_dir+'/{0}/{1}.JPEG'.format(name,name+'_'+str(succ_cnt))):
                continue
        else:
            del r
            continue
        succ_cnt+=1
        if succ_cnt>args.image_num-0.1:
            break

global count
count = 0
def run(args):
    '''
    multi Threads
    :return:
    '''
    while 1:
        global count
        count+=1
        print(count)
        ent=Ents_need.pop()
        name,urls=ent.split('\t')
        Urls=urls.split('|')
        if not os.path.exists(args.output_dir+'/' + name):
            os.mkdir(args.output_dir+'/' + name)
        else:
            pass
        try:
            download_img(Urls,name,args)
        except Exception as e:
            print(e)
            print('{0} fail110'.format(name))


if __name__ == '__main__':
    args=parse_args()
    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)
    Ents_ready = os.listdir(args.output_dir)
    Ents_ready = [e.strip() for e in Ents_ready]
    with open(args.entLinks, 'r') as f:
        Ents = f.readlines()
    Ents_need = [l for l in Ents if l.split('\t')[0] not in Ents_ready]
    for i in range(args.threads_num):
        _thread.start_new_thread(run, (args,))

    while 1:
        pass


