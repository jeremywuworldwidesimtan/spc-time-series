import hashlib, sys
import customtkinter as Ctk
from tkinter import filedialog

class RuleFilterButtons(Ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs) # Apparently you need to have parenthesis after super for the class to work
            
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        self.spcrule = Ctk.CTkLabel(self, text="Filter by SPC RULE:").grid(row=0,column=0,rowspan=2)
        self.button_r1 = Ctk.CTkButton(self, text=f"Rule 1", command=lambda: changeFilter(log_backend, 0, f"Rule 1")).grid(row=0,column=1)
        self.button_r2 = Ctk.CTkButton(self, text=f"Rule 2", command=lambda: changeFilter(log_backend, 0, f"Rule 2")).grid(row=0,column=2)
        self.button_r3 = Ctk.CTkButton(self, text=f"Rule 3", command=lambda: changeFilter(log_backend, 0, f"Rule 3")).grid(row=0,column=3)
        self.button_r4 = Ctk.CTkButton(self, text=f"Rule 4", command=lambda: changeFilter(log_backend, 0, f"Rule 4")).grid(row=0,column=4)
        self.button_r5 = Ctk.CTkButton(self, text=f"Rule 5", command=lambda: changeFilter(log_backend, 0, f"Rule 5")).grid(row=1,column=1)
        self.button_r6 = Ctk.CTkButton(self, text=f"Rule 6", command=lambda: changeFilter(log_backend, 0, f"Rule 6")).grid(row=1,column=2)
        self.button_r7 = Ctk.CTkButton(self, text=f"Rule 7", command=lambda: changeFilter(log_backend, 0, f"Rule 7")).grid(row=1,column=3)
        self.button_r8 = Ctk.CTkButton(self, text=f"Rule 8", command=lambda: changeFilter(log_backend, 0, f"Rule 8")).grid(row=1,column=4)
        self.button_spcall = Ctk.CTkButton(self, text="ALL", command=lambda: changeFilter(log_backend, 0, '')).grid(row=0,column=9,rowspan=2, sticky='ns')

class GraphFilterButtons(Ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)
            
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        self.graph = Ctk.CTkLabel(self, text="Filter by Graph:").grid(row=0,column=0,rowspan=2)
        self.button_raw = Ctk.CTkButton(self, text="RAW DATA", command=lambda: changeFilter(log_backend, 1, "RAW")).grid(row=0,column=1)
        self.button_a3 = Ctk.CTkButton(self, text="MOV. AVERAGE 3", command=lambda: changeFilter(log_backend, 1, "A3")).grid(row=0,column=2)
        self.button_a5 = Ctk.CTkButton(self, text="MOV. AVERAGE 5", command=lambda: changeFilter(log_backend, 1, "A5")).grid(row=1,column=1)
        self.button_a7 = Ctk.CTkButton(self, text="MOV. AVERAGE 7", command=lambda: changeFilter(log_backend, 1, "A7")).grid(row=1,column=2)
        self.button_graphall = Ctk.CTkButton(self, text="ALL", command=lambda: changeFilter(log_backend, 1, '')).grid(row=0,column=3,rowspan=2,sticky='ns')

class SeverityFilterButtons(Ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)
            
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        self.graph = Ctk.CTkLabel(self, text="Filter by Severity:").grid(row=0,column=0)
        self.button_raw = Ctk.CTkButton(self, text="LOW PRIORITY", command=lambda: changeFilter(log_backend, 2, "Low Priority")).grid(row=0,column=1)
        self.button_a3 = Ctk.CTkButton(self, text="WARNING", command=lambda: changeFilter(log_backend, 2, "Warning")).grid(row=0,column=2)
        self.button_a5 = Ctk.CTkButton(self, text="CRITICAL", command=lambda: changeFilter(log_backend, 2, "Critical")).grid(row=0,column=3)
        self.button_graphall = Ctk.CTkButton(self, text="ALL", command=lambda: changeFilter(log_backend, 2, '')).grid(row=0,column=4)

class FilterButtons(Ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)
            
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        self.spcFilter = RuleFilterButtons(self)
        self.spcFilter.grid(row=0,column=0,sticky='nsew')

        self.graphFilter = GraphFilterButtons(self)
        self.graphFilter.grid(row=1,column=0,sticky='nsew')

        self.severityFilter = SeverityFilterButtons(self)
        self.severityFilter.grid(row=2,column=0,sticky='nsew')

        self.currentfilter = Ctk.CTkLabel(self, text="Current Filter: ['','']", font=(fond, 14))
        self.currentfilter.grid(row=3,column=0,sticky='nsew')

class SpcLogs(Ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)
            
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        # create scrollable alertbox
        self.alerts = Ctk.CTkTextbox(self, activate_scrollbars=False, font=(fond, 16))
        self.alerts.grid(row=0, column=0, sticky="nsew")

        # create CTk scrollbar
        self.scrollbar = Ctk.CTkScrollbar(self, command=self.alerts.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # connect alertbox scroll event to CTk scrollbar
        self.alerts.configure(yscrollcommand=self.scrollbar.set)

class LogViewer(Ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SPC Logs Viewer")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.titleLabel = Ctk.CTkLabel(self, text="SPC Alerts Viewer", font=(fond_bold, 24), anchor='w')
        self.titleLabel.pack(expand=False, fill='both', padx=12, pady=12)

        self.spcLogs = SpcLogs(self)
        self.spcLogs.pack(expand=True, fill='both', padx=12, pady=12)

        self.filterButtons = FilterButtons(self)
        self.filterButtons.pack(expand=False, fill='both', padx=12, pady=12)

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
    if filterPos in range(3):
        filter[filterPos] = filterKw
    
    lv.winfo_children()[2].winfo_children()[3].configure(text = f"Current Filter: {filter[0]} {filter[1]} {filter[2]}" if filter != ['','',''] else f"Current Filter: None")
    refresh_display(logfilter(logs, filter))

def refresh_display(logs):
    global alertbox
    try:
        alertbox.configure(state='normal')
        alertbox.delete('1.0', 'end')
        alertbox.configure(state='disabled')
        display(logs)
    except:
        display(logs)

def display(logs):
    alertbox.configure(state='normal')
    for log in logs:
        if alertbox.index('end-1c')!='1.0':
            alertbox.insert('end', '\n')
        alertbox.insert('end', log)
    alertbox.configure(state='disabled')

def logfilter(log, filt = None):
    filtered_logs = []
    if filt == None or filt == ['','','']:
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
        elif len(filt) == 3:
            if filt[0] in l and filt[1] in l and filt[2] in l:
                filtered_logs.append(l)

    return filtered_logs

def changeListener():
    # Use mds hashing to check for change in the data file so that we can update the program if there is a change 
    global hash
    newhash = hashlib.md5(open(file, "rb").read()).hexdigest()
    if hash != newhash:
        load(file) # If there is change in the file "reload" the file with new changes
        hash = newhash

    lv.after(100, changeListener)

def quit_prog(tk):
    tk.withdraw()
    tk.quit()

if __name__ == '__main__':
    hash = ""

    if (len(sys.argv) < 2): # second argv is name of file
        file = filedialog.askopenfilename()
        # file = "tesst.txt"
    else:
        file = sys.argv[1]

    log_backend = []
    filter = ['','','']

    fond = "Segoe UI"
    fond_bold = "Segoe UI Bold"
    lv = LogViewer()
    alertbox = lv.winfo_children()[1].winfo_children()[0] # Targets the SPC alerts textbox

    display(logfilter(log_backend))

    load(file)
    lv.after(1, lambda: changeFilter(log_backend, 0, ''))
    lv.after(2001, changeListener)
    
    lv.mainloop()