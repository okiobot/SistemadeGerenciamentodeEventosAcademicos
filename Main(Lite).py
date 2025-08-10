import sqlite3 as sql

#Conexão usada para operações no banco de dados (CRUD)
conexao = sql.connect("BDEventosAcadêmicos")

#Cursor usado para operação na manipulação dos dados
cursor = conexao.cursor()

#Senha imaginária para acesso de funcionalidades administrativas
senha = "adm123"

#Exclusão das tabelas (desnecessário caso o usuário deseje que as informações persistam mesmo depois de fechar a aplicação)
cursor.execute ("DROP TABLE IF EXISTS Eventos")
cursor.execute ("DROP TABLE IF EXISTS Usuarios")
cursor.execute ("DROP TABLE IF EXISTS Inscritos")
cursor.execute("DROP TABLE IF EXISTS Certificados")

#Criação das tabelas
User = cursor.execute ("CREATE TABLE Usuarios (ID INTEGER PRIMARY KEY, Nome, Telefone, InstituiçãoEnsino, Senha, Perfil)")
Events = cursor.execute ("CREATE TABLE Eventos (ID INTEGER PRIMARY KEY, Nome, TipoEvento, DataI, DataF, Horário, Local, QuantidadeParticipantes, OrganizadorResponsável, Vagas)")
Subs = cursor.execute("CREATE TABLE Inscritos (ID INTEGER PRIMARY KEY, ID_Usuario, ID_Evento, FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID), FOREIGN KEY (ID_Evento) REFERENCES Eventos(ID))")
Licence = cursor.execute("CREATE TABLE Certificados (ID INTEGER PRIMARY KEY, ID_Evento, EventoNome, ID_Usuario, UsuarioNome, FOREIGN KEY (ID_Evento) REFERENCES Eventos(ID), FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID))")

#Inserts utilizados para testes
def UsersTest():
    cursor.execute("INSERT INTO Usuarios VALUES (NULL, 'Ricardo', '61123456789', 'UNICEUB', 'Carros', 'ESTUDANTE')")
    cursor.execute("INSERT INTO Usuarios VALUES (NULL, 'Marcos', '61999999999', 'UNICEUB', 'MAT', 'PROFESSOR')")
    conexao.commit()

def EventsTest():
    cursor.execute("INSERT INTO Eventos VALUES (NULL, 'INNOVA Summit','Palestra','20','23','14','São Paulo','1500','Caito Maia','1')")
    conexao.commit()

#Linha utilizada para demilitação 
def lin():
    print("=" * 90)

#Login do usuário em um conta já cadastrada
def Login():
    try:
        lin()
        Lnome = input("Digite o nome: ")
        Lsenha = input("Digite a senha: ")
        lin()
            
        print("Login realizado com sucesso!")
        while True:
            cursor.execute("SELECT * FROM Usuarios WHERE Nome = ? AND Senha = ?", (Lnome, Lsenha))
            usuario = cursor.fetchone()
            
            if usuario:
                usuario_id = usuario[0]
                lin()
                
                escolha = int(input("""Escolha uma das opções: 
[1] - Inscrever-se em eventos disponíveis
[2] - Verificar eventos inscritos
[3] - Certificados adquiridos
[0] - Voltar
"""))
                
                if escolha == 1:
                    for t in cursor.execute("SELECT * FROM Eventos"):
                        print("Estes são os eventos disponíveis: ")
                        print(f"""ID: {t[0]} | Nome: {t[1]} | Tipo do Evento: {t[2]} | Data de Início: {t[3]} | Data Final: {t[4]} | Horário: {t[5]}H |
Local: {t[6]} | Quantidade de Participantes {t[7]} | Organizador Responsável: {t[8]}""")
                        lin()
                
                    escolha = int(input("Escolha o evento que deseja participar(ID): "))
                    cursor.execute("SELECT ID FROM Eventos WHERE ID = ?", (escolha,))
                    evento = cursor.fetchone()
                    
                    cursor.execute("SELECT Vagas FROM Eventos WHERE ID = ?", (escolha,))
                    c = cursor.fetchone()
                    quant = int(c[0])
                    
                    #Caso o evento não possua mais vagas, a nova inscrição do usuário será negada
                    if quant == 0:
                        print("Não há mais vagas disponíveis")
                        
                    else:
                        if evento:
                            cursor.execute("SELECT * FROM Inscritos WHERE ID_Usuario = ? AND ID_Evento = ?", (usuario_id, escolha))
                            Jinscrito = cursor.fetchone()
                            
                            if Jinscrito:
                                print("Você já está inscrito neste evento")
                            else:
                               
                                #Quando um usuário é inscrito em um evento, a quantidade de vagas diminuí em 1
                                cursor.execute("INSERT INTO Inscritos (ID_Usuario, ID_Evento) VALUES (?, ?)", (usuario_id, escolha))
                                novoQ = quant - 1
                                cursor.execute("UPDATE Eventos SET Vagas = ? WHERE ID = ?", (novoQ,escolha))
                                conexao.commit()
                                print("Inscrição realizada com sucesso!")
                            
                        else:
                            print("Evento não encontrado")
                
                elif escolha == 2:
                    print("Estes são os eventos em que o usuário está inscrito: ")
                    cursor.execute("SELECT I.ID, I.ID_Usuario, I.ID_Evento, E.Nome FROM Inscritos I JOIN Eventos E ON I.ID_Evento = E.ID WHERE I.ID_Usuario = ?", (usuario_id,))
                    inscritos = cursor.fetchall()
            
                    if inscritos:
                        for w in inscritos:
                            print(f"ID da inscrição: {w[0]} | ID do Usuário: {w[1]} | ID do Evento: {w[2]} | Nome do Evento: {w[3]}")
                            lin()     
                    else: 
                        print("O usuário não está inscrito em nenhum evento no momento")
    
                elif escolha == 3:
                    print("Certificados emitidos:")
                    cursor.execute("SELECT * FROM Certificados WHERE ID_Usuario = ?", (usuario_id,))
                    certificados = cursor.fetchall()
                    
                    if certificados:
                        for n in certificados:
                            print(f"ID do Certificado: {n[0]} | ID do Evento: {n[1]} | Nome do Evento: {n[2]} | ID do Usuário: {n[3]} | Nome do Usuário: {n[4]}")
                    else:
                        print("O usuário não possui certificados ainda")
                    
                elif escolha == 0:
                    lin()
                    break
                    
            else:
                print("Usuário não cadastrado ou dados incorretos")
                lin()
                break
    
    except ValueError:
        print("Você inseriu um valor inválido")
        return

#Função para emitir certificado para todos os estudantes que estavam inscritos no curso selecionado, depois o exclui do banco de dados
def EmitirCertificado():
    try:
        cert = int(input("Escolha qual evento deseja finalizar e emitir certificados(ID): "))
        cursor.execute("SELECT * FROM Eventos WHERE ID = ?", (cert,))
        Evento = cursor.fetchone()
        
        if not Evento:
           print("Evento não encontrado")
           return
           
        EventoNome = Evento[1]      
        cursor.execute("SELECT ID_Usuario FROM Inscritos WHERE ID_Evento = ?", (cert,))
        Inscritos = cursor.fetchall()
        
        if not Inscritos:
            print("Nenhum usuário inscrito neste evento")
            lin()
            return

        for o in Inscritos:
            IDUsuario = o[0]
            cursor.execute("SELECT Nome FROM Usuarios WHERE ID = ?", (IDUsuario,))
            NomeUsuario = cursor.fetchone()[0]
            
            cursor.execute("SELECT * FROM Certificados WHERE ID_Evento = ? AND ID_Usuario = ?", (cert, IDUsuario))
            existe = cursor.fetchone()
            
            if existe:
                print(f"Certificado já emitido para {NomeUsuario}")
                
            else:
                cursor.execute("INSERT INTO Certificados (ID_Evento, EventoNome, ID_Usuario, UsuarioNome) VALUES (?,?,?,?)", (cert, EventoNome, IDUsuario, NomeUsuario))
                print(f"Certificado emitido para {NomeUsuario}")
        
        conexao.commit()
        print("Certificados emitidos com sucesso!")
        lin()
       
        #Deleta o evento depois de emitir os certificados aos usuários
        cursor.execute("DELETE FROM Eventos WHERE ID = ?", (cert,))
        print("Evento finalizado")
        conexao.commit()
        lin()            

    except ValueError:
        print("Você inseriu um valor inválido")

#Função para o usuário escolher as funções que deseja utilizar
def MenuGeral():
    try:
        lin()
        while True:
            escolha = int(input("""Escolha entre: 
[1] - Estudantes
[2] - Organizadores
"""))   

            if escolha == 1:
                MenuUserE()
            
            elif escolha == 2:
                I = input("Digite a senha: ")
                if I == senha:
                    MenuADM()
                else:
                    print("Senha incorreta")

    except ValueError:
        print("Você escolheu uma opção inexistente")

#Função para cadastro dos usuários
def MenuUserE():
    try:
        lin()
        escolha = int(input("""Escolha uma das opções abaixo: 
[1] - Cadastro de usuário
[2] - Login de usuário
"""))

        if escolha == 1:
            lin()
            while True:
                Nome = input("Insira o nome do usuário: ")
                if len(Nome) == 0:
                    print("O nome do usuário não pode estar vazio")
                    lin()
                    continue
                else:
                    break
            
            while True:
                Tel = (input("Insira um telefone(55): "))
                if len(Tel) > 11 or len(Tel) < 11:
                    print("Esse é um número inválido")
                    lin()
                else:
                    lin()
                    break
            
            while True:
                Senha = input("Insira uma senha: ")
                if len(Senha) == 0:
                    print("A senha do usuário não pode estar vazio")
                    lin()
                    continue
                else:
                    break
            lin()
            
            while True:
                IE = input("Insira a institução de ensino do usuário: ")
                if len(IE) == 0:
                    print("A instituição do usuário não pode estar vazia")
                    lin()
                    continue
                else:
                    break
            lin()
                 
            #fazer as faculdades credenciadas
            cursor.execute(f"INSERT INTO Usuarios VALUES (NULL,'{Nome}','{Tel}','{IE}','{Senha}','ESTUDANTE')")
            lin()
            conexao.commit()
            print("Usuário cadastrado com sucesso!")

        elif escolha == 2:
            Login()

    except ValueError:
        print("Você inseriu um valor inválido")

#Função para cadastrar professores credenciados
def MenuOrgP():
    try:
        while True:
            Nome = input("Insira o nome do usuário: ")
            if len(Nome) == 0:
                print("O nome do usuário não pode estar vazio")
                lin()
                continue
            else:
                break
        
        while True:
            Tel = (input("Insira um telefone(55): "))
            if len(Tel) > 11 or len(Tel) < 11:
                print("Esse é um número inválido")
                lin()
            else:
                lin()
                break
        
        while True:
            Senha = input("Insira uma senha: ")
            if len(Senha) == 0:
                print("A senha do usuário não pode estar vazio")
                lin()
                continue
            else:
                break
        lin()
        
        while True:
            IE = input("Insira a institução de ensino do usuário: ")
            if len(IE) == 0:
                print("A instituição do usuário não pode estar vazia")
                lin()
                continue
            else:
                break
        lin()

        cursor.execute(f"INSERT INTO Usuarios VALUES (NULL,'{Nome}','{Tel}','{IE}','{Senha}','PROFESSOR')")
        lin()
        conexao.commit()
        print("Usuário cadastrado com sucesso!")
        lin()
    except ValueError:
        print("Você inseriu um caracter inválido")

#Função para apresentação e utilização das funcionalidades exclusivas para organizadores
def MenuADM():
    try:
        lin()
        while True:
            escolha = int(input("""Escolha uma das opções abaixo: 
[1] - Adicionar eventos                     
[2] - Cadastrar um professor
[3] - Verificar eventos disponíveis 
[4] - Verificar usuários cadastrados
[5] - Emitir certificados
[0] - Voltar  
"""))

            if escolha == 1:
                lin()
                while True:
                    Nome = input("Insira o nome do evento: ")
                    if len(Nome) == 0:
                        print("O nome do evento não pode estar vazio")
                        lin()
                        continue
                    else:
                        break 
                
                while True:
                    TipoEvento = input("Qual o tipo do evento: ")
                    if len(TipoEvento) == 0:
                        print("O tipo do evento não pode estar vazio")
                        lin()
                        continue
                    else:
                        break
                
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
                        Horario = int(input("Qual o horário do evento: "))
                        if Horario > 24: 
                            print("O horário não pode ser maior que 24")
                            continue
                        elif Horario < 0:
                            print("O horário não pode ser menor que 0")
                            continue
                        else:
                            break
                    
                    except ValueError:
                        print("Você inseriu um valor inválido")
                        continue
                    
                while True:
                    Local = input("Qual o local do evento: ")
                    if len(Local) == 0:
                        print("O local do evento não pode estar vazio")
                        lin()
                        continue
                    else:
                        break
                
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
                cursor.execute(f"INSERT INTO Eventos VALUES (NULL, '{Nome}','{TipoEvento}','{DataI}','{DataF}','{Horario}','{Local}','{QP}','{ORE}', {QP})")
                print("Evento criado com sucesso!")
                lin()

            if escolha == 2:
                MenuOrgP()
            
            if escolha == 3:
                for a in cursor.execute("SELECT * FROM Eventos"):
                    print(f"""ID: {a[0]} | Nome: {a[1]} | Tipo do Evento: {a[2]} | Data de Início: {a[3]} | Data Final: {a[4]} | Horário: {a[5]}H |
Local: {a[6]} | Quantidade de Participantes {a[7]} | Organizador Responsável: {a[8]} | Vagas disponíveis: {a[9]}""")
                lin()
                
            if escolha == 4:
                try:
                    lin()
                    al = int(input("""Deseja verificar quais usuários?:
[1] - Apenas estudantes
[2] - Apenas professores
[3] - Todos
[0] - Voltar
"""))
                    if al == 1:
                        for t in cursor.execute("SELECT * FROM Usuarios WHERE Perfil = 'ESTUDANTE'"):
                            print(f"""ID: {t[0]}  |Nome: {t[1]} | Telefone: {t[2]} | Instituição de Ensino: {t[3]} | Senha: *** | Perfil: {t[5]}""")
                            lin()

                    elif al == 2:
                        for l in cursor.execute("SELECT * FROM Usuarios WHERE Perfil = 'PROFESSOR'"):
                            print(f"""ID: {l[0]} | Nome: {l[1]} | Telefone: {l[2]} | Instituição de Ensino: {l[3]} | Senha: *** | Perfil: {l[5]}""")
                            lin()
                            
                    elif al == 3:
                        for i in cursor.execute("SELECT * FROM Usuarios"):
                            print(f"""ID: {i[0]} | Nome: {i[1]} | Telefone: {i[2]} | Instituição de Ensino: {i[3]} | Senha: *** | Perfil: {i[5]}""")
                            lin()
                    
                    elif al == 0:
                        lin()
                        break
                      
                except ValueError:
                    print("Valor inválido inserido")

            if escolha == 5:
                EmitirCertificado()
                    
            if escolha == 0:
                lin()
                break

    except ValueError:
        print("Você digitou um caracter inválido")

#Execução das funções de teste
UsersTest()
EventsTest()

while True: 
    MenuGeral()
