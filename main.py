import os
import ply.lex as lex
import ply.yacc as yacc
from tkinter import END, Button, Scrollbar, Tk, Frame, Label, LabelFrame, Entry, Text

reserved = {
   'sudo' : 'SUDO',
   'pwd' : 'PWD',
   'ls' : 'LS',
   'touch' : 'TOUCH',
   'mkdir' : 'MKDIR',
   'rm' : 'RM',
   'rmdir' : 'RMDIR',
   'cat' : 'CAT',
   'tree' : 'TREE',
   'head' : 'HEAD',
   'tail' : 'TAIL',
}

tokens = [
   'ARGUMENTO',
] + list(reserved.values())

t_ignore = ' '

def t_ARGUMENTO(t):
   r'[a-zA-Z0-9.]+(\.[a-zA-Z0-9]+)*'
   t.type = reserved.get(t.value,'ARGUMENTO')
   return t

def t_newline(t):
   r'\n+'
   t.lexer.lineno += len(t.value)

def t_error(t):
   print(f"Token inválido: {t.value[0]}")
   t.lexer.skip(1)

lexer = lex.lex()

def p_start(p):
   '''script : expresion
             | SUDO expresion'''
   pass

def p_pwd(p):
   'expresion : PWD'
   if check_sudo():
      result = f"El script mostrará el directorio donde el usuario se encuentra ubicado actualmente con permisos de administrador."
      log = os.popen("sudo pwd").read()
   else:
      result = f"El script mostrará el directorio donde el usuario se encuentra ubicado actualmente."
      log = os.popen("pwd").read()
   update_result(result, False, log)

def p_ls(p):
   'expresion : LS'
   if check_sudo():
      result = f"El script mostrará en forma de lista el contenido del directorio actual con permisos de administrador."
      log = os.popen("sudo ls").read()
   else:
      result = f"El script mostrará en forma de lista el contenido del directorio actual."
      log = os.popen("ls").read()
   update_result(result, False, log)

def p_tree(p):
   'expresion : TREE'
   if check_sudo():
      result = f"El script mostrará por consola los directorios en forma de árbol con permisos de administrador."
      log = os.popen('sudo tree').read()
   else:
      result = f"El script mostrará por consola los directorios en forma de árbol."
      log = os.popen('tree').read()
   update_result(result, False, log)

def p_touch(p):
   'expresion : TOUCH ARGUMENTO'
   files = check_files()

   if check_sudo():
      result = f"El script creará un archivo llamado '{p[2]}' con permisos de administrador."
   else:
      result = f"El script creará un archivo llamado '{p[2]}'."

   if p[2] in files:
      log = "Este archivo ya existe en el directorio."
   else:
      if check_sudo():
         os.popen(f"sudo touch {p[2]}").read()
      else:
         os.popen(f"touch {p[2]}").read()
      log = "Archivo creado exitosamente."
   update_result(result, False, log)

def p_mkdir(p):
   'expresion : MKDIR ARGUMENTO'
   folders = check_folders()

   if check_sudo():
      result = f"El script creará una carpeta llamada '{p[2]}' con permisos de administrador."
   else:
      result = f"El script creará una carpeta llamada '{p[2]}'."

   if p[2] in folders:
      log = "Esta carpeta ya existe en el directorio."
   else:
      if check_sudo():
         os.popen(f"sudo mkdir {p[2]}")
      else:
         os.popen(f"mkdir {p[2]}")
      log = 'Carpeta creada exitosamente.'
   update_result(result, False, log)

def p_rm(p):
   'expresion : RM ARGUMENTO'
   files = check_files()

   if check_sudo():
      result = f"El script borrará el archivo '{p[2]}' con permisos de administrador."
   else:
      result = f"El script borrará el archivo '{p[2]}'."

   for file in files:
      if file == p[2]:
         if check_sudo():
            os.popen(f"sudo rm {p[2]}").read()
         else:
            os.popen(f"rm {p[2]}").read()
         log = 'Archivo borrado exitosamente.'
         break
      else:
         log = "El archivo no existe en el directorio"
   update_result(result, False, log)

def p_rmdir(p):
   'expresion : RMDIR ARGUMENTO'
   folders = check_folders()

   if check_sudo():
      result = f"El script borrará la carpeta '{p[2]}' con permisos de administrador."
   else:
      result = f"El script borrará la carpeta '{p[2]}'."

   for folder in folders:
      if folder == p[2]:
         if check_sudo():
            os.popen(f"sudo rmdir {p[2]}").read()
         else:
            os.popen(f"rmdir {p[2]}").read()
         log = 'Carpeta borrada exitosamente.'
         break
      else:
         log = "La carpeta no existe en el directorio"
   update_result(result, False, log)

def p_cat(p):
   'expresion : CAT ARGUMENTO'
   files = check_files()

   if check_sudo():
      result = f"El script mostrará por consola el contenido del archivo '{p[2]}' con permisos de administrador."
   else:
      result = f"El script mostrará por consola el contenido del archivo '{p[2]}'."

   for file in files:
      if file == p[2]:
         if check_sudo():
            log = os.popen(f"sudo cat {p[2]}").read()
         else:
            log = os.popen(f"cat {p[2]}").read()
         break
      else:
         log = "El archivo no existe en el directorio."

   update_result(result, False, log)

def p_head(p):
   'expresion : HEAD ARGUMENTO'
   files = check_files()

   if check_sudo():
      result = f"El script mostrará por consola las primeras 10 líneas del archivo '{p[2]}' con permisos de administrador."
   else:
      result = f"El script mostrará por consola las primeras 10 líneas del archivo '{p[2]}'."

   for file in files:
      if file == p[2]:
         if check_sudo():
            log = os.popen(f"sudo head {p[2]}").read()
         else:
            log = os.popen(f"head {p[2]}").read()
         break
      else:
         log = "El archivo no existe en el directorio."

   update_result(result, False, log)

def p_tail(p):
   'expresion : TAIL ARGUMENTO'
   files = check_files()

   if check_sudo():
      result = f"El script mostrará por consola las últimas 10 líneas del archivo '{p[2]}' con permisos de administrador."
   else:
      result = f"El script mostrará por consola las últimas 10 líneas del archivo '{p[2]}'."

   for file in files:
      if file == p[2]:
         if check_sudo():
            log = os.popen(f"sudo tail {p[2]}").read()
         else:
            log = os.popen(f"tail {p[2]}").read()
         break
      else:
         log = "El archivo no existe en el directorio."

   update_result(result, False, log)

def p_error(p):
   if p == None:
      error= "Error: No existe el arhivo especificado."
   else:
      error = f"Error de sintáxis en el carácter número: {p.lexpos+1}."
   log = ""
   update_result(error, True, log)
   
parser = yacc.yacc()

def update_result(result, error_flag, log):
   if error_flag == True:
      label_result.config(text="Script inválido.")
      label_description.config(text=result)
   else:
      label_result.config(text="Script válido.")
      label_description.config(text=result)
      label_log.insert('end', log)

def check_files():
   files = []
   dirs = os.popen("ls -p | grep -v /").read()
   files = dirs.splitlines()
   return files

def check_folders():
   folders = []
   dirs = os.popen("ls -d .*/ */").read()
   folders = dirs.splitlines()
   new_folders = [s.replace("/", "") for s in folders]
   return new_folders

def check_sudo():
   if "s" == script[0] and "u" == script[1] and "d" == script[2] and "o" == script[3] and " " == script[4]:
      return True
   else:
      return False

def clear_data():
   label_tokens.config(text="")
   label_positions.config(text="")
   label_result.config(text="")
   label_description.config(text="")
   entry_script.delete(0,"end")
   label_log.delete('1.0', END)

def evaluate_script(event):
   global script
   global tipos
   global posiciones

   tokens = []
   tipos = []
   posiciones = []
   script = entry_script.get()

   label_log.delete('1.0', END)

   if script == "clear":
      label_tokens.config(text="")
      label_positions.config(text="")
      label_result.config(text="")
      label_description.config(text="")
      entry_script.delete(0,"end")
   else:
      parser.parse(script)
      lexer.input(script)

      while True:
         token = lexer.token()
         if not token: 
            break
         tokens.append([token.value, token.type, token.lexpos])

      for i in range(len(tokens)):
         tipos.append(tokens[i][1])
         posiciones.append(tokens[i][2])

      label_tokens.config(text=f"Tokens: {tipos}")
      label_positions.config(text=f"Posiciones: {posiciones}")

def show_bash_clone():
   global entry_script
   global label_tokens
   global label_positions
   global label_result
   global label_description
   global label_log
   global background
   global font

   font = 'Helvetica 12'
   background = '#2A0944'
   frame = Frame(window, background=background)
   frame.place(relx=0, rely=0, relheight=1, relwidth=1)

   Label(frame, text='upchiapas@ubuntu', background=background, font='Helvetica 12 bold', fg='#FF37A6').place(x=5,y=5)
   Label(frame, text=':', background=background, font='Helvetica 12 bold', fg='white').place(x=160,y=4)
   Label(frame, text='~', background=background, font='Helvetica 12 bold', fg='#06BCC1').place(x=168,y=5)
   Label(frame, text='$', background=background, font=font, fg='white').place(x=179,y=5)

   entry_script = Entry(frame, width=66, background=background, font=font, fg='white', highlightthickness=0, border=0)
   entry_script.place(x=197,y=5)
   entry_script.focus_set()

   delete_boton = Button(text='Borrar', font='Helvetica 10 bold', bg='#F3B61F', fg='#2A0944', command=clear_data)
   delete_boton.place(x=630, y=10)

   window.bind('<Return>', evaluate_script)

   """ Analizador léxico """
   frame_lexico = LabelFrame(frame, text=' Analizador léxico ', font='Helvetica 12 bold', fg='white', background=background)
   frame_lexico.place(x=5, y=40)

   label_tokens = Label(frame_lexico, text='', background=background, font=font, fg='white', width=72, anchor='w', padx=10)
   label_tokens.pack()

   label_positions = Label(frame_lexico, text='', background=background, font=font, fg='white', width=72, anchor='w', padx=10)
   label_positions.pack()

   """ Analizador sintáctico """
   frame_sintactico = LabelFrame(frame, text=' Analizador sintáctico ', font='Helvetica 12 bold', fg='white', background=background)
   frame_sintactico.place(x=5, y=120)

   label_result = Label(frame_sintactico, text='', background=background, font=font, fg='white', width=72, anchor='w', padx=10)
   label_result.pack()

   label_description = Label(frame_sintactico, text='', background=background, width=72, font=font, fg='white', anchor='w', padx=10)
   label_description.pack()


   """ Analizador semántico """
   frame_semantico = LabelFrame(frame, text=' Analizador semántico ', font='Helvetica 12 bold', fg='white', background=background, width=70)
   frame_semantico.place(x=5, y=200)

   scrollbar = Scrollbar(frame_semantico)
   scrollbar.pack(side='right', fill='y')

   label_log = Text(frame_semantico, yscrollcommand=scrollbar.set, font=font, bg=background, fg='white', padx=10, width=70, height=15, relief='flat')
   label_log.pack()

   scrollbar.config(command=label_log.yview)

if __name__ == '__main__':
   window = Tk()
   window.title('[193269/193291] C3_A1_Analizador Semántico')
   window.configure(height=505, width=690, bg='#2A0944')
   window.eval('tk::PlaceWindow . center')

   show_bash_clone()

   window.mainloop()