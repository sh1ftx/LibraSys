# Feito por Kay
from auth import login
from ui import menu_principal, menu_biblioteca, menu_administracao
from biblioteca import menu_biblioteca as menu_biblioteca_func

def main():
    while True:
        nickname, is_admin = login()
        if nickname is None:
            print("Login falhou. Saindo...")
            break

        while True:
            escolha = menu_principal(is_admin)

            if escolha == "0":
                print("Saindo do sistema. Até logo!")
                return

            elif escolha == "1":
                # Menu principal da biblioteca
                menu_biblioteca_func(is_admin)

            elif escolha == "2" and is_admin:
                # Menu administração (ainda básico, pode expandir)
                while True:
                    adm_escolha = menu_administracao()
                    if adm_escolha == "0":
                        break
                    else:
                        print(f"Opção '{adm_escolha}' da administração ainda não implementada.")
                        input("Pressione Enter para continuar...")

            else:
                print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()
