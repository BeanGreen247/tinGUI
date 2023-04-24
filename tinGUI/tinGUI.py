import pathlib
import tkinter as tk
import threading
from tkinter import END, Tk, Toplevel, filedialog
import idlelib.percolator as ip
import idlelib.colorizer as ic
import re

version='v0.1.2.alpha'
# color def
bgColor = '#292929'
pythonCommentColor = '#FF0000'
CommentColor = '#57A546'
CLOUD2 = '#7f9da5'
LEMON = '#FAFA33'
OVERCAST = '#c3bdab'
PUMPKIN = '#ff7518'
STORMY = '#5a6caa'
SAILOR = '#38739D'
CLOUD = '#c7c4bf'
DK_SEAFOAM = '#9FE2BF'
PURPLE = '#A020F0'

class TextSyntax:
    cd = ic.ColorDelegator()

    cd.tagdefs['COMMENT'] = {'foreground': '#ffffff', 'background': bgColor}
    cd.tagdefs['KEYWORD'] = {'foreground': '#ffffff', 'background': bgColor}
    cd.tagdefs['BUILTIN'] = {'foreground': '#ffffff', 'background': bgColor}
    cd.tagdefs['STRING'] = {'foreground': '#ffffff', 'background': bgColor}
    cd.tagdefs['DEFINITION'] = {'foreground': '#ffffff', 'background': bgColor}

class PythonSyntax:
    #syntax highlighter patterns
    KEYWORD   = r"\b(?P<KEYWORD>False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b"
    EXCEPTION = r"([^.'\"\\#]\b|^)(?P<EXCEPTION>ArithmeticError|AssertionError|AttributeError|BaseException|BlockingIOError|BrokenPipeError|BufferError|BytesWarning|ChildProcessError|ConnectionAbortedError|ConnectionError|ConnectionRefusedError|ConnectionResetError|DeprecationWarning|EOFError|Ellipsis|EnvironmentError|Exception|FileExistsError|FileNotFoundError|FloatingPointError|FutureWarning|GeneratorExit|IOError|ImportError|ImportWarning|IndentationError|IndexError|InterruptedError|IsADirectoryError|KeyError|KeyboardInterrupt|LookupError|MemoryError|ModuleNotFoundError|NameError|NotADirectoryError|NotImplemented|NotImplementedError|OSError|OverflowError|PendingDeprecationWarning|PermissionError|ProcessLookupError|RecursionError|ReferenceError|ResourceWarning|RuntimeError|RuntimeWarning|StopAsyncIteration|StopIteration|SyntaxError|SyntaxWarning|SystemError|SystemExit|TabError|TimeoutError|TypeError|UnboundLocalError|UnicodeDecodeError|UnicodeEncodeError|UnicodeError|UnicodeTranslateError|UnicodeWarning|UserWarning|ValueError|Warning|WindowsError|ZeroDivisionError)\b"
    BUILTIN   = r"([^.'\"\\#]\b|^)(?P<BUILTIN>abs|all|any|ascii|bin|breakpoint|callable|chr|classmethod|compile|complex|copyright|credits|delattr|dir|divmod|enumerate|eval|exec|exit|filter|format|frozenset|getattr|globals|hasattr|hash|help|hex|id|input|isinstance|issubclass|iter|len|license|locals|map|max|memoryview|min|next|oct|open|ord|pow|print|quit|range|repr|reversed|round|set|setattr|slice|sorted|staticmethod|sum|type|vars|zip)\b"
    DOCSTRING = r"(?P<DOCSTRING>(?i:r|u|f|fr|rf|b|br|rb)?'''[^'\\]*((\\.|'(?!''))[^'\\]*)*(''')?|(?i:r|u|f|fr|rf|b|br|rb)?\"\"\"[^\"\\]*((\\.|\"(?!\"\"))[^\"\\]*)*(\"\"\")?)"
    STRING    = r"(?P<STRING>(?i:r|u|f|fr|rf|b|br|rb)?'[^'\\\n]*(\\.[^'\\\n]*)*'?|(?i:r|u|f|fr|rf|b|br|rb)?\"[^\"\\\n]*(\\.[^\"\\\n]*)*\"?)"
    TYPES     = r"\b(?P<TYPES>bool|bytearray|bytes|dict|float|int|list|str|tuple|object)\b"
    NUMBER    = r"\b(?P<NUMBER>((0x|0b|0o|#)[\da-fA-F]+)|((\d*\.)?\d+))\b"
    CLASSDEF  = r"(?<=\bclass)[ \t]+(?P<CLASSDEF>\w+)[ \t]*[:\(]" #recolor of DEFINITION for class definitions
    DECORATOR = r"(^[ \t]*(?P<DECORATOR>@[\w\d\.]+))"
    INSTANCE  = r"\b(?P<INSTANCE>super|self|cls)\b"
    COMMENT   = r"(?P<COMMENT>#[^\n]*)"
    SYNC      = r"(?P<SYNC>\n)"

    PROG   = rf"{KEYWORD}|{BUILTIN}|{EXCEPTION}|{TYPES}|{COMMENT}|{DOCSTRING}|{STRING}|{SYNC}|{INSTANCE}|{DECORATOR}|{NUMBER}|{CLASSDEF}"

    IDPROG = r"(?<!class)\s+(\w+)"

    TAGDEFS   = {   
                'COMMENT'    : {'foreground': pythonCommentColor  , 'background': bgColor},
                'TYPES'      : {'foreground': CLOUD2    , 'background': bgColor},
                'NUMBER'     : {'foreground': LEMON     , 'background': bgColor},
                'BUILTIN'    : {'foreground': OVERCAST  , 'background': bgColor},
                'STRING'     : {'foreground': PUMPKIN   , 'background': bgColor},
                'DOCSTRING'  : {'foreground': STORMY    , 'background': bgColor},
                'EXCEPTION'  : {'foreground': CLOUD2    , 'background': bgColor},
                'DEFINITION' : {'foreground': SAILOR    , 'background': bgColor},
                'DECORATOR'  : {'foreground': CLOUD2    , 'background': bgColor},
                'INSTANCE'   : {'foreground': CLOUD     , 'background': bgColor},
                'KEYWORD'    : {'foreground': DK_SEAFOAM, 'background': bgColor},
                'CLASSDEF'   : {'foreground': PURPLE    , 'background': bgColor},
            }

    cd         = ic.ColorDelegator()
    cd.prog    = re.compile(PROG, re.S|re.M)
    cd.idprog  = re.compile(IDPROG, re.S)
    cd.tagdefs = {**cd.tagdefs, **TAGDEFS}

class JavaSyntax:
    #syntax highlighter patterns
    KEYWORD   = r"\b(?P<KEYWORD>False|None|True|abstract|assert|boolean|break|byte|case|catch|char|class|continue|default|do|double|else|enum|extends|final|finally|float|for|if|implements|import|instanceof|int|interface|long|native|new|null|package|private|protected|public|return|short|static|strictfp|super|switch|synchronized|this|throw|throws|transient|try|void|volatile|while)\b"
    EXCEPTION = r"([^.'\"\\#]\b|^)(?P<EXCEPTION>CloneNotSupportedException|InterruptedException|ReflectiveOperationException|ClassNotFoundException|IllegalAccessException|InstantiationException|NoSuchFieldException|NoSuchMethodException|RuntimeException|ArithmeticException|ArrayStoreException|ClassCastException|EnumConstantNotPresentException|IllegalArgumentException|IllegalThreadStateException|NumberFormatException|IllegalMonitorStateException|IllegalStateException|IndexOutOfBoundsException|ArrayIndexOutOfBoundsException|StringIndexOutOfBoundsException|NegativeArraySizeException|NullPointerException|SecurityException|TypeNotPresentException|UnsupportedOperationException)\b"
    BUILTIN   = r"([^.'\"\\#]\b|^)(?P<BUILTIN>charAt|codePointAt|codePointBefore|codePointCount|compareTo|compareToIgnoreCase|concat|contains|contentEquals|copyValueOf|endsWith|equals|equalsIgnoreCase|format|getBytes|getChars|hashCode|indexOf|intern|isEmpty|lastIndexOf|length|matches|offsetByCodePoints|regionMatches|replace|replaceFirst|replaceAll|split|startsWith|subSequence|substring|toCharArray|toLowerCase|toString|toUpperCase|trim|valueOf|abs|acos|asin|atan|atan2|cbrt|ceil|copySign|cos|cosh|exp|expm1|floor|getExponent|hypot|IEEEremainder|log|log10|log1p|max|min|nextAfter|nextUp|pow|random|round|rint|signum|sin|sinh|sqrt|tan|tanh|toDegrees|toRadians|ulp)\b"
    DOCSTRING = r"(?P<DOCSTRING>(?i:r|u|f|fr|rf|b|br|rb)?'''[^'\\]*((\\.|'(?!''))[^'\\]*)*(''')?|(?i:r|u|f|fr|rf|b|br|rb)?\"\"\"[^\"\\]*((\\.|\"(?!\"\"))[^\"\\]*)*(\"\"\")?)"
    STRING    = r"(?P<STRING>(?i:r|u|f|fr|rf|b|br|rb)?'[^'\\\n]*(\\.[^'\\\n]*)*'?|(?i:r|u|f|fr|rf|b|br|rb)?\"[^\"\\\n]*(\\.[^\"\\\n]*)*\"?)"
    TYPES     = r"\b(?P<TYPES>byte|short|int|long|float|double|boolean|char)\b"
    NUMBER    = r"\b(?P<NUMBER>((0x|0b|0o|#)[\da-fA-F]+)|((\d*\.)?\d+))\b"
    CLASSDEF  = r"(?<=\bclass)[ \t]+(?P<CLASSDEF>\w+)[ \t]*[:\(]" #recolor of DEFINITION for class definitions
    DECORATOR = r"(^[ \t]*(?P<DECORATOR>@[\w\d\.]+))"
    INSTANCE  = r"\b(?P<INSTANCE>self)\b"
    COMMENT   = r"(?P<COMMENT>//[^\n]*)"
    SYNC      = r"(?P<SYNC>\n)"

    PROG   = rf"{KEYWORD}|{BUILTIN}|{EXCEPTION}|{TYPES}|{COMMENT}|{DOCSTRING}|{STRING}|{SYNC}|{INSTANCE}|{DECORATOR}|{NUMBER}|{CLASSDEF}"

    IDPROG = r"(?<!class)\s+(\w+)"

    TAGDEFS   = {   
                'COMMENT'    : {'foreground': CommentColor  , 'background': bgColor},
                'TYPES'      : {'foreground': CLOUD2    , 'background': bgColor},
                'NUMBER'     : {'foreground': LEMON     , 'background': bgColor},
                'BUILTIN'    : {'foreground': OVERCAST  , 'background': bgColor},
                'STRING'     : {'foreground': PUMPKIN   , 'background': bgColor},
                'DOCSTRING'  : {'foreground': STORMY    , 'background': bgColor},
                'EXCEPTION'  : {'foreground': CLOUD2    , 'background': bgColor},
                'DEFINITION' : {'foreground': SAILOR    , 'background': bgColor},
                'DECORATOR'  : {'foreground': CLOUD2    , 'background': bgColor},
                'INSTANCE'   : {'foreground': CLOUD     , 'background': bgColor},
                'KEYWORD'    : {'foreground': DK_SEAFOAM, 'background': bgColor},
                'CLASSDEF'   : {'foreground': PURPLE    , 'background': bgColor},
            }

    cd         = ic.ColorDelegator()
    cd.prog    = re.compile(PROG, re.S|re.M)
    cd.idprog  = re.compile(IDPROG, re.S)
    cd.tagdefs = {**cd.tagdefs, **TAGDEFS}

root = tk.Tk()
# Creating Menubar
menubar = tk.Menu(root)

# about window
about = tk.Tk()

# Add a Scrollbar(horizontal)
v=tk.Scrollbar(root, orient='vertical')
v.pack(side=tk.RIGHT, fill='y')

class AboutApp(tk.Frame):
    try:
        def __init__(self, master=about):
            try:
                super().__init__(master)
                self.master = master
                self.pack()
                self.label = tk.Label(self)
                self.label["text"] = "tinGUI is a text editor" + "\ncreated in Python with tkinter." + "\n\nCreated by BeanGreen247." + "\n\nContact info:" + \
            "\nGithub > https://github.com/BeanGreen247" + "\nEmail-1 > mozdrent@gmail.com" + "\nEmail-2 > mozdrent.business@outlook.com" + "\n\n2023"
                self.label.pack(side="top")
            except:
                pass
    except:
        pass

class Window:
    def __init__(self, master):
        self.master = master

        self.frame = tk.Frame(self.master, background='#050505')
        self.frame.pack(expand = True, fill = tk.BOTH)

        def openFile():
            try:
             tf = filedialog.askopenfilename(
             initialdir="C:/User/", #on linux opens /home/username/
             title="Open file",
             filetypes=(("Any Files", "*"),))
             try:
              tf = open(tf)
              self.text.delete('1.0', END)
              root.title("tinGUI " + version + " - " + str(pathlib.Path(tf.name)))
              data = tf.read()
              self.text.insert(END, data)
              tf.close()
             except:
                pass
            except:
                pass

        def newFile():
            try:
             tf = filedialog.asksaveasfile(
             initialdir="C:/User/", #on linux opens /home/username/
             title="New file",
             filetypes=(("Any Files", "*"),))
             root.title("tinGUI " + version + " - " + str(pathlib.Path(tf.name)))
             self.text.delete('1.0', END)
             try:
              tf = open(tf)
              data = tf.read()
              self.text.insert(END, data)
              tf.close()
             except:
                pass
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

        # WIP show about window
        def showAboutWindow():
            try:
                AboutApp(master=AboutApp.about).mainloop()
            except:
                pass

        def guiGroup0():
            # here we connect the scrollbar to the textbox view
            self.text = tk.Text(self.frame, undo = True, height = 40, width = 140, bg=bgColor, fg='#ffffff', insertbackground='#ffffff', yscrollcommand=v.set)
            self.text.pack(expand = True, fill = tk.BOTH)
            # enables draging of the scroll bar to navigate the text file
            v.config(command=self.text.yview)
            clearSyntaxFilters

        def clearSyntaxFilters():
            ip.Percolator(self.text).filters.clear()
            ip.Delegator.resetcache()
            ip.Percolator.close()

        def textSyntax():
            clearSyntaxFilters
            self.text.pack_forget()
            self.text = tk.Text(self.frame, undo = True, height = 40, width = 140, bg=bgColor, fg='#ffffff', insertbackground='#ffffff', yscrollcommand=v.set)
            self.text.pack(expand = True, fill = tk.BOTH)
            v.config(command=self.text.yview)
            with open(root.title().split('-')[1][1:]) as f:
                data = f.read()
            self.text.insert(END, data)
            clearSyntaxFilters
            try:
                ip.Percolator(self.text).insertfilter(TextSyntax.cd)
            except:
                pass
            
        def pythonSyntax():
            clearSyntaxFilters
            self.text.pack_forget()
            self.text = tk.Text(self.frame, undo = True, height = 40, width = 140, bg=bgColor, fg='#ffffff', insertbackground='#ffffff', yscrollcommand=v.set)
            self.text.pack(expand = True, fill = tk.BOTH)
            v.config(command=self.text.yview)
            with open(root.title().split('-')[1][1:]) as f:
                data = f.read()
            self.text.insert(END, data)
            clearSyntaxFilters
            try:
                ip.Percolator(self.text).insertfilter(PythonSyntax.cd)
            except:
                pass

        def javaSyntax():
            clearSyntaxFilters
            self.text.pack_forget()
            self.text = tk.Text(self.frame, undo = True, height = 40, width = 140, bg=bgColor, fg='#ffffff', insertbackground='#ffffff', yscrollcommand=v.set)
            self.text.pack(expand = True, fill = tk.BOTH)
            v.config(command=self.text.yview)
            with open(root.title().split('-')[1][1:]) as f:
                data = f.read()
            self.text.insert(END, data)
            clearSyntaxFilters
            try:
                ip.Percolator(self.text).insertfilter(JavaSyntax.cd)
            except:
                pass
        
        def guiGroup1(): 
            # Adding File Menu and commands
            file = tk.Menu(menubar, tearoff = 0)
            menubar.add_cascade(label ='File', menu = file)
            file.add_command(label ='New File', command = newFile)
            file.add_command(label ='Open...', command = openFile)
            file.add_command(label ='Save', command = saveFile)
            file.add_command(label ='Save As...', command = saveFileAs)
            file.add_separator()
            file.add_command(label ='Quit', command = root.destroy)

            # Adding Edit Menu and commands
            edit = tk.Menu(menubar, tearoff = 0)
            menubar.add_cascade(label ='Edit', menu = edit)
            edit.add_command(label ='Clear', command = clearTextField)

            # Adding Edit Menu and commands
            syntax = tk.Menu(menubar, tearoff = 0)
            menubar.add_cascade(label ='Syntax', menu = syntax)
            syntax.add_command(label ='Plain Text', command = textSyntax)
            syntax.add_command(label ='Python', command = pythonSyntax)
            syntax.add_command(label ='Java', command = javaSyntax)

            # Adding Help Menu and commands
            hMenu = tk.Menu(menubar, tearoff = 0)
            menubar.add_cascade(label ='Help', menu = hMenu)
            hMenu.add_command(label ='About tinGUI', command = showAboutWindow)
 
        threading.Thread(target=guiGroup0).start()
        threading.Thread(target=guiGroup1).start()

root.title("tinGUI " + version)
root.config(menu = menubar)
window = Window(root)
root.mainloop()