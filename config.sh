#!/bin/bash

# Detecta distribuição Linux
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo "$ID"
    else
        echo "unknown"
    fi
}

DISTRO=$(detect_distro)
echo -e "\n[INFO] Sistema detectado: \033[1;32m$DISTRO\033[0m"

# Instala Python, venv, pip, MongoDB
install_dependencies() {
    echo -e "\n[INFO] Instalando dependências..."

    case "$DISTRO" in
        ubuntu|debian)
            sudo apt update
            sudo apt install -y python3 python3-venv python3-pip mongodb
            sudo systemctl enable mongodb
            sudo systemctl start mongodb
            ;;
        arch)
            sudo pacman -Sy --noconfirm python python-virtualenv python-pip mongodb
            sudo systemctl enable mongodb
            sudo systemctl start mongodb
            ;;
        fedora)
            sudo dnf install -y python3 python3-venv python3-pip mongodb
            sudo systemctl enable mongod
            sudo systemctl start mongod
            ;;
        *)
            echo -e "[ERRO] Distribuição \033[1;31m$DISTRO\033[0m não suportada automaticamente."
            exit 1
            ;;
    esac
}

# Instala dependências
install_dependencies

# Cria ambiente virtual
echo -e "\n[INFO] Criando ambiente virtual em \033[1;34mconfigs/\033[0m"
python3 -m venv configs || { echo -e "[ERRO] Falha ao criar venv."; exit 1; }

# Ativa venv e instala pacotes
echo -e "\n[INFO] Instalando bibliotecas no ambiente virtual..."
./configs/bin/pip install --upgrade pip
./configs/bin/pip install pymongo rich

# Executa o main.py
echo -e "\n[INFO] Executando \033[1;36mmain.py\033[0m...\n"
if [ -f "app.py" ]; then
    ./configs/bin/python app.py
else
    echo -e "[ERRO] Arquivo \033[1;31mmain.py\033[0m não encontrado!"
    exit 1
fi
