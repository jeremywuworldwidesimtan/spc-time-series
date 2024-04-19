from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
import tkinter as Tk
import customtkinter as Ctk
from tkinter import ttk
import statistics, math, datetime, sys, hashlib, snapshot, configparser, json

class RawDataGraph(Ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        canvas_main = FigureCanvasTkAgg(fig1, master=self)
        canvas_main.get_tk_widget().pack(expand=True, fill='both', padx=12, pady=12)

class ThreeMAGraph(Ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        canvas_a3 = FigureCanvasTkAgg(fig2, master=self)
        canvas_a3.get_tk_widget().pack(expand=True, fill='both', padx=12, pady=12)
        
class FiveMAGraph(Ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        canvas_a5 = FigureCanvasTkAgg(fig3, master=self)
        canvas_a5.get_tk_widget().grid(column=0,row=0, sticky='nsew')

class SevenMAGraph(Ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        canvas_a7 = FigureCanvasTkAgg(fig4, master=self)
        canvas_a7.get_tk_widget().grid(column=0,row=0, sticky='nsew')

class Tabs(Ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add tabs
        self.add("Raw Data")
        self.add("3-point MA")
        self.add("5-point MA")
        self.add("7-point MA")

        # add widgets on tabs
        self.rdg = RawDataGraph(master=self.tab("Raw Data"))
        self.rdg.grid(row=0, column=0)

        self.tdg = ThreeMAGraph(master=self.tab("3-point MA"))
        self.tdg.grid(row=0, column=0)

        self.fdg = FiveMAGraph(master=self.tab("5-point MA"))
        self.fdg.grid(row=0, column=0)

        self.sdg = SevenMAGraph(master=self.tab("7-point MA"))
        self.sdg.grid(row=0, column=0)

        self.after(200, lambda: self.set("3-point MA"))
        self.after(400, lambda: self.set("5-point MA"))
        self.after(600, lambda: self.set("7-point MA"))
        self.after(800, lambda: self.set("Raw Data"))


class SpcMon(Ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SPC Monitor")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.titleLabel = Ctk.CTkLabel(self, text="SPC Monitor Program", font=(fond, 24), anchor='w')
        self.titleLabel.grid(row=0, column=0, padx=12, pady=12)

        self.tabview = Tabs(self)
        self.tabview.grid(row=1, column=0, padx=12, pady=12, sticky='nsew')

# Open the file and run initial md5
def init_load(csv):
    with open(csv, "rb") as f:
        hash = hashlib.md5(f.read()).hexdigest()
        print("A file has been loaded succesfully")

        load(csv)

# Load the file data into the program
def load(csv):
    global xs, ys
    try:
        with pd.read_csv(csv, chunksize=1, header=None) as reader:
            for chunk in reader:
                if chunk[0].to_numpy().item() not in xs: # fix a graphical error
                    xs = np.append(xs, chunk[0].to_numpy().item())
                    ys = np.append(ys, chunk[1].to_numpy().item())
                    # print(len(xs))
                    # print("Loaded XS/YS", xs, ys)
                    if len(xs) >= 100:
                        xs = np.delete(xs, 0)
                        ys = np.delete(ys, 0)
                # print(chunk[0].to_numpy().item())
    except:
        pass

def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def ani_init():
    pass

def sigma_lines(axe, avg, sigma, x = [0]):
    axe.axhline(y=avg + sigma, c="0.6", linestyle='dashed')
    axe.axhline(y=avg - sigma, c="0.6", linestyle='dashed')
    axe.axhline(y=avg + sigma + sigma, c="0.3", linestyle='dashed')
    axe.axhline(y=avg - sigma - sigma, c="0.3", linestyle='dashed')
    axe.axhline(y=avg - sigma - sigma - sigma, c="0", linestyle='dashed')
    axe.axhline(y=avg + sigma + sigma + sigma, c="0", linestyle='dashed')
    axe.axhline(y=avg, c="red", linestyle='dashed')
    axe.text(x[0], math.ceil(avg), "Median: %.4f; StDev: %.4f" % (avg, sigma))

def set_labels(axe, ttile):
    global xa_label, ya_label
    axe.set_xlabel(xa_label)
    axe.set_ylabel(ya_label)
    axe.set_title(ttile)

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

def rule1(valueList, indexList, limits, plot, var_name):
    ucl = limits[0]
    lcl = limits[1]
    for i,y in enumerate(valueList):
        if y > ucl or y < lcl:
            plot.scatter(indexList[i], valueList[i], c="b", zorder=420)
            rule1msg = f"({var_name}) {conf['spcalerts']['r1_severity']} ALERT: Rule 1 triggered at point {indexList[i]}, Please contact {parse_usergroup(ug[conf['spcalerts']['r1_contact']])}" if conf['spcalerts']['r1_contact'] != '' else f"({var_name}) {conf['spcalerts']['r1_severity']} ALERT: Rule 1 triggered at point {indexList[i]}"
            if rule1msg not in spcalerts:
                spcalerts.add(rule1msg)
                print(rule1msg)
                if WRITE_DATA:
                    with open(logfile, 'a+') as lf:
                        lf.write(rule1msg + '\n')

def rule2(valueList, indexList, avg, stdev, plot, var_name):
    for i,y in enumerate(valueList):
        if len(valueList) > 2:
            if (valueList[i-1] > avg + (stdev * 2) or valueList[i-1] < avg - (stdev * 2)) and (valueList[i] > avg + (stdev * 2) or valueList[i] < avg - (stdev * 2)):
                plot.scatter(indexList[i], valueList[i], c="b", zorder=420)
                plot.scatter(indexList[i-1], valueList[i-1], c="b", zorder=420)
                rule2msg = f"({var_name}) {conf['spcalerts']['r2_severity']} ALERT: Rule 2 triggered at point {indexList[i-1]} & {indexList[i]}, Please contact {parse_usergroup(ug[conf['spcalerts']['r2_contact']])}" if conf['spcalerts']['r2_contact'] != '' else f"({var_name}) {conf['spcalerts']['r2_severity']} ALERT: Rule 2 triggered at point {indexList[i-1]} & {indexList[i]}"
                if rule2msg not in spcalerts:
                    spcalerts.add(rule2msg)
                    print(rule2msg)
                    if WRITE_DATA and i == window_size - 1:
                        with open(logfile, 'a+') as lf:
                            lf.write(rule2msg + '\n')

def rule3(valueList, indexList, avg, stdev, plot, var_name):
    # Need to create a variable to store the streak which will be reset if its broken
    r3_streak = {}
    r3_streaks = []
    for i,y in enumerate(valueList):
        if i < len(valueList) - 1:
            if (valueList[i] < (avg - stdev) and valueList[i+1] < avg) or (valueList[i] > (avg + stdev) and valueList[i+1] > avg):
            # if (valueList[i] < (avg - stdev)) or (valueList[i] > (avg + stdev)):
                r3_streak[i] = valueList[i]
            else:
                r3_streak[i] = valueList[i]
                r3_streaks.append(r3_streak)
                r3_streak = {}

    # print([i for i in r3_streaks if bool(i) == True])
    for st in r3_streaks:
        if st is not {} and len(st) == 4:
            rule3msg = f"({var_name}) {conf['spcalerts']['r3_severity']} ALERT: Rule 3 triggered from point {indexList[min(st.keys())]} to {indexList[max(st.keys())]}, Please contact {parse_usergroup(ug[conf['spcalerts']['r3_contact']])}" if conf['spcalerts']['r3_contact'] != '' else f"({var_name}) {conf['spcalerts']['r3_severity']} ALERT: Rule 3 triggered from point {indexList[min(st.keys())]} to {indexList[max(st.keys())]}"
            for k,v in st.items():
                plot.scatter(indexList[k], valueList[k], c="b", zorder=420)
            if (rule3msg not in spcalerts) and (indexList[max(st.keys())] not in spcendpoints):
                spcalerts.add(rule3msg)
                print(rule3msg)
                spcendpoints.add(indexList[max(st.keys())])
                if WRITE_DATA and i == window_size - 1:
                    with open(logfile, 'a+') as lf:
                        lf.write(rule3msg + '\n')

def rule4(valueList, indexList, avg, plot, var_name):
    r4_streak = {}
    r4_streaks = []
    for i,y in enumerate(valueList):
        if i < len(valueList) - 1:
            if y < avg:
                r4_streak[i] = valueList[i]
                if valueList[i+1] > avg:
                    r4_streaks.append(r4_streak)
                    r4_streak = {}
            else:
                r4_streak[i] = valueList[i]
                if valueList[i+1] < avg:
                    r4_streaks.append(r4_streak)
                    r4_streak = {}
            
    # print(r4_streaks)
    for st in r4_streaks:
        if st is not {} and len(st) >= 8:
            rule4msg = f"({var_name}) {conf['spcalerts']['r4_severity']} ALERT: Rule 4 triggered from point {indexList[min(st.keys())]} to {indexList[max(st.keys())]}, Please contact {parse_usergroup(ug[conf['spcalerts']['r4_contact']])}" if conf['spcalerts']['r4_contact'] != '' else f"({var_name}) {conf['spcalerts']['r4_severity']} ALERT: Rule 4 triggered from point {indexList[min(st.keys())]} to {indexList[max(st.keys())]}"
            for k,v in st.items():
                plot.scatter(indexList[k], valueList[k], c="b", zorder=420)
            if (rule4msg not in spcalerts) and (indexList[max(st.keys())] not in spcendpoints):
                spcalerts.add(rule4msg)
                print(rule4msg)
                spcendpoints.add(indexList[max(st.keys())])
                if WRITE_DATA and i == window_size - 1:
                    with open(logfile, 'a+') as lf:
                        lf.write(rule4msg + '\n')

def rule5(valueList, indexList, plot, var_name):
    r5_streak_a = {}
    r5_streaks_a = []
    # Loop through each value in the list

    for i, y in enumerate(valueList):
        if i < len(valueList) - 1:
            if valueList[i+1] > y:
                r5_streak_a[i] = y
                if valueList[i+1] < y:
                    r5_streak_a[i+1] = valueList[i+1]
                    r5_streaks_a.append(r5_streak_a)
                    r5_streak_a = {}
            elif valueList[i+1] < y:
                r5_streak_a[i] = y
                r5_streaks_a.append(r5_streak_a)
                r5_streak_a = {}
            else:
                r5_streaks_a.append(r5_streak_a)
                r5_streak_a = {}

    # Create another set of dict and list to make it detectable the other way around (descending)
    r5_streak_b = {}
    r5_streaks_b = []
    # Loop through each value in the list
    for i, y in enumerate(valueList):
        if i < len(valueList) - 1:
            if valueList[i+1] < y:
                r5_streak_b[i] = y
                if valueList[i+1] > y:
                    r5_streak_b[i+1] = valueList[i+1]
                    r5_streaks_b.append(r5_streak_b)
                    r5_streak_b = {}
            elif valueList[i+1] > y:
                r5_streak_b[i] = y
                r5_streaks_b.append(r5_streak_b)
                r5_streak_b = {}
            else:
                r5_streaks_b.append(r5_streak_b)
                r5_streak_b = {}

    r5_streaks = r5_streaks_a + r5_streaks_b
    for st in r5_streaks:
        if st is not {} and len(st) == 6:
            rule5msg = f"({var_name}) {conf['spcalerts']['r5_severity']} ALERT: Rule 5 triggered from point {indexList[min(st.keys())]} to {indexList[max(st.keys())]}, Please contact {parse_usergroup(ug[conf['spcalerts']['r5_contact']])}" if conf['spcalerts']['r5_contact'] != '' else f"({var_name}) {conf['spcalerts']['r5_severity']} ALERT: Rule 5 triggered from point {indexList[min(st.keys())]} to {indexList[max(st.keys())]}"
            for k,v in st.items():
                plot.scatter(indexList[k], valueList[k], c="b", zorder=420)
            if (rule5msg not in spcalerts) and (indexList[max(st.keys())] not in spcendpoints):
                spcalerts.add(rule5msg)
                print(rule5msg)
                spcendpoints.add(indexList[max(st.keys())])
                if WRITE_DATA and i == window_size - 1:
                    with open(logfile, 'a+') as lf:
                        lf.write(rule5msg + '\n')

def rule6(valueList, indexList, avg, stdev, plot, var_name):
    r6_streak = {}
    r6_streaks = []
    for i,y in enumerate(valueList):
        # if x < len(yl) - 1:
            if y < (avg+stdev) and y > (avg-stdev):
                r6_streak[i] = valueList[i]
            else:
                r6_streaks.append(r6_streak)
                r6_streak = {}
    
    for st in r6_streaks:
        if st is not {} and len(st) >= 15:
            rule6msg = f"({var_name}) {conf['spcalerts']['r6_severity']} ALERT: Rule 6 triggered from point {indexList[min(st.keys())]} to {indexList[max(st.keys())]}, Please contact {parse_usergroup(ug[conf['spcalerts']['r6_contact']])}" if conf['spcalerts']['r6_contact'] != '' else f"({var_name}) {conf['spcalerts']['r6_severity']} ALERT: Rule 6 triggered from point {indexList[min(st.keys())]} to {indexList[max(st.keys())]}"
            for k,v in st.items():
                plot.scatter(indexList[k], valueList[k], c="b", zorder=420)
            if (rule6msg not in spcalerts) and (indexList[max(st.keys())] not in spcendpoints):
                spcalerts.add(rule6msg)
                print(rule6msg)
                spcendpoints.add(indexList[max(st.keys())])
                if WRITE_DATA and i == window_size - 1:
                    with open(logfile, 'a+') as lf:
                        lf.write(rule6msg + '\n')

def rule7(valueList, indexList, plot, var_name):
    r7_streak = {}
    r7_streaks = []
    up = False
    for i,y in enumerate(valueList):
        if i < len(valueList) - 1:
            if up:
                if y < valueList[i+1]:
                    r7_streak[i] = y
                    up = False
                else:
                    r7_streaks.append(r7_streak)
                    r7_streak = {}
            else:
                if y > valueList[i+1]:
                    r7_streak[i] = y
                    up = True
                else:
                    r7_streaks.append(r7_streak)
                    r7_streak = {}
    
    # print(r7_streaks)
    for st in r7_streaks:
        if st is not {} and len(st) >= 14:
            rule7msg = f"({var_name}) {conf['spcalerts']['r7_severity']} ALERT: Rule 7 triggered from point {indexList[min(st.keys())]} to {indexList[max(st.keys())]}, Please contact {parse_usergroup(ug[conf['spcalerts']['r7_contact']])}" if conf['spcalerts']['r7_contact'] != '' else f"({var_name}) {conf['spcalerts']['r7_severity']} ALERT: Rule 7 triggered from point {indexList[min(st.keys())]} to {indexList[max(st.keys())]}"
            for k,v in st.items():
                plot.scatter(indexList[k], valueList[k], c="b", zorder=420)
            if (rule7msg not in spcalerts) and (indexList[max(st.keys())] not in spcendpoints):
                spcalerts.add(rule7msg)
                print(rule7msg)
                spcendpoints.add(indexList[max(st.keys())])
                if WRITE_DATA and i == window_size - 1:
                    with open(logfile, 'a+') as lf:
                        lf.write(rule7msg + '\n')

def rule8(valueList, indexList, avg, stdev, plot, var_name):
    # Need to create a variable to store the streak which will be reset if its broken
    r8_streak = {}
    r8_streaks = []
    for i,y in enumerate(valueList):
        if i < len(valueList) - 1:
            if (y < (avg - stdev)) or (y > (avg + stdev)):
                r8_streak[i] = valueList[i]
            else:
                r8_streaks.append(r8_streak)
                r8_streak = {}

    for st in r8_streaks:
        if st is not {} and len(st) >= 8:
            rule8msg = f"({var_name}) {conf['spcalerts']['r8_severity']} ALERT: Rule 8 triggered from point {indexList[min(st.keys())]} to {indexList[max(st.keys())]}, Please contact {parse_usergroup(ug[conf['spcalerts']['r8_contact']])}" if conf['spcalerts']['r3_contact'] != '' else f"({var_name}) {conf['spcalerts']['r8_severity']} ALERT: Rule 8 triggered from point {indexList[min(st.keys())]} to {indexList[max(st.keys())]}"
            for k,v in st.items():
                plot.scatter(indexList[k], valueList[k], c="b", zorder=420)
            if (rule8msg not in spcalerts) and (indexList[max(st.keys())] not in spcendpoints):
                spcalerts.add(rule8msg)
                print(rule8msg)
                spcendpoints.add(indexList[max(st.keys())])
                if WRITE_DATA and i == window_size - 1:
                    with open(logfile, 'a+') as lf:
                        lf.write(rule8msg + '\n')

def data_range(data_list, wsize):
    return data_list[-(wsize):]

# We could try to move the SPC algorithms out of the graph so it does not rely on a plot to work but its too late and i want to end my SPC project faster
def animate(i):
    global xs, ys
    # Limit x and y lists to 30 items
    # xs = xs[-window_size:]
    # ys = ys[-window_size:]

    # Draw x and y lists
    xsdr = data_range(xs,window_size)
    ysdr = data_range(ys,window_size)
    ax.clear()
    set_labels(ax, "RAW DATA")
    ax.plot(xsdr, ysdr)
    # print("RAW XS/YS:", xs, ys)

    if len(ys) > 2:
        # Build MA3, MA5, MA7
        avg = np.nanmean(ysdr)
        stdev = statistics.stdev(ysdr)
        # avg = (a+b) / 2
        # stdev = math.sqrt(((b-a) ** 2)/12)
        ucl = avg + (stdev * 3)
        lcl = avg - (stdev * 3)
        # print(avg, stdev)

        # Sigma lines
        sigma_lines(ax, avg, stdev, xsdr)

        # Moving averages
        '''
        if len(ys) > 3:
            a3.clear()
            moving3 = moving_average(ys,3)[-window_size:]
            a3.plot(moving3)
            sigma_lines(a3, np.nanmean(moving3), statistics.stdev(moving3))

        if len(ys) > 5:
            a5.clear()
            moving5 = moving_average(ys,5)[-window_size:]
            a5.plot(moving5)
            sigma_lines(a5, np.nanmean(moving5), statistics.stdev(moving5))

        if len(ys) > 7:
            a7.clear()
            moving7 = moving_average(ys,7)[-window_size:]
            a7.plot(moving7)
            sigma_lines(a7, np.nanmean(moving7), statistics.stdev(moving7))
'''
        # Check for SPC rules
        # Rule 1
        rule1(ysdr, xsdr, [ucl,lcl], ax, "RAW")

        # Rule 2
        rule2(ysdr, xsdr, avg, stdev, ax, "RAW")

        # Rule 3
        rule3(ysdr, xsdr, avg, stdev, ax, "RAW")

        # Rule 4
        rule4(ysdr, xsdr, avg, ax, "RAW")

        # Rule 5
        rule5(ysdr, xsdr, ax, "RAW")

        # Rule 6
        rule6(ysdr, xsdr, avg, stdev, ax, "RAW")
        
        # Rule 7
        rule7(ysdr, xsdr, ax, "RAW")

        # Rule 8
        rule8(ysdr, xsdr, avg, stdev, ax, "RAW")

def animate_a3(i):
    global xs, ys
    if len(ys) > 2:
        pos = (xs[2:])
        podr = data_range(pos,window_size)

        # Moving averages
        if len(ys) > 3:
            a3.clear()
            moving3 = moving_average(ys,3)
            m3dr = data_range(moving3,window_size)
            # print("MA3", pos)
            set_labels(a3, "3PT MOVING AVG")
            a3.plot(podr, m3dr)

            # Fix bug: avg and stdev of MA graph should be based on MA values
            avg = np.nanmean(moving3)
            stdev = statistics.stdev(moving3)
            # avg = (a+b) / 2
            # stdev = math.sqrt(((b-a) ** 2)/12)
            ucl = avg + (stdev * 3)
            lcl = avg - (stdev * 3)
            sigma_lines(a3, np.nanmean(m3dr), statistics.stdev(m3dr), podr)

            # Check for SPC rules
            # Rule 1
            rule1(m3dr, podr, [ucl,lcl], a3, "A3")

            # Rule 2
            rule2(m3dr, podr, avg, stdev, a3, "A3")

            # Rule 3
            rule3(m3dr, podr, avg, stdev, a3, "A3")

            # Rule 4
            rule4(m3dr, podr, avg, a3, "A3")

            # Rule 5
            rule5(m3dr, podr, a3, "A3")

            # Rule 6
            rule6(m3dr, podr, avg, stdev, a3, "A3")
            
            # Rule 7
            rule7(m3dr, podr, a3, "A3")

            # Rule 8
            rule8(m3dr, podr, avg, stdev, a3, "A3")
           
def animate_a5(i):
    global xs, ys
    if len(ys) > 2:
        pos = (xs[4:])
        podr = data_range(pos, window_size)


        # Moving averages
        if len(ys) > 5:
            a5.clear()
            moving5 = moving_average(ys,5)
            m5dr = data_range(moving5, window_size)
            set_labels(a5, "5PT MOVING AVG")
            a5.plot(podr, m5dr)

            avg = np.nanmean(moving5)
            stdev = statistics.stdev(moving5)

            ucl = avg + (stdev * 3)
            lcl = avg - (stdev * 3)
            sigma_lines(a5, np.nanmean(m5dr), statistics.stdev(m5dr), podr)

            # Check for SPC rules
            # Rule 1
            rule1(m5dr, podr, [ucl,lcl], a5, "A5")

            # Rule 2
            rule2(m5dr, podr, avg, stdev, a5, "A5")

            # Rule 3
            rule3(m5dr, podr, avg, stdev, a5, "A5")

            # Rule 4
            rule4(m5dr, podr, avg, a5, "A5")

            # Rule 5
            rule5(m5dr, podr, a5, "A5")

            # Rule 6
            rule6(m5dr, podr, avg, stdev, a5, "A5")
            
            # Rule 7
            rule7(m5dr, podr, a5, "A5")

            # Rule 8
            rule8(m5dr, podr, avg, stdev, a5, "A5")

def animate_a7(i):
    global xs, ys
    if len(ys) > 2:
        pos = (xs[6:])
        podr = data_range(pos, window_size)


        # Moving averages
        if len(ys) > 7:
            a7.clear()
            moving7 = moving_average(ys,7)
            m7dr = data_range(moving7, window_size)
            set_labels(a7, "7PT MOVING AVG")
            a7.plot(podr, m7dr)

            avg = np.nanmean(moving7)
            stdev = statistics.stdev(moving7)

            ucl = avg + (stdev * 3)
            lcl = avg - (stdev * 3)
            sigma_lines(a7, np.nanmean(m7dr), statistics.stdev(m7dr), podr)

            # Check for SPC rules
            # Rule 1
            rule1(m7dr, podr, [ucl,lcl], a7, "A7")

            # Rule 2
            rule2(m7dr, podr, avg, stdev, a7, "A7")

            # Rule 3
            rule3(m7dr, podr, avg, stdev, a7, "A7")

            # Rule 4
            rule4(m7dr, podr, avg, a7, "A7")

            # Rule 5
            rule5(m7dr, podr, a7, "A7")

            # Rule 6
            rule6(m7dr, podr, avg, stdev, a7, "A7")
            
            # Rule 7
            rule7(m7dr, podr, a7, "A7")

            # Rule 8
            rule8(m7dr, podr, avg, stdev, a7, "A7")

def changeSpeed(spd):
    global ani
    if spd.isnumeric():
        print(spd)
        spd = int(spd)
        ani.event_source.interval = spd
        
def checkforchange():
    # Use md5 hashing to check for change in the data file so that we can update the program if there is a change 
    global hash, timeint
    with open(fil, "rb") as f:
        if hash != hashlib.md5(f.read()).hexdigest():
            load(fil) # If there is change in the file "reload" the file with new changes
            hash = hashlib.md5(f.read()).hexdigest()

    sm.after(timeint, checkforchange)

def parse_usergroup(k):
    ug_info = ""

    try:
        if len(k) == 1:
            ug_info = k[0]
        elif len(k) == 2:
            ug_info = k[0] + " and " + k[1]
        elif len(k) >= 3:
            for n in range(len(k) - 2):
                ug_info += f"{k[n]}, "
            ug_info += k[-2] + " and " + k[-1]
    except: #Flexibility
        ug_info = k

    return ug_info

# Test for external use
class Main():
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Initial
        conf = configparser.ConfigParser()
        conf.read('config.ini')

        fond = "Segoe UI Bold"
        plt.style.use('Solarize_Light2')
        WRITE_DATA = True

        # Global
        # global timeint
        # global ani
        # global spcalerts
        # global spcendpoints # This is to prevent repeated alerts when data points that triggered SPC goes off the screen and the algorithm recalculates and spams the alert messages
        # global window_size
        window_size = int(conf['spcmain']['winsize'])
        spcalerts = set()
        spcendpoints = set()
        plt.style.use('ggplot')

        # User configured ax labels
        xa_label = conf['spcmain']['xa_label']
        ya_label = conf['spcmain']['ya_label']

        # Matplotlib
        fig1, ax = plt.subplots()
        fig2, a3 = plt.subplots()
        fig3, a5 = plt.subplots()
        fig4, a7 = plt.subplots()
        xs = np.array([], copy=False, dtype=np.uint32)
        ys = np.array([], copy=False)
        # print("Init XS/YS:", xs, ys)

        # Tkinter
        sm = SpcMon()

        # Save files
        date_time = datetime.datetime.now().strftime('%Y.%m.%d-%H.%M.%S.%f')
        # datefile = pd.read_csv(data)

        # Use default values if none is specified
        if len(sys.argv) < 2:
            fil = "test2.csv"
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

        timeint = 500

        with open(logfile, 'r') as log:
            existing_log = log.read().split('\n')
            # print(existing_log)
        
        for l in existing_log:
            spcalerts.add(l)

        # Load all the graph animations before starting generation
        sm.after(1000, lambda: init_load(fil))
        sm.after(1200, checkforchange)

        ani = animation.FuncAnimation(fig1, animate, interval=timeint, init_func=ani_init, blit=False)
        ani_a3 = animation.FuncAnimation(fig2, animate_a3, interval=timeint, init_func=ani_init, blit=False)
        ani_a5 = animation.FuncAnimation(fig3, animate_a5, interval=timeint, init_func=ani_init, blit=False)
        ani_a7 = animation.FuncAnimation(fig4, animate_a7, interval=timeint, init_func=ani_init, blit=False)

        sm.mainloop()

if __name__ == '__main__':
    # Initial
    conf = configparser.ConfigParser()
    conf.read('config.ini')

    with open('usergroups.json') as f:
        ug = json.load(f)

    fond = "Segoe UI Bold"
    plt.style.use('Solarize_Light2')
    WRITE_DATA = True

    # Global
    # global timeint
    # global ani
    # global spcalerts
    # global spcendpoints # This is to prevent repeated alerts when data points that triggered SPC goes off the screen and the algorithm recalculates and spams the alert messages
    # global window_size
    window_size = int(conf['spcmain']['winsize'])
    spcalerts = set()
    spcendpoints = set()
    plt.style.use('ggplot')

    # User configured ax labels
    xa_label = conf['spcmain']['xa_label']
    ya_label = conf['spcmain']['ya_label']

    # Matplotlib
    fig1, ax = plt.subplots()
    fig2, a3 = plt.subplots()
    fig3, a5 = plt.subplots()
    fig4, a7 = plt.subplots()
    xs = np.array([], copy=False, dtype=np.uint32)
    ys = np.array([], copy=False)
    # print("Init XS/YS:", xs, ys)

    # Tkinter
    sm = SpcMon()

    # Save files
    date_time = datetime.datetime.now().strftime('%Y.%m.%d-%H.%M.%S.%f')
    # datefile = pd.read_csv(data)

    # Use default values if none is specified
    if len(sys.argv) < 2:
        fil = "test2.csv"
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

    timeint = 500

    with open(logfile, 'r') as log:
        existing_log = log.read().split('\n')
        # print(existing_log)
    
    for l in existing_log:
        spcalerts.add(l)

    # Load all the graph animations before starting generation
    sm.after(1000, lambda: init_load(fil))
    sm.after(1200, checkforchange)

    ani = animation.FuncAnimation(fig1, animate, interval=timeint, init_func=ani_init, blit=False)
    ani_a3 = animation.FuncAnimation(fig2, animate_a3, interval=timeint, init_func=ani_init, blit=False)
    ani_a5 = animation.FuncAnimation(fig3, animate_a5, interval=timeint, init_func=ani_init, blit=False)
    ani_a7 = animation.FuncAnimation(fig4, animate_a7, interval=timeint, init_func=ani_init, blit=False)

    sm.mainloop()