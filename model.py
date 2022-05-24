import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import make_pipeline
#import StandardScaler

def LR(file):
    df = pd.read_csv(file)
    column = []
    df.drop(columns = column, inplace=True)
    os = SMOTE()
    df.dropna(how = 'any', inplace=True)
    df = df.reset_index(drop=True)
    #print(len(df))

    #df["Increase"] = [0 for _ in range(len(df))]
    print(df)

    # for i in range(0, len(df) - 1):
    #     if df["High"][i] < df["High"][i + 1]:
    #         df["Increase"][i] = 1
    #     else: df["Increase"][i] = 0
    print(df.dtypes)
    


    y = df["High"]
    x = df.drop(columns=["High"])

    #x,y = os.fit_resample(x,y)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

    model = LinearRegression(copy_X=True, fit_intercept=True, n_jobs=None)
    #model = make_pipeline(StandardScaler(with_mean=False), LinearRegression())

    print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)

    model.fit(x_train, y_train)

    y_pred = model.predict(x_train)
    #pred_test = model.predict(x_test)

    print(confusion_matrix(y_test, y_pred))
    #print(confusion_matrix(y_test, pred_test))

    print(classification_report(y_test, y_pred))
    #print(classification_report(y_test, pred_test))

    print(y_pred)

    return model.intercept_



print(LR('BTC-USD.csv'))