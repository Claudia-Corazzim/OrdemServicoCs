# main.py
import tkinter as tk
from tkinter import ttk, messagebox
from database import criar_tabelas
from models import adicionar_cliente, buscar_clientes, adicionar_ordem, listar_ordens, excluir_cliente, excluir_ordem
from pdf_generator import gerar_pdf_os

criar_tabelas()

root = tk.Tk()
root.title("Gerenciador de OS - Oficina de Radiadores")
root.geometry("900x600")

# ----------- Funções da Interface -----------

def salvar_cliente():
    nome = ent_nome.get()
    telefone = ent_telefone.get()
    endereco = ent_endereco.get()
    if nome and nome != "Nome":
        adicionar_cliente(nome, telefone, endereco)
        messagebox.showinfo("Sucesso", "Cliente cadastrado!")
        limpar_campos_cliente()
        atualizar_clientes()
    else:
        messagebox.showwarning("Atenção", "Preencha o nome do cliente.")

def limpar_campos_cliente():
    ent_nome.delete(0, tk.END)
    ent_telefone.delete(0, tk.END)
    ent_endereco.delete(0, tk.END)
    
    # Restaurar os placeholders
    ent_nome.insert(0, "Nome")
    ent_telefone.insert(0, "Telefone")
    ent_endereco.insert(0, "Endereço")

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
    status = cb_status.get()
    veiculo = ent_veiculo_os.get()
    if veiculo == "Veículo":
        veiculo = ""
    placa = ent_placa_os.get()
    if placa == "Placa":
        placa = ""
    
    # Calcula o valor total baseado nos valores na descrição
    valor_total = 0
    import re
    for linha in descricao.split('\n'):
        if linha.strip():
            # Procura por quantidade no início da linha (ex: "2x" ou "2 x")
            qtd_match = re.match(r'^\s*(\d+)\s*[xX]\s*(.+)', linha)
            quantidade = int(qtd_match.group(1)) if qtd_match else 1
            
            # Procura por valor R$ na linha
            match = re.search(r'R\$\s*(\d+[.,]\d+)', linha)
            if match:
                valor_str = match.group(1)
                try:
                    valor_item = float(valor_str.replace(',', '.'))
                    valor_total += valor_item * quantidade
                except ValueError:
                    pass

    adicionar_ordem(cliente_id, entrada, saida, descricao, valor_total, status, veiculo, placa)
    messagebox.showinfo("Ordem", "Ordem de serviço salva!")
    limpar_campos_os()
    listar_os()

def limpar_campos_os():
    ent_entrada.delete(0, tk.END)
    ent_saida.delete(0, tk.END)
    ent_veiculo_os.delete(0, tk.END)
    ent_placa_os.delete(0, tk.END)
    txt_descricao.delete("1.0", tk.END)
    cb_status.set("Aguardando")
    
    # Restaurar os placeholders
    ent_entrada.insert(0, "Data Entrada")
    ent_saida.insert(0, "Data Saída")
    ent_veiculo_os.insert(0, "Veículo")
    ent_placa_os.insert(0, "Placa")

def atualizar_clientes():
    global cliente_ids
    cliente_ids = {}
    nomes = []
    for c in buscar_clientes():
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

def excluir_ordem_gui():
    selecionado = tree.focus()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione uma OS na lista para excluir.")
        return

    dados = tree.item(selecionado, "values")
    if messagebox.askyesno("Confirmar Exclusão", 
                          f"Tem certeza que deseja excluir a OS #{dados[0]} do cliente {dados[1]}?"):
        try:
            excluir_ordem(dados[0])
            messagebox.showinfo("Sucesso", "Ordem de serviço excluída com sucesso!")
            listar_os()  # Atualiza a lista de OS
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir ordem de serviço: {str(e)}")

def on_focus_in(event, placeholder):
    widget = event.widget
    if widget.get() == placeholder:
        widget.delete(0, tk.END)

def on_focus_out(event, placeholder):
    widget = event.widget
    if not widget.get():
        widget.insert(0, placeholder)

def excluir_cliente_gui():
    cliente = cb_clientes.get()
    if not cliente:
        messagebox.showwarning("Atenção", "Selecione um cliente para excluir.")
        return
    
    if messagebox.askyesno("Confirmar Exclusão", 
                          f"Tem certeza que deseja excluir o cliente {cliente}?\n" +
                          "Todas as ordens de serviço relacionadas também serão excluídas."):
        try:
            cliente_id = cliente_ids.get(cliente)
            excluir_cliente(cliente_id)
            messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
            atualizar_clientes()
            listar_os()  # Atualiza a lista de OS para remover as OS do cliente excluído
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir cliente: {str(e)}")

# ----------- GUI: Cadastro Cliente -----------
frame1 = tk.LabelFrame(root, text="Cadastro de Cliente")
frame1.pack(fill="x", padx=10, pady=5)

# Primeira linha: Nome e Telefone
ent_nome = tk.Entry(frame1, width=30)
ent_nome.insert(0, "Nome")
ent_nome.grid(row=0, column=0, padx=5, pady=5)
ent_nome.bind('<FocusIn>', lambda e: on_focus_in(e, "Nome"))
ent_nome.bind('<FocusOut>', lambda e: on_focus_out(e, "Nome"))

ent_telefone = tk.Entry(frame1, width=20)
ent_telefone.insert(0, "Telefone")
ent_telefone.grid(row=0, column=1)
ent_telefone.bind('<FocusIn>', lambda e: on_focus_in(e, "Telefone"))
ent_telefone.bind('<FocusOut>', lambda e: on_focus_out(e, "Telefone"))

# Segunda linha: Endereço
ent_endereco = tk.Entry(frame1, width=50)
ent_endereco.insert(0, "Endereço")
ent_endereco.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
ent_endereco.bind('<FocusIn>', lambda e: on_focus_in(e, "Endereço"))
ent_endereco.bind('<FocusOut>', lambda e: on_focus_out(e, "Endereço"))



tk.Button(frame1, text="Salvar Cliente", command=salvar_cliente).grid(row=0, column=4, padx=5)
tk.Button(frame1, text="Excluir Cliente", command=excluir_cliente_gui).grid(row=0, column=5, padx=5)

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

cb_status = ttk.Combobox(frame2, values=["Aguardando", "Em Execução", "Finalizada"], width=15)
cb_status.set("Aguardando")
cb_status.grid(row=0, column=3)

# Adiciona campos de veículo e placa
veic_frame = tk.Frame(frame2)
veic_frame.grid(row=1, column=0, columnspan=4, sticky='w', padx=5, pady=5)

ent_veiculo_os = tk.Entry(veic_frame, width=20)
ent_veiculo_os.insert(0, "Veículo")
ent_veiculo_os.pack(side=tk.LEFT, padx=5)
ent_veiculo_os.bind('<FocusIn>', lambda e: on_focus_in(e, "Veículo"))
ent_veiculo_os.bind('<FocusOut>', lambda e: on_focus_out(e, "Veículo"))

ent_placa_os = tk.Entry(veic_frame, width=10)
ent_placa_os.insert(0, "Placa")
ent_placa_os.pack(side=tk.LEFT, padx=5)
ent_placa_os.bind('<FocusIn>', lambda e: on_focus_in(e, "Placa"))
ent_placa_os.bind('<FocusOut>', lambda e: on_focus_out(e, "Placa"))

txt_descricao = tk.Text(frame2, height=4, width=90)
txt_descricao.grid(row=2, column=0, columnspan=5, padx=5)

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

# Frame para os botões
button_frame = tk.Frame(frame3)
button_frame.pack(pady=5)

tk.Button(button_frame, text="Gerar PDF da OS Selecionada", command=exportar_os_pdf).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Excluir OS Selecionada", command=excluir_ordem_gui).pack(side=tk.LEFT, padx=5)

# Iniciar dados
atualizar_clientes()
listar_os()

root.mainloop()
