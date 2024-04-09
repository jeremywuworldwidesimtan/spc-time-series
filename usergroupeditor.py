import customtkinter as Ctk
import json

class UGEditor(Ctk.CTk):
    def __init__(self):
        super().__init__()
        usergroups_list = list(ug.keys())
        usergroups_list.append("New Group")
        prev_ug = ""

        self.title("Configure Usergroups")

        self.titleLabel = Ctk.CTkLabel(self, text="Usergroups Config", font=("Segoe UI Bold", 24), anchor='w')
        self.titleLabel.pack(expand=False, fill='both', padx=12, pady=12)

        self.usergroupOption = Ctk.CTkOptionMenu(self, values=usergroups_list, command=self.usergroupLoad)
        self.usergroupOption.pack(expand=False, fill='both', padx=12, pady=12)

        self.usergroupEdit = UGTextBox(self)
        self.usergroupEdit.pack(expand=False, fill='both', padx=12, pady=12)
        self.usergroupLoad(usergroups_list[0]) # init
        prev_ug = self.usergroupOption.get()

    def usergroupLoad(self, c):
        self.usergroupEdit.load(ug[c])
        for g in ug.keys():
            self.save(g)

    def save(self, c):
        usergroup_text = self.usergroupEdit.winfo_children()[0].get('1.0', 'end')
        print(usergroup_text)
        ug[c] = usergroup_text.split('\n')
        print(ug)

class UGTextBox(Ctk.CTkFrame):
    # To display and allow users to edit usergroups
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)
            
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        # create scrollable alertbox
        self.textbox = Ctk.CTkTextbox(self, activate_scrollbars=False, font=("Segoe UI", 16))
        self.textbox.grid(row=0, column=0, sticky="nsew")

        # create CTk scrollbar
        self.scrollbar = Ctk.CTkScrollbar(self, command=self.textbox.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # connect alertbox scroll event to CTk scrollbar
        self.textbox.configure(yscrollcommand=self.scrollbar.set)

    def load(self, userlist):
        try:
            self.textbox.delete('1.0', 'end')
            self.populateData(userlist)
        except:
            self.populateData(userlist)

    def populateData(self, userList):
        for u in userList:
            if self.textbox.index('end-1c')!='1.0':
                self.textbox.insert('end', '\n')
            self.textbox.insert('end', u)

if __name__ == '__main__':
    # LOAD USERGROUP JASON
    with open('usergroups.json') as f:
        ug = json.load(f)

    uge = UGEditor()
    uge.mainloop()