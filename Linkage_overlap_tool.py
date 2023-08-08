from tkinter import *
from tkinter import ttk,scrolledtext,filedialog, messagebox
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

class App(Tk):
    def __init__(self):
        super().__init__()

        self.title("Linkage&Overlap tool")
        self.width = 800
        self.height = 800
        self.screen_width = self.winfo_screenwidth()
        self.screen_heigth = self.winfo_screenheight()

        self.x_offset = (self.screen_width/2) - (self.width/2)
        self.y_offset = (self.screen_heigth/2) - (self.height/2)
        self.geometry("%dx%d+%d+%d" % (self.width, self.height, self.x_offset, self.y_offset))

        self.radio_btn_val = StringVar(value = "file")
        self.input_file_path = StringVar()
        self.output_file_name = StringVar()
        self.output_file_path = StringVar()
        self.link_var = IntVar()
        self.overlap_var = IntVar()

        self.headline = Label(self, text="Welcome to Linkage&Overlap genes tool", font = ("Calibri",20, "bold"))
        self.headline_note = Label(self, text="This program is using SGD database downloaded on 2/6/2023 ", font = ("Calibri",13))
        self.input_headline = Label(self, text="Input", font = ("Calibri",17, "bold"))
        self.input_note = Label(self, text="Table input: all gene must be under the column name 'Gene' ; Text input: all genes must be separated by a comma", font = ("Calibri",10), fg = "#ff3333")
        self.gene_file_rb = Radiobutton(self, text="Load Excel Table", variable=self.radio_btn_val, value="file", command= self.gene_list_type)
        self.gene_text_rb = Radiobutton(self, text="Text", variable=self.radio_btn_val, value="text", command= self.gene_list_type)
        self.input_location = Entry(self, state="disabled", width = 60, textvariable=self.input_file_path)
        self.open_button = ttk.Button(self,text='Open a File', command=self.select_file)
        self.text_area = scrolledtext.ScrolledText(self, state="disabled", wrap = WORD, width = 36, height = 10, font = ("Times New Roman",15))
        self.first_separator = ttk.Separator(self, orient='horizontal')
        self.method_headline = Label(self, text="Search Method", font = ("Calibri",17, "bold"))
        self.method_note = Label(self, text="At least one of the search methods options must be selected", font = ("Calibri",10), fg = "#ff3333")
        self.linkage_box = Checkbutton(self, text = "Linkage", variable = self.link_var, onvalue = 1, offvalue = 0)
        self.overlapping_box = Checkbutton(self, text = "Overlapping genes", variable = self.overlap_var, onvalue = 1, offvalue = 0)
        self.second_separator = ttk.Separator(self, orient='horizontal')
        self.output_headline = Label(self, text="Output", font = ("Calibri",17, "bold"))
        self.output_note = Label(self, text="Choose file name and location for your result file", font = ("Calibri",10), fg = "#ff3333")
        self.output_location_label = Label(self, text="Output location", font = ("Calibri",12))
        self.output_location = Entry(self, width = 60, state="disabled", textvariable=self.output_file_path)
        self.output_btn= Button(self, text= "Output location", command= self.path_file)
        self.output_file_name_label = Label(self, text="Output file name", font = ("Calibri",12))
        self.file_name = Entry(self, width = 60, state="normal", textvariable=self.output_file_name)
        self.run_btn = Button(self, width = 10, height = 2, text= "Run", command= self.generate_table)
        self.progress_bar = ttk.Progressbar(self, orient='horizontal' ,mode='indeterminate')
        

        self.headline.place(x=200, y=5)
        self.headline_note.place(x=200, y=40)
        self.input_headline.place(x=5, y=65)
        self.input_note.place(x=5, y=95)
        self.gene_file_rb.place(x=20, y=130)
        self.gene_text_rb.place(x=20, y=170)
        self.input_location.place(x=250, y=135)
        self.open_button.place(x=625, y=132)
        self.text_area.place(x=250, y=180)
        self.first_separator.place(x=0, y=415, relwidth=1)
        self.method_headline.place(x=5, y=420)
        self.method_note.place(x=5, y=450)
        self.linkage_box.place(x=150, y=470)
        self.overlapping_box.place(x=10, y=470)
        self.second_separator.place(x=0, y=540, relwidth=1)
        self.output_headline.place(x=5, y=550)
        self.output_note.place(x=5, y=580)
        self.output_location_label.place(x=30, y=610)
        self.output_location.place(x=250, y=610)
        self.output_btn.place(x=625, y=605)
        self.output_file_name_label.place(x=30, y=640)
        self.file_name.place(x=250, y=640)
        self.run_btn.place(x=400, y=700)
        
        
    def gene_list_type(self):
        if self.radio_btn_val.get() == 'text':
            self.open_button.config(state= "disabled")
            self.text_area.config(state= "normal")
        elif self.radio_btn_val.get() == 'file':
            self.text_area.config(state= "disabled")
            self.open_button.config(state= "normal")

    def select_file(self):
        filetypes = (('xlsx files','*.xlsx'),('csv files','*.csv'),('xls files', '*.xls'))
        filename = filedialog.askopenfilename(title='Open a file',initialdir='/',filetypes=filetypes)
        self.input_file_path.set(filename)
        self.input_location.delete(0,END)
        self.input_location.insert(0,self.input_file_path)

    def path_file(self):
        output_path = filedialog.askdirectory()
        self.output_file_path.set(output_path)
        self.output_location.delete(0,END)
        self.output_location.insert(0,self.output_file_path)

    def get_genes_from_file(self, input_file_path):
        print(input_file_path)
        gene_list_df = pd.read_excel(input_file_path)
        gene_list = gene_list_df['Gene'].str.upper().tolist()
        return gene_list
 
    def clear(self):
        self.run_btn.config(state="normal")
        self.radio_btn_val.set("file")
        self.input_file_path.set("")
        self.open_button.config(state="normal")
        self.text_area.delete('1.0', END)
        self.text_area.config(state="disabled")
        self.link_var.set(0)
        self.overlap_var.set(0)
        self.output_file_path.set("")
        self.output_file_name.set("")

    def monitor(self, thread):
        if thread.is_alive():
            # check the thread every 100ms
            self.after(100, lambda: self.monitor(thread))
        else:
            self.progress_bar.stop()
            self.progress_bar.place_forget()
            messagebox.showinfo(title="Progress", message="Done! File has been saved!")
            self.clear()

    def generate_table(self):  
        
        self.progress_bar.place(x=390, y=670)
        self.progress_bar.start()
        
        if self.radio_btn_val.get() == 'text':
            text_input = self.text_area.get('1.0',END).upper()
            text_input_temp = ''.join(text_input.splitlines())
            gene_list = text_input_temp.split(',')
            
        elif self.radio_btn_val.get() == 'file':
            gene_list = self.get_genes_from_file(self.input_file_path.get())
        
        output_file = os.path.join(self.output_file_path.get(), f"{self.output_file_name.get()}.csv")

        generate_table_thread = GenerateTable(gene_list, self.overlap_var.get(), self.link_var.get(), output_file)
        generate_table_thread.start()
        self.monitor(generate_table_thread)

if __name__=="__main__":
    app=App()
    app.mainloop()