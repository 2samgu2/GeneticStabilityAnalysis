import os
import sys
import numpy as np
from matplotlib.pyplot import savefig, subplots, tight_layout


def main(argv):
    wd = os.getcwd()
    spa_dir = os.path.join( wd, "SPA2" )
    uol1 = []
    for file in os.listdir( spa_dir ):
        if file.endswith(".npy"):
            info = file.replace(".npy", "")
            arr = info.split("_")
            file_path = os.path.join(spa_dir, file)
            data = np.load(file_path)
            arr.append(data)
            uol1.append(arr)

    uol2 = sorted(uol1, key = lambda x: x[3])

    num_cs = 5 # num classifiers
    rows = 1
    cols = 3

    f, axs = subplots(rows, cols, figsize = (15,5), sharex = True)

    lines = [None for n in range(num_cs)]
    names = [None for n in range(num_cs)]
    for col in range(cols):
        start = col*num_cs
        stop = (col+1)*num_cs
        cur_col= uol2[start:stop]
        if (col == 0):
            axs[col].set_ylim(0.5, 1.0)
        if (col == 1):
            axs[col].set_ylim(0.35, 0.6)
        if (col == 2):
            axs[col].set_ylim(0.3, 0.8)

        axs[col].grid(True)

        for c in cur_col:
            axs[col].set_title(c[3])
            acc = [i for i in c[4]]
            axs[col].plot(np.arange(0,101,5), acc, label = c[1] )
        handles, labels = axs[col].get_legend_handles_labels()

    f.legend(handles, labels, bbox_to_anchor=(0.02, 1.02, 0.95, .102), loc=3,ncol=5, mode="expand", borderaxespad=0.)

    f.tight_layout()
    savefig('foo.png', bbox_inches='tight')
"""
                if (c[2] == "greedy"):
                    acc = [i[1] for i in c[4]]
                    if (row == 0):
                        acc2 = 0.97
                    elif (row == 1):
                        acc2 = 0.6
                    elif (row == 2):
                        acc2 = 0.75
                    acc = [acc2] + acc
                    acc = np.array(acc)
                    axs[row,col].plot(np.arange(0,101,1), acc, label = c[2])
                else:
                    if (row == 0):
                        acc2 = 0.97
                    elif (row == 1):
                        acc2 = 0.6
                    elif (row == 2):
                        acc2 = 0.75
                    acc = c[4].tolist()
                    if (c[2] != "percent"):
                        acc = [acc2] + acc
                    acc = np.array(acc)
                    axs[row,col].plot(np.arange(0,101,5), acc, label = c[2])
                if (col == 0):
                    axs[row][col].set_ylabel(c[3])
                handles, labels = axs[row][col].get_legend_handles_labels()
                lines = handles
                names = labels
                    
    f.legend(lines, names, bbox_to_anchor=(0.3, 1.02, 0.4, .102), loc=3,ncol=3, mode="expand", borderaxespad=0.)
"""


if __name__ == "__main__":
    main(sys.argv[1:])