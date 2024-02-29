import random, time, datetime, csv, sys
import tkinter as Tk

random.seed(442)
tk = Tk.Tk()
WRITE_DATA = True

global dadu
global window_size
global i
global spcActive

window_size = 30
dadu = 0
i = 0
xs = []
ys = []
print(len(sys.argv))
# Save files
date_time = datetime.datetime.now().strftime('%Y.%m.%d-%H.%M.%S.%f')
if (len(sys.argv) < 2): # second argv is name of file
    data = "test.csv"
else:
    data = sys.argv[1]

if len(sys.argv) < 3 or not (sys.argv[2].isnumeric()): # third argv is the speed
    timeint = int(0.5 * 1000)
else:
    timeint = int(int(sys.argv[2]) * 1000)

def write_csv(data_file):
    with open(data, 'a+') as outfile: # use a to append file instead of overwriting it
        writer = csv.writer(outfile)
        writer.writerow(data_file) # write a new row of data

def generator(i, min, max, dadu = 0):
    global xs
    global ys
    # global dadu # This is the line that got me stuck but i think it is cool now
    a = min
    b = max
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
    # print(xs)
    ys.append(y)

    # Limit x and y lists to 30 items
    xs = xs[-window_size:]
    ys = ys[-window_size:]

    return y

def changeDadu(v):
    global dadu
    # print("dadu changed to", v)
    dadu = v
    spc_label['text'] = f"SPC: {v}"

def outputData(min, max):
    global i
    global spcActive
    if spcActive:
        data_value = generator(i, min, max, dadu)
        print(data_value)
        i += 1

        if WRITE_DATA:
            write_csv([i, data_value])

    tk.after(ms = timeint, func = lambda: outputData(low_value, high_value))

def spcActivate(spcActivate):
    # Turn SPC on or off
    global spcActive
    if spcActivate:
        spcActive = True
    else:
        spcActive = False

if __name__ == '__main__':
    dadu = 0
    spcActive = False
    open(data,'w')
    if (len(sys.argv) < 5) or not ((sys.argv[3].isnumeric()) and (sys.argv[4].isnumeric())): # 3 argvs, filename, speed, min value, max value
        low_value = 1
        high_value = 101
    else:
        low_value = int(sys.argv[3])
        high_value = int(sys.argv[4])
    
    # Set up plot to call animate() function periodically
    label = Tk.Label(tk,text="spc data generator").grid(column=0, row=0)

    # Buttons to trigger the SPC rules
    buttons_frame = Tk.Frame(tk)
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
    buttonOn = Tk.Button(buttons_frame, text="Spc Start", command=lambda: spcActivate(True))
    buttonOn.grid(column=5, row=0)
    buttonOff = Tk.Button(buttons_frame, text="Spc Stop", command=lambda: spcActivate(False))
    buttonOff.grid(column=5, row=1)
    spc_label = Tk.Label(buttons_frame, text="SPC: 0")
    spc_label.grid(column=0, row=1)

    buttons_frame.grid(column=0, row=1)

    tk.after(ms = 2000, func = lambda: outputData(low_value, high_value))

    Tk.mainloop()

