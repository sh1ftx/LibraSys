from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich.panel import Panel
from rich import box
from bson import ObjectId
from datetime import datetime
from db import colecao_livros, colecao_historico

console = Console()

def registrar_historico(livro_id, acao, detalhes=""):
    colecao_historico.insert_one({
        "livro_id": ObjectId(livro_id),
        "acao": acao,
        "detalhes": detalhes,
        "data": datetime.now()
    })

def adicionar_livro():
    console.clear()
    console.print(Panel.fit("[bold cyan]ADICIONAR LIVRO[/]"))
    titulo = Prompt.ask("Título")
    autor = Prompt.ask("Autor")
    ano = IntPrompt.ask("Ano de publicação")
    status = "disponível"

    livro = {
        "titulo": titulo,
        "autor": autor,
        "ano": ano,
        "status": status,
        "data_cadastro": datetime.now()
    }

    result = colecao_livros.insert_one(livro)
    registrar_historico(result.inserted_id, "Cadastro", f"Livro cadastrado com status '{status}'")

    console.print(f"[green]Livro '{titulo}' adicionado com sucesso![/green]")
    input("Pressione Enter para continuar...")

def listar_livros(filtro_status=None):
    console.clear()
    console.print(Panel.fit("[bold cyan]LISTAGEM DE LIVROS[/]"))

    query = {"status": filtro_status} if filtro_status else {}
    livros = list(colecao_livros.find(query))

    if not livros:
        console.print("[yellow]Nenhum livro encontrado com os critérios informados.[/yellow]")
        input("Pressione Enter para continuar...")
        return

    tabela = Table(title="Livros", box=box.MINIMAL_DOUBLE_HEAD)
    tabela.add_column("ID", style="dim", width=12)
    tabela.add_column("Título", style="cyan")
    tabela.add_column("Autor", style="magenta")
    tabela.add_column("Ano", justify="center")
    tabela.add_column("Status", style="green")

    for l in livros:
        tabela.add_row(str(l["_id"]), l["titulo"], l["autor"], str(l["ano"]), l["status"])

    console.print(tabela)
    input("Pressione Enter para continuar...")

def listar_livros_menu():
    console.clear()
    console.print(Panel.fit("[bold cyan]OPÇÕES DE LISTAGEM[/]"))
    console.print("[bold white]1.[/] Listar todos os livros")
    console.print("[bold white]2.[/] Listar apenas livros disponíveis")
    console.print("[bold white]3.[/] Listar apenas livros emprestados")
    console.print("[bold white]4.[/] Listar apenas livros reservados")
    console.print("[bold red]0.[/] Voltar")

    opcao = Prompt.ask("\nEscolha uma opção")

    match opcao:
        case "1": listar_livros()
        case "2": listar_livros("disponível")
        case "3": listar_livros("emprestado")
        case "4": listar_livros("reservado")
        case "0": return
        case _:
            console.print("[red]Opção inválida![/red]")
            input("Pressione Enter...")

def buscar_livros():
    console.clear()
    console.print(Panel.fit("[bold cyan]BUSCAR LIVROS POR FILTROS[/]"))
    titulo = Prompt.ask("Título (enter para ignorar)", default="").strip()
    autor = Prompt.ask("Autor (enter para ignorar)", default="").strip()
    ano_str = Prompt.ask("Ano (enter para ignorar)", default="").strip()
    status = Prompt.ask("Status (disponível, emprestado, reservado) (enter para ignorar)", default="").strip().lower()

    query = {}
    if titulo:
        query["titulo"] = {"$regex": titulo, "$options": "i"}
    if autor:
        query["autor"] = {"$regex": autor, "$options": "i"}
    if ano_str.isdigit():
        query["ano"] = int(ano_str)
    if status in ("disponível", "emprestado", "reservado"):
        query["status"] = status

    livros = list(colecao_livros.find(query))
    if not livros:
        console.print("[yellow]Nenhum livro encontrado com os filtros aplicados.[/yellow]")
        input("Pressione Enter para continuar...")
        return

    tabela = Table(title="Resultado da busca", box=box.MINIMAL_DOUBLE_HEAD)
    tabela.add_column("ID", style="dim", width=12)
    tabela.add_column("Título", style="cyan")
    tabela.add_column("Autor", style="magenta")
    tabela.add_column("Ano", justify="center")
    tabela.add_column("Status", style="green")

    for l in livros:
        tabela.add_row(str(l["_id"]), l["titulo"], l["autor"], str(l["ano"]), l["status"])

    console.print(tabela)
    input("Pressione Enter para continuar...")

def emprestar_livro():
    console.clear()
    console.print(Panel.fit("[bold cyan]EMPRESTAR LIVRO[/]"))
    listar_livros("disponível")

    livro_id = Prompt.ask("Digite o ID do livro para emprestar").strip()
    try:
        livro = colecao_livros.find_one({"_id": ObjectId(livro_id)})
        if not livro:
            console.print("[red]Livro não encontrado.[/red]")
        elif livro["status"] != "disponível":
            console.print(f"[yellow]Livro está com status '{livro['status']}', não pode ser emprestado.[/yellow]")
        else:
            colecao_livros.update_one({"_id": ObjectId(livro_id)}, {"$set": {"status": "emprestado"}})
            registrar_historico(livro_id, "Empréstimo", "Livro emprestado.")
            console.print(f"[green]Livro '{livro['titulo']}' emprestado com sucesso![/green]")
    except Exception as e:
        console.print(f"[red]Erro: {e}[/red]")
    input("Pressione Enter para continuar...")

def devolver_livro():
    console.clear()
    console.print(Panel.fit("[bold cyan]DEVOLVER LIVRO[/]"))
    listar_livros("emprestado")

    livro_id = Prompt.ask("Digite o ID do livro para devolver").strip()
    try:
        livro = colecao_livros.find_one({"_id": ObjectId(livro_id)})
        if not livro:
            console.print("[red]Livro não encontrado.[/red]")
        elif livro["status"] != "emprestado":
            console.print(f"[yellow]Livro está com status '{livro['status']}', não pode ser devolvido.[/yellow]")
        else:
            colecao_livros.update_one({"_id": ObjectId(livro_id)}, {"$set": {"status": "disponível"}})
            registrar_historico(livro_id, "Devolução", "Livro devolvido.")
            console.print(f"[green]Livro '{livro['titulo']}' devolvido com sucesso![/green]")
    except Exception as e:
        console.print(f"[red]Erro: {e}[/red]")
    input("Pressione Enter para continuar...")

def visualizar_historico():
    console.clear()
    console.print(Panel.fit("[bold cyan]HISTÓRICO DE ALTERAÇÕES[/]"))
    listar_livros()
    livro_id = Prompt.ask("Digite o ID do livro para visualizar histórico").strip()
    try:
        historico = list(colecao_historico.find({"livro_id": ObjectId(livro_id)}).sort("data", -1))
        if not historico:
            console.print("[yellow]Nenhum histórico encontrado para este livro.[/yellow]")
        else:
            tabela = Table(title="Histórico", box=box.MINIMAL_DOUBLE_HEAD)
            tabela.add_column("ID", style="dim", width=12)
            tabela.add_column("Ação", style="cyan")
            tabela.add_column("Detalhes", style="magenta")
            tabela.add_column("Data", style="green")

            for h in historico:
                tabela.add_row(str(h["_id"]), h["acao"], h["detalhes"], h["data"].strftime("%d/%m/%Y %H:%M:%S"))

            console.print(tabela)
    except Exception as e:
        console.print(f"[red]Erro: {e}[/red]")
    input("Pressione Enter para continuar...")

def atualizar_livro(is_admin=False):
    console.clear()
    console.print(Panel.fit("[bold cyan]ATUALIZAR INFORMAÇÕES DO LIVRO[/]"))
    listar_livros()
    livro_id = Prompt.ask("Digite o ID do livro para atualizar").strip()
    try:
        livro = colecao_livros.find_one({"_id": ObjectId(livro_id)})
        if not livro:
            console.print("[red]Livro não encontrado.[/red]")
            input("Pressione Enter...")
            return

        console.print(f"Título atual: {livro['titulo']}")
        novo_titulo = Prompt.ask("Novo título (enter para manter)", default=livro['titulo'])
        console.print(f"Autor atual: {livro['autor']}")
        novo_autor = Prompt.ask("Novo autor (enter para manter)", default=livro['autor'])
        console.print(f"Ano atual: {livro['ano']}")
        novo_ano = Prompt.ask("Novo ano (enter para manter)", default=str(livro['ano']))

        updates = {
            "titulo": novo_titulo,
            "autor": novo_autor,
            "ano": int(novo_ano) if novo_ano.isdigit() else livro['ano']
        }

        if is_admin:
            console.print(f"Status atual: {livro['status']}")
            novo_status = Prompt.ask("Novo status (disponível, emprestado, reservado) (enter para manter)", default=livro['status']).lower()
            if novo_status in ("disponível", "emprestado", "reservado"):
                updates["status"] = novo_status

        colecao_livros.update_one({"_id": ObjectId(livro_id)}, {"$set": updates})
        registrar_historico(livro_id, "Atualização", f"Campos atualizados: {list(updates.keys())}")
        console.print("[green]Livro atualizado com sucesso![/green]")
    except Exception as e:
        console.print(f"[red]Erro: {e}[/red]")
    input("Pressione Enter para continuar...")

def apagar_livro():
    console.clear()
    console.print(Panel.fit("[bold red]APAGAR LIVRO[/]"))
    listar_livros()
    livro_id = Prompt.ask("Digite o ID do livro para apagar").strip()
    try:
        livro = colecao_livros.find_one({"_id": ObjectId(livro_id)})
        if not livro:
            console.print("[red]Livro não encontrado.[/red]")
            input("Pressione Enter...")
            return

        confirm = Prompt.ask(f"Confirma apagar o livro '{livro['titulo']}'? (s/n)", choices=["s", "n"])
        if confirm == "s":
            colecao_livros.delete_one({"_id": ObjectId(livro_id)})
            colecao_historico.delete_many({"livro_id": ObjectId(livro_id)})
            console.print("[green]Livro e histórico apagados com sucesso![/green]")
        else:
            console.print("[yellow]Operação cancelada.[/yellow]")
    except Exception as e:
        console.print(f"[red]Erro: {e}[/red]")
    input("Pressione Enter para continuar...")

def gerenciar_historico():
    console.clear()
    console.print(Panel.fit("[bold red]GERENCIAR HISTÓRICO[/]"))
    historico = list(colecao_historico.find().sort("data", -1))
    if not historico:
        console.print("[yellow]Nenhum registro de histórico encontrado.[/yellow]")
        input("Pressione Enter para continuar...")
        return

    tabela = Table(title="Histórico Geral", box=box.MINIMAL_DOUBLE_HEAD)
    tabela.add_column("ID", style="dim", width=12)
    tabela.add_column("Livro ID", style="cyan")
    tabela.add_column("Ação", style="magenta")
    tabela.add_column("Detalhes", style="green")
    tabela.add_column("Data", style="white")

    for h in historico:
        tabela.add_row(str(h["_id"]), str(h["livro_id"]), h["acao"], h["detalhes"], h["data"].strftime("%d/%m/%Y %H:%M:%S"))

    console.print(tabela)

    apagar_id = Prompt.ask("Digite o ID do registro para apagar (enter para sair)", default="").strip()
    if apagar_id:
        try:
            result = colecao_historico.delete_one({"_id": ObjectId(apagar_id)})
            if result.deleted_count == 1:
                console.print("[green]Registro apagado com sucesso![/green]")
            else:
                console.print("[yellow]Registro não encontrado.[/yellow]")
        except Exception as e:
            console.print(f"[red]Erro: {e}[/red]")
    input("Pressione Enter para continuar...")

def menu_biblioteca(is_admin=False):
    while True:
        console.clear()
        console.print(Panel.fit("[bold cyan]MENU BIBLIOTECA[/]", subtitle="Administração" if is_admin else "Usuário"))
        console.print("[bold white]1.[/] Adicionar livro")
        console.print("[bold white]2.[/] Listar livros")
        console.print("[bold white]3.[/] Buscar livros por filtros")
        console.print("[bold white]4.[/] Emprestar livro")
        console.print("[bold white]5.[/] Devolver livro")
        console.print("[bold white]6.[/] Visualizar histórico de um livro")
        console.print("[bold white]7.[/] Atualizar informações de um livro")

        if is_admin:
            console.print("[bold red]8.[/] Apagar livro")
            console.print("[bold red]9.[/] Gerenciar histórico (apagar registros)")

        console.print("[bold red]0.[/] Voltar")

        opcao = Prompt.ask("\nEscolha uma opção")

        match opcao:
            case "1": adicionar_livro()
            case "2": listar_livros_menu()
            case "3": buscar_livros()
            case "4": emprestar_livro()
            case "5": devolver_livro()
            case "6": visualizar_historico()
            case "7": atualizar_livro(is_admin)
            case "8" if is_admin: apagar_livro()
            case "9" if is_admin: gerenciar_historico()
            case "0": return
            case _:
                console.print("[red]Opção inválida![/red]")
                input("Pressione Enter para continuar...")
