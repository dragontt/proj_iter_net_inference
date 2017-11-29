#!/usr/bin/python
import sys
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


## global variables
## color theme
color_theme = {"black":(0,0,0), 
                "blue":(31, 119, 180), "blue_L":(174, 199, 232), 
                "orange":(255, 127, 14), "orange_L":(255, 187, 120),
                "green":(44, 160, 44), "green_L":(152, 223, 138), 
                "red":(214, 39, 40), "red_L":(255, 152, 150),
                "magenta":(148, 103, 189), "magenta_L":(197, 176, 213),
                "brown":(140, 86, 75), "brown_L":(196, 156, 148),
                "pink":(227, 119, 194), "pink_L":(247, 182, 210), 
                "grey":(127, 127, 127), "grey_L":(199, 199, 199),
                "yellow":(255, 215, 0), "yellow_L":(219, 219, 141), 
                "cyan":(23, 190, 207), "cyan_L":(158, 218, 229)}
for c in color_theme.keys():
    (r, g, b) = color_theme[c]
    color_theme[c] = (r/255., g/255., b/255.)


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Plot network evaluations by benchmarking againt ChIP binding and PWM binding potential")
    parser.add_argument('-f', '--evaluation_files', nargs='+')
    parser.add_argument('-l', '--evaluation_labels', nargs='+')
    parser.add_argument('-c', '--evaluation_colors', nargs='+', help='%s' % color_theme.keys())
    parser.add_argument('-s', '--step', default=1600, type=float)
    parser.add_argument('-t', '--num_tfs', default=320, type=int)
    parser.add_argument('-o', '--output_file_prefix')
    parsed = parser.parse_args(argv[1:])
    return parsed


def plot_analysis(fns, colors, labels, figure_name, num_tfs, step, eval_method, chance_eval_chip=None, chance_eval_pwm=None, chance_eval_intersected=None, dash_last_line=False):

    # compute ChIP and PWM supports
    eval_chip = [None] * (len(fns)+1)
    eval_pwm = [None] * (len(fns)+1)
    eval_intersected = [None] * (len(fns)+1)
    [eval_chip[0], eval_pwm[0], eval_intersected[0]] = parse_chance_binding_overlap(fns[0])
    for i in range(len(fns)):
        [eval_chip[i+1], eval_pwm[i+1], eval_intersected[i+1]] = parse_binding_overlap(fns[i], eval_method)
    # print 'chip chance:', eval_chip[0][0], 'pwm chance:', eval_pwm[0][0]

    ## configure output figure
    x_ticks = [format(float(i)*step/num_tfs, '.0f') for i in range(1,len(eval_chip[0])+1)]  
    font_size = 14
    matplotlib.rcParams.update({'font.size': 16})  
    
    ##### ChIP support #####
    fig, ax = plt.subplots(figsize=(5,4.5), dpi=150)
    ## plot evaluation of randomly simulated edges
    if chance_eval_chip is not None:
        ax.fill_between(np.arange(20), chance_eval_chip[0], chance_eval_chip[1], 
                        facecolor="black", alpha=.25, label=labels[1])
    ## plot theoratical chance
    ax.plot(eval_chip[0], color=colors[0], linestyle=":", label=labels[0], linewidth=3)
    ## plot evaluation of predicted targets
    for i in range(1,len(eval_chip)):
        line_style = "--" if i == len(eval_chip)-1 and dash_last_line else "-"
        k = i if chance_eval_chip is None else i+1
        ax.plot(eval_chip[i], color=colors[i], linestyle=line_style, label=labels[k], linewidth=3)
    
    ## figure makeup
    plt.xticks(range(len(eval_chip[0])), x_ticks)
    plt.xlabel('Avg num of predicted targets per TF')
    plt.ylabel('Interactions supported by ChIP (%)')
    ax.yaxis.grid(True, linestyle='-', alpha=.2, linewidth=.5)
    plt.xlim(-1, len(eval_chip[0]))
    plt.ylim(0, 60)
    plt.yticks(np.arange(0,60.5,10))
    for label in ax.xaxis.get_ticklabels()[::2]:
        label.set_visible(False)
    handles, labels = ax.get_legend_handles_labels()
    # handles.insert(0, handles.pop())
    # labels.insert(0, labels.pop())
    plt.legend(handles[::-1], labels[::-1], fontsize=font_size)
    plt.tight_layout()
    plt.savefig(figure_name + '.ChIP_support.pdf', fmt='pdf')

    ##### PWM support #####
    fig, ax = plt.subplots(figsize=(5,4.5), dpi=150)
    ## plot evaluation of randomly simulated edges
    if chance_eval_pwm is not None:
        ax.fill_between(np.arange(20), chance_eval_pwm[0], chance_eval_pwm[1], 
                        facecolor="black", alpha=.25, label=labels[1])
    ## plot theoratical chance
    ax.plot(eval_pwm[0], color=colors[0], linestyle=":", label=labels[0], linewidth=3)
    ## plot evaluation of predicted edges
    for i in range(1,len(eval_pwm)):
        line_style = "--" if i == len(eval_pwm)-1 and dash_last_line else "-"
        k = i if chance_eval_pwm is None else i+1
        ax.plot(eval_pwm[i], color=colors[i], linestyle=line_style, label=labels[k], linewidth=3)
    # ax.scatter(18, 10, s=75, c=color_theme["yellow"])
    # ax.annotate('ChIP network', xy=(17.95, 9.75), xycoords='data', xytext=(-80, -55), textcoords='offset points', arrowprops=dict(arrowstyle="->"))

    ## figure makeup
    plt.xticks(range(len(eval_pwm[0])), x_ticks)
    plt.xlabel('Avg num of predicted targets per TF')
    plt.ylabel('Interactions supported by PWM (%)')
    ax.yaxis.grid(True, linestyle='-', alpha=.2, linewidth=.5)
    plt.xlim(-1, len(eval_pwm[0]))
    plt.ylim(0, 25)
    plt.yticks(np.arange(0,25.5,5))
    for label in ax.xaxis.get_ticklabels()[::2]:
        label.set_visible(False)
    handles, labels = ax.get_legend_handles_labels()
    # handles.insert(0, handles.pop())
    # labels.insert(0, labels.pop())
    plt.legend(handles[::-1], labels[::-1], fontsize=font_size)
    plt.tight_layout()
    plt.savefig(figure_name + '.PWM_support.pdf', fmt='pdf')


def plot_bar_analysis(fns, colors, labels, figure_name, num_tfs, step, eval_method, chance_eval_chip, chance_eval_pwm, chance_eval_intersected):

    matplotlib.rcParams.update({'font.size': 16}) 

    # compute chip and pwm supports
    eval_chip = [None] * (len(fns)+1)
    eval_pwm = [None] * (len(fns)+1)
    eval_intersected = [None] * (len(fns)+1)
    [eval_chip[0], eval_pwm[0], eval_intersected[0]] = parse_chance_binding_overlap(fns[0])
    for i in range(len(fns)):
        [eval_chip[i+1], eval_pwm[i+1], eval_intersected[i+1]] = parse_binding_overlap(fns[i], eval_method)

    # make bar plots
    indx = range(3)
    width = .35
    colors[0] = color_theme["grey"]
    fig, ax = plt.subplots(figsize=(5,4.5), dpi=150)

    # plot bars with error bar for random
    ax.bar([ind*3+width for ind in indx], (eval_chip[0][1], eval_pwm[0][1], eval_intersected[0][1]), width, color=colors[0], label=labels[0], yerr=[1.03, 1.38, 0.31], ecolor='k')
    # plot bars for others
    for i in range(1, len(eval_chip)):
        ax.bar([ind*3+width*(i+1) for ind in indx], (eval_chip[i][1], eval_pwm[i][1], eval_intersected[i][1]), width, color=colors[i], label=labels[i])
    
    ax.set_ylabel("Interaction support rate (%)")
    ax.set_xticks([ind*3+width*(i) for ind in indx])
    ax.set_xticklabels(("ChIP", "PWM", "ChIP+PWM"))
    ax.set_ylim([0, 50])
    handles, labels = ax.get_legend_handles_labels()
    # handles.insert(0, handles.pop())
    # labels.insert(0, labels.pop())
    # ax.legend(handles[::-1], labels[::-1], prop={'size':12})
    plt.tight_layout()
    plt.savefig(figure_name + '.bar_top_3200.pdf', fmt='pdf')


def parse_binding_overlap(fn, method):
    chip_indx = 5
    pwm_indx = 4
    intersected_indx = 6

    lines = open(fn, "r").readlines()
    chip = [0] * (len(lines))
    pwm = [0] * (len(lines))
    intersected = [0] * (len(lines))

    if method == "cumulative":
        for i in range(len(lines)):
            line = lines[i].split()
            chip[i] = float(line[chip_indx])/float(line[2])
            pwm[i] = float(line[pwm_indx])/float(line[2])
            intersected[i] = float(line[intersected_indx])/float(line[2])
    
    elif method == "binned":
        for i in range(len(lines)):
            line = lines[i].split()
            if i == 0:
                chip[i] = float(line[chip_indx])/float(line[2])
                pwm[i] = float(line[pwm_indx])/float(line[2])
                intersected[i] = float(line[intersected_indx])/float(line[2])
            else:
                chip[i] = (float(line[chip_indx]) - float(prevline[chip_indx]))/(float(line[2]) - float(prevline[2]))
                pwm[i] = (float(line[pwm_indx]) - float(prevline[pwm_indx]))/(float(line[2]) - float(prevline[2]))
                intersected[i] = (float(line[intersected_indx]) - float(prevline[intersected_indx]))/(float(line[2]) - float(prevline[2]))
            prevline = line  
    return [np.array(chip)*100, np.array(pwm)*100, np.array(intersected)*100]


def parse_chance_binding_overlap(fn):
    evalPoints = np.loadtxt(fn).shape[0]

    line = open(fn, 'r').readline()
    line = line.split()
    chip = [float(line[1])/float(line[7]) for _ in range(evalPoints)]
    pwm = [float(line[0])/float(line[7]) for _ in range(evalPoints)]
    intersected = [float(line[3])/float(line[7]) for _ in range(evalPoints)]
    return [np.array(chip)*100, np.array(pwm)*100, np.array(intersected)*100]


def main(argv):
    parsed = parse_args(argv)

    ## parse arguments
    evaluation_files = parsed.evaluation_files
    evaluation_labels = ['Random: expectation'] + parsed.evaluation_labels
    if parsed.evaluation_colors is None:
        evaluation_colors = ['black'] + np.random.choice(np.array(color_theme.keys()), 
                                        size=len(evaluation_files), replace=False).tolist()
    else:
        evaluation_colors = ['black'] + parsed.evaluation_colors
    evaluation_colors = [color_theme[c] for c in evaluation_colors]

    ## plot evaluations
    plot_analysis(evaluation_files, evaluation_colors, 
                    evaluation_labels, parsed.output_file_prefix, 
                    parsed.num_tfs, parsed.step, "cumulative")


if __name__ == "__main__":
    main(sys.argv)
