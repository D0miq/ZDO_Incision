from sklearn import svm
from joblib import dump, load
from sklearn.linear_model import SGDClassifier

def classify(svc, test_data):
    return svc.predict(test_data)

    
def create_svm():
    #return svm.SVC(kernel='linear')
    return svm.SVC()
    

def read_model():
    return load('svc_model.joblib')


def prepare_model(train_data, train_target):
    svc = svm.SVC(kernel='linear')
    #svc = SGDClassifier(loss='hinge')
    svc.fit(train_data, train_target)
    dump(svc, 'svc_model.joblib')
