import numpy as np
from dnn.deep_convnet import DeepConvNet

network = DeepConvNet()

network.load_params("dnn/deep_convnet_params.pkl")

def predict(x):
    pre = network.predict(x.reshape(1,1,28,28))
    pre_label = int(np.argmax(pre))
    return pre_label

