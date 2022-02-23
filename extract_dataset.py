import os
from PIL import Image
import json
import numpy as np
import argparse
from tqdm import tqdm

def load_funsd(data_path, split='train'):
    
    if(split=='train'):
        data_path = os.path.join(data_path, 'training_data')
    elif(split=='test'):
        data_path = os.path.join(data_path, 'testing_data')
    else:
        raise Exception('invalid split')
    

    if(os.path.exists(data_path)==False):
        raise Exception('dataset not found')
    
    instances = []
    
    annotations_path = os.path.join(data_path, 'annotations')
    images_path = os.path.join(data_path, 'images')

    for annotation_file in os.listdir(annotations_path):
        
        image_file = os.path.join(images_path, annotation_file.replace('.json','.png'))

        with Image.open(image_file) as image:
            image = np.array(image)
        try:
            annotation = json.load(open(os.path.join(annotations_path, annotation_file), encoding='utf-8'))
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

def save_extracted(instances, data_path):
    
    annotations_path = os.path.join(data_path, 'annotations')
    images_path = os.path.join(data_path, 'images')

    if(os.path.exists(data_path)==False):
        os.mkdir(data_path)
        os.mkdir(images_path)
        os.mkdir(annotations_path)
    else:
        raise Exception('Output directory:', data_path, 'already exists')

    for instance in tqdm(instances):
        
        annotation_file = os.path.join(annotations_path, instance['filename'] + '.txt')
        image_file = os.path.join(images_path, instance['filename'] + '.png')

        image = Image.fromarray(instance['image'])
        text = instance['text']
        
        image.save(image_file)
        f = open(annotation_file, 'w', encoding='utf-8')
        f.write(text)
        f.close()


#input_data_path  = "../../FUNSD/"
#output_data_path = "../../OCRDataset/"
#python extract_dataset.py ../../FUNSD/ ./OCRDataset/

if(__name__=='__main__'):
    parser = argparse.ArgumentParser(description='Process FUNSD dataset to extract the images and annotations')
    parser.add_argument('input_path', type=str, help='Path of FUNSD')
    parser.add_argument('output_data_path', type=str, help='Path of the output')
    args = parser.parse_args()

    input_path = args.input_path
    output_path = args.output_data_path

    if(os.path.exists(output_path)==False):
        os.mkdir(output_path)
    else:
        raise Exception('Output directory:', output_path, 'already exists')



    output_path_train = os.path.join(output_path, 'training_data/')
    output_path_test  = os.path.join(output_path, 'testing_data/')


    instances_train = load_funsd(input_path, split='train')
    instances_test  = load_funsd(input_path, split='test')


    
    save_extracted(instances_train, output_path_train)
    save_extracted(instances_test, output_path_test)