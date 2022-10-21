import pandas as pd
import numpy as np
import os

class LR:

    def __init__(self, x, y, a, e, l) -> None:
        self.m = len(x)
        self.n = len(x[0]) + 1
        self.X = x
        for i in range(self.m):
            self.X[i].append(1)
        self.X = np.array(self.X)
        self.y = np.array(y)
        self.W = np.array([0]*self.n)
        self.a = a
        self.e = e
        self.l = l
    
    def DCost(self):
        ret = []
        for d in range(self.n):
            res = 0
            for i in range(self.m):
                tmp = 0
                for j in range(self.n):
                    tmp += self.W[j]*self.X[i][j]
                res += (tmp - self.y[i])*self.X[i][d]
            res += self.l*self.W[d]
            ret.append(res/self.m)
        return np.array(ret)

    def GradDescent(self):
        dJ = self.DCost()
        self.W = np.subtract(self.W, self.a*dJ)
        flag = np.any((abs(dJ) > self.e))
        
        while flag:
            dJ = self.DCost()
            self.W = np.subtract(self.W, self.a*dJ)
            flag = np.any((abs(dJ) > self.e))
        
        return self.W
    

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'univariate_linear_regression.csv')
df = pd.read_csv(filename)

df_train = df[:int(0.70*len(df))]
df_test = df[int(0.70*len(df)):]

X_train = df_train.iloc[:, [0]].values.tolist()
y_train = list(df_train['y'])
X_test = df_test.iloc[:, [0]].values.tolist()
y_test = list(df_test['y'])

mean_error = float('inf')
mn_l = 0

for l in range(50):
    model = LR(X_train, y_train, 0.01, 0.0001, l)
    w = model.GradDescent()

    y_pred = []
    for i in X_test:
        res = 0
        for j in range(len(i)):
            res += i[j]*w[j]
        res += w[-1]
        y_pred.append(res)

    mae = 0
    for i in range(len(y_pred)):
        mae += abs(y_test[i] - y_pred[i])
    mae /= len(y_test)
    
    if mean_error > mae:
        mean_error = mae
        mn_l = l

print("Least Error Occurs at Lambda =", mn_l)
print("Mean Absolute Error =", mean_error)