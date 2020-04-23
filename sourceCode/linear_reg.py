from sklearn.linear_model import LinearRegression
from matplotlib.figure import Figure
import random
import pandas as pd
import numpy as np


def getAns(dependent="", independent=[], username=""):
    reg = LinearRegression()
    tmp = open("./static/{}/loadfile.txt".format(username), "r", encoding="utf-8")
    filename = tmp.readlines()[-1][:-1]
    tmp.close()
    data = pd.read_csv(filename)
    ys = data[dependent].values
    xs = data[independent].values
    reg.fit(xs, ys)
    ans = {}
    n = len(ys)
    k = len(independent) + 1
    ans["coefficient"] = np.array([reg.intercept_] + list(reg.coef_))
    ans["R-squared"] = reg.score(xs, ys)
    ans["Adjusted R-squared"] = 1 - (1 - ans["R-squared"]) * (n - 1) / (n - k)
    ans["F-value"] = ans["R-squared"] / (1 - ans["R-squared"]) * (n - k) / (k - 1)
    return ans


def showAns(dependent="", independent=[], username=""):
    ans = getAns(dependent, independent, username)
    length = len(independent) + 1
    equation = ""
    independent.insert(0, "")
    for i in range(length):
        if ans["coefficient"][i] > 0:
            equation += " + " + str(abs(ans["coefficient"][i])) + independent[i]
        elif ans["coefficient"][i] == 0:
            continue
        else:
            equation += " - " + str(abs(ans["coefficient"][i])) + independent[i]
    if equation[1] == '+':
        equation = dependent + " =" + equation[2:]
    else:
        equation = dependent + " =" + equation
    return "<h2>Equation is</h2><p>" + equation + "</p>" + "<p>F-value: " + str(ans["F-value"]) + "</p>" + "<p>R-squared: " + \
           str(ans["R-squared"]) + "</p>" + "<p>Adjuested R-square: " + str(ans["Adjusted R-squared"]) + "</p>"


def create_figure(dependent="", independent=[], username=""):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig


if __name__ == "__main__":
    print(showAns("open", ["high", "low"], "dcy"))
