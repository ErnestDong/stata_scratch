"""
fuctions to be used
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
import scipy


def gethtml(lst: list):
    lenth = len(lst)
    html = "<table border='1' style=\"margin: auto;\"><tr>"
    for line in range(lenth):
        if line == 0:
            tmp = lst[line].split(',')
            for i in tmp:
                html += "<th>{}</th>".format(i)
            html += "</tr>"
        else:
            html += "<tr>"
            tmp = lst[line].split(',')
            for i in tmp:
                html += "<td>{}</td>".format(i)
            html += "</tr>"
    return html + "</table>"


def get_corr(data: pd):
    """
    get corr matrix in html table
    :param data: dataframe
    :return:
    """
    corr = data.corr()
    lst = corr.values.tolist()
    name = list(corr.columns)
    # print(name)
    length = len(name)
    for i in range(length):
        lst[i].insert(0, name[i])
    lst.insert(0, ["corr"] + name)
    # ans="<table border=\"1\">"
    a = data.corr()
    plt.subplots(figsize=(9, 9))
    sns.heatmap(a, annot=True, vmax=1, square=True, cmap="Blues")
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    plt.clf()
    # for i in lst:
    #     ans+="<tr>"
    #     for j in i:
    #         if j not in name:
    #             ans+="<td bgcolor='#{}'>{}</td>".format(colorize(j),str(j)[:4])
    #         else:
    #             ans+="<td bgcolor='#{}'>{}</td>".format(colorize(j),str(j))
    #     ans+="</tr>"
    return "<img src=\"{}\"><br>".format(imd)  # ans+"</table>"


def create_b_figure(ans: dict) -> str:
    args = ans["var"][1:]
    bvalue = ans["coefficient"]
    plt.bar(args, bvalue)
    for a, b in zip(args, bvalue):
        plt.text(a,
                 b + 0.003,
                 '%.3f' % b,
                 ha='center',
                 va='bottom',
                 fontsize=11)
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


def create_p_figure(ans: dict) -> str:
    args = ans["var"][1:]
    pvalue = ans["P>|t|"]
    plt.bar(args, pvalue)
    for a, b in zip(args, pvalue):
        plt.text(a,
                 b + 0.003,
                 '%.3f' % b,
                 ha='center',
                 va='bottom',
                 fontsize=11)
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


def create_t_figure(ans: dict) -> str:
    n = ans["observation"]
    args = ans["var"][1:]
    k = ans["df"]
    tvalue = ans["t"]
    t_1 = scipy.stats.t.ppf(0.995, n - k)
    t_5 = scipy.stats.t.ppf(0.975, n - k)
    t_10 = scipy.stats.t.ppf(0.95, n - k)
    plt.bar(args, tvalue)
    for a, b in zip(args, tvalue):
        plt.text(a,
                 b + 0.003,
                 '%.3f' % b,
                 ha='center',
                 va='bottom',
                 fontsize=11)
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


if __name__ == '__main__':
    # data = pd.read_csv("./tk/daily_Ashare.csv")
    # print(get_corr(data))
    pass
