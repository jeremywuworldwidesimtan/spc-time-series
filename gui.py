import spcmonitor, extendedmonitor, logsviewer
import customtkinter as Ctk

class mainD(Ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SPC Monitor")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.spcmon = spcmonitor.SpcMon()
        self.spcmon.grid(row=0, column=0, padx=12, pady=12)


if __name__ == '__main__':
    main = mainD()
    main.mainloop()