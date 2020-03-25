import matplotlib.pyplot as plt 
import pandas as pd
from sklearn.metrics import roc_curve, roc_auc_score, classification_report, precision_recall_curve


def plot_roc_curve(y_true, y_pred, title):
    plt.figure()
    lw=2
    fpr, tpr, thresh = roc_curve(y_true, y_pred)
    auc = roc_auc_score(y_true, y_pred)
    plt.plot(fpr, tpr, color='green', lw=lw, label='AUROC: {:0.3f}'.format(auc))

    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(title)
    plt.legend(loc="lower right")
    plt.show()