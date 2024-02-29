import hashlib, sys
import tkinter as Tk
from tkinter import ttk
from tkinter import filedialog

tk = Tk.Tk()
hash = ""

if (len(sys.argv) < 2): # second argv is name of file
    file = filedialog.askopenfilename()
    # file = "tesst.txt"
else:
    file = sys.argv[1]

log_backend = []
filter = ['','']

def changeFile():
    global file
    file = filedialog.askopenfilename()
    init_load()

def init_load():
    global hash
    with open(file, 'rb') as f:
        hash = hashlib.md5(f.read()).hexdigest()
        # print(hash)

def load(file):
    global log_backend
    global filter
    with open(file, 'r') as f:
        log_backend = f.read().split('\n')
        refresh_display(logfilter(log_backend, filter))
        # print(log_backend[:5])

def changeFilter(logs, filterPos, filterKw):
    global filter
    if filterPos in range(2):
        filter[filterPos] = filterKw
    
    currentfilter['text'] = f"Current Filter {str(filter)}"
    refresh_display(logfilter(logs, filter))

def refresh_display(logs):
    try:
        spc_alerts['state'] = 'normal'
        spc_alerts.delete('1.0', 'end')
        spc_alerts['state'] = 'disabled'
        display(logs)
    except:
        display(logs)

def display(logs):
    spc_alerts['state'] = 'normal'
    for log in logs:
        if spc_alerts.index('end-1c')!='1.0':
            spc_alerts.insert('end', '\n')
        spc_alerts.insert('end', log)
    spc_alerts['state'] = 'disabled'

def logfilter(log, filt = None):
    filtered_logs = []
    if filt == None or filt == ['','']:
        #Difault
        filtered_logs = log
        return filtered_logs

    for l in log:
        if len(filt) == 1:
            if filt[0] in l:
                filtered_logs.append(l)
        elif len(filt) == 2:
            if filt[0] in l and filt[1] in l:
                filtered_logs.append(l)

    return filtered_logs

def changeListener():
    # Use mds hashing to check for change in the data file so that we can update the program if there is a change 
    global hash
    newhash = hashlib.md5(open(file, "rb").read()).hexdigest()
    if hash != newhash:
        load(file) # If there is change in the file "reload" the file with new changes
        hash = newhash

    tk.after(100, changeListener)

def quit_prog(tk):
    tk.withdraw()
    tk.quit()

if __name__ == '__main__':
    # SPC alert tabs
    spc_alerts = Tk.Text(tk)
    yscrollbar1 = ttk.Scrollbar(tk, orient = 'vertical', command = spc_alerts.yview)
    spc_alerts['yscrollcommand'] = yscrollbar1.set
    spc_alerts.grid(column = 0, row = 0, sticky = 'nwes')
    yscrollbar1.grid(column = 1, row = 0, sticky = 'ns')
    tk.grid_columnconfigure(0, weight = 1)
    tk.grid_rowconfigure(0, weight = 1)
    spc_alerts.grid(column=0,row=0, sticky='nsew')

    display(logfilter(log_backend))
    filter_buttons = Tk.Frame(tk)
    spcrow = Tk.Frame(filter_buttons)
    graphrow = Tk.Frame(filter_buttons)

    spcrule = Tk.Label(spcrow, text="Filter by SPC RULE:").grid(row=0,column=0)
    button_r1 = Tk.Button(spcrow, text=f"Rule 1", command=lambda: changeFilter(log_backend, 0, f"Rule 1")).grid(row=0,column=1)
    button_r2 = Tk.Button(spcrow, text=f"Rule 2", command=lambda: changeFilter(log_backend, 0, f"Rule 2")).grid(row=0,column=2)
    button_r3 = Tk.Button(spcrow, text=f"Rule 3", command=lambda: changeFilter(log_backend, 0, f"Rule 3")).grid(row=0,column=3)
    button_r4 = Tk.Button(spcrow, text=f"Rule 4", command=lambda: changeFilter(log_backend, 0, f"Rule 4")).grid(row=0,column=4)
    button_r5 = Tk.Button(spcrow, text=f"Rule 5", command=lambda: changeFilter(log_backend, 0, f"Rule 5")).grid(row=0,column=5)
    button_r6 = Tk.Button(spcrow, text=f"Rule 6", command=lambda: changeFilter(log_backend, 0, f"Rule 6")).grid(row=0,column=6)
    button_r7 = Tk.Button(spcrow, text=f"Rule 7", command=lambda: changeFilter(log_backend, 0, f"Rule 7")).grid(row=0,column=7)
    button_r8 = Tk.Button(spcrow, text=f"Rule 8", command=lambda: changeFilter(log_backend, 0, f"Rule 8")).grid(row=0,column=8)
    button_spcall = Tk.Button(spcrow, text="ALL", command=lambda: changeFilter(log_backend, 0, '')).grid(row=0,column=9)
    spcrow.grid(row=0,column=0,sticky='nsew')

    graph = Tk.Label(graphrow, text="Filter by Graph:").grid(row=0,column=0)
    button_raw = Tk.Button(graphrow, text="RAW DATA", command=lambda: changeFilter(log_backend, 1, "RAW")).grid(row=0,column=1)
    button_a3 = Tk.Button(graphrow, text="MOV. AVERAGE 3", command=lambda: changeFilter(log_backend, 1, "A3")).grid(row=0,column=2)
    button_a5 = Tk.Button(graphrow, text="MOV. AVERAGE 5", command=lambda: changeFilter(log_backend, 1, "A5")).grid(row=0,column=3)
    button_a7 = Tk.Button(graphrow, text="MOV. AVERAGE 7", command=lambda: changeFilter(log_backend, 1, "A7")).grid(row=0,column=4)
    button_graphall = Tk.Button(graphrow, text="ALL", command=lambda: changeFilter(log_backend, 1, '')).grid(row=0,column=5)
    graphrow.grid(row=1,column=0,sticky='nsew')

    currentfilter = Tk.Label(filter_buttons, text="Current Filter: ['','']")
    currentfilter.grid(row=2,column=0,sticky='nsew')

    # button_load = Tk.Button(filter_buttons, text="Load File", command=lambda: changeFile()).grid(row=0,column=1)
    filter_buttons.grid(column=0,row=1, sticky='nsew')

    load(file)
    tk.after(2001, changeListener)
    
    Tk.mainloop()