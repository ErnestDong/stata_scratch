from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt
import base64
from io import BytesIO


def getAns(dependent="", independent=[], session={}):
    """get p-value, f-value, R-square etc."""
    reg = LinearRegression()
    filename = session["filename"]
    data = pd.read_csv(filename)
    y = data[dependent].values
    xs = data[independent].values
    ys = np.log(y)
    reg.fit(xs, ys)
    ans = {}
    ans["var"] = [dependent, "Constant"] + independent
    n = len(ys)
    k = len(independent) + 1
    ans["coefficient"] = np.append(reg.intercept_, reg.coef_).tolist()
    ans["R-squared"] = reg.score(xs, ys)
    ans["Adjusted R-squared"] = 1 - (1 - ans["R-squared"]) * (n - 1) / (n - k)
    try:
        ans["F-value"] = ans["R-squared"] / (1 - ans["R-squared"]) * (n - k) / (k - 1)
    except ZeroDivisionError:
        ans["F-value"] = 9999999999999999
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
    try:
        ans["t"] = [ans["coefficient"][i] / ans["stderr"][i] for i in range(k)]
    except ZeroDivisionError:
        ans["t"] = 9999999
    ans["P>|t|"] = [scipy.stats.t.sf(i, n - k) for i in ans["t"]]
    return ans


def format_(x):
    return str(x).rjust(10, ' ')


def showAns(dependent="", ans={}, session={}):
    """turn to html pages"""
    username = session["username"]
    csvfile = open("./static/{}/downloads/ans.csv".format(username), "w", encoding="utf-8")
    print("dependent variable: ", dependent, file=csvfile)
    print("variables,Coefficients,Standard Errors,t values,Probabilities", file=csvfile)
    for i in range(ans["df"]):
        print(ans["var"][i + 1], ans["coefficient"][i], ans["stderr"][i], ans["t"][i], ans["P>|t|"][i], sep=',',
              file=csvfile)
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


def create_b_figure(ans={}):
    args = ans["var"][1:]
    bvalue = ans["coefficient"]
    plt.bar(args, bvalue)
    for a, b in zip(args, bvalue):
        plt.text(a, b + 0.003, '%.3f' % b, ha='center', va='bottom', fontsize=11)
    plt.xlabel('variables')
    plt.ylabel('b-value')
    plt.ylim(min(0, min(bvalue) * 1.2), max(0, max(bvalue) * 1.2))
    plt.rcParams['figure.figsize'] = (8.0, 4.0)
    plt.title = "b value"
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    plt.clf()
    return imd


def create_p_figure(ans={}):
    args = ans["var"][1:]
    pvalue = ans["P>|t|"]
    plt.bar(args, pvalue)
    for a, b in zip(args, pvalue):
        plt.text(a, b + 0.003, '%.3f' % b, ha='center', va='bottom', fontsize=11)
    plt.xlabel('variables')
    plt.ylabel('p-value')
    plt.ylim(min(0, min(pvalue) * 1.2), max(0, max(pvalue) * 1.2))
    plt.axhline(y=0.01, ls="-", c="violet", label="1%")
    plt.axhline(y=0.05, ls="-", c="mediumpurple", label="5%")
    plt.axhline(y=0.1, ls="-", c="cornflowerblue", label="10%")
    plt.rcParams['figure.figsize'] = (8.0, 4.0)
    plt.title = "p value"
    plt.legend()
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    plt.clf()
    return imd


def create_t_figure(ans={}):
    n = ans["observation"]
    args = ans["var"][1:]
    k = ans["df"]
    tvalue = ans["t"]
    t_1 = scipy.stats.t.ppf(0.995, n - k)
    t_5 = scipy.stats.t.ppf(0.975, n - k)
    t_10 = scipy.stats.t.ppf(0.95, n - k)
    plt.bar(args, tvalue)
    for a, b in zip(args, tvalue):
        plt.text(a, b + 0.003, '%.3f' % b, ha='center', va='bottom', fontsize=11)
    plt.xlabel('variables')
    plt.ylabel('t-value')
    plt.ylim(min(0, min(tvalue) * 1.2), max(0, max(tvalue) * 1.2))
    plt.axhline(y=t_1, ls="-", c="violet", label="1%")
    plt.axhline(y=t_5, ls="-", c="mediumpurple", label="5%")
    plt.axhline(y=t_10, ls="-", c="cornflowerblue", label="10%")
    plt.rcParams['figure.figsize'] = (8.0, 4.0)
    plt.title = "t value"
    plt.legend()
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    plt.clf()
    return imd


if __name__ == "__main__":
    # a=np.array([[1,2],[3,4]])
    # b=np.linalg.inv(a)
    # print(np.dot(a,b))
    print(getAns("年龄", ["是否使用互联网", "log年收入"], "dcy"))
    # getAns("open", ["amount", "low"], "dcy")
    # data=pd.read_csv("./sourceCode/tk/daily_Ashare.csv")
    # reg('open',['high','low'],'dcy',data)
    # print(type(np.ones(10)))
    # print(format_(str(1.1304568502168702e-07)))
    # create_t_figure("open", ["amount", "low"], "dcy")
