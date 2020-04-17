from matplotlib.figure import Figure
import random


def showAns(dependent="", independent=[]):
    wfile = open("./static/downloads/ans.csv", "a", encoding="utf-8")
    print("hello,world,", file=wfile)
    wfile.close()
    return "<h1>Hello World</h1>"


def create_figure(dependent="", independent=[]):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig


if __name__ == "__main__":
    pass
