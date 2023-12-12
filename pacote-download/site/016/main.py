from flask import Flask, render_template, redirect, request, flash, send_from_directory
import json
import ast
import os
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY']='KRONNIE'

logado = False

@app.route('/')
def home():
    global logado
    logado = False
    return render_template('login.html')

@app.route('/adm')
def adm():
   if logado == True:
      with open('usuarios.json') as usuariosTemp:
       usuarios = json.load(usuariosTemp)
       
       return render_template("administrador.html", usuarios = usuarios)
   
   if logado == False:
     return redirect('/')
   
@app.route('/usuario')
def usuarios():
    if logado == True:
         arquivo = []
         for documento in os.listdir('arquivos'):
            arquivo.append(documento)
         return render_template('usuario.html', arquivos = arquivo)
    else:
         return redirect('/')



@app.route('/login', methods=['POST'])
def login():
    
    global logado
    
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    conect_BD = mysql.connector.connect(host='localhost', database='usuarios', user='root', password='')
    
    cont = 0
    if conect_BD.is_connected():
       print('conectado')
       cursur = conect_BD.cursor()
       cursur.execute('SELECT * FROM usuario;')
       usuariosBD = cursur.fetchall()
      
    for usuario in usuariosBD:
        cont += 1
        usuarioNome = str(usuario[1])
        usuarioSenha = str(usuario[2])
      
      
        if nome == 'adm' and senha == '000':
           logado = True
           return redirect('/adm')
        
        
        if usuarioNome == nome and usuarioSenha == senha:
           logado  = True
           return redirect('/usuario')
           
        if cont >= len(usuariosBD):
          flash('USUÁRIO INVÁLIDO!')
          return redirect("/")
    else:
          return redirect('/')
        
@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    global logado
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    conect_BD = mysql.connector.connect(host='localhost', database='usuarios', user='root', password='')
    
    if conect_BD.is_connected():
      cursur = conect_BD.cursor()
      cursur.execute(f"insert into usuario values(default, '{nome}', '{senha}');")
    if conect_BD.is_connected():
        cursur.close()
        conect_BD.close()

    
    logado = True
    flash(F'{nome} CADASTRADO!!')
    return redirect('/adm')
    
@app.route('/excluirUsuario', methods = ['POST'])
def excluirUsuario():
   usuario = request.form.get('usuarioPexcluir')
   usuarioDict = ast.literal_eval(usuario)
   nome = usuarioDict['nome']
   with open('usuarios.json') as usuariosTemp:
      usuariosJson = json.load(usuariosTemp)
      for c in usuariosJson:
         if c == usuarioDict:
            usuariosJson.remove(usuarioDict)
            with open('usuarios.json', 'w') as usuariosAexcluir:
               json.dump(usuariosJson, usuariosAexcluir, indent=4)


   flash(F'{nome} EXCLUIDO')
   return redirect('/adm')



@app.route("/upload", methods=['POST'])
def upload():

   arquivo = request.files.get('documento')
   nome_arquivo = arquivo.filename.replace(" ","-")
   arquivo.save(os.path.join('arquivos', nome_arquivo))
   flash('Arquivo salvo')
   return redirect('/adm')


@app.route('/download', methods = ['POST'])
def download():
   nomeArquivo = request.form.get('arquivosParaDownload')

   return send_from_directory('arquivos', nomeArquivo, as_attachment=True)


                      


    
          
          
if __name__ in "__main__":
   app.run(debug=True)