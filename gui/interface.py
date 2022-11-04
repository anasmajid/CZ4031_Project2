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
                   command=self.connect, borderwidth = 0, bg="#96AB9C", fg="white", height = 1, width=13)
        connectButton.grid(row=3,column=3,sticky=W,padx=20, columnspan=1)

        #Input query box
        title_label_2 = tk.Label(root, 
		 text="INPUT QUERY",
		 fg = "black",
         bg= "#ECEEEF",
		 font= ("Helvetica",12, "bold"), pady =10, padx = 20)
        title_label_2.grid(row=4,column=0,columnspan=1)

        self.inputQueryText = tk.Text(root, width=60, height=15,padx=20,pady=20)
        self.inputQueryText.grid(row=5,column=0,padx=20,pady=10,columnspan=6,rowspan = 2)

       
        # #Annotate Button to get plan
        # annotateButton = tk.Button(root, 
        #            text="Annotate Query", font = ("bold",12), 
        #            command=self.annotateQuery, borderwidth = 0, bg="#96AB9C", fg="white", height = 2, width=26)
        # annotateButton.grid(row=7,column=0,sticky=W,padx=20, pady =8, columnspan=2)
        
        #clearButton for clearing input textbox
        clearButton = tk.Button(root, 
                   text="Clear Input", font = ("bold",12), 
                   command=self.clearInput, borderwidth = 0, bg="#96AB9C", fg="white", height = 2, width=26)
        clearButton.grid(row=7,column=0,sticky=W,padx=20, pady=8, columnspan=2)

        #execute Button to get plan
        executeButton = tk.Button(root, 
                   text="Get Plan", font = ("bold",12), 
                   command=self.getPlan, borderwidth = 0, bg="#96AB9C", fg="white", height = 2, width=26)
        executeButton.grid(row=7,column=2,sticky=W,padx=20, pady =8, columnspan=2)
        
        

        # output plans - show output text 
        title_label_2 = tk.Label(root, 
        text="OUTPUT",
        fg = "black",
        bg= "#ECEEEF",
        font= ("Helvetica",13, "bold"), pady =10, padx = 8)
        title_label_2.grid(row=0,column=6,columnspan=4)

        planListLabel = tk.Label(root,text="List of Plans: ", font= ("bold",11),pady=10,padx=10)
        planListLabel.grid(row=1,column=6,sticky=W)

        alternatives = ["Query Execution Plan","Alternate Query Plan"]
        self.clickedPlan = StringVar()
        self.clickedPlan.set("Query Execution Plan") # default value
        w = OptionMenu(root,self.clickedPlan,"Select Query Plan",*alternatives )
        w.grid(row=1,column=7,sticky=W)

        #updateOutputButton is a button to update the output textbox corresponding to either query plan or alternate plan
        updateOutputButton = tk.Button(root, 
                   text="Update", font = ("bold",12), 
                   command=self.updateOutputPlan, borderwidth = 0, bg="#96AB9C", fg="white", height = 1, width=10)
        updateOutputButton.grid(row=1,column=8,sticky=W,padx=20, columnspan=1)

        #output plan on textbox
        title_label_c = tk.Label(root, text="QUERY EXECUTION PLAN",fg = "black",bg= "#ECEEEF",font= ("Helvetica",12, "bold"))
        title_label_c.grid(row=2, column=6, columnspan=2, pady =10)

        self.outputQueryText = tk.Text(root, width=52, height=23,padx=20)
        self.outputQueryText.grid(row=3,column=6,padx=10,columnspan=4,rowspan = 4)

        #Button to display query tree
        queryTreeButton = tk.Button(root, 
                   text="Show Query Tree", font = ("bold",12), 
                   command=self.getQueryTree, borderwidth = 0, bg="#96AB9C", fg="white", height = 2, width=22)
        queryTreeButton.grid(row=7,column=6,sticky=W,padx=26, pady=8, columnspan=2)

        #Annotate Button to get plan
        annotateButton = tk.Button(root, 
                   text="Annotate Query", font = ("bold",12), 
                   command=self.annotateQuery, borderwidth = 0, bg="#96AB9C", fg="white", height = 2, width=22)
        annotateButton.grid(row=7,column=8,sticky=W, padx=26, pady =8, columnspan=2)
        


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

    def annotateQuery(self):
        print("annotating sql query ")
        new_window = tk.Toplevel()
        new_window.geometry('480x500+0+0')
        new_window.title("Explanations")
        labelText = tk.Label(master=new_window, text="Explanation on annotated queries", pady=20,font = ("bold",11))
        labelText.grid(row=0,column=0,padx=20)
        outputQueryAnnotateText = tk.Text(master= new_window, width=50, height=26,padx=20)
        outputQueryAnnotateText.grid(row=1, column=0, sticky=W,padx= 20)

        # SAMPLE TEXT FOR ANNOTATION EXPLANATIONS
        outputQueryAnnotateText.insert(tk.END, "STEP 1: Sequential scan from customers table \nSTEP 2: Index Scan from food table \nSTEP 3: Hash index join on attribute orderID")

        


    def getPlan(self):
        print("getting plan")

        # send sql query plan to BE
        print("Sql query: ",self.inputQueryText.get('1.0',END))

        # display QEP plan retrived and show on output textbox
        self.outputQueryText.delete('1.0', END)

        # SAMPLE TEXT FOR OUTPUT QEP
        self.outputQueryText.insert(tk.END, "STEP 1: Sequential scan from customers table \nSTEP 2: Index Scan from food table \nSTEP 3: Hash index join on attribute orderID")
        

    def updateOutputPlan(self):
        print("updating output plan")
        print("Option now: ", self.clickedPlan.get())

    def getQueryTree(self):
        print("showing query tree plan on new window")



    # def get_query_result(self, query):
    #     # DBConnection takes 5 arguments
    #     connection = DBConnection(self.host, self.port, self.database, self.user, self.password)
    #     result = connection.execute(query)[0][0]
    #     connection.close()
    #     return result



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
    root.geometry('1080x620+0+0')
    root.mainloop()