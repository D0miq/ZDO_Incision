from joblib import dump, load
from sklearn import svm


def classify(svc, test_data):
    return svc.predict(test_data)


def create_svm():
    return svm.SVC()


def read_model():
    return load('svc_model.joblib')


def prepare_model(train_data, train_target):
    svc = svm.SVC(kernel='linear')
    svc.fit(train_data, train_target)
    dump(svc, 'svc_model.joblib')
