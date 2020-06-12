import os

def getAns(dependent: str, independent: list, session: dict) -> dict:
    # 为防止系统因素故注释掉
    # os.system("touch ~/Desktop/demo.csv")
    ans={}
    return ans


def showAns(dependent: str, ans: dict, session: dict) -> str:
    return "<center><p>Hello World!</h></center>"

def showFigure(ans: dict) -> dict:
    return {"demo.png":"/static/pic/demo.jpeg"}


if __name__ == "__main__":
    print(getAns("open", ["amount", "low"], "dcy"))
