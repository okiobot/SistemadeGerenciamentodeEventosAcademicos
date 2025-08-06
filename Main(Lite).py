import sqlite3 as sql

conexao = sql.connect("BDEventosAcadêmicos")
cursor = conexao.cursor()

#cliente ver quais eventos tá inscrito

senha = "adm123"
 
cursor.execute ("DROP TABLE IF EXISTS Eventos")
cursor.execute ("DROP TABLE IF EXISTS Usuarios")
cursor.execute ("DROP TABLE IF EXISTS Inscritos")

User = cursor.execute ("CREATE TABLE Usuarios (ID INTEGER PRIMARY KEY, Nome, Telefone, InstituiçãoEnsino, Senha, Perfil)")
Events = cursor.execute ("CREATE TABLE Eventos (ID INTEGER PRIMARY KEY, Nome, TipoEvento, DataI, DataF, Horário, Local, QuantidadeParticipante, OrganizadorResponsável)")
Subs = cursor.execute("CREATE TABLE Inscritos (ID INTEGER PRIMARY KEY, ID_Usuario, ID_Evento, FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID), FOREIGN KEY (ID_Evento) REFERENCES Eventos(ID))")

def UsersTest():
    cursor.execute("INSERT INTO Usuarios VALUES (NULL, 'Ricardo', '61123456789', 'UNICEUB', 'Carros', 'ESTUDANTE')")
    conexao.commit()

def lin():
    print("=" * 90)

def login():
    try:
        while True:
            Lnome = input("Digite o nome: ")
            Lsenha = input("Digite a senha: ")
            
            cursor.execute("SELECT * FROM Usuarios WHERE Nome = ? AND Senha = ?", (Lnome, Lsenha))
            usuario = cursor.fetchone()
            
            if usuario:
                usuario_id = usuario[0]
                
                print("Login realizado com sucesso!")
                for t in cursor.execute("SELECT * FROM Eventos"):
                    print("Estes são os eventos disponíveis: ")
                    print(f"""ID: {t[0]} | Nome: {t[1]} | Tipo do Evento: {t[2]} | Data de Início: {t[3]} | Data Final: {t[4]} | Horário: {t[5]}H |
Local: {t[6]} | Quantidade de Participantes {t[7]} | Organizador Responsável: {t[8]}""")
                    lin()
            
                escolha = int(input("Escolha o evento que deseja participar(ID): "))
                cursor.execute("SELECT ID FROM Eventos WHERE ID = ?", (escolha,))
                evento = cursor.fetchone()

                if evento:
                    cursor.execute("SELECT * FROM Inscritos WHERE ID_Usuario = ? AND ID_Evento = ?", (usuario_id, escolha))
                    Jinscrito = cursor.fetchone()
                    
                    if Jinscrito:
                        print("Você já está inscrito neste evento")
                    else:
                        cursor.execute("INSERT INTO Inscritos (ID_Usuario, ID_Evento) VALUES (?, ?)", (usuario_id, escolha))
                        conexao.commit()
                        print("Inscrição realizada com sucesso!")
                     
                else:
                    print("Evento não encontrado")
            
            else:
                print("Usuário não cadastrado ou dados incorretos")
                lin()
                break
    
    except ValueError:
        print("Você inseriu um valor inválido")

def MenuGeral():
    try:
        lin()
        while True:
            escolha = int(input("""Escolha entre: 
[1] - Estudantes
[2] - Organizadores
"""))   

            if escolha == 1:
                MenuUser()
            
            elif escolha == 2:
                I = input("Digite a senha: ")
                if I == senha:
                    MenuADM()
                else:
                    print("Senha incorreta")

    except ValueError:
        print("Você escolheu uma opção inexistente")

def MenuUser():
        try:
            lin()
            escolha = int(input("""Escolha uma das opções abaixo: 
[1] - Cadastro de usuário
[2] - Inscrição de usuário
"""))

            if escolha == 1:
                    
                    lin()
                    Nome = input("Insira o nome do usuário: ")
                    while True:
                        Tel = input("Insira um telefone(55): ")
                        if len(Tel) > 11 or len(Tel) < 11:
                            print("Esse é um número inválido")
                            continue
                        else:
                            break
                    Senha = input("Insira uma senha: ")
                    IE = input("Insira a institução de ensino do usuário: ")
                    #fazer as faculdades credenciadas
                    while True:
                        Perfil = input("Escolha o perfil entre 'ESTUDANTE' ou 'PROFESSOR': ")
                        PerfilM = Perfil.upper()
                        if PerfilM == "ESTUDANTE" or PerfilM == "PROFESSOR":
                            cursor.execute(f"INSERT INTO Usuarios VALUES (NULL,'{Nome}','{Tel}','{IE}','{Senha}','{PerfilM}')")
                            conexao.commit()
                            print("Usuário cadastrado com sucesso!")
                            lin()
                            break
        
            if escolha == 2:
                login()

        except ValueError:
            print("Você inseriu um caracter inválido")

def MenuADM():
    try:
        lin()
        escolha = int(input("""Escolha uma das opções abaixo: 
[1] - Adicionar eventos                     
[2] - Verificar eventos disponíveis
[3] - Verificar usuários cadastrados
"""))

        if escolha == 1:
            lin()
            Nome = input("Digite o nome do evento: ") 
            TipoEvento = input("Qual o tipo do evento: ")
            
            while True:
                try:
                    DataI = int(input("Qual é a data de início: "))
                    DataF = int(input("E a data de finalização: "))
                    if DataF > 31 or DataI < 0:
                        print("Você inseriu um valor inválido")
                        continue
                    else:
                        break

                except ValueError:
                    print("Você inseriu um valor inválido")

            while True:
                try:
                    #pode negativo arruma
                    #ver pds do horario quebrado
                    Horario = int(input("Qual o horário do evento: "))
                    if Horario > 24 or Horario < 0:
                        print("O horário não pode ser maior que 24")
                        continue
                    else:
                        break
                
                except ValueError:
                    print("Você inseriu um valor inválido")
                    continue
                
            Local = input("Qual o local do evento: ")
            
            while True:
                try: 
                    QP = int(input("Qual a quantidade de participantes do evento: "))
                    
                    if QP < 0:
                        print("O valor não pode ser negativo")
                        continue
                    else:
                        break            
                
                except ValueError:
                    print("Você inseriu um valor inválido")
                    continue
           
            ORE = input("Qual é o organizador responsável do evento: ")
            cursor.execute(f"INSERT INTO Eventos VALUES (NULL, '{Nome}','{TipoEvento}','{DataI}','{DataF}','{Horario}','{Local}','{QP}','{ORE}')")
            print("Evento criado com sucesso!")
            lin()
            for a in cursor.execute("SELECT * FROM Eventos"):
                print(f"""ID: {a[0]} | Nome: {a[1]} | Tipo do Evento: {a[2]} | Data de Início: {a[3]} | Data Final: {a[4]} | Horário: {a[5]}H |
Local: {a[6]} | Quantidade de Part'icipantes {a[7]} | Organizador Responsável: {a[8]}""")
            lin()

        if escolha == 2:
            for v in cursor.execute("SELECT * FROM Eventos"):
                print(v)
                lin()
            
        if escolha == 3:
            cursor.execute("SELECT * FROM Usuarios")
            rows = cursor.fetchall()
            for t in rows:
                print(t)
                lin()
    
    except ValueError:
        print("Você digitou um caracter inválido")

while True: 
    UsersTest()
    MenuGeral()


'''
    for i in cursor.execute("SELECT * FROM Usuarios"):
        print(f"""ID: {i[0]} |Nome: {i[1]} | Telefone: {i[2]} | Instituição de Ensino: {i[3]} | Senha: *** | Perfil: {i[5]}""")
        
    for a in cursor.execute("SELECT * FROM Eventos"):
        print(f"""ID: {a[0]} | Nome: {a[1]} | Tipo do Evento: {a[2]} | Data de Início: {a[3]} | Data Final: {a[4]} | Horário: {a[5]}H |
Local: {a[6]} | Quantidade de Participantes {a[7]} | Organizador Responsável: {a[8]}""")
      
    for b in cursor.execute("SELECT * FROM Inscritos"):
        print(b)
'''

#Autenticação de usuários = esse vai ser junto com os outros 2