from sklearn import svm
from joblib import dump, load


def classify(svc, test_data):
    pred = svc.predict(test_data)


def read_model():
    return load('svc_model.joblib')


def prepare_model(train_data, train_target):
    svc = svm.SVC()
    svc.fit(train_data, train_target)
    dump(svc, 'svc_model.joblib')
