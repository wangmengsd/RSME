import numpy as np
import os
import random
import pickle

def get_img_vec_array(proportion,img_vec_path='fb15k_vit.pickle',eutput_file='/home/syh/MMKG/img_vec_id_fb15k_{}_vit.pickle',dim=1000):
    img_vec=pickle.load(open(img_vec_path,'rb'))
    img_vec={k.split('/')[-2]:v for k,v in img_vec.items()}
    f=open('./data/FB15K_{}/ent_id'.format(proportion),'r')
    Lines=f.readlines()

    id2ent={}
    img_vec_array=[]
    for l in Lines:
        ent,id=l.strip().split()
        id2ent[id]=ent
        if ent.replace('/','.')[1:] in img_vec.keys():
            print(id,ent)
            # id2vec[id]=img_vec[ent.replace('/','.')[1:]]
            img_vec_array.append(img_vec[ent.replace('/','.')[1:]])
        else:
            img_vec_array.append([0 for i in range(dim)])
    img_vec_by_id=np.array(img_vec_array)
    out=open(eutput_file.format(proportion),'wb')
    pickle.dump(img_vec_by_id,out)
    out.close()


def get_img_vec_array_forget(proportion,remember_proportion,rank_file='fb15k_vit_rank.txt',eutput_file='rel_MPR_PD_vit_{}_mrp{}.pickle'):
    with open(rank_file,'r') as f:
        Ranks=f.readlines()
        rel_rank={}
        for r in Ranks:
            try:
                rel,mrp=r.strip().split('\t')
            except Exception as e:
                print(e)
                print(r)
                continue
            rel_rank[rel[10:]]=float(mrp[12:])

    with open('./data/FB15K_{}/rel_id'.format(proportion),'r') as f:
        Lines=f.readlines()

    rel_id_pd=[]
    for l in Lines:
        rel,_=l.strip().split()
        try:
            if rel_rank[rel]<remember_proportion/100.0:
                rel_id_pd.append([1])
            else:
                rel_id_pd.append([0])
        except Exception as e:
            print(e)
            rel_id_pd.append([0])
            continue

    rel_id_pd=np.array(rel_id_pd)

    with open(eutput_file.format(proportion,remember_proportion),'wb') as out:
        pickle.dump(rel_id_pd,out)


def sample(proportion,data_path='./src_data/FB15K'):
    with open(data_path+'/train') as f:
        Ls=f.readlines()
        L = [random.randint(0, len(Ls)-1) for _ in range(round(len(Ls)*proportion))]
        Lf=[Ls[l] for l in L]

    if not os.path.exists(data_path+'_{}/'.format(round(proportion*100))):
        os.mkdir(data_path+'_{}/'.format(round(proportion*100)))
    Ent=set()

    with open(data_path+'_{}/train'.format(round(100*proportion)),'w') as f:
        for l in Lf:
            h,r,t=l.strip().split()
            Ent.add(h)
            Ent.add(r)
            Ent.add(t)
            f.write(l)
            f.flush()

    with open(data_path+'/valid','r') as f:
        Ls = f.readlines()

    with open(data_path+'_{}/valid'.format(round(100*proportion)),'w') as f:
        for l in Ls:
            h,r,t=l.strip().split()
            if h in Ent and r in Ent and t in Ent:
                f.write(l)
                f.flush()
            else:
                print(l.strip()+' pass')

    with open(data_path+'/test','r') as f:
        Ls = f.readlines()

    with open(data_path+'_{}/test'.format(round(proportion*100)),'w') as f:
        for l in Ls:
            h, r, t = l.strip().split()
            if h in Ent and r in Ent and t in Ent:
                f.write(l)
                f.flush()
            else:
                print(l.strip()+' pass')

if __name__ == '__main__':
    pass
    # get_img_vec_array_forget(30, 20)
    # sample(0.3)
    # get_img_vec_array(30)




# sc_img_vec_id()


#
# chouqu(0.03)
# chouqu(0.05)
# chouqu(0.07)
# chouqu(0.1)
# chouqu(0.15)
#
# sc_img_vec_id(3)
#
#
# sc_img_vec_id(5)
#
# sc_img_vec_id(7)
#
# sc_img_vec_id(15)

# chouqu(0.1)
# sc_img_vec_id_forget(100,20)

# chouqu(0.01)

# sc_img_vec_id(100)

# chouqu(1)

# sc_img_vec_id(100)
# sc_img_vec_id_forget(60,20)
# sc_img_vec_id_forget(80,20)
# sc_img_vec_id_forget(40,20)
# sc_img_vec_id_forget(5,20)
# sc_img_vec_id_forget(7,20)
# sc_img_vec_id_forget(15,20)
# sc_img_vec_id_forget(20,5)