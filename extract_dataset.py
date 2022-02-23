import os
from PIL import Image
import json
import numpy as np
import argparse
from tqdm import tqdm

def load_funsd(data_path, split='train'):
    
    if(split=='train'):
        data_path = data_path + 'training_data'
    elif(split=='test'):
        data_path = data_path + 'testing_data'
    else:
        raise Exception('invalid split')
    
    if(os.path.exists(data_path)==False):
        raise Exception('dataset not found')
    
    
    instances = []
    
    annotation_files = os.listdir(data_path+'/annotations/')
    for annotation_file in annotation_files:
        image_file = data_path+'/images/'+annotation_file.replace('.json','.png')
        with Image.open(image_file) as image:
            image = np.array(image)
        try:
            annotation = json.load(open(data_path+'/annotations/'+annotation_file, encoding='utf-8'))
            form = annotation['form']
            for idx in range(len(form)):
                element = form[idx]
                bbox = element['box']
                subimage = image[bbox[1]:bbox[3], bbox[0]:bbox[2]]
                text = element['text']
                instance = {
                    'image': subimage,
                    'text': text,
                    'filename': split+'_'+annotation_file.replace('.json','')+'_'+str(idx)
                }
                instances.append(instance)

        except Exception as e:
            print('Error reading file:', annotation_file, e)
    return(instances)

def save_extracted(data, output_data_path):

    if(os.path.exists(output_data_path)==False):
        os.mkdir(output_data_path)
        os.mkdir(output_data_path+'images/')
        os.mkdir(output_data_path+'annotations/')
    else:
        raise Exception('Output directory:', output_data_path, 'already exists')

    for instance in tqdm(data):
        annotation_file = output_data_path+'annotations/'+ instance['filename'] + '.txt'
        image_file = output_data_path+'images/'+ instance['filename'] + '.png'
        image = Image.fromarray(instance['image'])
        image.save(image_file)
        text = instance['text']
        f = open(annotation_file, 'w', encoding='utf-8')
        f.write(text)
        f.close()


#input_data_path  = "../../FUNSD/"
#output_data_path = "../../OCRDataset/"
#python extract_dataset.py ../../FUNSD/ ./OCRDataset/

if(__name__=='__main__'):
    parser = argparse.ArgumentParser(description='Process FUNSD dataset to extract the images and annotations')
    parser.add_argument('input_data_path', type=str, help='Path of FUNSD')
    parser.add_argument('output_data_path', type=str, help='Path of the output')
    args = parser.parse_args()

    input_data_path = args.input_data_path
    output_data_path = args.output_data_path

    train_output_data_path = os.path.join(output_data_path, 'training_data/')
    test_output_data_path  = os.path.join(output_data_path, 'testing_data/')



    train_data = load_funsd(data_path=input_data_path, split='train')
    test_data  = load_funsd(data_path=input_data_path, split='test')

    if(os.path.exists(output_data_path)==False):
        os.mkdir(output_data_path)
    else:
        raise Exception('Output directory:', output_data_path, 'already exists')
    
    save_extracted(train_data, train_output_data_path)
    save_extracted(test_data, test_output_data_path)