# main.py
import tkinter as tk
from tkinter import ttk, messagebox
from database import criar_tabelas
from models import adicionar_cliente, buscar_clientes, adicionar_ordem, listar_ordens
from pdf_generator import gerar_pdf_os

criar_tabelas()

root = tk.Tk()
root.title("Gerenciador de OS - Oficina de Radiadores")
root.geometry("900x600")

# ----------- Funções da Interface -----------

def salvar_cliente():
    nome = ent_nome.get()
    telefone = ent_telefone.get()
    veiculo = ent_veiculo.get()
    placa = ent_placa.get()
    if nome and nome != "Nome":
        adicionar_cliente(nome, telefone, veiculo, placa)
        messagebox.showinfo("Sucesso", "Cliente cadastrado!")
        limpar_campos_cliente()
        atualizar_clientes()
    else:
        messagebox.showwarning("Atenção", "Preencha o nome do cliente.")

def limpar_campos_cliente():
    ent_nome.delete(0, tk.END)
    ent_telefone.delete(0, tk.END)
    ent_veiculo.delete(0, tk.END)
    ent_placa.delete(0, tk.END)
    
    # Restaurar os placeholders
    ent_nome.insert(0, "Nome")
    ent_telefone.insert(0, "Telefone")
    ent_veiculo.insert(0, "Veículo")
    ent_placa.insert(0, "Placa")

def salvar_ordem():
    cliente = cb_clientes.get()
    cliente_id = cliente_ids.get(cliente)
    if not cliente_id:
        messagebox.showwarning("Atenção", "Selecione um cliente válido.")
        return
    entrada = ent_entrada.get()
    if entrada == "Data Entrada":
        entrada = ""
    saida = ent_saida.get()
    if saida == "Data Saída":
        saida = ""
    descricao = txt_descricao.get("1.0", "end").strip()
    try:
        valor_text = ent_valor.get()
        if valor_text == "Valor":
            raise ValueError
        valor = float(valor_text)
    except ValueError:
        messagebox.showwarning("Atenção", "Informe um valor numérico válido.")
        return
    status = cb_status.get()

    adicionar_ordem(cliente_id, entrada, saida, descricao, valor, status)
    messagebox.showinfo("Ordem", "Ordem de serviço salva!")
    limpar_campos_os()
    listar_os()

def limpar_campos_os():
    ent_entrada.delete(0, tk.END)
    ent_saida.delete(0, tk.END)
    txt_descricao.delete("1.0", tk.END)
    ent_valor.delete(0, tk.END)
    cb_status.set("Aguardando")
    
    # Restaurar os placeholders
    ent_entrada.insert(0, "Data Entrada")
    ent_saida.insert(0, "Data Saída")
    ent_valor.insert(0, "Valor")

def atualizar_clientes():
    global cliente_ids
    cliente_ids = {}
    nomes = []
    for c in buscar_clientes():
        if c[3]:  # Se tem placa
            nome = f"{c[1]} - {c[3]}"  # Nome - Placa
        else:
            nome = c[1]  # Só o nome
        nomes.append(nome)
        cliente_ids[nome] = c[0]
    cb_clientes['values'] = nomes
    if nomes:  # Se houver clientes, seleciona o primeiro
        cb_clientes.set(nomes[0])

def listar_os():
    for item in tree.get_children():
        tree.delete(item)
    for o in listar_ordens():
        tree.insert("", "end", values=o)

def exportar_os_pdf():
    selecionado = tree.focus()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione uma OS na lista.")
        return

    dados = tree.item(selecionado, "values")
    arquivo = gerar_pdf_os(dados)
    messagebox.showinfo("PDF Gerado", f"Arquivo salvo em:\n{arquivo}")

def on_focus_in(event, placeholder):
    widget = event.widget
    if widget.get() == placeholder:
        widget.delete(0, tk.END)

def on_focus_out(event, placeholder):
    widget = event.widget
    if not widget.get():
        widget.insert(0, placeholder)

# ----------- GUI: Cadastro Cliente -----------
frame1 = tk.LabelFrame(root, text="Cadastro de Cliente")
frame1.pack(fill="x", padx=10, pady=5)

ent_nome = tk.Entry(frame1, width=30)
ent_nome.insert(0, "Nome")
ent_nome.grid(row=0, column=0, padx=5, pady=5)
ent_nome.bind('<FocusIn>', lambda e: on_focus_in(e, "Nome"))
ent_nome.bind('<FocusOut>', lambda e: on_focus_out(e, "Nome"))
ent_nome.bind("<FocusIn>", lambda e: on_focus_in(e, "Nome"))
ent_nome.bind("<FocusOut>", lambda e: on_focus_out(e, "Nome"))

ent_telefone = tk.Entry(frame1, width=20)
ent_telefone.insert(0, "Telefone")
ent_telefone.grid(row=0, column=1)
ent_telefone.bind('<FocusIn>', lambda e: on_focus_in(e, "Telefone"))
ent_telefone.bind('<FocusOut>', lambda e: on_focus_out(e, "Telefone"))
ent_telefone.bind("<FocusIn>", lambda e: on_focus_in(e, "Telefone"))
ent_telefone.bind("<FocusOut>", lambda e: on_focus_out(e, "Telefone"))

ent_veiculo = tk.Entry(frame1, width=20)
ent_veiculo.insert(0, "Veículo")
ent_veiculo.grid(row=0, column=2)
ent_veiculo.bind('<FocusIn>', lambda e: on_focus_in(e, "Veículo"))
ent_veiculo.bind('<FocusOut>', lambda e: on_focus_out(e, "Veículo"))
ent_veiculo.bind("<FocusIn>", lambda e: on_focus_in(e, "Veículo"))
ent_veiculo.bind("<FocusOut>", lambda e: on_focus_out(e, "Veículo"))

ent_placa = tk.Entry(frame1, width=10)
ent_placa.insert(0, "Placa")
ent_placa.grid(row=0, column=3)
ent_placa.bind('<FocusIn>', lambda e: on_focus_in(e, "Placa"))
ent_placa.bind('<FocusOut>', lambda e: on_focus_out(e, "Placa"))
ent_placa.bind("<FocusIn>", lambda e: on_focus_in(e, "Placa"))
ent_placa.bind("<FocusOut>", lambda e: on_focus_out(e, "Placa"))

tk.Button(frame1, text="Salvar Cliente", command=salvar_cliente).grid(row=0, column=4, padx=5)

# ----------- GUI: Cadastro de OS -----------
frame2 = tk.LabelFrame(root, text="Nova Ordem de Serviço")
frame2.pack(fill="x", padx=10, pady=5)

cb_clientes = ttk.Combobox(frame2, width=50)
cb_clientes.grid(row=0, column=0, padx=5, pady=5)

ent_entrada = tk.Entry(frame2, width=12)
ent_entrada.insert(0, "Data Entrada")
ent_entrada.grid(row=0, column=1)
ent_entrada.bind('<FocusIn>', lambda e: on_focus_in(e, "Data Entrada"))
ent_entrada.bind('<FocusOut>', lambda e: on_focus_out(e, "Data Entrada"))
ent_entrada.bind("<FocusIn>", lambda e: on_focus_in(e, "Data Entrada"))
ent_entrada.bind("<FocusOut>", lambda e: on_focus_out(e, "Data Entrada"))

ent_saida = tk.Entry(frame2, width=12)
ent_saida.insert(0, "Data Saída")
ent_saida.grid(row=0, column=2)
ent_saida.bind('<FocusIn>', lambda e: on_focus_in(e, "Data Saída"))
ent_saida.bind('<FocusOut>', lambda e: on_focus_out(e, "Data Saída"))
ent_saida.bind("<FocusIn>", lambda e: on_focus_in(e, "Data Saída"))
ent_saida.bind("<FocusOut>", lambda e: on_focus_out(e, "Data Saída"))

ent_valor = tk.Entry(frame2, width=10)
ent_valor.insert(0, "Valor")
ent_valor.grid(row=0, column=3)
ent_valor.bind('<FocusIn>', lambda e: on_focus_in(e, "Valor"))
ent_valor.bind('<FocusOut>', lambda e: on_focus_out(e, "Valor"))
ent_valor.bind("<FocusIn>", lambda e: on_focus_in(e, "Valor"))
ent_valor.bind("<FocusOut>", lambda e: on_focus_out(e, "Valor"))

cb_status = ttk.Combobox(frame2, values=["Aguardando", "Em Execução", "Finalizada"], width=15)
cb_status.set("Aguardando")
cb_status.grid(row=0, column=4)

txt_descricao = tk.Text(frame2, height=4, width=90)
txt_descricao.grid(row=1, column=0, columnspan=5, padx=5)

tk.Button(frame2, text="Salvar OS", command=salvar_ordem).grid(row=1, column=5)

# ----------- GUI: Lista de Ordens -----------
frame3 = tk.LabelFrame(root, text="Ordens de Serviço Registradas")
frame3.pack(fill="both", expand=True, padx=10, pady=5)

cols = ("ID", "Cliente", "Entrada", "Saída", "Descrição", "Valor", "Status")
tree = ttk.Treeview(frame3, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, minwidth=50, width=110)
tree.pack(fill="both", expand=True)

tk.Button(frame3, text="Gerar PDF da OS Selecionada", command=exportar_os_pdf).pack(pady=5)

# Iniciar dados
atualizar_clientes()
listar_os()

root.mainloop()
