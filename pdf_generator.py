# pdf_generator.py
from fpdf import FPDF
import os

def gerar_pdf_os(dados_os):
    """
    dados_os: tupla com os valores da OS (id, cliente, entrada, saída, descrição, valor, status)
    """
    pdf = FPDF()
    pdf.add_page()
      # Adiciona o logo se existir
    logo_path = os.path.join("images", "logo.png")
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=10, y=10, w=50)  # Ajuste w (largura) conforme necessário
        
    # Informações de contato e endereço
    pdf.set_font("Arial", '', 10)
    whatsapp_icon = os.path.join("images", "whatsapp.png")
    if os.path.exists(whatsapp_icon):
        pdf.image(whatsapp_icon, x=70, y=15, w=5)  # ícone pequeno do WhatsApp
    pdf.set_xy(77, 15)
    pdf.cell(0, 5, "(19) 99676-0164", ln=True)
      pdf.set_xy(70, 20)
    pdf.multi_cell(0, 5, "Av. Pedro Botesi, 2352\nJd. Scomparim - Mogi Mirim - SP", align='L')
    
    pdf.ln(20)  # Espaço após o cabeçalho
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, f"Ordem de Serviço Nº {dados_os[0]}", ln=True, align="C")
    
    # Primeira tabela - Informações do Cliente
    pdf.set_font("Arial", 'B', 12)
    pdf.ln(10)
    pdf.cell(0, 8, f"Data de Entrada: {dados_os[2]}", ln=True, border=1)
    
    # Nome e Telefone na mesma linha
    pdf.cell(130, 8, f"Cliente: {dados_os[1]}", border=1)
    pdf.cell(0, 8, f"Telefone: {dados_os[1]}", border=1, ln=True)  # Ajuste para pegar o telefone do cliente quando disponível
    
    # Endereço
    pdf.cell(0, 8, f"Endereço: _______________________________________________________", border=1, ln=True)
    
    # Veículo e Placa
    pdf.cell(130, 8, f"Veículo: _________________", border=1)
    pdf.cell(0, 8, f"Placa: _________", border=1, ln=True)
    
    pdf.ln(10)
    
    # Segunda tabela - Serviços
    pdf.cell(20, 8, "Qtd", border=1, align='C')
    pdf.cell(140, 8, "Descrição", border=1, align='C')
    pdf.cell(0, 8, "Valor", border=1, align='C', ln=True)
    
    # Descrição dos serviços
    pdf.set_font("Arial", '', 12)
    descricao_linhas = dados_os[4].split('\n')
    for linha in descricao_linhas:
        if linha.strip():  # Se a linha não estiver vazia
            pdf.cell(20, 8, "1", border=1)  # Quantidade padrão 1
            pdf.cell(140, 8, linha, border=1)
            pdf.cell(0, 8, "", border=1, ln=True)
    
    # Adicionar algumas linhas em branco para serviços adicionais
    for _ in range(3):
        pdf.cell(20, 8, "", border=1)
        pdf.cell(140, 8, "", border=1)
        pdf.cell(0, 8, "", border=1, ln=True)
    
    pdf.ln(5)
    
    # Forma de pagamento e total
    valor = float(dados_os[5]) if dados_os[5] else 0.0
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(100, 8, "Forma de Pagamento: ________________", ln=True)
    pdf.cell(0, 8, f"Total: R$ {valor:.2f}", ln=True)
    
    # Observações
    pdf.ln(5)
    pdf.cell(0, 8, "Observações:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 8, "_" * 70 + "\n" + "_" * 70)
    
    # Data de Saída
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, f"Data de Saída: {dados_os[3]}", ln=True)
    
    # Status
    pdf.cell(0, 8, f"Status: {dados_os[6]}", ln=True)

    output_dir = "pdfs"
    os.makedirs(output_dir, exist_ok=True)
    arquivo = os.path.join(output_dir, f"os_{dados_os[0]}.pdf")
    pdf.output(arquivo)
    return arquivo
