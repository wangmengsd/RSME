# -*- coding: UTF-8 -*-
'''
To export image urls from imageNet datasets in dolt.
'''
import argparse
import pymysql

def parse_args():
    """
    parase args
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',default="localhost")
    parser.add_argument('--DBUser', default='root')
    parser.add_argument('--DBPasswd', default='')
    parser.add_argument('--DB', default='image_net')
    parser.add_argument('--nums', default=50)
    parser.add_argument('--entIDs', default='entities')
    parser.add_argument('--output_file', default='ent_links')
    args = parser.parse_args()                                       # 步骤三
    return args

def exportURL(args):
    '''
    To export image urls from imageNet datasets in dolt.
    :param args: parameters of Dolt sql server
    :return:
    '''
    with open(args.entIDs,'r') as f: #The ids of entities in WN18
        Ents=f.readlines()

    with open(args.output_file,'a') as f: #The ids and urls of entities in WN18
        conn = pymysql.connect(host=args.host, user=args.DBUser, password=args.DBPasswd, db=args.DB)
        cursor = conn.cursor()
        count=0
        for ent in Ents:
            f.write(ent.strip()+'\t')
            sql = "SELECT * FROM `images_synsets` where synset_type='n' and synset_id='{0}' LIMIT 50".format(ent.strip()[1:])
            print(sql)
            cursor.execute(sql)
            ret = cursor.fetchall()
            if len(ret)==0:
                print('None')
                continue
            print(ret)
            for t in ret:
                f.write(t[3]+'|')
            f.write('\n')
            f.flush()
            count+=1
            print(count)
        cursor.close()
        conn.close()

if __name__ == '__main__':
    args=parse_args()
    exportURL(args)


