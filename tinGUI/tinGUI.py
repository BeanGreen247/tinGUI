import idlelib.colorizer as ic
import idlelib.percolator as ip
import re
import pathlib
import tkinter as tk
import threading
from tkinter import END, filedialog

root = tk.Tk()
# Creating Menubar
menubar = tk.Menu(root)

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

class App():
    def __init__(self):
        super().__init__()

        self.frame = tk.Frame(self.master, background='#050505')
        self.frame.pack(expand = True, fill = tk.BOTH)

        self.text = tk.Text(self.frame, undo = True, height = 40, width = 140, bg='#292929', fg='#ffffff', insertbackground='#ffffff')
        self.text.pack(expand = True, fill = tk.BOTH)

class Window:
    # global variable
    fileExtension = ''

    def __init__(self, master):
        self.master = master
        
        self.frame = tk.Frame(self.master, background='#050505')
        self.frame.pack(expand = True, fill = tk.BOTH)

        def openFile():
            tf = filedialog.askopenfilename(
            initialdir="C:/User/", #on linux opens /home/username/
            title="Open Text file",
            filetypes=(("Any Files", "*"),))
            try:
             tf = open(tf)
             self.text.delete('1.0', END)
             root.title("tinGUI - " + str(pathlib.Path(tf.name)))
             data = tf.read()
             self.text.insert(END, data)
             global fileExtension
             fileExtension = str(pathlib.Path(tf.name).suffix)
             tf.close()
            except:
                pass

        def clearTextField():
            self.text.delete('1.0', END)

        def saveFile():
            try:
                path = root.title().split('-')[1][1:]
            except:
                path = filedialog.asksaveasfile(filetypes =[("All files", "*.*")]).name
            if path != '':
                with open(path, 'w') as f:
                    content = self.text.get('1.0', tk.END)
                    f.write(content)
            else:
                saveFileAs()
            self.text.edit_modified(0)

        def saveFileAs():
            try:
                path = filedialog.asksaveasfile(filetypes =[("All files", "*.*")]).name
                with open(path, 'w') as f:
                    f.write(self.text.get('1.0', tk.END))
            except:
                pass
 
        def guiGroup0(): 
            # Adding File Menu and commands
            file = tk.Menu(menubar, tearoff = 0)
            menubar.add_cascade(label ='File', menu = file)
            file.add_command(label ='New File', command = None)
            file.add_command(label ='Open...', command = openFile)
            file.add_command(label ='Save', command = saveFile)
            file.add_command(label ='Save As...', command = saveFileAs)
            file.add_separator()
            file.add_command(label ='Quit', command = root.destroy)

            # Adding Edit Menu and commands
            edit = tk.Menu(menubar, tearoff = 0)
            menubar.add_cascade(label ='Edit', menu = edit)
            edit.add_command(label ='Clear', command = clearTextField)

        def guiGroup1():
            self.text = tk.Text(self.frame, undo = True, height = 40, width = 140, bg='#292929', fg='#ffffff', insertbackground='#ffffff')
            self.text.pack(expand = True, fill = tk.BOTH)
            ip.Percolator(self.text).insertfilter(PythonSyntax.cdg)

        # WIP
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

        threading.Thread(target=guiGroup0).start()
        threading.Thread(target=guiGroup1).start()

root.title("tinGUI")
root.config(menu = menubar)
window = Window(root)
root.mainloop()