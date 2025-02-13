# Problema da Mochila - Algoritmo Evolutivo
Desenvolvimento: Marcelo-Uk

Este projeto é uma aplicação Django que implementa um algoritmo evolutivo para resolver o problema da mochila. O sistema apresenta gráficos interativos que mostram a evolução das soluções ao longo das gerações.

## Pré-requisitos

- Python 3.x instalado
- Git instalado

## Instalação

1. **Clone o repositório:**

   git clone https://github.com/seu-usuario/knapsack-project.git
   cd knapsack-project

2. **Crie e ative um ambiente virtual**

Windows usando 'Git Bash':
python -m venv venv
source venv/scripts/activate

3. **Instale as dependências**

pip install -r requirements.txt

4. **Realize as migrações do banco de dados**

python manage.py migrate

5. **Rode o servidor**

python manage.py runserver

6. **Acesse a aplicação**

Abra o navegador e acesse: http://127.0.0.1:8000/

**Funcionalidades**

    Interface Web:
    Na página inicial, são exibidos os dados do problema (tabela de itens) e um botão para iniciar a evolução.

    Algoritmo Evolutivo:
    O algoritmo evolui soluções para o problema da mochila ao longo de várias gerações.

    Gráficos Interativos:
    São apresentados:
        Um gráfico de linha mostrando o melhor fitness por geração.
        Um gráfico de dispersão (scatter plot) com um slider que permite visualizar a distribuição dos indivíduos (após uma projeção PCA) para cada geração, destacando o melhor indivíduo.

**Observações**

    Os dados do problema (itens, pesos e benefícios) estão definidos de forma fixa (hardcoded) no backend.
    Este projeto usa Chart.js para visualização dos gráficos e scikit-learn para a projeção dos cromossomos usando PCA.