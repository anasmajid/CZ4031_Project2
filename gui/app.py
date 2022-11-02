import sys
import json
import argparse
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter.font import Font
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
# from query_description import 
# from pyconnect import DBConnection


class App(object):

    def __init__(self,parent):
        self.root = parent
        self.root.title("Query Plan Analyser")

        title_label_1 = tk.Label(root, 
		 text="CONNECTION",
		 fg = "black",
         bg= "#ECEEEF",
		 font= ("Helvetica",12, "bold"), pady =10, padx = 20)
        title_label_1.grid(row=0,column=0,columnspan=1)
        
        #Host
        host_text = StringVar()
        host_label = tk.Label(root,text="Host", font= ("bold",11),pady=10,padx=20)
        host_label.grid(row=1,column=0,sticky=W)
        self.host_entry = tk.Entry(root,textvariable=host_text)
        self.host_entry.grid(row=1,column=1)
        
        #Username
        username_text = StringVar()
        username_label = tk.Label(root,text="Username", font= ("bold",11),pady=10,padx=20)
        username_label.grid(row=1,column=2,sticky=W)
        self.username_entry = tk.Entry(root,textvariable=username_text)
        self.username_entry.grid(row=1,column=3)
        
        #Port
        port_text = StringVar()
        port_label = tk.Label(root,text="Port", font= ("bold",11),pady=10,padx=20)
        port_label.grid(row=2,column=0,sticky=W)
        self.port_entry = tk.Entry(root,textvariable=port_text)
        self.port_entry.grid(row=2,column=1)

        #Password
        password_text = StringVar()
        password_label = tk.Label(root,text="Password", font= ("bold",11),pady=10,padx=20)
        password_label.grid(row=2,column=2,sticky=W)
        self.password_entry = tk.Entry(root,textvariable=password_text)
        self.password_entry.grid(row=2,column=3)

        #DBname
        dbName_text = StringVar()
        dbName_label = tk.Label(root,text="DBname", font= ("bold",11),pady=10,padx=20)
        dbName_label.grid(row=3,column=0,sticky=W)
        self.dbName_entry = tk.Entry(root,textvariable=dbName_text)
        self.dbName_entry.grid(row=3,column=1)
        
        #connnectButton
        connectButton = tk.Button(root, 
                   text="Connect", font = ("bold",12), 
                   command=self.connect, borderwidth = 0, bg="#96AB9C", fg="white", height = 1, width=14)
        connectButton.grid(row=3,column=3,sticky=W,padx=20, columnspan=1)

        #Input query box
        title_label_2 = tk.Label(root, 
		 text="INPUT QUERY",
		 fg = "black",
         bg= "#ECEEEF",
		 font= ("Helvetica",12, "bold"), pady =10, padx = 20)
        title_label_2.grid(row=4,column=0,columnspan=1)

        self.inputQueryText = tk.Text(root, width=40, height=7,padx=20)
        self.inputQueryText.grid(row=5,column=0,padx=20,columnspan=3,rowspan = 2)

        #side buttons "Execute" and "clear" for input querybox
        #connnectButton
        executeButton = tk.Button(root, 
                   text="Execute", font = ("bold",12), 
                   command=self.connect, borderwidth = 0, bg="#96AB9C", fg="white", height = 2, width=15)
        executeButton.grid(row=5,column=3,sticky=W,padx=20, pady =8, columnspan=1)
        
        #clearButton
        clearButton = tk.Button(root, 
                   text="Clear", font = ("bold",12), 
                   command=self.clearInput, borderwidth = 0, bg="#96AB9C", fg="white", height = 2, width=15)
        clearButton.grid(row=6,column=3,sticky=W,padx=20, pady=8, columnspan=1)


        #Query execution plan Output
        title_label_c = tk.Label(root, text="QUERY PLAN",fg = "black",bg= "#ECEEEF",font= ("Helvetica",12, "bold"))
        title_label_c.grid(row=7, column=0, columnspan=1, pady =10)

        self.outputQueryText = tk.Text(root, width=40, height=10,padx=20, wrap = WORD)
        self.outputQueryText.grid(row=8,column=0,padx=20,columnspan=3,rowspan = 2)

        
        #query plan button
        queryPlanButton = tk.Button(root, 
                   text="Query Plan", font = ("bold",12), 
                   command=self.showQueryPlan, borderwidth = 0, bg="#96AB9C", fg="white", height = 2, width=15)
        queryPlanButton.grid(row=8,column=3,sticky=W,padx=20, pady=8, columnspan=1)

        #query tree button
        queryTreeButton = tk.Button(root, 
                   text="Query Tree", font = ("bold",12), 
                   command=self.showQueryTree, borderwidth = 0, bg="#96AB9C", fg="white", height = 2, width=15)
        queryTreeButton.grid(row=9,column=3,sticky=W,padx=20, pady =8, columnspan=1)

        #clear output button
        clearOutputButton = tk.Button(root, 
                   text="Clear Output", font = ("bold",12), 
                   command=self.clearOutput, borderwidth = 0, bg="#96AB9C", fg="white", height = 2, width=28)
        clearOutputButton.grid(row=10,column=0,sticky=W,padx=20, pady=25, columnspan=2)


        #Quit Program Button
        quitProgramButton = tk.Button(root, 
                   text="Quit Program", font = ("bold",12), 
                   command=self.quitProgram, borderwidth = 0, bg="#96AB9C", fg="white", height = 2, width=28)
        quitProgramButton.grid(row=10,column=2,sticky=W,padx=20, pady=25, columnspan=2)



    #function to connect to db
    def connect(self):
        print("connecting to database")
        try: 
            # connect to db with input fields in connection box
            messagebox.showinfo(message = "Connected to database!")
        except:
            # unnable to connect to db
            messagebox.showwarning(message="unable to connect to database!")

    def showQueryPlan(self):
        print("printing query plan")

    def showQueryTree(self):
        print("printing query tree")

    def clearInput(self):
        print("clearing input")
        self.inputQueryText.delete('1.0', END)

    def clearOutput(self):
        print("clearing output")
        self.outputQueryText.delete('1.0', END)

    def quitProgram(self):
        result = messagebox.askokcancel(
            "Quit the game.", "Are you sure?", icon='warning')
        if result == True:
            self.root.destroy()


    # def retrieve_input(self):
    #     global query_old
    #     global query_new
    #     global desc
    #     global result
    #     query_old = self.input1.get("1.0", END)
    #     query_new = self.input2.get("1.0", END)
    #     result_old = self.get_query_result(query_old)
    #     result_new = self.get_query_result(query_new)
    #     result_old_obj = json.loads(json.dumps(result_old))
    #     result_new_obj = json.loads(json.dumps(result_new))
    #     result_old_nlp = self.get_description(result_old_obj)
    #     result_new_nlp = self.get_description(result_new_obj)
    #     result_old_tree = self.get_tree(result_old_obj)
    #     result_new_tree = self.get_tree(result_new_obj)
    #     result_diff = self.get_difference(result_old_obj, result_new_obj)
    #     self.nlp1.configure(state='normal')
    #     self.nlp2.configure(state='normal')
    #     self.tree1.configure(state='normal')
    #     self.tree2.configure(state='normal')
    #     self.diff.configure(state='normal')

    #     self.nlp1.delete("1.0", END)
    #     self.nlp1.insert(END, result_old_nlp)
    #     self.nlp2.delete("1.0", END)
    #     self.nlp2.insert(END, result_new_nlp)
    #     self.tree1.delete("1.0", END)
    #     self.tree1.insert(END, result_old_tree)
    #     self.tree2.delete("1.0", END)
    #     self.tree2.insert(END, result_new_tree)
    #     self.diff.delete("1.0", END)
    #     self.diff.insert(END, result_diff)

    # def clear_input(self):
    #     self.input1.delete("1.0", END)
    #     self.input2.delete("1.0", END)

    # def clear_output(self):
    #     self.nlp1.delete("1.0", END)
    #     self.nlp2.delete("1.0", END)
    #     self.tree1.delete("1.0", END)
    #     self.tree2.delete("1.0", END)
    #     self.diff.delete("1.0", END)
    #     self.nlp1.configure(state='disabled')
    #     self.nlp2.configure(state='disabled')
    #     self.tree1.configure(state='disabled')
    #     self.tree2.configure(state='disabled')
    #     self.diff.configure(state='disabled')

    # def get_query_result(self, query):
    #     # DBConnection takes 5 arguments
    #     connection = DBConnection(self.host, self.port, self.database, self.user, self.password)
    #     result = connection.execute(query)[0][0]
    #     connection.close()
    #     return result

    # def get_description(self, json_obj):
    #     descriptions = get_text(json_obj)
    #     result = ""
    #     for description in descriptions:
    #         result = result + description + "\n"
    #     return result

    # def get_tree(self, json_obj):
    #     head = parse_json(json_obj)
    #     return generate_tree("", head)

    # def get_difference(self, json_object_A, json_object_B):
    #     diff = get_diff(json_object_A, json_object_B)
    #     return diff



if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--host', help='postgresql connection host')
    # parser.add_argument('--port', help='postgresql connection port')
    # parser.add_argument('--database', help='the tpch database to connect')
    # parser.add_argument('--user', help='db user')
    # parser.add_argument('--password', help='db password')
    # args = parser.parse_args()
    # host = args.host
    # port = args.port
    # database = args.database
    # user = args.user
    # password = args.password
    
    root = tk.Tk()

    app = App(root)
    root.geometry('600x700+0+0')
    root.configure(bg="#ECEEEF")
    # print(sys.argv)
    root.mainloop()