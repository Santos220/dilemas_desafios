import psycopg2
from psycopg2 import Error

def testar_conexao():
    try:
        conexao = psycopg2.connect(
            host="localhost",
            port="5433",
            database="torneio_db",
            user="admin",
            password="senha123"
        )
        
        cursor = conexao.cursor()
        
        print("[Conexão Realizada!]\n")
        
        # 3. Executando um comando de teste
        print("Consultando os algoritmos cadastrados...")
        cursor.execute("SELECT id_algoritmo, nome FROM algoritmo;")
        
        # 4. Pegando a resposta do banco
        algoritmos = cursor.fetchall()
        
        for algo in algoritmos:
            # algo[0] é o ID, algo[1] é o Nome
            print(f"ID: {algo[0]} | Nome: {algo[1]}")

    except Error as e:
        print(f"Erro ao conectar com o banco: {e}")
        
    finally:
        if 'conexao' in locals() and conexao:
            cursor.close()
            conexao.close()
            print("\n[Conexão Encerrada]")

if __name__ == "__main__":
    testar_conexao()