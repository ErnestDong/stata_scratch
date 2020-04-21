import pandas as pd
def gethtml(lst):
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


def whoami():
    """
    get who am i
    :return: last username
    """
    rfile = open("whoami", "r", encoding="utf-8")
    name = rfile.readlines()[-1][:-1]
    rfile.close()
    return name


def get_corr(data):
    """
    get corr matrix in html table
    :param data: dataframe
    :return:
    """
    corr=data.corr()
    lst=corr.values.tolist()
    name=list(corr.columns)
    # print(name)
    length=len(name)
    for i in range(length):
        lst[i].insert(0,name[i])
    lst.insert(0,["corr"]+name)
    ans="<table border=\"1\">"
    for i in lst:
        ans+="<tr>"
        for j in i:
            if j not in name:
                ans+="<td bgcolor='#{}'>{}</td>".format(colorize(j),str(j)[:4])
            else:
                ans+="<td bgcolor='#{}'>{}</td>".format(colorize(j),str(j))
        ans+="</tr>"
    return ans+"</table>"

def colorize(corr):
    if isinstance(corr,str):
        return "FFFFFF"
    if corr < 0.1:
        return "afdfe4"
    if corr <0.2:
        return "94d6da"
    if corr < 0.3:
        return "90d7ec"
    if corr < 0.4:
        return "7bbfea"
    if corr < 0.5:
        return "33a3dc"
    if corr < 0.6:
        return "228bfd"
    if corr < 0.7:
        return "2570a1"
    if corr < 0.8:
        return "009ad6"
    if corr < 0.9:
        return "246802"
    return "2a5caa"
if __name__ == '__main__':
    data=pd.read_csv("./tk/daily_Ashare.csv")
    print(get_corr(data))