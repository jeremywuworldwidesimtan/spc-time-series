from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
import tkinter as Tk
import customtkinter as Ctk
from spcmonitor import sigma_lines
import statistics, math, datetime, sys, hashlib, snapshot, configparser

WRITE_DATA = True

class ExtMon(Ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SPC Extended Monitor")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.titleLabel = Ctk.CTkLabel(self, text="Extended Graph Viewer", font=("Segoe UI bold", 24), anchor='w')
        self.titleLabel.pack(expand=False, fill='both', padx=12, pady=12)

        canvas_main = FigureCanvasTkAgg(fig, master=self)
        canvas_main.get_tk_widget().pack(fill='both', expand=True, padx=12, pady=12)

# Open the file and run initial md5
def init_load(csv):
    with open(csv, "rb") as f:
        hash = hashlib.md5(f.read()).hexdigest()
        print(hash)

        load(csv)

# Load the file data into the program
def load(csv):
    global xs, ys
    try:
        with pd.read_csv(csv, chunksize=1, header=None) as reader:
            # copilot alternative 1
            # [xs.append(chunk[0].to_numpy().item()) and ys.append(chunk[1].to_numpy().item()) for chunk in reader if chunk[0].to_numpy().item() not in xs]
            # copilot alt 2
            # new_list = [(chunk[0].to_numpy().item(), chunk[1].to_numpy().item()) for chunk in reader if chunk[0].to_numpy().item() not in xs]
            # xs, ys = zip(*new_list) # unzip the list of tuples into two lists
            # print(f"[{new_list}]")
            # print(xs, ys)
            for chunk in reader:
                if chunk[0].to_numpy().item() not in xs: # fix a graphical error
                    xs = np.append(xs, chunk[0].to_numpy().item())
                    ys = np.append(ys, chunk[1].to_numpy().item())
                    # print("Loaded XS/YS", xs, ys)
                    if len(xs) >= 500:
                        xs = np.delete(xs, 0)
                        ys = np.delete(ys, 0)
                # print(chunk[0].to_numpy().item())
    except:
        pass

def periodic_timepoint(tp, per):
    '''
    Displays the data points in a notation relative to the period for periodical data
    For example days can be represented in the format of week no. (dayofweek no.) using this fucntion
    '''
    p_tp = f"{tp//per} ({(tp % per)})"
    return p_tp

def data_range(data_list, points_p_period, period_count):
    # Return list with the most recent n * period number of data
    if period_count <= 1:
        # print("Data list", data_list)
        return data_list[-(points_p_period):]
    else:
        # print("Data list", data_list)
        return data_list[-(points_p_period*period_count):]

def ani_init():
    pass

def animate(i):
    global period, axs, xs, ys, ps
    # print(xs, ys)

    for ax in np.ndarray.flatten(axs):
        ax.clear()

    # print("Displayed XS/YS", xs, ys)

    xs_window1 = data_range(xs, 30, 1)
    ys_window1 = data_range(ys, 30, 1)
    if ps[0] > 0:
        axs[0].plot(
            list(map((lambda x: periodic_timepoint(x, period)), data_range(xs, period, ps[0]))), 
            data_range(ys, period, ps[0]))
    
    if ps[1] > 0:
        axs[1].plot(
            list(map((lambda x: periodic_timepoint(x, period)), data_range(xs, period, ps[1]))), 
            data_range(ys, period, ps[1]))
    
    if ps[2] > 0:
    # print(period_data(xs, period, 3))
        axs[2].plot(
            list(map((lambda x: periodic_timepoint(x, period)), data_range(xs, period, ps[2]))), 
            data_range(ys, period, ps[2]))
    
    if ps[3] > 0:
    # print(period_data(xs, period, 4))
        axs[3].plot(
            list(map((lambda x: periodic_timepoint(x, period)), data_range(xs, period, ps[3]))), 
            data_range(ys, period, ps[3]))
    
    # print(i)
    if len(xs) % 50 == 0 and len(xs) > 40:
        print("Starting snapshot count...")
        snapshot_check(xs_window1[10], 10, ys_window1[10:20])
    
    if len(ys) > 2:
        for j, ax in enumerate(axs):
            sigma_lines(ax, np.nanmean(data_range(ys, period, ((2*j) + 1))), statistics.stdev(data_range(ys, period, ((2*j) + 1))), xs)
        
def checkforchange():
    # Use md5 hashing to check for change in the data file so that we can update the program if there is a change 
    global hash, timeint
    with open(fil, "rb") as f:
        if hash != hashlib.md5(f.read()).hexdigest():
            load(fil) # If there is change in the file "reload" the file with new changes
            hash = hashlib.md5(f.read()).hexdigest()

    em.after(timeint, checkforchange)

def snapshot_check(index, snap_count, snapshot_data):
    global fil
    if snapshot.validate_snapshot(snapshot_data, fil, index, snap_count):
        snapmsg = f"Snapshot successfully validated at point {index} to {index+snap_count}"
        if snapmsg not in spcalerts:
                spcalerts.add(snapmsg)
                print(snapmsg)
                if WRITE_DATA:
                    with open(logfile, 'a+') as lf:
                        lf.write(snapmsg + '\n')

def parsePS(p1, p2, p3, p4):
    # This is to ease import into the graph using global variables
    return [p1, p2, p3 ,p4]

if __name__ == '__main__':
    conf = configparser.ConfigParser()
    conf.read('config.ini')

    spcalerts = set()
    # print(sys.argv)
    window_size = int(conf['spcmain']['winsize'])
    period = int(conf['extendeddatamonitor']['period_points'])

    # The period sizes to view
    ps = parsePS(
        int(conf['extendeddatamonitor']['p1']),
        int(conf['extendeddatamonitor']['p2']),
        int(conf['extendeddatamonitor']['p3']),
        int(conf['extendeddatamonitor']['p4'])
    )

    plt.style.use('ggplot')
    xs = np.array([], copy=False, dtype=np.uint32)
    ys = np.array([], copy=False)
    # print("Init XS/YS:", xs, ys)

    fig, axs = plt.subplots(4,1)
    fig.tight_layout(pad=1.5)
    # At least I did something today 3/4/24
    for ax in np.ndarray.flatten(axs):
        ax.tick_params(axis='x', rotation=90)

    # Tkinter
    em = ExtMon()

    # Save files
    date_time = datetime.datetime.now().strftime('%Y.%m.%d-%H.%M.%S.%f')
    # datefile = pd.read_csv(data)

    # Use default values if none is specified
    if len(sys.argv) < 2:
        fil = "test.csv"
    else:
        fil = sys.argv[1]

    if len(sys.argv) < 3 : # third argv is the speed
        timeint = int(0.5 * 1000)
    else:
        try:    
            timeint = int(float(sys.argv[2]))
        except ValueError:    
            timeint = int(0.5 * 1000)
            print("That's not a float!")

    if len(sys.argv) < 4: # Fourth argv is the logfile (this is useful for SPC alerts system that we going to build later)
        logfile = "LOG-" + date_time + ".txt"
    else:
        logfile = sys.argv[3]

    # print(sys.argv[0], timeint)

    em.after(1, lambda: init_load(fil))
    em.after(3, checkforchange)

    # couldnot find a way to get old approach working so i think this is a compromise worth taking
    ani = animation.FuncAnimation(fig, animate, interval=timeint, init_func=ani_init, blit=False)

    em.mainloop()
    # plt.draw()
    # plt.show()