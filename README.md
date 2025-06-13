# Sistema de Gerenciamento de Ordens de Serviço - Oficina de Radiadores

Sistema desenvolvido em Python com interface gráfica Tkinter para gerenciamento de ordens de serviço de uma oficina de radiadores.

## Funcionalidades

- Cadastro de clientes
- Registro de ordens de serviço
- Visualização de ordens em uma tabela
- Exportação de OS para PDF
- Status de andamento do serviço

## Como usar

1. Instale as dependências:
```bash
pip install fpdf
```

2. Execute o programa:
```bash
python main.py
```

## Estrutura do projeto

- `main.py`: Interface gráfica e lógica principal
- `models.py`: Funções de acesso ao banco de dados
- `database.py`: Configuração do banco de dados SQLite
- `pdf_generator.py`: Geração de PDFs das ordens de serviço
