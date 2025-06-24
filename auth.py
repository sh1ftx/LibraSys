from rich.console import Console
from rich.prompt import Prompt

console = Console()

USUARIOS = {
    "admin": "@adm123"
}

def login():
    console.clear()
    console.print("[bold cyan]=== LOGIN ===[/bold cyan]\n")
    nickname = Prompt.ask("Usuário")
    
    if nickname == "admin":
        senha = Prompt.ask("Senha", password=True)
        if USUARIOS.get(nickname) != senha:
            console.print("[red]Senha incorreta![/red]")
            return None, False
    else:
        console.print("[yellow]Usuário comum detectado. Sem senha necessária.[/yellow]")
    
    console.print(f"[green]Bem vindo, {nickname}![/green]")
    is_admin = (nickname == "admin")
    return nickname, is_admin
