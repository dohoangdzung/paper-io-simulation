import matplotlib.pyplot as plt
import numpy as np
import log_parse


def plot_pysim_log(mem_log, time_stamps, text, xmin, xmax, ymin, ymax):
    time = mem_log["time"]
    total = mem_log["total"]
    dirty = mem_log["dirty"]
    cache = mem_log["cache"]
    used = mem_log["used"]
    # free = mem_log["free"]
    # available = list(np.array(free) + np.array(cache) - np.array(dirty))
    # dirty_ratio = list(np.array(available) * 0.4)
    # dirty_bg_ratio = list(np.array(available) * 0.1)

    read_starts = time_stamps["read_start"]
    read_ends = time_stamps["read_end"]
    write_starts = time_stamps["write_start"]
    write_ends = time_stamps["write_end"]

    plot_log(time, read_starts, read_ends, write_starts, write_ends, total, cache, dirty, used,
             "python simulator result", xmax, xmin, ymax, ymin)


def plot_sim_result(time_log_file, mem_log_file, title, xmin, xmax, ymin, ymax):
    sim_time_log = log_parse.read_timelog(time_log_file)
    sim_mem_log = log_parse.read_sim_log(mem_log_file)

    read_starts = []
    read_ends = []
    write_starts = []
    write_ends = []
    for i in range(len(sim_time_log)):
        if sim_time_log[i][0] == "read":
            read_starts.append(sim_time_log[i][1])
            read_ends.append(sim_time_log[i][2])
        if sim_time_log[i][0] == "write":
            write_starts.append(sim_time_log[i][1])
            write_ends.append(sim_time_log[i][2])

    time = sim_mem_log["time"]
    total = sim_mem_log["total"]
    cache = sim_mem_log["cache"]
    dirty = sim_mem_log["dirty"]
    used = sim_mem_log["used"]

    plot_log(time, read_starts, read_ends, write_starts, write_ends, total, cache, dirty, used,
             title, xmax, xmin, ymax, ymin)


def plot_log(time, read_starts, read_ends, write_starts, write_ends, total, cache, dirty, used,
             title, xmax, xmin, ymax, ymin):
    free = list(np.array(total) - np.array(used))
    available = list(np.array(free) + np.array(cache) - np.array(dirty))
    dirty_ratio = list(np.array(available) * 0.4)
    dirty_bg_ratio = list(np.array(available) * 0.1)

    plt.figure()
    plt.title(title)

    # start = read_starts[0]
    # for idx in range(len(read_starts)):
    #     if idx == 0:
    #         plt.axvspan(xmin=read_ends[idx] - start, xmax=write_starts[idx] - start, color="k",
    #                     alpha=0.2, label="computation")
    #         plt.axvspan(xmin=0, xmax=read_ends[idx] - start, color="g", alpha=0.2, label="read")
    #         plt.axvspan(xmin=write_starts[idx] - start, xmax=write_ends[idx] - start, color="b", alpha=0.2,
    #                     label="write")
    #     else:
    #         plt.axvspan(xmin=read_ends[idx] - start, xmax=write_starts[idx] - start, color="k", alpha=0.2)
    #         plt.axvspan(xmin=read_starts[idx] - start, xmax=read_ends[idx] - start, color="g", alpha=0.2)
    #         plt.axvspan(xmin=write_starts[idx] - start, xmax=write_ends[idx] - start, color="b", alpha=0.2)

    plt.plot(time, total, color='k', linewidth=1, linestyle="-.", label="total mem")
    plt.plot(time, used, color='g', linewidth=1, label="used mem")
    plt.plot(time, cache, color='m', linewidth=1, label="cache")
    plt.plot(time, dirty, color='r', linewidth=1, label="dirty")
    plt.plot(time, available, color='b', linewidth=1, linestyle="-.", label="available mem")
    plt.plot(time, dirty_ratio, color='k', linewidth=1, linestyle="-.", label="dirty_ratio")
    plt.plot(time, dirty_bg_ratio, color='r', linewidth=1, linestyle="-.", label="dirty_bg_ratio")
    plt.legend(loc="upper right")

    plt.ylim(top=ymax, bottom=ymin)
    plt.xlim(right=xmax, left=xmin)
    # plt.text(1, 200000, text, fontsize=9)

    plt.show()


def compare_sep(real_time_file, real_mem_file,
                pysim_time_file, pysim_mem_file,
                simgrid_time_file, simgrid_mem_file,
                size, title, xmin, xmax, ymin, ymax):
    figure = plt.figure()
    plt.tight_layout()

    ax1 = figure.add_subplot(3, 1, 1)
    ax2 = figure.add_subplot(3, 1, 2, sharex=ax1)
    ax3 = figure.add_subplot(3, 1, 3, sharex=ax1)

    # REAL RESULTS
    real_subplot(ax1, real_time_file, real_mem_file, xmin, xmax, ymin, ymax, bar_alpha=0.2, linestyle="-", linewidth=1)

    # PYSIM RESULTS
    sim_subplot(ax2, pysim_time_file, pysim_mem_file, "python simulator", bar_alpha=0.2)
    sim_subplot(ax3, simgrid_time_file, simgrid_mem_file, "SimGrid simulator", bar_alpha=0.2)

    plt.ylim(top=ymax, bottom=ymin)
    plt.xlim(right=xmax, left=xmin)
    # plt.text(1, 200000, text, fontsize=9)
    plt.subplots_adjust(left=0.1, bottom=0.05, right=0.95, top=0.95, wspace=0, hspace=0.25)
    plt.show()


def compare_overlap(real_time_file, real_mem_file,
                    sim_time_file, sim_mem_file, title, xmin, xmax, ymin, ymax):
    figure = plt.figure()
    plt.tight_layout()

    ax1 = figure.add_subplot(2, 1, 1)
    ax2 = figure.add_subplot(2, 1, 2, sharex=ax1)

    real_subplot(ax1, real_time_file, real_mem_file, xmin, xmax, ymin, ymax, alpha=0.2)
    sim_subplot(ax1, sim_time_file, sim_mem_file, "", alpha=0.3)

    plt.ylim(top=ymax, bottom=ymin)
    plt.xlim(right=xmax, left=xmin)
    plt.show()


def real_subplot(subplot_ax, real_time_file, real_mem_file, xmin, xmax, ymin, ymax,
                 bar_alpha=0.2, line_alpha=1, linestyle=".-", linewidth=1.5):
    timestamps = log_parse.read_timelog(real_time_file, skip_header=False)
    atop_log = log_parse.read_atop_log(real_mem_file, dirty_ratio=0.4, dirty_bg_ratio=0.1)
    dirty_data = np.array(atop_log["total"])
    intervals = len(dirty_data)
    time = np.arange(0, intervals)

    start = timestamps[0][1]

    for i in range(len(timestamps)):
        if timestamps[i][0] == "read":
            subplot_ax.axvspan(xmin=timestamps[i][1] - start, xmax=timestamps[i][2] - start, color="g", alpha=bar_alpha,
                               label="read" if i == 0 else "")
        else:
            subplot_ax.axvspan(xmin=timestamps[i - 1][2] - start, xmax=timestamps[i][1] - start, color="k", alpha=bar_alpha,
                               label="computation" if i == 1 else "")
            subplot_ax.axvspan(xmin=timestamps[i][1] - start, xmax=timestamps[i][2] - start, color="b", alpha=bar_alpha,
                               label="write" if i == 1 else "")

    # app_cache = list(np.array(app_mem) + np.array(cache_used))
    # subplot_ax.plot(time, atop_log["total"], color='k', linewidth=1.5, linestyle=linestyle, label="total mem", alpha=line_alpha)
    subplot_ax.plot(time, atop_log["used_mem"], color='g', linewidth=linewidth, linestyle=linestyle,
                    label="used mem", alpha=line_alpha)
    subplot_ax.plot(time, atop_log["cache"], color='m', linewidth=linewidth, linestyle=linestyle,
                    label="cache used", alpha=line_alpha)
    subplot_ax.plot(time, atop_log["dirty_data"], color='r', linewidth=linewidth, linestyle=linestyle,
                    label="dirty data", alpha=line_alpha)
    subplot_ax.plot(time, atop_log["avai_mem"], color='b', linewidth=linewidth, linestyle=linestyle,
                    label="available mem", alpha=line_alpha)
    subplot_ax.plot(time, atop_log["dirty_ratio"], color='k', linewidth=linewidth, linestyle=linestyle,
                    label="dirty_ratio", alpha=line_alpha)
    # subplot_ax.plot(time, atop_log["dirty_bg_ratio"], color='r', linewidth=1, linestyle="-.", label="dirty_bg_ratio",
    #                 alpha=alpha)
    subplot_ax.set_title("Real pipeline", fontsize=10)
    subplot_ax.legend(fontsize='small', loc='upper right')


def sim_subplot(subplot_ax, sim_time_file, sim_mem_file, title, bar_alpha=0.4, line_alpha=1):
    sim_time_log = log_parse.read_timelog(sim_time_file)
    sim_mem_log = log_parse.read_sim_log(sim_mem_file)

    read_starts = []
    read_ends = []
    write_starts = []
    write_ends = []
    for i in range(len(sim_time_log)):
        if sim_time_log[i][0] == "read":
            read_starts.append(sim_time_log[i][1])
            read_ends.append(sim_time_log[i][2])
        if sim_time_log[i][0] == "write":
            write_starts.append(sim_time_log[i][1])
            write_ends.append(sim_time_log[i][2])

    time = sim_mem_log["time"]
    total = sim_mem_log["total"]
    cache = sim_mem_log["cache"]
    dirty = sim_mem_log["dirty"]
    used = sim_mem_log["used"]

    free = list(np.array(total) - np.array(used))
    available = list(np.array(free) + np.array(cache) - np.array(dirty))
    dirty_ratio = list(np.array(available) * 0.4)
    dirty_bg_ratio = list(np.array(available) * 0.1)

    start = read_starts[0]
    for idx in range(len(read_starts)):
        if idx == 0:
            subplot_ax.axvspan(xmin=read_ends[idx] - start, xmax=write_starts[idx] - start, color="k",
                               alpha=bar_alpha, label="computation")
            subplot_ax.axvspan(xmin=0, xmax=read_ends[idx] - start, color="g", alpha=bar_alpha, label="read")
            subplot_ax.axvspan(xmin=write_starts[idx] - start, xmax=write_ends[idx] - start, color="b", alpha=bar_alpha,
                               label="write")
        else:
            subplot_ax.axvspan(xmin=read_ends[idx] - start, xmax=write_starts[idx] - start, color="k", alpha=bar_alpha)
            subplot_ax.axvspan(xmin=read_starts[idx] - start, xmax=read_ends[idx] - start, color="g", alpha=bar_alpha)
            subplot_ax.axvspan(xmin=write_starts[idx] - start, xmax=write_ends[idx] - start, color="b", alpha=bar_alpha)

    subplot_ax.plot(time, total, color='k', linewidth=1, label="total mem", alpha=line_alpha)
    subplot_ax.plot(time, used, color='g', linewidth=1, label="used mem", alpha=line_alpha)
    subplot_ax.plot(time, cache, color='m', linewidth=1, label="cache", alpha=line_alpha)
    subplot_ax.plot(time, dirty, color='r', linewidth=1, label="dirty", alpha=line_alpha)
    subplot_ax.plot(time, available, color='b', linewidth=1, label="available mem", alpha=line_alpha)
    subplot_ax.plot(time, dirty_ratio, color='k', linewidth=1, label="dirty_ratio", alpha=line_alpha)
    # subplot_ax.plot(time, dirty_bg_ratio, color='r', linewidth=1, label="dirty_bg_ratio", alpha=alpha)

    subplot_ax.set_title(title, fontsize=10)


input_size = 75
# plot_sim_result("pysim/%dgb_sim_time.csv" % input_size, "pysim/%dgb_sim_mem.csv" % input_size,
#                 "python simulator: %dGB" % input_size, 0, 500, -1000, 280000)

compare_sep("real/%dgb/timestamps_pipeline.csv" % input_size, "real/%dgb/atop_mem.log" % input_size,
            "pysim/%dgb_sim_time.csv" % input_size, "pysim/%dgb_sim_mem.csv" % input_size,
            "simgrid_ext/%dgb_sim_time.csv" % input_size, "simgrid_ext/%dgb_sim_mem.csv" % input_size,
            input_size, "Simulation results with %dGB input file" % input_size, 0, 800, -1000, 280000)

# compare_overlap("real/%dgb/timestamps_pipeline.csv" % input_size, "real/%dgb/atop_mem.log" % input_size,
#                 "pysim/%dgb_sim_time.csv" % input_size, "pysim/%dgb_sim_mem.csv" % input_size,
#                 "Simulation results with %dGB input file" % input_size, 0, 1500, -1000, 280000)


# plot_sim_result("simgrid_ext/9_sim_mem.csv", "simgrid_ext/9_sim_mem.csv",
#                 "WRENCH Ext: 9 pipelines", 0, 150, -1000, 280000)
