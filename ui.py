from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.table import Table
from rich.align import Align

console = Console()

def painel_titulo(text="GERENCIADOR DE BIBLIOTECA"):
    console.clear()
    painel = Panel.fit(
        f"📚 [bold cyan]{text}[/bold cyan]",
        style="bold green",
        subtitle="Powered by MongoDB + Python",
        padding=(1, 4),
        border_style="bright_blue"
    )
    console.print(Align.center(painel))

def menu_principal(is_admin=False):
    painel_titulo()
    console.print()
    console.print("[bold white]1.[/] 📚 Biblioteca")
    if is_admin:
        console.print("[bold white]2.[/] 🔒 Administração")
    console.print("[bold red]0.[/] 🚪 Sair\n")

    escolha = Prompt.ask("[bold cyan]Escolha uma opção[/bold cyan]", choices=["1","2","0"] if is_admin else ["1","0"])
    return escolha

def menu_administracao():
    console.clear()
    painel = Panel.fit("[bold magenta]Área Administrativa[/bold magenta]", style="magenta", border_style="magenta")
    console.print(Align.center(painel))
    console.print("[bold white]1.[/] Gerenciar usuários (em breve)")
    console.print("[bold white]2.[/] Relatórios (em breve)")
    console.print("[bold red]0.[/] Voltar\n")

    escolha = Prompt.ask("[bold cyan]Escolha uma opção[/bold cyan]", choices=["1","2","0"])
    return escolha

def menu_biblioteca(is_admin=False):
    console.clear()
    painel = Panel.fit("[bold cyan]MENU BIBLIOTECA[/bold cyan]", border_style="cyan")
    console.print(Align.center(painel))
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
    console.print("[bold red]0.[/] Voltar\n")

    opcoes = ["0","1","2","3","4","5","6","7"]
    if is_admin:
        opcoes += ["8","9"]

    escolha = Prompt.ask("[bold cyan]Escolha uma opção[/bold cyan]", choices=opcoes)
    return escolha

def submenu_listagem():
    console.clear()
    painel = Panel.fit("[bold cyan]OPÇÕES DE LISTAGEM[/bold cyan]", border_style="cyan")
    console.print(Align.center(painel))
    console.print("[bold white]1.[/] Listar todos os livros")
    console.print("[bold white]2.[/] Listar apenas livros disponíveis")
    console.print("[bold white]3.[/] Listar apenas livros emprestados")
    console.print("[bold white]4.[/] Listar apenas livros reservados")
    console.print("[bold red]0.[/] Voltar\n")

    escolha = Prompt.ask("[bold cyan]Escolha uma opção[/bold cyan]", choices=["0","1","2","3","4"])
    return escolha

def mostrar_tabela_livros(livros):
    if not livros:
        console.print("[yellow]Nenhum livro encontrado.[/yellow]")
        return

    tabela = Table(title="Livros", box="MINIMAL_DOUBLE_HEAD", border_style="bright_blue")
    tabela.add_column("ID", style="dim", width=12)
    tabela.add_column("Título", style="cyan")
    tabela.add_column("Autor", style="magenta")
    tabela.add_column("Ano", justify="center")
    tabela.add_column("Status", style="green")

    for l in livros:
        tabela.add_row(str(l["_id"]), l["titulo"], l["autor"], str(l["ano"]), l["status"])

    console.print(tabela)

def mostrar_tabela_historico(historicos):
    if not historicos:
        console.print("[yellow]Nenhum registro de histórico encontrado.[/yellow]")
        return

    tabela = Table(title="Histórico", box="MINIMAL_DOUBLE_HEAD", border_style="bright_magenta")
    tabela.add_column("ID", style="dim", width=12)
    tabela.add_column("Ação", style="cyan")
    tabela.add_column("Detalhes", style="magenta")
    tabela.add_column("Data", style="green")

    for h in historicos:
        tabela.add_row(str(h["_id"]), h["acao"], h["detalhes"], h["data"].strftime("%d/%m/%Y %H:%M:%S"))

    console.print(tabela)

def mensagem_sucesso(texto):
    console.print(f"[green]✔ {texto}[/green]")

def mensagem_erro(texto):
    console.print(f"[red]✘ {texto}[/red]")

def mensagem_aviso(texto):
    console.print(f"[yellow]⚠ {texto}[/yellow]")

def esperar():
    console.print()
    input("[bold cyan]Pressione Enter para continuar...[/bold cyan]")
