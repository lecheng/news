import mlpy
import singlepass
from pca import *
from data import save_result


def kmeans_run():
    rawdata ,vector = singlepass.load_data()
    datMat = singlepass.mat(rawdata)
    cls,means,steps = mlpy.kmeans(datMat,k=366,plus=True)
    save_result(cls)

def singlepass_run():
    singlepass.init_group()
    dataset = singlepass.load_data()
    print(dataset)
    lowdataset = pca_plus(dataset)
    print(lowdataset)
    cls = singlepass.singlepass(lowdataset)
    save_result(cls)

if __name__=='__main__':
    singlepass_run()