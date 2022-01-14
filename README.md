## Datasets：

**WN18：**

WN18 is a well-known KG which is originally extracted from WordNet. You can download [here](https://github.com/DeepGraphLearning/KnowledgeGraphEmbedding/tree/master/data/wn18).

**FB15K:**

FB15K is a widely used dataset in KG embedding extracted from Freebase. You can download [here](https://github.com/DeepGraphLearning/KnowledgeGraphEmbedding/tree/master/data/FB15k).

**WN18-IMG：**

WN18-IMG is an extended dataset of WN18 [4] which prepares 10 images for each entity. 由于版权原因，本文无法直接给出图片。你可以通过如下方法获取WN18-IMG。

WordNet 中的实体图片可以从ImageNet中获取，具体的实体图片地址可以从[Dolt](https://github.com/dolthub/dolt)中获得。具体步骤如下

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

本项目实现了4种image Encoder，分别是Vision Transformer、Resnet50、VGG16、PHash。你能从image_encoder.py中使用他们。

```/
conda install pytorch-gpu
pip install pytorch_pretrained_vit
conda install imagehash
python image_encoder.py
```

## Filter Gate：

The filter gate serves to filter images from the dataset level which are potentially incorrect, and it is implemented infilter_gate.py


MRP：

## Experiments

tools.py


```/
conda install matplotlib
```
