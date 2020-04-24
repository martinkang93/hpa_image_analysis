import sklearn.manifold
import numpy as np
import pandas as pd

def url2filename(url):
    filename = url.split('/')[9]
    return filename

def url2tissue_type(url):
    tissue_type = url.split('/')[6]
    return tissue_type

def url2organ(url):
    organ = url.split('/')[7]
    return organ

def url2antibody(url):
    antibody = url.split('/')[5]
    return antibody

def url2gene(url):
    gene = url.split('/')[4]
    return gene

def url2patient(url):
    patient = url.split('/')[8]
    return patient

def load_embedding(filename, embedding_dir='/data/hpa/colon/embeddings'):
    if filename.split('.')[0]+'.npy' in os.listdir(embedding_dir):
        return np.load(os.path.join(embedding_dir, filename))
    else:
        return np.nan
    

    