from sklearn.linear_model import LinearRegression
from matplotlib.figure import Figure
import random
import pandas as pd
import numpy as np
from sympy import stats
import scipy
import matplotlib.pyplot as plt
import base64
from io import BytesIO

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
    sigma_square = ans["SS"]["RSS"] / (n - k)
    one = np.ones(n)
    xs = np.insert(xs, 0, values=one, axis=1)
    tmp = np.dot(xs.T, xs)
    var_cov_beta = sigma_square * np.linalg.inv(tmp)
    ans["stderr"] = np.sqrt(var_cov_beta.diagonal()).tolist()
    ans["t"] = [ans["coefficient"][i] / ans["stderr"][i] for i in range(k)]
    ans["P>|t|"] = [scipy.stats.t.sf(i, n - k) for i in ans["t"]]
    return ans


def format_(x):
    return str(x).rjust(10, ' ')


def showAns(dependent="", independent=[], username=""):
    """turn to html pages"""
    ans = getAns(dependent, independent, username)
    csvfile=open("./static/{}/downloads/ans.csv".format(username),"w",encoding="utf-8")
    print("dependent variable: ", dependent, file=csvfile)
    print("variables,Coefficients,Standard Errors,t values,Probabilities",file=csvfile)
    for i in range(ans["df"]):
        print(ans["var"][i+1],ans["coefficient"][i],ans["stderr"][i],ans["t"][i],ans["P>|t|"][i],sep=',',file=csvfile)
    csvfile.close()
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
    </table><table style="width:600px;" border="1">
    """.format(str(ans["observation"]), str(ans["df"] - 1), str(ans["observation"] - ans["df"]),
               str(ans["F-value"]), str(ans["Prob>F"]), str(ans["R-squared"]), str(ans["Adjusted R-squared"]),
               str(ans["Root MSE"]))
    for i in range(len(ans["var"])):
        if i == 0:
            html += """<tr><td>{}</td><td>Coef.</td><td>Std. Err.</td><td>t</td><td> P>|t| </td></tr>""".format(
                ans["var"][0])
        else:
            html += """<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>""".format(ans["var"][i],
                                                                                                  ans["coefficient"][
                                                                                                      i - 1],
                                                                                                  ans["stderr"][i - 1],
                                                                                                  ans["t"][i - 1],
                                                                                                  ans["P>|t|"][i - 1])
    return html + "</table>"


def create_t_figure(dependent="", independent=[], username=""):
    ans=getAns(dependent,independent,username)
    n=ans["observation"]
    args=ans["var"][1:]
    k=ans["df"]
    tvalue=ans["t"]
    t_1=scipy.stats.t.ppf(0.995,n-k)
    t_5=scipy.stats.t.ppf(0.975,n-k)
    t_10=scipy.stats.t.ppf(0.95,n-k)
    x = np.linspace(scipy.stats.t.ppf(0.01, n-k),scipy.stats.t.ppf(0.99, n-k), 100)
    plt.plot(x, scipy.stats.t.pdf(x, n-k),'r-', lw = 5, alpha = 0.6, label = 't pdf')
    for i in range(k):
        plt.plot([tvalue[i]]*10,list(i/100 for i in range(10)),label=args[i])
    tmp=[t_1,t_5,t_10]
    for i in range(3):
        plt.plot([tmp[i]]*10,list(i/100 for i in range(10)),label=["1%","5%","10%"][i])
    # X = np.linspace(-np.pi, np.pi, 256, endpoint=True)  # -π to+π的256个值
    # C, S = np.cos(X), np.sin(X)
    plt.rcParams['figure.figsize'] = (8.0, 4.0)  # 设置figure_size尺寸800x400
    # plt.plot(X, C)
    # plt.plot(X, S)
    plt.title="t value"
    plt.legend()
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    # 将matplotlib图片转换为HTML
    imb = base64.b64encode(plot_data)  # 对plot_data进行编码
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    return imd


if __name__ == "__main__":
    # a=np.array([[1,2],[3,4]])
    # b=np.linalg.inv(a)
    # print(np.dot(a,b))
    print(showAns("open", ["amount", "low"], "dcy"))
    # getAns("open", ["amount", "low"], "dcy")
    # data=pd.read_csv("./sourceCode/tk/daily_Ashare.csv")
    # reg('open',['high','low'],'dcy',data)
    # print(type(np.ones(10)))
    print(format_(str(1.1304568502168702e-07)))
    # create_t_figure("open", ["amount", "low"], "dcy")
