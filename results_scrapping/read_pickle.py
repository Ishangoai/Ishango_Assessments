import pickle

with open('cookies.pkl', 'rb') as f:
    data = pickle.load(f)
    print(data)

