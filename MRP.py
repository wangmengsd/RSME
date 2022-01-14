import pickle
from pathlib import Path
import numpy as np
from collections import defaultdict

def get_filtered_triples(base_path,output_file):
    ent_1_1_triple=[]
    root = Path(base_path)
    files = ['train', 'valid', 'test']

    for f in files:
        cnt_1, cnt_2, cnt_3, cnt_above_3 = 0, 0, 0, 0
        triples = open(root / (f ), 'r').readlines()
        triples=[triple.strip().split('\t') for triple in triples]
        # triples = triples.tolist() # return type is np.array
        num = len(triples)
        heads = defaultdict(defaultdict)
        for tri in triples:
            h, r, t = tri[:]
            h=h.strip()
            r=r.strip()
            t=t.strip()
            if t not in heads[h]:
                heads[h][t] = []
            heads[h][t].append((h,r,t))
        for k, v in heads.items():
            for kk, l in v.items():
                if len(l) == 1:
                    cnt_1 += 1
                    ent_1_1_triple.append(l[0])
                if len(l) == 2:
                    cnt_2 += 2
                if len(l) == 3:
                    cnt_3 += 3
                if len(l) > 3: cnt_above_3 += len(l)
        print(f)
        print('total triples: {}, 1-1-1: {}, 1-2-1: {}, 1-3-1: {}, 1-n-1:{}(n>3)'
              .format(num, cnt_1, cnt_2, cnt_3, cnt_above_3))
        cnt = [cnt_1, cnt_2, cnt_3, cnt_above_3]
        ratio = [float(format(i / num, '.4f')) for i in cnt]
        print('ratio: 1-1-1: {}, 1-2-1: {}, 1-3-1: {}, 1-n-1:{}(n>3)'.
              format(ratio[0], ratio[1], ratio[2], ratio[3]))
    out=open(output_file,'wb')
    pickle.dump(ent_1_1_triple,out)
    out.close()

def get_rank(triples: list, img_vectors: dict, tails,tail_norm_vector_file='fb15k_tail_norm_vector.pickle'):
    triples.sort()
    tails = sorted(list(tails))
    filtered_tails, tail_vectors, cur_ranks = [], [], []
    for i, t in enumerate(tails):
        print('{0} in {1}'.format(t,t in img_vectors.keys())  )
        if t in img_vectors.keys():
            tail_vectors.append(img_vectors[t])
            filtered_tails.append(t)
    h_t = defaultdict(list)   #dict，head--->tail
    heads = set()
    for tri in triples:
        if tri[2] in filtered_tails:
            h_t[tri[0]].append(tri[2])
        heads.add(tri[0])
    heads = sorted(list(heads))
    infile=open(tail_norm_vector_file,'rb')
    tail_norm_vector = pickle.load(infile)
    infile.close()
    for h in heads:
        if h not in img_vectors or h_t[h] == []:
            continue
        head_norm_vector = np.tile(np.array(img_vectors[h])/np.sqrt(np.sum(img_vectors[h] ** 2)),(len(tail_vectors), 1)) #头实体向量标准化
        scores = np.sum(head_norm_vector * tail_norm_vector, axis=1)
        # cosine_scores, type: np.array, the bigger the better
        true_tail_idx = [filtered_tails.index(t) for t in h_t[h]]
        score_rank = np.argsort(-scores).tolist()
        ranks = [1 + score_rank.index(i) for i in true_tail_idx]
        # ranks = [score_rank.index(i) for i in true_tail_idx]
        cur_avg_rank = sum(ranks) / len(ranks)
        cur_ranks.append(cur_avg_rank / len(score_rank))
    return sum(cur_ranks) / len(cur_ranks), '%.1f' % cur_avg_rank + '/' + str(len(tails))


def calculate_MRP(img_vec_file='fb15k_vgg16.pickle',triples_file='fb15k_1_1_triples.pickle',output_file='fb15k_vgg_rank.txt',base_path='./'):
    root = Path(base_path)
    img_vec = pickle.load(open(root / img_vec_file , 'rb'))
    triples_all = pickle.load(open(root / triples_file, 'rb'))
    rel_triples = {}
    all_ranks, rels, ratio = [], [], []

    ent_vec = {'/'+k.split('/')[-2].replace('.','/'): v for k, v in img_vec.items()} #change image address format
    tail_ent = set() #储存所有实体ent
    for triple in triples_all: # 按关系分类，统计rel_triples
        triple = [i.strip(' ') for i in triple]
        h, r, t = triple
        r_list = rel_triples.get(r, list())
        r_list.append(triple)
        rel_triples[r] = r_list
        tail_ent.add(t)
    cnt = 1
    for rel, triples in rel_triples.items():
        print('process relations: {}/{}'.format(cnt, len(rel_triples.keys())))
        # print(wn8_ent_vec.keys())
        score, ratio_str = get_rank(triples, ent_vec, tail_ent)  #tirples: all triples under this relation, ent_vec:dict, path-entity vector, tail_ent: all tail entities
        print(score,ratio_str)
        rels.append(rel)
        all_ranks.append(score)
        ratio.append(ratio_str)
        cnt += 1
    avg_rank = sum(all_ranks) / len(all_ranks)
    with open(root / output_file, 'w') as f:
        for i in range(len(all_ranks)):
            f.write('relation id: ' + rels[i] + '\t'
                    + 'rank: ' + str(all_ranks[i]) + '\t'
                    + 'percentage: ' + ratio[i] + '\n')
        f.write('average rank: ' + str(avg_rank))
    print('average rank:{}'.format(avg_rank))


if __name__ == '__main__':
    calculate_MRP()