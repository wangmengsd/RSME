# -*- coding: UTF-8 -*-
'''
Image encoder.  Get visual embeddings of images.
'''
import torch.nn
import torchvision.models as models
from torch.autograd import Variable
import torch.cuda
import torchvision.transforms as transforms
from PIL import Image
import pickle
from pytorch_pretrained_vit import ViT
import os
import imagehash

class ImageEncoder():
    TARGET_IMG_SIZE = 224
    img_to_tensor = transforms.ToTensor()
    Normalizer = transforms.Normalize((0.5,), (0.5,))

    @staticmethod
    def get_embedding(self):
        pass

    # 特征提取
    def extract_feature(self,base_path):
        self.model.eval()
        if not os.path.exists(base_path):
            os.mkdir(base_path)
        ents = os.listdir(base_path)
        dict = {}


        while len(ents) > 0:
            print(len(ents))
            ents_50 = []
            ents_50_ok = []
            for i in range(5):
                if len(ents) > 0:
                    ent = ents.pop()
                    try:
                        ents_50.append(base_path + ent + '/' + os.listdir(base_path + ent + '/')[0])
                    except Exception as e:
                        print(e)
                        continue

            tensors = []
            for imgpath in ents_50:
                try:
                    img = Image.open(imgpath).resize((384, 384))
                except Exception as e:
                    print(e)
                    continue
                img_tensor = self.img_to_tensor(img)
                img_tensor = self.Normalizer(img_tensor)

                if img_tensor.size()[0] == 3:
                    tensors.append(img_tensor)
                    ents_50_ok.append(imgpath)


            tensor = torch.stack(tensors, 0)
            tensor = tensor.cuda()

            result = self.model(Variable(tensor))
            result_npy = result.data.cpu().numpy()
            for i in range(len(result_npy)):
                dict[ents_50_ok[i]] = result_npy[i]

        return dict

class VisionTransformer(ImageEncoder):
    def __init__(self):
        super(VisionTransformer, self).__init__()
        self.model = ViT('B_16_imagenet1k', pretrained=True)

    def get_embedding(self,base_path):
        self.model.eval()
        self.model.cuda()
        self.d=self.extract_feature(base_path)
        return self.d

    def save_embedding(self,output_file):
        with open(output_file, 'wb') as out:
            pickle.dump(self.d, out)

class Resnet50(ImageEncoder):
    def __init__(self):
        super(Resnet50, self).__init__()
        self.model = models.resnet50(pretrained=True)

    def get_embedding(self,base_path):
        self.model.eval()
        self.model.cuda()
        self.d=self.extract_feature(base_path)
        return self.d

    def save_embedding(self,output_file):
        with open(output_file, 'wb') as out:
            pickle.dump(self.d, out)

class VGG16(ImageEncoder):
    def __init__(self):
        super(VGG16, self).__init__()
        self.model =models.vgg16(pretrained=True)

    def get_embedding(self,base_path):
        self.model.eval()
        self.model.cuda()
        self.d=self.extract_feature(base_path)
        return self.d

    def save_embedding(self,output_file):
        with open(output_file, 'wb') as out:
            pickle.dump(self.d, out)

class PHash(ImageEncoder):
    def __init__(self):
        super(PHash, self).__init__()
        self.model=imagehash

    def get_embedding(self,base_path,hash_size):
        if not os.path.exists(base_path):
            os.mkdir(base_path)
        ents = os.listdir(base_path)
        dict = {}
        while len(ents) > 0:
            print(len(ents))
            ents_50 = []
            ents_50_ok = []
            for i in range(5):
                if len(ents) > 0:
                    ent = ents.pop()
                    try:
                        ents_50.append(base_path + ent + '/' + os.listdir(base_path + ent + '/')[0])
                    except Exception as e:
                        print(e)
                        continue

            result_npy = []
            for imgpath in ents_50:
                try:
                    image_hash= imagehash.phash(Image.open(imgpath), hash_size=hash_size)
                except Exception as e:
                    print(e)
                    continue

                result_npy.append(image_hash)
                ents_50_ok.append(imgpath)

            for i in range(len(result_npy)):
                dict[ents_50_ok[i]] = result_npy[i]

        self.d=dict
        return dict



    def save_embedding(self,output_file):
        with open(output_file, 'wb') as out:
            pickle.dump(self.d, out)


if __name__ == "__main__":

    model1 = VisionTransformer()
    base_path = './img_data/fb15k/'
    model1.get_embedding(base_path)
    model1.save_embedding('fb15k_vit.pickle')

    model2 = Resnet50()
    base_path = './img_data/fb15k/'
    model2.get_embedding(base_path)
    model2.save_embedding('fb15k_resnet50.pickle')

    model3 = VGG16()
    base_path = './img_data/fb15k/'
    model3.get_embedding(base_path)
    model3.save_embedding('fb15k_vgg16.pickle')

    model4 = PHash()
    base_path = './img_data/fb15k/'
    model4.get_embedding(base_path,2)
    model4.save_embedding('fb15k_phash.pickle')

