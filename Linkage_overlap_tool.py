import customtkinter
from tkinter import *
from tkinter import filedialog, messagebox
import pandas as pd
import openpyxl 
import finding_genes_module as fg
import os
from threading import Thread



class GenerateTable(Thread):
    def __init__(self, gene_list, overlap, linkage, output_file):
        super().__init__()
        self.gene_list = gene_list
        self.overlap = overlap
        self.linkage = linkage
        self.output_file_path = output_file

    def run(self):
        db_location = os.path.join(os.getcwd(),"SGD.csv")
        SGD_database = pd.read_csv(db_location, index_col=0)
        Final_data_table = pd.DataFrame()  
        overlapping_genes = pd.DataFrame()  
        linkage_genes = pd.DataFrame()  
            
        for gene in self.gene_list:   
            if gene in SGD_database[['Standard Name']].values:
                column = 'Standard Name'
            elif gene in SGD_database[['Systematic Name']].values:
                column = 'Systematic Name'
            else:
                print(f"This gene is not present in SGD database: {gene}")
            if len(column) != 0:
                gene_start, gene_end, gene_chromosome = fg.info_genes(SGD_database, gene, column)
                if self.overlap == 1:
                    overlapping_genes = fg.finding_overlapping_genes(SGD_database, gene,gene_start,gene_end,gene_chromosome)
                if self.linkage == 1:
                    linkage_genes = fg.list_of_nearest_genes(SGD_database, gene,gene_start,gene_end,gene_chromosome)
                All_temp = [overlapping_genes, linkage_genes]
                All_data = pd.concat(All_temp).drop_duplicates(subset=['Systematic Name'])
                Final_data_table_temp = [Final_data_table, All_data]
                Final_data_table = pd.concat(Final_data_table_temp)

        Final_data_table.to_csv(self.output_file_path, index=False)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("dark-blue")
          
        self.title("Linkage & Overlap tool")
        self.width = 800
        self.height = 650
        self.resizable(False, False)
        self.screen_width = self.winfo_screenwidth()
        self.screen_heigth = self.winfo_screenheight()

        self.x_offset = (self.screen_width/2) - (self.width/2)
        self.y_offset = (self.screen_heigth/2) - (self.height/2)
        self.geometry("%dx%d+%d+%d" % (self.width, self.height, self.x_offset, self.y_offset))
        
        self.base_frame = customtkinter.CTkFrame(self)
        self.base_frame.pack()

        self.create_head_frame()
        self.create_input_frame()
        self.create_search_method_frame()
        self.create_output_frame()
        self.create_footer_frame()

    def create_head_frame(self):

        self.head_frame = customtkinter.CTkFrame(master=self.base_frame)
        self.head_frame.grid(row=0, column=0, padx=10, pady=10)

        self.title = customtkinter.CTkLabel(self.head_frame, text="Linkage & Overlap Tool")
        self.title.grid(row=0, column=0)

        self.theme_switch_var = customtkinter.StringVar(value="on")
        self.theme_switch = customtkinter.CTkSwitch(self.head_frame, text="Dark Mode", command=self.theme_switch_toogle, variable=self.theme_switch_var, onvalue="on", offvalue="off")
        self.theme_switch.grid(row=0, column=3, padx=50)

    def create_input_frame(self):

        self.input_type_frame = customtkinter.CTkFrame(master=self.base_frame)
        self.input_type_frame.grid(row=1, column=0, padx=10, pady=10)

        self.input_type_rb_val = customtkinter.StringVar(value = "file")
        self.input_file_path = customtkinter.StringVar()

        self.input_from_file_rb = customtkinter.CTkRadioButton(self.input_type_frame, text="Load Excel Table", variable=self.input_type_rb_val, value="file", command= self.gene_list_type)
        self.input_from_text_rb = customtkinter.CTkRadioButton(self.input_type_frame, text="Text", variable=self.input_type_rb_val, value="text", command= self.gene_list_type)

        self.input_from_file_rb.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.input_from_text_rb.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.input_file_location = customtkinter.CTkEntry(self.input_type_frame, state="disabled", width = 400, textvariable=self.input_file_path)
        self.open_filedialog_btn = customtkinter.CTkButton(self.input_type_frame,text='Choose a File', command=self.select_file)
        self.text_input = customtkinter.CTkTextbox(self.input_type_frame, state="disabled" ,wrap = WORD, width = 400, height = 200, font = ("Times New Roman",15))

        self.input_file_location.grid(row=0, column=1, padx=5, pady=5)
        self.open_filedialog_btn.grid(row=0, column=2, sticky="e", padx=(5,10), pady=5)
        self.text_input.grid(row=1, column=1, padx=5, pady=5)

    def create_search_method_frame(self):

        self.search_method_frame = customtkinter.CTkFrame(master=self.base_frame)
        self.search_method_frame.grid(row=2, column=0, padx=10, pady=10)

        self.link_var = customtkinter.IntVar()
        self.overlap_var = customtkinter.IntVar()

        self.linkage_checkbox = customtkinter.CTkCheckBox(self.search_method_frame, text = "Linkage", variable = self.link_var, onvalue = 1, offvalue = 0)
        self.overlapping_checkbox = customtkinter.CTkCheckBox(self.search_method_frame, text = "Overlapping genes", variable = self.overlap_var, onvalue = 1, offvalue = 0)
        
        self.linkage_checkbox.grid(row=0, column=0)
        self.overlapping_checkbox.grid(row=0, column=1)

    def create_output_frame(self):    

        self.file_saving_frame = customtkinter.CTkFrame(master=self.base_frame)
        self.file_saving_frame.grid(row=3, column=0, padx=10, pady=10)

        self.output_file_name = customtkinter.StringVar()
        self.output_file_path = customtkinter.StringVar()

        self.save_file_to_label = customtkinter.CTkLabel(self.file_saving_frame, text="Save to", font = ("Calibri",12))
        self.file_saving_path = customtkinter.CTkEntry(self.file_saving_frame, width = 400, state="disabled", textvariable=self.output_file_path)
        self.save_to_btn= customtkinter.CTkButton(self.file_saving_frame, text= "Save to", command= self.path_file)
        self.output_file_name_label = customtkinter.CTkLabel(self.file_saving_frame, text="Output file name", font = ("Calibri",12))
        self.file_name = customtkinter.CTkEntry(self.file_saving_frame, width = 400, state="normal", textvariable=self.output_file_name)
        
        self.save_file_to_label.grid(row=0, column=0, padx=10, pady=10)
        self.file_saving_path.grid(row=0, column=1, padx=10, pady=10)
        self.save_to_btn.grid(row=0, column=2, padx=10, pady=10)
        self.output_file_name_label.grid(row=1, column=0, padx=10, pady=10)
        self.file_name.grid(row=1, column=1, padx=10, pady=10)

    def create_footer_frame(self):  

        self.footer_frame = customtkinter.CTkFrame(master=self.base_frame)
        self.footer_frame.grid(row=4, column=0, padx=10, pady=10)

        self.run_btn = customtkinter.CTkButton(self.footer_frame, text= "Run", command= self.generate_table)
        self.progress_bar = customtkinter.CTkProgressBar(self.footer_frame, orientation='horizontal' ,mode='indeterminate')

        self.run_btn.grid(row=0, column=1)
    
    def gene_list_type(self):
        if self.input_type_rb_val.get() == 'text':
            self.open_filedialog_btn.configure(state= "disabled")
            self.text_input.configure(state= "normal")
        elif self.input_type_rb_val.get() == 'file':
            self.text_input.configure(state= "disabled")
            self.open_filedialog_btn.configure(state= "normal")

    def select_file(self):
        filetypes = (('xlsx files','*.xlsx'),('csv files','*.csv'),('xls files', '*.xls'))
        filename = filedialog.askopenfilename(title='Open a file',initialdir='/',filetypes=filetypes)
        self.input_file_path.set(filename)
        self.input_file_location.delete(0,END)
        self.input_file_location.insert(0,self.input_file_path)

    def path_file(self):
        output_path = filedialog.askdirectory()
        self.output_file_path.set(output_path)
        self.file_saving_path.delete(0,END)
        self.file_saving_path.insert(0,self.output_file_path)

    def get_genes_from_file(self, input_file_path):
        gene_list_df = pd.read_excel(input_file_path)
        gene_list = gene_list_df['Gene'].str.upper().tolist()
        return gene_list
 
    def clear_UI(self):
        self.run_btn.configure(state="normal")
        self.input_type_rb_val.set("file")
        self.input_file_path.set("")
        self.open_filedialog_btn.configure(state="normal")
        self.text_input.delete('1.0', END)
        self.text_input.configure(state="disabled")
        self.link_var.set(0)
        self.overlap_var.set(0)
        self.output_file_path.set("")
        self.output_file_name.set("")

    def monitor(self, thread):
        if thread.is_alive():
            self.after(100, lambda: self.monitor(thread))
        else:
            self.progress_bar.stop()
            self.progress_bar.grid_forget()
            messagebox.showinfo(title="Progress", message="Done! File has been saved!")
            self.clear_UI()

    def generate_table(self):  

        
        self.progress_bar.grid(row=1, column=1, padx=10, pady=10)
        self.progress_bar.start()
        
        if self.input_type_rb_val.get() == 'text':
            text_input = self.text_input.get('1.0',END).upper()
            text_input_temp = ''.join(text_input.splitlines())
            gene_list = text_input_temp.split(',')   
        elif self.input_type_rb_val.get() == 'file':
            gene_list = self.get_genes_from_file(self.input_file_path.get())
        
        output_file = os.path.join(self.output_file_path.get(), f"{self.output_file_name.get()}.csv")
        generate_table_thread = GenerateTable(gene_list, self.overlap_var.get(), self.link_var.get(), output_file)
        generate_table_thread.start()
        self.monitor(generate_table_thread)

    def theme_switch_toogle(self):
        if self.theme_switch_var.get() == "on":
            customtkinter.set_appearance_mode("dark")
            customtkinter.set_default_color_theme("dark-blue")
        elif self.theme_switch_var.get() == "off":
            customtkinter.set_appearance_mode("light")
            customtkinter.set_default_color_theme("blue")

if __name__=="__main__":
    app = App()
    app.mainloop()