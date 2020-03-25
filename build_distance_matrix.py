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

df = pd.read_csv('./data/colon_enhanced.csv')
error_log = []

for gene in tqdm(df['gene'].unique()):
	gene_df = df[df['gene']==gene]
	for antibody in gene_df['antibody'].unique():

		if os.path.exists('/data/hpa/colon/healthy_distance_matrices/{}.npy'.format(gene+'-'+antibody)): continue
		if os.path.exists('/data/hpa/colon/cancer_distance_matrices/{}.npy'.format(gene+'-'+antibody)): continue

		antibody_df = gene_df[gene_df['antibody']==antibody]
		if len(antibody_df['disease_type'].unique()) == 2:
			healthy = []
			cancer = []
			healthy_file = []
			cancer_file = []
			for index, row in antibody_df.iterrows():
				filename = row['s3_aws_urls'].split('/')[-1].split('.')[0]

				if os.path.exists('/data/hpa/colon/embeddings/{}.npy'.format(filename)):
					mean_vector = np.load('/data/hpa/colon/embeddings/{}.npy'.format(filename))
				else:
					img = img_load_aws(row['s3_aws_urls'])
					if img is None: continue
					if len(img.shape) != 3: continue
					patch_list = patch_generator(img, (299, 299))
					if not len(patch_list)>0:
						error_log.append(row['s3_aws_urls'])
						continue
					features = img_vectorizer.generate_vectors(patch_list)
					mean_vector = np.mean(features, axis=0)
				
				if row['disease_type'] != 'colorectal cancer':
					healthy.append(mean_vector)
					healthy_file.append(row['s3_aws_urls'])
				else:
					cancer.append(mean_vector)
					cancer_file.append(row['s3_aws_urls'])
					np.save('/data/hpa/colon/embeddings/{}.npy'.format(filename), mean_vector)

				if not os.path.exists('/data/hpa/colon/embeddings/{}.npy'.format(filename)):
					np.save('/data/hpa/colon/embeddings/{}.npy'.format(filename), mean_vector)

			if (len(healthy) == 0) or (len(cancer) == 0):
				continue

			#distance_matrix = scipy.spatial.distance.cdist(np.array(healthy), np.array(cancer), metric='cosine')

			healthy_matrix = scipy.spatial.distance.cdist(np.array(healthy), np.array(healthy), metric='cosine')
			cancer_matrix = scipy.spatial.distance.cdist(np.array(cancer), np.array(cancer), metric='cosine')
			
			#distance_pairs = []

			#for i in range(len(healthy_file)):
			#	for j in range(len(cancer_file)):
			#		distance_pairs.append([healthy_file[i], cancer_file[j], distance_matrix[i][j]])

			healthy_pairs = []
			cancer_pairs = []

			for i in range(len(healthy_file)):
				for j in range(len(healthy_file)):
					healthy_pairs.append([healthy_file[i], healthy_file[j], healthy_matrix[i][j]])

			for i in range(len(cancer_file)):
				for j in range(len(cancer_file)):
					cancer_pairs.append([cancer_file[i], cancer_file[j], cancer_matrix[i][j]])



			#np.save('/data/hpa/colon/distance_matrices/{}.npy'.format(gene+'-'+antibody), distance_pairs)
			np.save('/data/hpa/colon/healthy_distance_matrices/{}.npy'.format(gene+'-'+antibody), healthy_pairs)
			np.save('/data/hpa/colon/cancer_distance_matrices/{}.npy'.format(gene+'-'+antibody), cancer_pairs)

			# np.save('./data/distance_matrices/{}.npy'.format(gene+'-'+antibody), distance_matrix)
		else:
			print('No overlapping gene-antibody normal & cancer pairs')


