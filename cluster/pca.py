from numpy import *
import mlpy

def pca(datamat,ratio=0.5):
	allfeats = shape(datamat)[1]
	print('allfeats:%d' %allfeats)
	topNfeat = int(allfeats * ratio)
	meanvals = mean(datamat,axis=0)
	meanremoved = datamat - meanvals
	covmat = cov(meanremoved,rowvar=0)
	eigvals,eigvects = linalg.eig(mat(covmat))
	eigvalind = argsort(eigvals)
	eigvalind = eigvalind[:-(topNfeat+1):-1]
	redeigvects = eigvects[:,eigvalind]
	lowddatamat = meanremoved * redeigvects
	print('lowfeats:%d' %shape(lowddatamat)[1])
	return lowddatamat

def pca_plus(datamat):
	allfeats = shape(datamat)[1]
	print('allfeats:%d' %allfeats)
	pca = mlpy.PCA()
	pca.learn(datamat)
	lowddatamat = pca.transform(datamat)
	print('lowfeats:%d' %shape(lowddatamat)[1])
	return lowddatamat