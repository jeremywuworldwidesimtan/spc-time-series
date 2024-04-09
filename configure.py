import customtkinter as Ctk
import configparser, json

class App(Ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Configure SPC Engine")
        self.geometry("900x600")

        self.titleLabel = Ctk.CTkLabel(self, text="SPC Engine Config", font=(fond, 24), anchor='w')
        self.titleLabel.pack(expand=False, fill='both', padx=12, pady=12)
        self.settings = ScrollableSettings(self)
        self.settings.pack(expand=True, fill='both', padx=12)
        self.saveButton = Ctk.CTkButton(self, text='Save', height=24, command=self.save)
        self.saveButton.pack(expand=False, fill='both', padx=12, pady=12)

    def save(self):
        values = []
        validation = True
        for sec in self.winfo_children()[1].winfo_children()[0].winfo_children()[0].winfo_children():
            for wid in sec.winfo_children():
                try:
                    # print(wid.getData())
                    values.append(wid.getData())
                except:
                    pass

        # print(values)

        # Wtf m i doin here
        # List order
        # (0-17) [rate, toogle, filename, logname, prefix, generator, debug, seed, min, max, winsize, xlabel, ylabel, period, 1, 2, 3, 4]
        # (18-33) [r1s, r1c, r2s, r2c, r3s, r3c, r4s, r4c, r5s, r5c, r6s, r6c, r7s, r7c, r8s, r8c]
        try:
            # Type validation
            float(values[0])
            int(values[7])
            int(values[8])
            int(values[9])
            int(values[10])
            int(values[13])
            int(values[14])
            int(values[15])
            int(values[16])
            int(values[17])
        except:
            validation = False

        # Reuqire fields validation
        if (
            values[0].strip() == '' or
            values[10].strip() == '' or
            values[13].strip() == '' or 
            values[14].strip() == '' or 
            values[15].strip() == '' or 
            values[16].strip() == '' or 
            values[17].strip() == ''
        ):
            validation = False

        # Field validation for customfilename-related values if CFN is enabled
        if str(values[1]).lower() == 'true' and (values[2].strip() == '' or values[3].strip() == ''):
            validation = False
        
        # Field validation for prefix if CFN is disabled
        if str(values[1]).lower() == 'false' and (values[4].strip() == ''):
            validation = False

        # Field validation for generator-related values if generator is enabled
        if str(values[5]).lower() == 'true' and (values[7].strip() == '' or values[8].strip() == '' or values[9].strip() == ''):
            validation = False

        if validation:
            # SAVE
            conf.set('main', 'rate', values[0])
            conf.set('main', 'customfilename_toggle', str(values[1]).lower())
            conf.set('main', 'customfilename_data', values[2])
            conf.set('main', 'customfilename_log', values[3])
            conf.set('main', 'prefix', values[4])
            conf.set('generator', 'enable', str(values[5]).lower())
            conf.set('generator', 'deebaag', str(values[6]).lower())
            conf.set('generator', 'seed', values[7])
            conf.set('generator', 'min', values[8])
            conf.set('generator', 'max', values[9])
            conf.set('spcmain', 'winsize', values[10])
            conf.set('spcmain', 'xa_label', values[11])
            conf.set('spcmain', 'ya_label', values[12])
            conf.set('extendeddatamonitor', 'period_points', values[13])
            conf.set('extendeddatamonitor', 'p1', values[14])
            conf.set('extendeddatamonitor', 'p2', values[15])
            conf.set('extendeddatamonitor', 'p3', values[16])
            conf.set('extendeddatamonitor', 'p4', values[17])
            # SPC alerts settings
            conf.set('spcalerts', 'r1_severity', values[18])
            conf.set('spcalerts', 'r1_contact', values[19])
            conf.set('spcalerts', 'r2_severity', values[20])
            conf.set('spcalerts', 'r2_contact', values[21])
            conf.set('spcalerts', 'r3_severity', values[22])
            conf.set('spcalerts', 'r3_contact', values[23])
            conf.set('spcalerts', 'r4_severity', values[24])
            conf.set('spcalerts', 'r4_contact', values[25])
            conf.set('spcalerts', 'r5_severity', values[26])
            conf.set('spcalerts', 'r5_contact', values[27])
            conf.set('spcalerts', 'r6_severity', values[28])
            conf.set('spcalerts', 'r6_contact', values[29])
            conf.set('spcalerts', 'r7_severity', values[30])
            conf.set('spcalerts', 'r7_contact', values[31])
            conf.set('spcalerts', 'r8_severity', values[32])
            conf.set('spcalerts', 'r8_contact', values[33])

            # print({section: dict(conf[section]) for section in conf.sections()})
            with open('config.ini', 'w') as configfile:
                conf.write(configfile)

            print("Save successful")
        else:
            print("Save error. Make sure that the field values are valid and all the required fields are filled.")

class ScrollableSettings(Ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master=master)

        self.required = Ctk.CTkLabel(self, text="Settings marked with an asterisk (*) are required fields.", font=(fond, 22), anchor='w')
        self.required.pack(expand=True, fill='both', padx=12, pady=12)

        self.mainSec = MainSection(self)
        self.mainSec.pack(expand=True, fill='both', padx=12, pady=12)

        self.genSec = GenSection(self)
        self.genSec.pack(expand=True, fill='both', padx=12, pady=12)

        self.monSec = MonitorSection(self)
        self.monSec.pack(expand=True, fill='both', padx=12, pady=12)

        self.EDMSec = EDMSection(self)
        self.EDMSec.pack(expand=True, fill='both', padx=12, pady=12)

        self.alertSec = AlertSection(self)
        self.alertSec.pack(expand=True, fill='both', padx=12, pady=12)

class MainSection(Ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)

        self.secLabel = Ctk.CTkLabel(self, text="Main Settings", font=(fond, 36), anchor='w')
        self.secLabel.pack(expand=True, fill='both', padx=12, pady=12)

        self.rate = Settings_Label(self, settingName="Rate*", value=conf['main']['rate'], desc="Set the rate in which data comes in.")
        self.rate.pack(expand=True, fill='both', padx=12, pady=12)

        self.CFNToggle = Settings_Checkbox(self, settingName="Custom file names", mode=conf['main'].getboolean('customfilename_toggle'), desc="Whether or not to use custom file names for log files. Use this if you want to load your own data.")
        self.CFNToggle.pack(expand=True, fill='both', padx=12, pady=12)

        self.CFNLabel = Ctk.CTkLabel(self, text="* The following settings will only apply if the checkbox is ticked", font=(fond, 22), anchor='w')
        self.CFNLabel.pack(expand=True, fill='both', padx=12, pady=12)

        self.CFNDataFileName = Settings_Label(self, settingName="(CFN) Data file name*", value=conf['main']['customfilename_data'], desc="The custom name for the .csv data file.")
        self.CFNDataFileName.pack(expand=True, fill='both', padx=12, pady=12)

        self.CFNDataFileName = Settings_Label(self, settingName="(CFN) Log file name*", value=conf['main']['customfilename_log'], desc="The custom name for the log file.")
        self.CFNDataFileName.pack(expand=True, fill='both', padx=12, pady=12)

        self.prefLabel = Ctk.CTkLabel(self, text="* The following settings will only apply if the checkbox is unchecked", font=(fond, 22), anchor='w')
        self.prefLabel.pack(expand=True, fill='both', padx=12, pady=12)

        self.prefix = Settings_Label(self, settingName="Prefix*", value=conf['main']['prefix'], desc="The prefix for the data and log file. Format: {Prefix}-{Date and time}.csv/txt")
        self.prefix.pack(expand=True, fill='both', padx=12, pady=12)

class GenSection(Ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)

        self.secLabel = Ctk.CTkLabel(self, text="Data Generator Settings", font=(fond, 36), anchor='w')
        self.secLabel.pack(expand=True, fill='both', padx=12, pady=12)

        self.genToggle = Settings_Checkbox(self, settingName="Toggle data generator", mode=conf['generator'].getboolean('enable'), desc="Toggle the data generator to generate artifical data for testing.")
        self.genToggle.pack(expand=True, fill='both', padx=12, pady=12)

        self.debugToggle = Settings_Checkbox(self, settingName="Debug", mode=conf['generator'].getboolean('deebaag'), desc="Whether or not to debug the data generator by displaying the values generated in the CLI.")
        self.debugToggle.pack(expand=True, fill='both', padx=12, pady=12)

        self.seed = Settings_Label(self, settingName="Seed*", value=conf['generator']['seed'], desc="Set the seed for the data generator.")
        self.seed.pack(expand=True, fill='both', padx=12, pady=12)

        self.minValue = Settings_Label(self, settingName="Minimum value*", value=conf['generator']['min'], desc="Set the minimum value that can be generated from the data generator.")
        self.minValue.pack(expand=True, fill='both', padx=12, pady=12)

        self.maxValue = Settings_Label(self, settingName="Maximum value*", value=conf['generator']['max'], desc="Set the maximum value that can be generated from the data generator.")
        self.maxValue.pack(expand=True, fill='both', padx=12, pady=12)

class MonitorSection(Ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)

        self.secLabel = Ctk.CTkLabel(self, text="SPC Data Monitor Settings", font=(fond, 36), anchor='w')
        self.secLabel.pack(expand=True, fill='both', padx=12, pady=12)

        self.windowSize = Settings_Label(self, settingName="Window Size*", value=conf['spcmain']['winsize'], desc="Set the amount of values to show in the rolling window graph.")
        self.windowSize.pack(expand=True, fill='both', padx=12, pady=12)

        self.graphX = Settings_Label(self, settingName="X Label", value=conf['spcmain']['xa_label'], desc="Set the label for the X axis.")
        self.graphX.pack(expand=True, fill='both', padx=12, pady=12)       
        
        self.graphY = Settings_Label(self, settingName="Y Label", value=conf['spcmain']['ya_label'], desc="Set the label for the Y axis.")
        self.graphY.pack(expand=True, fill='both', padx=12, pady=12)

class EDMSection(Ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)

        self.secLabel = Ctk.CTkLabel(self, text="Extended Data Monitor Settings", font=(fond, 36), anchor='w')
        self.secLabel.pack(expand=True, fill='both', padx=12, pady=12)

        self.periodSize = Settings_Label(self, settingName="Period Size*", value=conf['extendeddatamonitor']['period_points'], desc="Set the size of a single period.")
        self.periodSize.pack(expand=True, fill='both', padx=12, pady=12)

        self.perLabel = Ctk.CTkLabel(self, text="Periods to show settings. Enter 0 if you need fewer than four graphs.", font=(fond, 22), anchor='w')
        self.perLabel.pack(expand=True, fill='both', padx=12, pady=12)

        self.per1 = Settings_Label(self, settingName="Periods to Show 1", value=conf['extendeddatamonitor']['p1'], desc="Set the number of periods to show in graph 1.")
        self.per1.pack(expand=True, fill='both', padx=12, pady=12)

        self.per2 = Settings_Label(self, settingName="Periods to Show 2", value=conf['extendeddatamonitor']['p2'], desc="Set the number of periods to show in graph 2.")
        self.per2.pack(expand=True, fill='both', padx=12, pady=12)

        self.per3 = Settings_Label(self, settingName="Periods to Show 3", value=conf['extendeddatamonitor']['p3'], desc="Set the number of periods to show in graph 3.")
        self.per3.pack(expand=True, fill='both', padx=12, pady=12)

        self.per4 = Settings_Label(self, settingName="Periods to Show 4", value=conf['extendeddatamonitor']['p4'], desc="Set the number of periods to show in graph 4.")
        self.per4.pack(expand=True, fill='both', padx=12, pady=12)

class AlertSection(Ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)

        severity_choices = ['Low Priority', 'Warning', 'Critical']
        usergroup_choices = list(ug.keys())

        self.secLabel = Ctk.CTkLabel(self, text="Alert Settings", font=(fond, 36), anchor='w')
        self.secLabel.pack(expand=True, fill='both', padx=12, pady=12)

        # Prefer looping but don't know how to properly implement these if I do loop
        self.r1Severity = Settings_Option(self, settingName="Severity of Rule 1", value=conf['spcalerts']['r1_severity'], optionsList=severity_choices, desc="Specify the severity/priority of SPC rule 1").pack(expand=True, fill='both', padx=12, pady=12)
        self.r1Contact = Settings_Option(self, settingName="Contact for Rule 1 violation", value=conf['spcalerts']['r1_contact'], optionsList=usergroup_choices, desc="Specify contact information in the event of rule 1 violation").pack(expand=True, fill='both', padx=12, pady=12)
        self.r2Severity = Settings_Option(self, settingName="Severity of Rule 2", value=conf['spcalerts']['r2_severity'], optionsList=severity_choices, desc="Specify the severity/priority of SPC rule 2").pack(expand=True, fill='both', padx=12, pady=12)
        self.r2Contact = Settings_Option(self, settingName="Contact for Rule 2 violation", value=conf['spcalerts']['r2_contact'], optionsList=usergroup_choices, desc="Specify contact information in the event of rule 2 violation").pack(expand=True, fill='both', padx=12, pady=12)
        self.r3Severity = Settings_Option(self, settingName="Severity of Rule 3", value=conf['spcalerts']['r3_severity'], optionsList=severity_choices, desc="Specify the severity/priority of SPC rule 3").pack(expand=True, fill='both', padx=12, pady=12)
        self.r3Contact = Settings_Option(self, settingName="Contact for Rule 3 violation", value=conf['spcalerts']['r3_contact'], optionsList=usergroup_choices, desc="Specify contact information in the event of rule 3 violation").pack(expand=True, fill='both', padx=12, pady=12)
        self.r4Severity = Settings_Option(self, settingName="Severity of Rule 4", value=conf['spcalerts']['r4_severity'], optionsList=severity_choices, desc="Specify the severity/priority of SPC rule 4").pack(expand=True, fill='both', padx=12, pady=12)
        self.r4Contact = Settings_Option(self, settingName="Contact for Rule 4 violation", value=conf['spcalerts']['r4_contact'], optionsList=usergroup_choices, desc="Specify contact information in the event of rule 4 violation").pack(expand=True, fill='both', padx=12, pady=12)
        self.r5Severity = Settings_Option(self, settingName="Severity of Rule 5", value=conf['spcalerts']['r5_severity'], optionsList=severity_choices, desc="Specify the severity/priority of SPC rule 5").pack(expand=True, fill='both', padx=12, pady=12)
        self.r5Contact = Settings_Option(self, settingName="Contact for Rule 5 violation", value=conf['spcalerts']['r5_contact'], optionsList=usergroup_choices, desc="Specify contact information in the event of rule 5 violation").pack(expand=True, fill='both', padx=12, pady=12)
        self.r6Severity = Settings_Option(self, settingName="Severity of Rule 6", value=conf['spcalerts']['r6_severity'], optionsList=severity_choices, desc="Specify the severity/priority of SPC rule 6").pack(expand=True, fill='both', padx=12, pady=12)
        self.r6Contact = Settings_Option(self, settingName="Contact for Rule 6 violation", value=conf['spcalerts']['r6_contact'], optionsList=usergroup_choices, desc="Specify contact information in the event of rule 6 violation").pack(expand=True, fill='both', padx=12, pady=12)
        self.r7Severity = Settings_Option(self, settingName="Severity of Rule 7", value=conf['spcalerts']['r7_severity'], optionsList=severity_choices, desc="Specify the severity/priority of SPC rule 7").pack(expand=True, fill='both', padx=12, pady=12)
        self.r7Contact = Settings_Option(self, settingName="Contact for Rule 7 violation", value=conf['spcalerts']['r7_contact'], optionsList=usergroup_choices, desc="Specify contact information in the event of rule 7 violation").pack(expand=True, fill='both', padx=12, pady=12)
        self.r8Severity = Settings_Option(self, settingName="Severity of Rule 8", value=conf['spcalerts']['r8_severity'], optionsList=severity_choices, desc="Specify the severity/priority of SPC rule 8").pack(expand=True, fill='both', padx=12, pady=12)
        self.r8Contact = Settings_Option(self, settingName="Contact for Rule 8 violation", value=conf['spcalerts']['r8_contact'], optionsList=usergroup_choices, desc="Specify contact information in the event of rule 8 violation").pack(expand=True, fill='both', padx=12, pady=12)

class Settings_Label(Ctk.CTkFrame):
    def __init__(self, master, settingName, value, desc = ''):
        super().__init__(master=master, fg_color="transparent")

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)

        self.setLabel = Ctk.CTkLabel(self, text=settingName, font=(fond, 22))
        self.setLabel.grid(row=0, column=0, sticky='w')

        if desc:
            self.setDesc = Ctk.CTkLabel(self, text=desc, font=("Segoe UI", 14))
            self.setDesc.grid(row=1, column=0, sticky='w', columnspan=2)

        self.valueEntry = Ctk.CTkEntry(self)
        self.valueEntry.insert('0', value)
        self.valueEntry.grid(row=0, column=1, padx=12, sticky='e')

    def getData(self):
        return self.valueEntry.get()
    
class Settings_Checkbox(Ctk.CTkFrame):
    def __init__(self, master, settingName, mode, desc = ''):
        super().__init__(master=master, fg_color="transparent")

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)

        self.setLabel = Ctk.CTkLabel(self, text=settingName, font=(fond, 22))
        self.setLabel.grid(row=0, column=0, sticky='w')

        if desc:
            self.setDesc = Ctk.CTkLabel(self, text=desc, font=("Segoe UI", 14))
            self.setDesc.grid(row=1, column=0, sticky='w', columnspan=2)

        self.valueEntry = Ctk.CTkCheckBox(self, text='')
        self.valueEntry.grid(row=0, column=1, sticky='e')

        if mode:
            self.valueEntry.select()
        else:
            self.valueEntry.deselect()

    def getData(self):
        return True if self.valueEntry.get() == 1 else False

class Settings_Option(Ctk.CTkFrame):
    def __init__(self, master, settingName, value, optionsList, desc = ''):
        super().__init__(master=master, fg_color="transparent")

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)

        self.setLabel = Ctk.CTkLabel(self, text=settingName, font=(fond, 22))
        self.setLabel.grid(row=0, column=0, sticky='w')

        if desc:
            self.setDesc = Ctk.CTkLabel(self, text=desc, font=("Segoe UI", 14))
            self.setDesc.grid(row=1, column=0, sticky='w', columnspan=2)

        self.valueEntry = Ctk.CTkOptionMenu(self, values=optionsList)
        if value in optionsList:
            self.valueEntry.set(value)
        else:
            self.valueEntry.set(optionsList[0])
        self.valueEntry.grid(row=0, column=1, padx=12, sticky='e')

    def getData(self):
        return self.valueEntry.get()

if __name__ == '__main__':
    with open('usergroups.json') as f:
        ug = json.load(f)
    
    conf = configparser.ConfigParser()
    conf.read('config.ini')

    fond = "Segoe UI Bold"

    root = App()
    root.mainloop()
