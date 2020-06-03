from scipy import stats
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm


def hausmantest(session: dict):
    filename = session["filename"]
    data = pd.read_csv(filename).dropna()
    independent = session["independent"]
    dependent = session["dependent"]
    X = list(independent)
    all = list(independent)
    params = []
    ts_b = []
    sd_b = []
    p_values = []
    raw = data[all]
    for i in range(len(X)):
        tmp = X.pop(i)
        tmp_y = data[tmp]
        X1 = data[X]
        X1 = sm.add_constant(X1)
        haus_reg1 = sm.RLM(tmp_y, X1)
        haus_reg1 = haus_reg1.fit()
        u = pd.DataFrame(haus_reg1.resid, columns=['resid'])
        newdf = pd.concat([u, raw], axis=1)
        haus_reg2 = sm.RLM(data[dependent], newdf)
        haus_reg2 = haus_reg2.fit()
        sd_b.append(np.round(haus_reg2.bse.values[1], 3))
        ts_b.append(np.round(haus_reg2.tvalues.values[1], 3))
        p_values.append(np.round(haus_reg2.pvalues.values[1], 4))
        params.append(np.round(haus_reg2.params.values[1], 4))
        X = list(independent)
    html = """<center><h2>Hausman Test</h2><table border='1'><tr><th>variable</th><th>Coefficients</th><th>std err</th><th>t-value</th><th>p-value</th></tr>"""
    for i in range(len(independent)):
        html += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
            X[i], params[i], sd_b[i], ts_b[i], p_values[i])
    return html + "</table></center>"


if __name__ == '__main__':
    print(
        hausmantest({
            "filename":
            "/Users/dcy/code/asdfghjkl/sourceCode/tk/daily_Ashare.csv",
            "dependent": "open",
            "independent": ["high", "low"],
            "ans": {
                "coefficient": [1, 2, 3]
            }
        }))
