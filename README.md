## Datasets：

**WN18：**

WN18 is a well-known KG which is originally extracted from WordNet. You can download [here](https://github.com/DeepGraphLearning/KnowledgeGraphEmbedding/tree/master/data/wn18) or [here](https://github.com/thunlp/IKRL).

**FB15K:**

FB15K is a widely used dataset in KG embedding extracted from Freebase. You can download [here](https://github.com/DeepGraphLearning/KnowledgeGraphEmbedding/tree/master/data/FB15k).

**WN18-IMG：**

WN18-IMG is an extended dataset of WN18 [4] which prepares 10 images for each entity. Due to copyright reasons, it is not possible to give images directly in this article. You can obtain WN18-IMG by the following methods.

Entity images in WN18 can be obtained from ImageNet, and the specific entity image addresses can be obtained from [Dolt](https://github.com/dolthub/dolt). The specific steps are as follows:

1.Install Dolt

Dolt is a SQL database that you can fork, clone, branch, merge, push and pull just like a git repository. To install on Linux or Mac based systems run this command in your terminal:

```/
sudo bash -c 'curl -L https://github.com/dolthub/dolt/releases/latest/download/install.sh | bash'
```

2.Clone ImageNet

```
dolt clone dolthub/image-net
```

3.Start dolt sql server  

```
dolt sql-server &
```

4.Create conda environment

```/
conda create --name RSME python=3.7
conda activate RSME
conda install pymysql
conda install requests
conda install Pillow
```

5.Run export scripts

```/
python ./tools/export_urls.py --entIDs=./data/wn_enties 
python ./tools/image_downloader.py --output_dir=./data/wn8 --entLinks=./data/ent_links --threads_num=5
```


**FB15K-IMG：**

[mmkb](https://github.com/mniepert/mmkb) provides a list of URLs that can be downloaded with a [script](https://github.com/mniepert/mmkb/blob/master/download-images.py) which also scales the images (thanks to [https://github.com/jrieke](https://github.com/jrieke)).


## Image Encoder
This project implements 4 types of image Encoder, Vision Transformer, Resnet50, VGG16, PHash. you can use them from image_encoder.py.
```/
conda install pytorch-gpu
pip install pytorch_pretrained_vit
conda install imagehash
python image_encoder.py
```

## Filter Gate：

The filter gate serves to filter images from the dataset level which are potentially incorrect, and it is implemented infilter_gate.py.


## MRP：
MRP is used to calculate the importance of pictures to relations, which is implemented in MRP.py.


