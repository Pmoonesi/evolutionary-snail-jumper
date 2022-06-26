import matplotlib.pyplot as plt
import numpy as np

def read_file():
    with open('statistics.txt', 'r') as f:
        statistics = f.readlines()

    return statistics

def get_statistics(s_list):
    min_list, avg_list, max_list = [], [], []
    for s in s_list:
        if s.strip() == "":
            continue
        [min, avg, max] = [float(n) for n in s.split('-')]
        min_list.append(min)
        avg_list.append(avg)
        max_list.append(max)
    return np.array(min_list), np.array(avg_list), np.array(max_list)

def draw_box_chart(min_list, avg_list, max_list):
    assert len(min_list) == len(avg_list) == len(max_list)
    lyerr = avg_list - min_list
    uyerr = max_list - avg_list
    yerr = np.concatenate((lyerr, uyerr), axis=None).reshape(2, len(avg_list))
    plt.errorbar(np.arange(len(avg_list)), avg_list, yerr=yerr, fmt='Xg', ecolor='red', elinewidth=1.5, capsize=2, linestyle='dashed')
    plt.xlim(-1, len(avg_list))
    plt.show()

if __name__ == "__main__":
    s = read_file()
    mins, means, maxes = get_statistics(s)
    draw_box_chart(mins, means, maxes)
