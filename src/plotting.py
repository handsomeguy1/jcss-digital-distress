import matplotlib.pyplot as plt

def save_simple_hist(series, path, title):
    fig = plt.figure()
    series.dropna().hist()
    plt.title(title)
    plt.tight_layout()
    fig.savefig(path, dpi=300)
    plt.close(fig)
