import os
import sys
import numpy as np
from matplotlib.pyplot import savefig, subplots, tight_layout


def main(argv):
    wd = os.getcwd()
    spa_dir = os.path.join( wd, "SPA" )
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
    #for i in uol2:
        #print(i[:4])

    num_tests = 3
    rows = 3
    cols = 5

    f, axs = subplots(rows, cols, figsize = (18,10), sharex = True)

    lines = [None for n in range(num_tests)]
    names = [None for n in range(num_tests)]
    for row in range(rows):
        start = row*(num_tests*cols)
        stop = (row+1)*(num_tests*cols)
        cur_row= uol2[start:stop]
        for col in range(cols):
            start = col*num_tests
            stop = (col+1)*num_tests
            cur_col = cur_row[start:stop]
            if (row == 0):
                axs[row][col].set_ylim(0.15, 1.0)
            if (row == 1):
                axs[row][col].set_ylim(0.2, 0.65)
            if (row == 2):
                axs[row][col].set_ylim(0.05, 0.8)
            if (col != 0):
                axs[row][col].set_yticklabels([])

            axs[row][col].grid(True)

            for c in cur_col:
                if (row == 0):
                    axs[row][col].set_title(c[1])

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
    f.tight_layout()
    savefig('foo.png', bbox_inches='tight')

if __name__ == "__main__":
    main(sys.argv[1:])