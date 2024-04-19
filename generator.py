import random, time, datetime, csv, sys, configparser
import tkinter as Tk
import pandas as pd
import customtkinter as Ctk

class Generator(Ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SPC Data Generator (For Testing Purposes)")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.titleLabel = Ctk.CTkLabel(self, text="SPC Generator", font=("Segoe UI Bold", 24), anchor='w')
        self.titleLabel.grid(column=0, row=0, columnspan=2)

        # Buttons to trigger the SPC rules
        self.button0 = Ctk.CTkButton(self, text="No SPC", command=lambda: changeDadu(0))
        self.button0.grid(column=0, row=1)
        self.button1 = Ctk.CTkButton(self, text="SPC 1", command=lambda: changeDadu(1))
        self.button1.grid(column=1, row=1)
        self.button2 = Ctk.CTkButton(self, text="SPC 2", command=lambda: changeDadu(2))
        self.button2.grid(column=2, row=1)
        self.button3 = Ctk.CTkButton(self, text="SPC 3", command=lambda: changeDadu(3))
        self.button3.grid(column=3, row=1)
        self.button4 = Ctk.CTkButton(self, text="SPC 4", command=lambda: changeDadu(4))
        self.button4.grid(column=4, row=1)
        self.button5 = Ctk.CTkButton(self, text="SPC 5", command=lambda: changeDadu(5))
        self.button5.grid(column=1, row=2)
        self.button6 = Ctk.CTkButton(self, text="SPC 6", command=lambda: changeDadu(6))
        self.button6.grid(column=2, row=2)
        self.button7 = Ctk.CTkButton(self, text="SPC 7", command=lambda: changeDadu(7))
        self.button7.grid(column=3, row=2)
        self.button8 = Ctk.CTkButton(self, text="SPC 8", command=lambda: changeDadu(8))
        self.button8.grid(column=4, row=2)
        self.buttonOn = Ctk.CTkButton(self, text="Spc Start", command=lambda: spcActivate(True))
        self.buttonOn.grid(column=5, row=1)
        self.buttonOff = Ctk.CTkButton(self, text="Spc Stop", command=lambda: spcActivate(False))
        self.buttonOff.grid(column=5, row=2)
        self.spc_label = Ctk.CTkLabel(self, text="SPC: 0")
        self.spc_label.grid(column=0, row=2)

        instructions = Ctk.CTkLabel(self, text="Press any SPC button to trigger SPC rules, The rules may be triggered once every 30 time points")
        instructions.grid(column=0, row=3, columnspan=6)

def write_csv(data_file):
    with open(data, 'a+') as outfile: # use a to append file instead of overwriting it
        writer = csv.writer(outfile)
        writer.writerow(data_file) # write a new row of data

def generator(i, min, max, dadu = 0):
    global xs
    global ys
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
    gen.winfo_children()[-2].configure(text=f"SPC: {v}")

def outputData(min, max):
    global i
    global spcActive
    if spcActive:
        data_value = generator(i, min, max, dadu)
        if DEBUG:
            print(data_value)
        i += 1

        # if WRITE_DATA: (It's an optional generator program now, this line is no longer necessary)
        write_csv([i, data_value])

    gen.after(ms = timeint, func = lambda: outputData(low_value, high_value))

def spcActivate(spcActivate):
    # Turn SPC on or off
    global spcActive
    if spcActivate:
        spcActive = True
    else:
        spcActive = False

if __name__ == '__main__':
    # Read the config file to set some things up
    conf = configparser.ConfigParser()
    conf.read('config.ini')

    DEBUG = conf['generator'].getboolean('deebaag')

    gen = Generator()
    # print(sys.argv)

    window_size = 30
    xs = []
    ys = []
    # print(len(sys.argv))
    # Save files
    date_time = datetime.datetime.now().strftime('%Y.%m.%d-%H.%M.%S.%f')
    if (len(sys.argv) < 2): # second argv is name of file
        data = "test.csv"
    else:
        data = sys.argv[1]

    if len(sys.argv) < 3 : # third argv is the speed
        timeint = int(0.5 * 1000)
    else:
        try:    
            timeint = int(float(sys.argv[2]))
        except ValueError:    
            timeint = int(0.5 * 1000)
            print("That's not a float!")

    # print(sys.argv[0], timeint)

    if len(sys.argv) < 4 or not (sys.argv[3].isnumeric()): # fourth argv is the seed
        seed = 42
    else:
        seed = int(sys.argv[3])

    random.seed(seed)

    try:
        df = pd.read_csv(data, header=None)
        print(max(df[0]))
        i = max(df[0])
    except pd.errors.EmptyDataError:
        i = 0

    dadu = 0
    spcActive = False
    open(data,'a+')
    if (len(sys.argv) < 6) or not ((sys.argv[4].isnumeric()) and (sys.argv[5].isnumeric())): # 3 argvs, filename, rate, seed, min value, max value
        low_value = 1
        high_value = 101
    else:
        if int(sys.argv[4]) < int(sys.argv[5]):
            low_value = int(sys.argv[4])
            high_value = int(sys.argv[5])
        else:
            high_value = int(sys.argv[4])
            low_value = int(sys.argv[5])
    
    gen.after(ms = timeint, func = lambda: outputData(low_value, high_value))

    gen.mainloop()

