import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter.font import Font
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from PIL import Image

# import relevant files
import annotation 
import preprocessing


class App(object):

    def __init__(self,parent):
        
        self.root = parent
        self.root.title("Query Plan Analyser")
        self.currentQueryPlans = [] #store state of query plans retrieved from backend
        self.rawQueryPlans = []

        title_label_1 = tk.Label(self.root, 
		 text="CONNECTION",
		 fg = "black",
         bg= "#ECEEEF",
		 font= ("Helvetica",12, "bold"), pady =10, padx = 20)
        title_label_1.grid(row=0,column=0,columnspan=1)
        
        #Host
        host_text = StringVar()
        host_label = tk.Label(self.root,text="Host", font= ("bold",11),pady=10,padx=20)
        host_label.grid(row=1,column=0,sticky=W)
        self.host_entry = tk.Entry(self.root,textvariable=host_text)
        self.host_entry.grid(row=1,column=1)
        
        #Username
        username_text = StringVar()
        username_label = tk.Label(self.root,text="Username", font= ("bold",11),pady=10,padx=20)
        username_label.grid(row=1,column=2,sticky=W)
        self.username_entry = tk.Entry(self.root,textvariable=username_text)
        self.username_entry.grid(row=1,column=3)

        #Password
        password_text = StringVar()
        password_label = tk.Label(self.root,text="Password", font= ("bold",11),pady=10,padx=20)
        password_label.grid(row=2,column=2,sticky=W)
        self.password_entry = tk.Entry(self.root,textvariable=password_text)
        self.password_entry.grid(row=2,column=3)

        #DBname
        dbName_text = StringVar()
        dbName_label = tk.Label(self.root,text="DBname", font= ("bold",11),pady=10,padx=20)
        dbName_label.grid(row=2,column=0,sticky=W)
        self.dbName_entry = tk.Entry(self.root,textvariable=dbName_text)
        self.dbName_entry.grid(row=2,column=1)

        # Default values
        self.host_entry.insert(tk.END,"localhost")
        self.dbName_entry.insert(tk.END,"TPC-H")
        self.username_entry.insert(tk.END,"postgres")
        self.password_entry.insert(tk.END,"Superlim016")

        
        
        #connnectButton
        connectButton = tk.Button(self.root, 
                   text="Connect", font = ("bold",12), 
                   command=self.connect, borderwidth = 0, bg="#96AB9C", fg="white", height = 1, width=13)
        connectButton.grid(row=3,column=3,sticky=W,padx=20,pady=10, columnspan=1)

        #Input query box
        title_label_2 = tk.Label(self.root, 
		 text="INPUT QUERY",
		 fg = "black",
         bg= "#ECEEEF",
		 font= ("Helvetica",12, "bold"), pady =10, padx = 20)
        title_label_2.grid(row=4,column=0,columnspan=1)

        self.inputQueryText = tk.Text(self.root, width=60, height=15,padx=20,pady=20,font= ("Helvetica",11))
        self.inputQueryText.grid(row=5,column=0,padx=20,pady=10,columnspan=6,rowspan = 2,)
        
        #clearButton for clearing input textbox
        clearButton = tk.Button(self.root, 
                   text="Clear Input", font = ("bold",12), 
                   command=self.clearInput, borderwidth = 0, bg="#96AB9C", fg="white", height = 2, width=26)
        clearButton.grid(row=7,column=0,sticky=W,padx=20, pady=8, columnspan=2)

        #execute Button to get plan
        executeButton = tk.Button(self.root, 
                   text="Get Plan", font = ("bold",12), 
                   command=self.getPlan, borderwidth = 0, bg="#96AB9C", fg="white", height = 2, width=26)
        executeButton.grid(row=7,column=2,sticky=W,padx=20, pady =8, columnspan=2)
        

        # output plans - show output text 
        title_label_2 = tk.Label(self.root, 
        text="OUTPUT",
        fg = "black",
        bg= "#ECEEEF",
        font= ("Helvetica",13, "bold"), pady =10, padx = 8)
        title_label_2.grid(row=0,column=6,columnspan=4)

        planListLabel = tk.Label(self.root,text="List of Plans: ", font= ("bold",11),pady=10,padx=10)
        planListLabel.grid(row=1,column=6,sticky=W)

        alternatives = ["Query Execution Plan","Alternate Query Plan"]
        self.clickedPlan = StringVar()
        self.clickedPlan.set("Query Execution Plan") # default value
        w = OptionMenu(self.root,self.clickedPlan,"Select Query Plan",*alternatives )
        w.grid(row=1,column=7,sticky=W)

        #updateOutputButton is a button to update the output textbox corresponding to either query plan or alternate plan
        updateOutputButton = tk.Button(self.root, 
                   text="Update", font = ("bold",12), 
                   command=self.updateOutputPlan, borderwidth = 0, bg="#96AB9C", fg="white", height = 1, width=10)
        updateOutputButton.grid(row=1,column=8,sticky=W,padx=20, columnspan=1)

        #output plan on textbox
        title_label_c = tk.Label(self.root, text="QUERY EXECUTION PLAN",fg = "black",bg= "#ECEEEF",font= ("Helvetica",11, "bold"))
        title_label_c.grid(row=2, column=6, columnspan=2, pady =10)
        self.outputQueryText = tk.Text(self.root, width=52, height=23,padx=20,font= ("Helvetica",11))
        self.outputQueryText.grid(row=3,column=6,padx=10,columnspan=4,rowspan = 4)

        #Button to display query tree
        queryTreeButton = tk.Button(self.root, 
                   text="Show Query Tree", font = ("bold",12), 
                   command=self.getQueryTree, borderwidth = 0, bg="#96AB9C", fg="white", height = 2, width=22)
        queryTreeButton.grid(row=7,column=6,sticky=W,padx=26, pady=8, columnspan=2)

        #Annotate Button to get plan
        annotateButton = tk.Button(self.root, 
                   text="Annotate Query", font = ("bold",12), 
                   command=self.annotateQuery, borderwidth = 0, bg="#96AB9C", fg="white", height = 2, width=22)
        annotateButton.grid(row=7,column=8,sticky=W, padx=26, pady =8, columnspan=2)

    #Establish connection to db
    def connect(self):
        print("connecting to database")
        try: 
            # connect to db with input fields in connection box
            dbConfig = {
                "host" : self.host_entry.get(),
                "database" : self.dbName_entry.get(),
                "user": self.username_entry.get(),
                "password": self.password_entry.get()
            }
            print(dbConfig)
            if_connect = preprocessing.connect(dbConfig)
            if if_connect:
                messagebox.showinfo(message = "Connected to database!")
            else:
                messagebox.showwarning(message="unable to connect to database!")
            # API 1. Send dbConfig details to backend to establish connection with postgresql

            # messagebox.showinfo(message = "Connected to database!")
            # print("Connect message")
        except:
            # unnable to connect to db
            messagebox.showwarning(message="unable to connect to database!")
            print("Unable to Connect message")

    def showQueryPlan(self):
        print("printing query plan")

    def showQueryTree(self):
        print("printing query tree")

    def clearInput(self):
        print("clearing input")
        self.inputQueryText.delete('1.0', END)

    def getPlan(self):

        inputSql = self.inputQueryText.get('1.0',END)
    
        try: 
            # API 2. Send sql Input to backend and receives a list of query plans, [QEP, AQP]
            self.rawQueryPlans = preprocessing.getQueryPlan(inputSql) #[[QEP t1, QEP t2..], [AQP]]
            queryPlans = preprocessing.stringOutput(self.rawQueryPlans) # [QEP, AQP]
            # print("queryPlan: ",queryPlans)
            self.currentQueryPlans = queryPlans  #storing [QEP,AQP] from be into a state variable in interface object

            if (self.clickedPlan.get()=="Alternate Query Plan"):
                queryPlan = queryPlans[1] #AQP
            else: #Default value is standard QEP
                queryPlan = queryPlans[0]

            # format output query plan
            formattedOutputQueryPlan = ""
            splitSteps = queryPlan.split(" -> ")

            for step in splitSteps:
                step = " ".join(step.strip().split())
                formattedOutputQueryPlan += "\n=> "
                formattedOutputQueryPlan += step
                formattedOutputQueryPlan += "\n"

            self.outputQueryText.delete('1.0', END)
            self.outputQueryText.insert(tk.END,formattedOutputQueryPlan)
            
        except:
            print("Error!")
            tk.messagebox.showwarning(message="Error! Please check the sql input again!")



    def annotateQuery(self):
        if (self.currentQueryPlans!=[]):
            new_window = tk.Toplevel()
            new_window.geometry('550x550+0+0')
            new_window.title("Annotated Explanations")
            labelText = tk.Label(master=new_window, text="Explanation on Annotated Queries", pady=20,font= ("Helvetica",12, "bold"))
            labelText.grid(row=0,column=0,padx=20)
            outputQueryAnnotateText = tk.Text(master= new_window, width=58, height=26,padx=20,font= ("Helvetica",11))
            outputQueryAnnotateText.grid(row=1, column=0, sticky=W,padx= 20)

            # Obtain annotated explanations by passing in the currentQueryplan
            annotations = annotation.Annotation()
            if (self.clickedPlan.get()=="Query Execution Plan"):
                annotatedExplanation = annotations.getAnnotatedExplanations(self.currentQueryPlans[0])
                outputQueryAnnotateText.insert(tk.END, annotatedExplanation)
            elif (self.clickedPlan.get()=="Alternate Query Plan"):
                annotatedExplanation = annotations.getAnnotatedExplanations(self.currentQueryPlans[1])
                outputQueryAnnotateText.insert(tk.END, annotatedExplanation)
            else:
                annotatedExplanation = annotations.getAnnotatedExplanations(self.currentQueryPlans[0])
                outputQueryAnnotateText.insert(tk.END, annotatedExplanation)
        else:
            tk.messagebox.showwarning(message="You have not executed any sql inputs!")


    def updateOutputPlan(self):

        print("updating output plan")
        if (self.clickedPlan.get()=="Alternate Query Plan"):
                queryPlan = self.currentQueryPlans[1] #AQP
        else: #Default value is standard QEP
            queryPlan = self.currentQueryPlans[0]

        # format output query plan
        formattedOutputQueryPlan = ""
        splitSteps = queryPlan.split(" -> ")
        for step in splitSteps:
            step = " ".join(step.strip().split())
            formattedOutputQueryPlan += "\n=> "
            formattedOutputQueryPlan += step
            formattedOutputQueryPlan += "\n"

        self.outputQueryText.delete('1.0', END)
        self.outputQueryText.insert(tk.END,formattedOutputQueryPlan)


    def getQueryTree(self):
        # print("get tree")

        if (self.currentQueryPlans!=[]):
            print("showing query tree plan on new window")
            # Decide whether tree is shown for QEP or AQP
            print("self.rawQueryPlans", self.rawQueryPlans)
            
            # plan = self.rawQueryPlans
            if (self.clickedPlan.get()=="Alternate Query Plan"):
                # send command 1 for AQP
                preprocessing.create_graph(1,self.rawQueryPlans)
                img = Image.open("query1testaqp.png")
                img.show()
            else:
                # send command 0 for QEP tree
                preprocessing.create_graph(0,self.rawQueryPlans)
                img = Image.open("query1testqep.png")
                img.show()





# 1. App.connect() sends a dictionary dbConfig to backend (sends a dictionary of the user input for host,pw,database,username) 
# 2. App.getPlan() sends a sql input to the backend and should receive a list of query plans in the format [QEP, AQP]
# 3. App.getQueryTree() receieves a tree data stucture of QEP and displays the tree in a visual manner
