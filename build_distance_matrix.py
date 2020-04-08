from utils.utils import img_load_aws, save_patch
from utils.image_preproc import patch_generator
from feature_extraction import InceptionV3Vectorizer
import numpy as np
import scipy
from tqdm import tqdm
import pandas as pd
import os
import pickle as pkl
import json

img_vectorizer = InceptionV3Vectorizer()

organ = 'colon'

if not os.path.exists('/data/hpa/{}/distance_matrices'.format(organ)):
	os.makedirs('/data/hpa/{}/distance_matrices'.format(organ))
if not os.path.exists('/data/hpa/{}/embeddings'.format(organ)):
	os.makedirs('/data/hpa/{}/embeddings'.format(organ))

df = pd.read_csv('./data/{}_enhanced.csv'.format(organ))

if not os.path.exists('./error_log.pkl'):
	error_log = []
else:
	error_log = pkl.load(open('./error_log.pkl'.format(organ), 'rb'))

for gene in tqdm(df['gene'].unique()):
	gene_df = df[df['gene']==gene]
	for antibody in gene_df['antibody'].unique():

		if os.path.exists('/data/hpa/{}/distance_matrices/{}.npy'.format(organ, gene+'-'+antibody)): continue

		antibody_df = gene_df[gene_df['antibody']==antibody]
		vector_list = []
		file_list = []
		for index, row in antibody_df.iterrows():
			filename = row['s3_aws_urls'].split('/')[-1].split('.')[0]

			if row['s3_aws_urls'] in error_log:
				continue

			if os.path.exists('/data/hpa/{}/embeddings/{}.npy'.format(organ, filename)):
				mean_vector = np.load('/data/hpa/{}/embeddings/{}.npy'.format(organ, filename))
			else:
				img = img_load_aws(row['s3_aws_urls'])

				if (img is None) or (len(img.shape)!=3):
					error_log.append(row['s3_aws_urls'])
					pkl.dump(error_log, open('./error_log.pkl', 'wb'))						
					continue

				patch_list = patch_generator(img, (299, 299))

				if not len(patch_list)>0:
					error_log.append(row['s3_aws_urls'])
					pkl.dump(error_log, open('error_log.pkl', 'wb'))
					continue
				
				features = img_vectorizer.generate_vectors(patch_list)
				mean_vector = np.mean(features, axis=0)
			
			vector_list.append(mean_vector)
			file_list.append(row['s3_aws_urls'])

			if not os.path.exists('/data/hpa/{}/embeddings/{}.npy'.format(organ, filename)):
				np.save('/data/hpa/{}/embeddings/{}.npy'.format(organ, filename), mean_vector)

		if len(vector_list) == 0:
			continue

		distance_matrix = scipy.spatial.distance.cdist(np.array(vector_list), np.array(vector_list), metric='cosine')
		
		distance_pairs = []

		for i in range(len(file_list)):
			for j in range(len(file_list)):
				distance_pairs.append([file_list[i], file_list[j], distance_matrix[i][j]])



		np.save('/data/hpa/{}/distance_matrices/{}.npy'.format(organ, gene+'-'+antibody), distance_pairs)

		# np.save('./data/distance_matrices/{}.npy'.format(gene+'-'+antibody), distance_matrix)


