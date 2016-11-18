import numpy as np
from sklearn.cross_validation import train_test_split
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.datasets import make_moons
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier

'''
未验证
'''

X, y = make_moons(
    n_samples=500,  # the number of observations
    random_state=1,
    noise=0.3
)
XTrain, XTest, yTrain, yTest = train_test_split(X, y, random_state=1, test_size=0.5)


def detect_plot_dimension(X, h=0.02, b=0.05):
    x_min, x_max = X[:, 0].min() - b, X[:, 0].max() + b
    y_min, y_max = X[:, 1].min() - b, X[:, 1].max() + b
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    dimension = xx, yy
    return dimension


def detect_decision_boundary(dimension, model):
    xx, yy = dimension  # unpack the dimensions
    boundary = model.predict(np.c_[xx.ravel(), yy.ravel()])
    boundary = boundary.reshape(xx.shape)  # Put the result into a color plot
    return boundary


def plot_decision_boundary(panel, dimension, boundary, colors=['#DADDED', '#FBD8D8']):
    xx, yy = dimension  # unpack the dimensions
    panel.contourf(xx, yy, boundary, cmap=ListedColormap(colors), alpha=1)
    panel.contour(xx, yy, boundary, colors="g", alpha=1, linewidths=0.5)  # the decision boundary in green


def plot_dataset(panel, X, y, colors=["#EE3D34", "#4458A7"], markers=["x", "o"]):
    panel.scatter(X[y == 1, 0], X[y == 1, 1], color=colors[0], marker=markers[0])
    panel.scatter(X[y == 0, 0], X[y == 0, 1], color=colors[1], marker=markers[1])


def calculate_prediction_error(model, X, y):
    yPred = model.predict(X)
    score = 1 - round(metrics.accuracy_score(y, yPred), 2)
    return score


def plot_prediction_error(panel, dimension, score, b=.3):
    xx, yy = dimension  # unpack the dimensions
    panel.text(xx.max() - b, yy.min() + b, ('%.2f' % score).lstrip('0'), size=15, horizontalalignment='right')


def explore_fitting_boundaries(model, n_neighbors, datasets, width):
    # determine the height of the plot given the aspect ration of each panel should be equal
    height = float(width) / len(n_neighbors) * len(datasets.keys())
    nrows = len(datasets.keys())
    ncols = len(n_neighbors)

    # set up the plot
    figure, axes = plt.subplots(nrows, ncols,
                                figsize=(width, height),
                                sharex=True,
                                sharey=True
                                )

    # X, y = make_moons(
    #     n_samples=500,  # the number of observations
    #     random_state=1,
    #     noise=0.3
    # )

    dimension = detect_plot_dimension(X, h=0.02)  # the dimension each subplot based on the data

    # Plotting the dataset and decision boundaries

    i = 0
    for n in n_neighbors:
        model.n_neighbors = n
        model.fit(datasets["Training Set"][0], datasets["Training Set"][1])
        boundary = detect_decision_boundary(dimension, model)
    j = 0
    for d in datasets.keys():
        try:
            panel = axes[j, i]
        except (TypeError, IndexError):
            if (nrows * ncols) == 1:
                panel = axes
            elif nrows == 1:  # if you only have one dataset
                panel = axes[i]
            elif ncols == 1:  # if you only try one number of neighbors
                panel = axes[j]
        plot_decision_boundary(panel, dimension, boundary)  # plot the decision boundary
        plot_dataset(panel, X=datasets[d][0], y=datasets[d][1])  # plot the observations
        score = calculate_prediction_error(model, X=datasets[d][0], y=datasets[d][1])
        plot_prediction_error(panel, dimension, score, b=0.2)  # plot the score

    # make compacted layout

    panel.set_frame_on(False)
    panel.set_xticks([])
    panel.set_yticks([])

    # format the axis labels

    if i == 0:
        panel.set_ylabel(d)
    if j == 0:
        panel.set_title('k={}'.format(n))
    j += 1
    i += 1

    plt.subplots_adjust(hspace=0, wspace=0)  # make compacted layout


if __name__ == "__main__":
    # specify the model and settings

    print(X[:10, ])
    print(y[:10])
    plt.scatter(X[y == 1, 0], X[y == 1, 1], color="#EE3D34", marker="x")
    plt.scatter(X[y == 0, 0], X[y == 0, 1], color="#4458A7", marker="o")
    plt.show()
    model = KNeighborsClassifier()
    n_neighbors = [200, 99, 50, 23, 11, 1]
    datasets = {
        "Training Set": [XTrain, yTrain],
        "Test Set": [XTest, yTest]
    }
    width = 20

    # explore_fitting_boundaries(model, n_neighbors, datasets, width)

    explore_fitting_boundaries(model=model, n_neighbors=n_neighbors, datasets=datasets, width=width)
