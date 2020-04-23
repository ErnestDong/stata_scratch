from sklearn.linear_model import LinearRegression
from matplotlib.figure import Figure
import random
import pandas as pd
import numpy as np
from sympy import stats
import scipy


def getAns(dependent="", independent=[], username=""):
    """get p-value, f-value, R-square etc."""
    reg = LinearRegression()
    tmp = open("./static/{}/loadfile.txt".format(username), "r", encoding="utf-8")
    filename = tmp.readlines()[-1][:-1]
    tmp.close()
    data = pd.read_csv(filename)
    ys = data[dependent].values
    xs = data[independent].values
    reg.fit(xs, ys)
    ans = {}
    ans["var"] = [dependent, "Constant"] + independent
    n = len(ys)
    k = len(independent) + 1
    ans["coefficient"] = np.append(reg.intercept_, reg.coef_).tolist()
    ans["R-squared"] = reg.score(xs, ys)
    ans["Adjusted R-squared"] = 1 - (1 - ans["R-squared"]) * (n - 1) / (n - k)
    ans["F-value"] = ans["R-squared"] / (1 - ans["R-squared"]) * (n - k) / (k - 1)
    ans["SS"] = {}
    prediction = reg.predict(xs)
    # print(sum(prediction**2)/sum(ys**2))
    tmp = sum((ys - ys.mean()) ** 2)
    ans["observation"] = n
    ans["df"] = k
    ans["SS"]["ESS"] = tmp * ans["R-squared"]
    ans["SS"]["RSS"] = tmp - ans["SS"]["ESS"]
    ans["Prob>F"] = scipy.stats.f.sf(ans["F-value"], k - 1, n - k)
    ans["Root MSE"] = (ans["SS"]["RSS"] / (n - k)) ** 0.5
    return ans


def format_(x):
    return str(x)[:10].rjust(10, ' ')


def showAns(dependent="", independent=[], username=""):
    """turn to html pages"""
    ans = getAns(dependent, independent, username)
    html = """
        <table border="1" style="width: 600px;">
      <tr align="middle">
        <td>
          Source
        </td>
        <td>SS</td>
        <td>df</td>
        <td>MS</td>
      </tr>
      <tr align="right">
        <td>Model</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
      </tr>
      <tr align="right">
        <td>Residual</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
      </tr>
      <tr align="right">
        <td>Total</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
      </tr>
    </table>
    """.format(format_(ans["SS"]["ESS"]), format_(ans["df"] - 1), format_(ans["SS"]["ESS"] / (ans["df"] - 1)),
               format_(ans["SS"]["RSS"]), format_(ans["observation"] - ans["df"]),
               format_(ans["SS"]["RSS"] / (ans["observation"] - ans["df"])),
               format_(ans["SS"]["ESS"] + ans["SS"]["RSS"]), format_(ans["observation"] - 1),
               format_((ans["SS"]["ESS"] + ans["SS"]["RSS"]) / (ans["observation"] - 1)))
    html += """
    <table style="width: 600px;">
      <tr>
        <td align="left">
          Number of obs
        </td>
        <td align="middle">=</td>
        <td align="right">{}</td>
      </tr>
      <tr>
        <td align="left">
          F({},{})
        </td>
        <td align="middle">=</td>
        <td align="right">{}</td>
      </tr>
      <tr>
        <td align="left">
          Prob>F
        </td>
        <td align="middle">=</td>
        <td align="right">{}</td>
      </tr>
      <tr>
        <td align="left">
          R-square
        </td>
        <td align="middle">=</td>
        <td align="right">{}</td>
      </tr>
      <tr>
        <td align="left">
          Adj R-square
        </td>
        <td align="middle">=</td>
        <td align="right">{}</td>
      </tr>
      <tr>
        <td align="left">
          Root MSE
        </td>
        <td align="middle">=</td>
        <td align="right">{}</td>
      </tr>
    </table>
    """.format(str(ans["observation"]), str(ans["df"] - 1), str(ans["observation"] - ans["df"]),
               str(ans["F-value"]),str(ans["Prob>F"]),str(ans["R-squared"]),str(ans["Adjusted R-squared"]),
               str(ans["Root MSE"]))

    return html


def create_figure(dependent="", independent=[], username=""):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig


if __name__ == "__main__":
    print(getAns("open", ["high", "low"], "dcy"))
    # data=pd.read_csv("./sourceCode/tk/daily_Ashare.csv")
    # reg('open',['high','low'],'dcy',data)
