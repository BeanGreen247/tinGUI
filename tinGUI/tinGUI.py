import idlelib.colorizer as ic
import idlelib.percolator as ip
import re
import pathlib
import tkinter as tk
from tkinter import END, filedialog

class PythonSyntax:
    cdg = ic.ColorDelegator()
    cdg.prog = re.compile(r'\b(?P<MYGROUP>tkinter)\b|' + ic.make_pat(), re.S)
    cdg.idprog = re.compile(r'\s+(\w+)', re.S)

    cdg.tagdefs['MYGROUP'] = {'foreground': '#7F7F7F', 'background': '#292929'}

    # These five lines are optional. If omitted, default colours are used.
    cdg.tagdefs['COMMENT'] = {'foreground': '#FF0000', 'background': '#292929'}
    cdg.tagdefs['KEYWORD'] = {'foreground': '#007F00', 'background': '#292929'}
    cdg.tagdefs['BUILTIN'] = {'foreground': '#7F7F00', 'background': '#292929'}
    cdg.tagdefs['STRING'] = {'foreground': '#7F3F00', 'background': '#292929'}
    cdg.tagdefs['DEFINITION'] = {'foreground': '#007F7F', 'background': '#292929'}

class Window:
    # global variable
    fileExtension = ''

    def __init__(self, master):
        self.master = master

        self.frame = tk.Frame(self.master, background='#050505')
        self.frame.pack(expand = True, fill = tk.BOTH)

        def openFile():
            tf = filedialog.askopenfilename(
            initialdir="C:/User/", 
            title="Open Text file", 
            filetypes=(("Any Files", "*"),))
            try:
                tf = open(tf)
                self.text.delete('1.0', END)
                root.title("tinGUITest")
                data = tf.read()
                self.text.insert(END, data)
                global fileExtension
                fileExtension = str(pathlib.Path(tf.name).suffix)
                tf.close()
            except:
                pass

        def clearTextField():
            self.text.delete('1.0', END)

        def savefile():    
            try:
                path = root.title().split('-')[1][1:]   
            except:
                path = ''
            if path != '':
                with open(path, 'w') as f:
                    content = self.text.get('1.0', tk.END)
                f.write(content) 
            else:
                savefileas()    
            self.text.edit_modified(0)
        
        def savefileas():    
            try:
                path = filedialog.asksaveasfile(filetypes = (("All files", "*.*"))).name
                root.title('tinGUITest - ' + path)
            except:
                return
            with open(path, 'w') as f:
                f.write(self.text.get('1.0', tk.END))
 
        self.button = tk.Button(self.frame, text="Open", command=openFile, bg='#292929', fg='#ffffff')
        self.button.pack(side="left")

        self.button = tk.Button(self.frame, text="Save", command=savefile, bg='#292929', fg='#ffffff')
        self.button.pack(side="left")

        self.button = tk.Button(self.frame, text="Clear", command=clearTextField, bg='#292929', fg='#ffffff')
        self.button.pack(side="left")

        self.button = tk.Button(self.frame, text="Quit", command=root.destroy, bg='#292929', fg='#ffffff')
        self.button.pack(side="left")

        self.text = tk.Text(self.frame, undo = True, height = 40, width = 140, bg='#292929', fg='#ffffff', insertbackground='#ffffff')
        self.text.pack(expand = True, fill = tk.BOTH)

        # syntax highlighting per language
        #def syntaxHihglighting():
        #    try:
        #        global fileExtension
        #        print(fileExtension)
        #        if fileExtension == ".py" :
        #            ip.Percolator(self.text).insertfilter(PythonSyntax.cdg)
        #        else:
        #            pass
        #    except:
        #        pass
        #syntaxHihglighting

        ip.Percolator(self.text).insertfilter(PythonSyntax.cdg)
 
 
root = tk.Tk()
root.title("tinGUITest")
window = Window(root)
root.mainloop()