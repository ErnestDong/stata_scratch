import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats
import pandas as pd
import numpy as np
def whitetest(session:dict):
    dependent=session["dependent"]
    independent = session["independent"]
    data=pd.read_csv(session["filename"]).dropna()
    y = data[dependent]
    x = data[independent]
    coef=session["ans"]["coefficient"]
    tmp=np.array(coef[1:]).T*x
    # print(tmp.values)
    yhat=[]
    for i in tmp.values:
        yhat.append(sum(i)+coef[0])
    u = np.array(yhat)-y
    u2 = u ** 2
    X = sm.add_constant(data[independent])
    white = sm.OLS(u2, X)
    white = white.fit()
    R_square = np.round(white.rsquared, 4)
    chi = R_square*len(x)
    pvalue = stats.chi2.sf(chi,len(coef))
    chi1 = stats.chi2.cdf(0.99, len(coef))
    chi2 = stats.chi2.cdf(0.95, len(coef))
    chi3 = stats.chi2.cdf(0.99, len(coef))
    if pvalue>chi1:
        return "<h2>White Test</h2><p>chi({})={}***</p><p>99% heteroscedasticity</p>".format(len(coef),chi)
    if pvalue>chi2:
        return "<h2>White Test</h2><p>chi2({})={}**</p><p>95% heteroscedasticity</p>".format(len(coef),chi)
    if pvalue>chi3:
        return "<h2>White Test</h2><p>chi2({})={}*</p><p>90% heteroscedasticity</p>".format(len(coef),chi)
    return "<h2>White Test</h2><p>chi({})={}</p>".format(len(coef),chi)
if __name__ == '__main__':
    print(whitetest({"filename":"/Users/dcy/code/asdfghjkl/sourceCode/tk/daily_Ashare.csv","dependent":"open","independent":["high","low"],"ans":{"coefficient":[1,2,3]}}))