import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64


def gethtml(lst: list):
    lenth = len(lst)
    html = "<table border='1'><tr>"
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


if __name__ == '__main__':
    # data = pd.read_csv("./tk/daily_Ashare.csv")
    # print(get_corr(data))
    pass
