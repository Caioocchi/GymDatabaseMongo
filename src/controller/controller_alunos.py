import pandas as pd
from model.Alunos import Alunos
from conexion.mongo_queries import MongoQueries

class Controller_Cliente:
    def __init__(self):
        self.mongo = MongoQueries()
        



        
    def inserir_Aluno(self) -> Alunos:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        cpf = input("Digite o número de CPF: ")

        if self.verifica_existencia_cliente(cpf):

            nome = input("Nome: ")
            telefone = input("Telefone: ")
            pagamento = input("Pagamento (A para adimplente e I para inadimplente): ")
            vencimento_mensalidade = input("Dia de vencimento da mensalidade: ")

            #Controller_Exercicios.listar_exercicios(self,oracle,need_connect= True)
            exercicio = input("Digite exercicio preferido: ")

            # Insere e persiste o novo cliente
            self.mongo.db["Alunos"].insert_one({"Cpf": cpf, "Nome_Aluno": nome,"Telefone": telefone,"Pagamento":pagamento,"Vencimento_Mensalidade": vencimento_mensalidade,"Alunos_Exercicio": exercicio})
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_aluno = self.recupera_cliente(cpf)
            # Cria um novo objeto Cliente
            nome = df_aluno.nome_aluno.values[0]
            cpf = df_aluno.cpf.values[0]
            pagamento = df_aluno.pagamento.values[0]
            vencimento = df_aluno.vencimento_mensalidade.values[0]
            telefone = df_aluno.telefone.values[0]
            exercicio = df_aluno.alunos_exercicios.values[0]
            novo_aluno = Alunos(nome,cpf,pagamento,vencimento,telefone,exercicio)
            # Exibe os atributos do novo cliente
            print(novo_aluno.to_string())
            self.mongo.close()
            # Retorna o objeto novo_cliente para utilização posterior, caso necessário
            return novo_aluno
        else:
            self.mongo.close()
            print(f"O CPF {cpf} já está cadastrado.")
            return None

        



    def atualizar_aluno(self) -> Alunos:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do cliente a ser alterado
        cpf = input("Insira o CPF do cliente a ser alterado:")

        # Verifica se o cliente existe na base de dados
        if not self.verifica_existencia_aluno(cpf):

            print("1 - Nome\n 2 - Telefone")
            aux = int(input("Insira qual atributo irá ser alterado"))
            #Alterar nome      
            if aux == 1:

                novo_nome = input("Insira o novo nome: ")

                self.mongo.db["Alunos"].update_one({"Cpf": f"{cpf}"}, {"$set": {"Nome_Aluno": novo_nome}})

                df_aluno = self.recupera_aluno(cpf)


                nome = df_aluno.nome_aluno.values[0]
                cpf = df_aluno.cpf.values[0]
                pagamento = df_aluno.pagamento.values[0]
                vencimento = df_aluno.vencimento_mensalidade.values[0]
                telefone = df_aluno.telefone.values[0]
                alunos_exercicios = df_aluno.alunos_exercicios.values[0]


                aluno_atualizado = Alunos(nome,cpf,pagamento,vencimento,telefone,alunos_exercicios)

                print(aluno_atualizado.to_string())

                return aluno_atualizado
            
            #Alterar Telefone
            elif aux == 2:
                while True:
                    novo_telefone = input("Insira o novo telefone: ")
                    if (len(str(novo_telefone))) > 11:
                        print("Telefone inválido")
                    else:
                        self.mongo.db["Alunos"].update_one({"Cpf": f"{cpf}"}, {"$set": {"Telefone": telefone}})
                        df_aluno = self.recupera_aluno(cpf)


                        nome = df_aluno.nome_aluno.values[0]
                        cpf = df_aluno.cpf.values[0]
                        pagamento = df_aluno.pagamento.values[0]
                        vencimento = df_aluno.vencimento_mensalidade.values[0]
                        telefone = df_aluno.telefone.values[0]
                        alunos_exercicios = df_aluno.alunos_exercicios.values[0]


                        aluno_atualizado = Alunos(nome,cpf,pagamento,vencimento,telefone,alunos_exercicios)

                        print(aluno_atualizado.to_string())

                        return aluno_atualizado
                    


    
    def excluir_cliente(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o CPF do Cliente a ser alterado
        cpf = input("CPF do Aluno que irá excluir: ")

        # Verifica se o cliente existe na base de dados
        if not self.verifica_existencia_aluno(cpf):            
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_aluno = self.recupera_aluno(cpf)
            # Revome o cliente da tabela
            self.mongo.db["Alunos"].delete_one({"Cpf":f"{cpf}"})

            df_aluno = self.recupera_aluno(cpf)


            nome = df_aluno.nome_aluno.values[0]
            cpf = df_aluno.cpf.values[0]
            pagamento = df_aluno.pagamento.values[0]
            vencimento = df_aluno.vencimento_mensalidade.values[0]
            telefone = df_aluno.telefone.values[0]
            alunos_exercicios = df_aluno.alunos_exercicios.values[0]


            aluno_excluido = Alunos(nome,cpf,pagamento,vencimento,telefone,alunos_exercicios)
            self.mongo.close()
            # Exibe os atributos do cliente excluído
            print("ALuno Removido com Sucesso!")
            print(aluno_excluido.to_string())
        else:
            self.mongo.close()
            print(f"O CPF {cpf} não existe.")

            

            
    def verifica_existencia_aluno(self, cpf:str=None, external:bool=False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_aluno = pd.DataFrame(self.mongo.db["ALunos"].find({"Cpf":f"{cpf}"}, {"Cpf": 1, "Nome_Aluno": 1, "_id": 0}))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_aluno.empty

    


    def recupera_aluno(self, cpf:str=None, external:bool=False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_aluno = pd.DataFrame(list(self.mongo.db["Alunos"].find({"Cpf":f"{cpf}"}, {"cpf": 1, "Nome_Aluno": 1, "_id": 0})))
        
        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_aluno