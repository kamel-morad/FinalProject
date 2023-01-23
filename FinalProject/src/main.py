import tkinter
import tkinter.messagebox
from tkinter import filedialog as fd
import os
import customtkinter

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):

    

    def select_file(self):
        filetypes = [("C files",".c")]
        filename= ''
        filename = fd.askopenfilename(title='Open a file',filetypes=filetypes)
        if not filename:
            tkinter.messagebox.showinfo(
            title='Selected File',
            message = "You Must Choose A File First!"
        )
            return
        else:
            filename = filename
            print (filename)
       


        tkinter.messagebox.showinfo(
            title='Selected File',
            message = "File has been selected successfully!"
        )

    def sidebar_button_event(self):
        cmdStr = "python3 engine.py --spec=spec.yaml --specDefine=define.h --input=example_code/example.c"
        os.system(cmdStr)
            
        
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Bug Detector")
        
        #self.geometry(f"{700}x{580}")
        self.geometry(f"{1000}x{700}")
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Bug Detection", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.labelName = customtkinter.CTkLabel(self.sidebar_frame,text="Powered By Rajih Gadban\nAnd Kamel Morad \nVersion 3.7.2", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.labelName.grid(row=5, column=0, padx=20, pady=(20, 10))

        
        self.main_button_1 = customtkinter.CTkButton(master=self, command=self.sidebar_button_event,fg_color="transparent", border_width=2,text="Start Fixing",text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.main_button_2 = customtkinter.CTkButton(master=self, command=self.select_file,fg_color="transparent", border_width=2,text="Upload Your File",text_color=("gray10", "#DCE4EE"))
        self.main_button_2.grid(row=3, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        
        # create textbox
        #self.label = customtkinter.CTkLabel(self, width=200,text="A bug fixing tool that can be adapted to\nYour processes to help you analyze and\nDetect bugs in your own code.",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label = customtkinter.CTkLabel(master=self, width=200,text="Never allow the same bug to bite you twice.",font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label.grid(row=1, column=1, padx=(0, 0), pady=(0, 0), sticky="nsew")

if __name__ == "__main__":
    app = App()
    app.mainloop()