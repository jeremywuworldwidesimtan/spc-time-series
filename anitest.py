from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
import tkinter as Tk
from tkinter import ttk
import random, statistics, math, datetime, csv, time

# Initial
random.seed(12)
WRITE_DATA = False

# Global
global dadu
global speed
global ani
global spcalerts
global spcendpoints # This is to prevent repeated alerts when data points that triggered SPC goes off the screen and the algorithm recalculates and spams the alert messages
global window_size
window_size = 30
spcalerts = set()
spcendpoints = set()
plt.style.use('ggplot')

# Matplotlib
fig1, ax = plt.subplots()
fig2, a3 = plt.subplots()
fig3, a5 = plt.subplots()
fig4, a7 = plt.subplots()
xs = []
ys = []

# Tkinter
root = Tk.Tk()
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Save files
date_time = datetime.datetime.now().strftime('%Y.%m.%d-%H.%M.%S.%f')
data = "TSD-" + date_time + ".csv"
logfile = "LOG-" + date_time + ".txt"
# datefile = pd.read_csv(data)

def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def write_csv(data_file):
    with open(data, 'a+') as outfile: # use a to append file instead of overwriting it
        writer = csv.writer(outfile)
        writer.writerow(data_file) # write a new row of data

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

def rule1(valueList, indexList, limits, plot, var_name):
    ucl = limits[0]
    lcl = limits[1]
    for i,y in enumerate(valueList):
        if y > ucl or y < lcl:
            plot.scatter(indexList[i], valueList[i], c="r")
            rule1msg = f"({var_name}) ALERT: Rule 1 triggered at point {indexList[i]}"
            if rule1msg not in spcalerts:
                spcalerts.add(rule1msg)
                insertText(rule1msg)
                print(rule1msg)
                if WRITE_DATA:
                    with open(logfile, 'a+') as lf:
                        lf.write(rule1msg + '\n')

def rule2(valueList, indexList, avg, stdev, plot, var_name):
    for i,y in enumerate(valueList):
        if len(valueList) > 2:
            if (valueList[i-1] > avg + (stdev * 2) or valueList[i-1] < avg - (stdev * 2)) and (valueList[i] > avg + (stdev * 2) or valueList[i] < avg - (stdev * 2)):
                plot.scatter(indexList[i], valueList[i], c="r")
                plot.scatter(indexList[i-1], valueList[i-1], c="r")
                rule2msg = f"({var_name}) ALERT: Rule 2 triggered at point {indexList[i-1]} & {indexList[i]}"
                if rule2msg not in spcalerts:
                    spcalerts.add(rule2msg)
                    insertText(rule2msg)
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
            rule3msg = f"({var_name}) ALERT: Rule 3 triggered from point {indexList[min(st.keys())]} to {indexList[max(st.keys())]}"
            for k,v in st.items():
                plot.scatter(indexList[k], valueList[k], c="r")
            if (rule3msg not in spcalerts) and (indexList[max(st.keys())] not in spcendpoints):
                spcalerts.add(rule3msg)
                insertText(rule3msg)
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
            rule4msg = f"({var_name}) ALERT: Rule 4 triggered from point {indexList[min(st.keys())]} to {indexList[max(st.keys())]}"
            for k,v in st.items():
                plot.scatter(indexList[k], valueList[k], c="r")
            if (rule4msg not in spcalerts) and (indexList[max(st.keys())] not in spcendpoints):
                spcalerts.add(rule4msg)
                insertText(rule4msg)
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
            rule5msg = f"({var_name}) ALERT: Rule 5 triggered from point {indexList[min(st.keys())]} to {indexList[max(st.keys())]}"
            for k,v in st.items():
                plot.scatter(indexList[k], valueList[k], c="r")
            if (rule5msg not in spcalerts) and (indexList[max(st.keys())] not in spcendpoints):
                spcalerts.add(rule5msg)
                insertText(rule5msg)
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
            rule6msg = f"({var_name}) ALERT: Rule 6 triggered from point {indexList[min(st.keys())]} to {indexList[max(st.keys())]}"
            for k,v in st.items():
                plot.scatter(indexList[k], valueList[k], c="r")
            if (rule6msg not in spcalerts) and (indexList[max(st.keys())] not in spcendpoints):
                spcalerts.add(rule6msg)
                insertText(rule6msg)
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
            rule7msg = f"({var_name}) ALERT: Rule 7 triggered from point {indexList[min(st.keys())]} to {indexList[max(st.keys())]}"
            for k,v in st.items():
                plot.scatter(indexList[k], valueList[k], c="r")
            if (rule7msg not in spcalerts) and (indexList[max(st.keys())] not in spcendpoints):
                spcalerts.add(rule7msg)
                insertText(rule7msg)
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
            rule8msg = f"({var_name}) ALERT: Rule 8 triggered from point {indexList[min(st.keys())]} to {indexList[max(st.keys())]}"
            for k,v in st.items():
                plot.scatter(indexList[k], valueList[k], c="r")
            if (rule8msg not in spcalerts) and (indexList[max(st.keys())] not in spcendpoints):
                spcalerts.add(rule8msg)
                insertText(rule8msg)
                print(rule8msg)
                spcendpoints.add(indexList[max(st.keys())])
                if WRITE_DATA and i == window_size - 1:
                    with open(logfile, 'a+') as lf:
                        lf.write(rule8msg + '\n')

def animate(i, xs, ys):
    a = 1
    b = 101
    rv = random.randint(a,b) + random.random()
    # Spiking and triggering
    # the biggest problem is being able to run patterns for more than 1 iteration and for different iterations.
    trigger = 30 # Trigger once every n time points
    # dadu = random.randint(1,8)
    # print(dadu)

    if i % trigger in range(15) and i >= 30:
        if dadu == 1:
            if i % trigger == 0:
                # Rule 1
                y = rv * 5 if rv > 30 else rv * 10
            else:
                y = rv
        elif dadu == 2:
            # Rule 2
            if i % trigger in range(2):
                # y = rv * 2 if rv > 50 else (rv + 50) * 2
                y = random.randint(130,160)
            else:
                y = rv
        elif dadu == 3:
            # Rule 3
            if i % trigger in range(4):
                # y = rv * 1.5 if rv > 50 else (rv + 50) * 1.5
                y = random.randint(120, 150)
            else:
                y = rv
        elif dadu == 4:
            # Rule 4
            if i % trigger in range(8):
                y = rv * 1.5 if rv > 50 else (rv + 50) * 1.5
            else:
                y = rv
        elif dadu == 5:
            # Rule 5
            if i % trigger in range(8):
                if i % trigger == 0: # One point before the data points
                    y = 70
                elif i % trigger == 7: # One point after the data points
                    y = 30
                else:
                    y = 50 + ((i % trigger) * 2)
            else:
                y = rv
        elif dadu == 6:
            # Rule 6
            if i % trigger in range(15):
                y = random.randint(40, 60)
            else:
                y = rv
        elif dadu == 7:
            if i % trigger in range(14):
                if i % trigger % 2 == 0:
                    y = random.randint(25,45)
                else:
                    y = random.randint(55,75)
            else:
                y = rv
        elif dadu == 8:
            if i % trigger in range(8):
                if (i % trigger) % 4 == 1 or (i % trigger) % 4 == 2:
                    y = random.randint(0,20)
                else:
                    y = random.randint(80,100)
            else:
                y = rv
        else:
            y = rv
    else:
        y = rv
        
    # Add x and y to lists
    xs.append(i)
    ys.append(y)

    # Limit x and y lists to 30 items
    xs = xs[-window_size:]
    ys = ys[-window_size:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # print("RAW", xs)
    # print(ys)
    # print([i, ys[-1]])

    if WRITE_DATA:
        write_csv([(i + 1), ys[-1]])
    # print (len(ys))

    if len(ys) > 2:
        # Build MA3, MA5, MA7
        avg = np.nanmean(ys)
        stdev = statistics.stdev(ys)
        # avg = (a+b) / 2
        # stdev = math.sqrt(((b-a) ** 2)/12)
        ucl = avg + (stdev * 3)
        lcl = avg - (stdev * 3)
        # print(avg, stdev)

        # Sigma lines
        sigma_lines(ax, avg, stdev, xs)

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
        rule1(ys, xs, [ucl,lcl], ax, "RAW")

        # Rule 2
        rule2(ys, xs, avg, stdev, ax, "RAW")

        # Rule 3
        rule3(ys, xs, avg, stdev, ax, "RAW")

        # Rule 4
        rule4(ys, xs, avg, ax, "RAW")

        # Rule 5
        rule5(ys, xs, ax, "RAW")

        # Rule 6
        rule6(ys, xs, avg, stdev, ax, "RAW")
        
        # Rule 7
        rule7(ys, xs, ax, "RAW")

        # Rule 8
        rule8(ys, xs, avg, stdev, ax, "RAW")

def animate_a3(i, xs, ys):
    if len(ys) > 2:
        pos = (xs[2:])[-window_size:]
        avg = np.nanmean(ys)
        stdev = statistics.stdev(ys)
        # avg = (a+b) / 2
        # stdev = math.sqrt(((b-a) ** 2)/12)
        ucl = avg + (stdev * 3)
        lcl = avg - (stdev * 3)

        # Moving averages
        if len(ys) > 3:
            a3.clear()
            moving3 = moving_average(ys,3)[-window_size:]
            # print("MA3", pos)
            a3.plot(pos, moving3)
            sigma_lines(a3, np.nanmean(moving3), statistics.stdev(moving3), pos)

            # Check for SPC rules
            # Rule 1
            rule1(moving3, pos, [ucl,lcl], a3, "A3")

            # Rule 2
            rule2(moving3, pos, avg, stdev, a3, "A3")

            # Rule 3
            rule3(moving3, pos, avg, stdev, a3, "A3")

            # Rule 4
            rule4(moving3, pos, avg, a3, "A3")

            # Rule 5
            rule5(moving3, pos, a3, "A3")

            # Rule 6
            rule6(moving3, pos, avg, stdev, a3, "A3")
            
            # Rule 7
            rule7(moving3, pos, a3, "A3")

            # Rule 8
            rule8(moving3, pos, avg, stdev, a3, "A3")
           
def animate_a5(i, xs, ys):
    if len(ys) > 2:
        pos = (xs[4:])[-window_size:]
        avg = np.nanmean(ys)
        stdev = statistics.stdev(ys)
        # avg = (a+b) / 2
        # stdev = math.sqrt(((b-a) ** 2)/12)
        ucl = avg + (stdev * 3)
        lcl = avg - (stdev * 3)

        # Moving averages
        if len(ys) > 5:
            a5.clear()
            moving5 = moving_average(ys,5)[-window_size:]
            # print("MA3", pos)
            a5.plot(pos, moving5)
            sigma_lines(a5, np.nanmean(moving5), statistics.stdev(moving5), pos)

            # Check for SPC rules
            # Rule 1
            rule1(moving5, pos, [ucl,lcl], a5, "A5")

            # Rule 2
            rule2(moving5, pos, avg, stdev, a5, "A5")

            # Rule 3
            rule3(moving5, pos, avg, stdev, a5, "A5")

            # Rule 4
            rule4(moving5, pos, avg, a5, "A5")

            # Rule 5
            rule5(moving5, pos, a5, "A5")

            # Rule 6
            rule6(moving5, pos, avg, stdev, a5, "A5")
            
            # Rule 7
            rule7(moving5, pos, a5, "A5")

            # Rule 8
            rule8(moving5, pos, avg, stdev, a5, "A5")

def animate_a7(i, xs, ys):
    if len(ys) > 2:
        pos = (xs[6:])[-window_size:]
        avg = np.nanmean(ys)
        stdev = statistics.stdev(ys)
        # avg = (a+b) / 2
        # stdev = math.sqrt(((b-a) ** 2)/12)
        ucl = avg + (stdev * 3)
        lcl = avg - (stdev * 3)

        # Moving averages
        if len(ys) > 7:
            a7.clear()
            moving7 = moving_average(ys,7)[-window_size:]
            # print("MA3", pos)
            a7.plot(pos, moving7)
            sigma_lines(a7, np.nanmean(moving7), statistics.stdev(moving7), pos)

            # Check for SPC rules
            # Rule 1
            rule1(moving7, pos, [ucl,lcl], a7, "A7")

            # Rule 2
            rule2(moving7, pos, avg, stdev, a7, "A7")

            # Rule 3
            rule3(moving7, pos, avg, stdev, a7, "A7")

            # Rule 4
            rule4(moving7, pos, avg, a7, "A7")

            # Rule 5
            rule5(moving7, pos, a7, "A7")

            # Rule 6
            rule6(moving7, pos, avg, stdev, a7, "A7")
            
            # Rule 7
            rule7(moving7, pos, a7, "A7")

            # Rule 8
            rule8(moving7, pos, avg, stdev, a7, "A7")

def changeDadu(v):
    global dadu
    # print("dadu changed to", v)
    dadu = v
    spc_label['text'] = f"SPC: {v}"

def changeSpeed(spd):
    global ani
    if spd.isnumeric():
        print(spd)
        spd = int(spd)
        ani.event_source.interval = spd

def tkinit(tab):
    tabs.select(tab)

def ani_pause():
    ani.pause()
    ani_a3.pause()
    ani_a5.pause()
    ani_a7.pause()

def ani_resume():
    ani.resume()
    ani_a3.resume()
    ani_a5.resume()
    ani_a7.resume()

def insertText(tex):
    numlines = int(spc_alerts.index('end - 1 line').split('.')[0])
    spc_alerts['state'] = 'normal'
    if spc_alerts.index('end-1c')!='1.0':
        spc_alerts.insert('end', '\n')
    spc_alerts.insert('end', tex)
    spc_alerts['state'] = 'disabled'

def updateSpcAlertsText():
    oldSPC = spcalerts
    for alert in spcalerts:
        spc_all_alerts.insert('end', alert + "\n")
    if oldSPC != spcalerts:
        spc_all_alerts.delete('1.0', 'end')
        for alert in spcalerts:
            spc_all_alerts.insert('end', alert + "\n")
        
        oldSPC = spc_alerts
    
    # root.after(10, updateSpcAlertsText)

if __name__ == '__main__':
    dadu = 0
    speed = 500
    # Set up plot to call animate() function periodically
    label = Tk.Label(root,text="1997 nba").grid(column=0, row=0)
    tabs = ttk.Notebook(root)
    tab_raw = Tk.Frame(tabs)
    tab_m3 = Tk.Frame(tabs)
    tab_m5 = Tk.Frame(tabs)
    tab_m7 = Tk.Frame(tabs)
    tab_alerts = Tk.Frame(tabs)
    tab_all_alerts = Tk.Frame(tabs)
    instructions = Tk.Label(root, text="Press any SPC button to trigger SPC rules, The rules may be triggered once every 30 time points")
    instructions.grid(column=0, row=2)

    # Buttons to trigger the SPC rules
    buttons_frame = Tk.Frame(root)
    button0 = Tk.Button(buttons_frame, text="No SPC", command=lambda: changeDadu(0))
    button0.grid(column=0, row=0)
    button1 = Tk.Button(buttons_frame, text="SPC 1", command=lambda: changeDadu(1))
    button1.grid(column=1, row=0)
    button2 = Tk.Button(buttons_frame, text="SPC 2", command=lambda: changeDadu(2))
    button2.grid(column=2, row=0)
    button3 = Tk.Button(buttons_frame, text="SPC 3", command=lambda: changeDadu(3))
    button3.grid(column=3, row=0)
    button4 = Tk.Button(buttons_frame, text="SPC 4", command=lambda: changeDadu(4))
    button4.grid(column=4, row=0)
    button5 = Tk.Button(buttons_frame, text="SPC 5", command=lambda: changeDadu(5))
    button5.grid(column=1, row=1)
    button6 = Tk.Button(buttons_frame, text="SPC 6", command=lambda: changeDadu(6))
    button6.grid(column=2, row=1)
    button7 = Tk.Button(buttons_frame, text="SPC 7", command=lambda: changeDadu(7))
    button7.grid(column=3, row=1)
    button8 = Tk.Button(buttons_frame, text="SPC 8", command=lambda: changeDadu(8))
    button8.grid(column=4, row=1)
    spc_label = Tk.Label(buttons_frame, text="SPC: 0")
    spc_label.grid(column=0, row=1)

    buttons_frame.grid(column=0, row=3)

    # SPC controls including speed controls
    controls_frame = Tk.Frame(root)
    speed_entry = Tk.Label(controls_frame, text='Speed (def = 250)')
    speed_input = Tk.Entry(controls_frame)
    speed_button = Tk.Button(controls_frame, text="Change Speed", command=lambda: changeSpeed(speed_input.get()))
    speed_entry.grid(column=0, row=0)
    speed_input.grid(column=1, row=0)
    speed_button.grid(column=2, row=0)
    controls_frame.grid(column=0, row=4)

    # Graph tabs
    canvas_main = FigureCanvasTkAgg(fig1, master=tab_raw)
    canvas_main.get_tk_widget().grid(column=0,row=0, sticky='nsew')
    canvas_a3 = FigureCanvasTkAgg(fig2, master=tab_m3)
    canvas_a3.get_tk_widget().grid(column=0,row=0, sticky='nsew') 
    canvas_a5 = FigureCanvasTkAgg(fig3, master=tab_m5)
    canvas_a5.get_tk_widget().grid(column=0,row=0, sticky='nsew')
    canvas_a7 = FigureCanvasTkAgg(fig4, master=tab_m7)
    canvas_a7.get_tk_widget().grid(column=0,row=0, sticky='nsew')

    # SPC alert tabs
    spc_alerts = Tk.Text(tab_alerts)
    yscrollbar1 = ttk.Scrollbar(tab_alerts, orient = 'vertical', command = spc_alerts.yview)
    spc_alerts['yscrollcommand'] = yscrollbar1.set
    spc_alerts.grid(column = 0, row = 0, sticky = 'nwes')
    yscrollbar1.grid(column = 1, row = 0, sticky = 'ns')
    tab_alerts.grid_columnconfigure(0, weight = 1)
    tab_alerts.grid_rowconfigure(0, weight = 1)
    spc_alerts.grid(column=0,row=0, sticky='nsew')

    spc_all_alerts = Tk.Text(tab_all_alerts)
    yscrollbar2 = ttk.Scrollbar(tab_all_alerts, orient = 'vertical', command = spc_all_alerts.yview)
    spc_all_alerts['yscrollcommand'] = yscrollbar2.set
    spc_all_alerts.grid(column = 0, row = 0, sticky = 'nwes')
    yscrollbar2.grid(column = 1, row = 0, sticky = 'ns')
    tab_all_alerts.grid_columnconfigure(0, weight = 1)
    tab_all_alerts.grid_rowconfigure(0, weight = 1)
    spc_all_alerts.grid(column=0,row=0, sticky='nsew')

    tabs.add(tab_raw, text="Raw Data", sticky='nsew')
    tabs.add(tab_m3, text="3-datapoint MA", sticky='nsew')
    tabs.add(tab_m5, text="5-datapoint MA", sticky='nsew')
    tabs.add(tab_m7, text="7-datapoint MA", sticky='nsew')
    tabs.add(tab_alerts, text="SPC Alerts", sticky='nsew')
    tabs.add(tab_all_alerts, text="SPC All Alerts", sticky='nsew')
    tabs.grid(column=0,row=1, sticky='nsew')

    # Load all the graph animations before starting generation
    root.after(200, ani_pause)
    root.after(400,lambda: tkinit(tab_m3))
    root.after(600,lambda: tkinit(tab_m5))
    root.after(800,lambda: tkinit(tab_m7))
    root.after(1000,lambda: tkinit(tab_raw))
    root.after(1200,ani_resume)

    ani = animation.FuncAnimation(fig1, animate, fargs=(xs, ys), interval=speed, init_func=ani_init, blit=False)
    ani_a3 = animation.FuncAnimation(fig2, animate_a3, fargs=(xs, ys), interval=speed, init_func=ani_init, blit=False)
    ani_a5 = animation.FuncAnimation(fig3, animate_a5, fargs=(xs, ys), interval=speed, init_func=ani_init, blit=False)
    ani_a7 = animation.FuncAnimation(fig4, animate_a7, fargs=(xs, ys), interval=speed, init_func=ani_init, blit=False)

    Tk.mainloop()