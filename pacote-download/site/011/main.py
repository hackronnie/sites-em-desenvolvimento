from flask import Flask, render_template, redirect, request, flash
import json

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

@app.route('/login', methods=['POST'])
def login():
    
    global logado
    
    nome = request.form.get('nome')
    senha = request.form.get('senha')

    with open('usuarios.json') as usuariosTemp:
     usuarios = json.load(usuariosTemp)

     cont = 0

     for usuario in usuarios:
        cont += 1
      
        if nome == 'adm' and senha == '000':
           logado = True
           return redirect('/adm')
        
        
        if usuario['nome'] == nome and usuario['senha'] == senha:
            return render_template('usuario.html')
           
        if cont >= len(usuarios):
          flash('USUÁRIO INVÁLIDO!')
          return redirect("/")
        
@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    user =[]
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    user = [
       {
          "nome":nome,
          "senha":senha
       }
    ]
    with open('usuarios.json') as usuariosTemp:
     usuarios = json.load(usuariosTemp)

     usuarioNovo = user + usuarios

    with open('usuarios.json','w') as gravarTemp:
     json.dump(usuarioNovo, gravarTemp, indent=4)

     flash('Usuário Cadastrado com sucesso!')
     return redirect('/adm')



           
           


    
          
          
if __name__ in "__main__":
   app.run(debug=True)