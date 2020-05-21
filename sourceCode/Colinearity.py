import numpy as np
import statsmodels.api as sm
import pandas as pd
import scipy

def auxiliary_regression(session: dict):
    filename = session["filename"]
    data = pd.read_csv(filename).dropna()
    independent = session["independent"]
    observation = len(data)
    X = list(independent)
    if len(X)<=2:
        return """<p>two variables won't be colinear</p>"""
    f_1 = scipy.stats.f.ppf(0.99, len(X) - 1, observation - len(X))
    f_5 = scipy.stats.f.ppf(0.95, len(X) - 1, observation - len(X))
    f_10 = scipy.stats.f.ppf(0.90, len(X) - 1, observation - len(X))
    html = """<table border='1'><tr><th>variable</th><th>R-square</th><th>VIF</th><th>F-value</th></tr>"""
    for i in range(len(X)):
        temp_y = X[i]
        X.pop(i)
        au_reg = sm.OLS(data[temp_y], sm.add_constant(data[X]))
        au_reg = au_reg.fit()
        R2 = au_reg.rsquared
        F = np.round(R2/(len(X))/(1-R2)*(1+observation-len(X)),4)
        if F>f_1:
            F = str(F)+"***"
        elif F>f_5:
            F = str(F)+"**"
        elif F>f_10:
            F = str(F)+"*"
        VIF = np.round(1 / (1 - R2), 4)
        R2 = np.round(R2, 4)
        html += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(independent[i],R2,VIF,F)
        X.insert(i, temp_y)
    return html+"</table>"


if __name__ == '__main__':
    print(auxiliary_regression({"independent": ['open', 'high'], "dependent": "low",
                                "filename": "/Users/dcy/code/asdfghjkl/sourceCode/tk/daily_Ashare.csv"}))
    # data = pd.read_csv("/Users/dcy/code/asdfghjkl/sourceCode/tk/daily_Ashare.csv")
    # print(len(data))
    # f_1 = scipy.stats.f.ppf(0.995, len(X) - 1, observation - len(X))
    f_1 = scipy.stats.f.ppf(0.99, 2,5)
    f_5 = scipy.stats.f.ppf(0.95, 2, 5)
    f_10 = scipy.stats.f.ppf(0.90, 2, 5)
    print(f_1)