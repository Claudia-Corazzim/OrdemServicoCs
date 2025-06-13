# pdf_generator.py
from fpdf import FPDF
import os

def gerar_pdf_os(dados_os):
    """
    dados_os: tupla com os valores da OS (id, cliente, entrada, saída, descrição, valor, status)
    """
    pdf = FPDF()
    pdf.add_page()
      # Logo 10% maior
    logo_path = os.path.join("images", "logo.png")
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=10, y=8, w=49.5)
    
    # Informações da empresa - centralizadas verticalmente com o logo
    # Altura do logo é aproximadamente 33 pixels (w=49.5 mantém a proporção original)
    # Distribuir o conteúdo uniformemente ao longo da altura do logo
    linha_altura = 4  # altura de cada linha de texto
    espacamento = 2   # espaço entre as linhas
    y_start = 8      # mesmo Y do logo
    x_start = 105    # metade direita da página (210/2)
      # Nome da empresa
    pdf.set_font("Arial", 'B', 12)
    pdf.set_xy(x_start, y_start)
    pdf.cell(95, linha_altura, "Sergio Eduardo Padilha Corazzim", ln=True)
    
    # CNPJ
    pdf.set_font("Arial", '', 10)
    pdf.set_xy(x_start, y_start + linha_altura + espacamento)
    pdf.cell(95, linha_altura, "CNPJ: 08.101.093/0001-52", ln=True)
    
    # WhatsApp
    whatsapp_icon = os.path.join("images", "whatsapp.png")
    if os.path.exists(whatsapp_icon):
        pdf.image(whatsapp_icon, x=x_start, y=y_start + 2*(linha_altura + espacamento), w=4)
        pdf.set_xy(x_start + 5, y_start + 2*(linha_altura + espacamento))
        pdf.cell(95, linha_altura, "(19) 99676-0164", ln=True)
    
    # Endereço
    pdf.set_xy(x_start, y_start + 3*(linha_altura + espacamento))
    pdf.cell(95, linha_altura, "Av. Pedro Botesi, 2352 - Jd. Scomparim", ln=True)
    pdf.set_xy(x_start, y_start + 4*(linha_altura + espacamento))
    pdf.cell(95, linha_altura, "Mogi Mirim - SP", ln=True)
    
    # Ordem de Serviço
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 8, f"Ordem de Serviço Nº {dados_os[0]}", ln=True, align="C")
    
    # Informações do Cliente
    pdf.set_font("Arial", 'B', 11)
    pdf.ln(5)
    pdf.cell(0, 6, f"Data de Entrada: {dados_os[2]}", ln=True, border=1)
    pdf.cell(130, 6, f"Cliente: {dados_os[1]}", border=1)
    pdf.cell(0, 6, f"Telefone: {dados_os[7]}", border=1, ln=True)
    pdf.cell(0, 6, f"Endereço: {dados_os[8] or '_______________________________________________________'}", border=1, ln=True)
    pdf.cell(130, 6, f"Veículo: {dados_os[9] or '_________________'}", border=1)
    pdf.cell(0, 6, f"Placa: {dados_os[10] or '_________'}", border=1, ln=True)
    pdf.ln(5)    # Tabela de Serviços
    pdf.cell(20, 6, "Qtd", border=1, align='C')
    pdf.cell(140, 6, "Descrição", border=1, align='C')
    pdf.cell(0, 6, "Valor", border=1, align='C', ln=True)
    pdf.set_font("Arial", '', 11)
    descricao_linhas = dados_os[4].split('\n')
    total = 0
    import re
    
    def extrair_quantidade_e_texto(linha):
        # Padrões possíveis: "2x", "2 x", "2X", "2 X"
        padrao_qtd = re.match(r'^\s*(\d+)\s*[xX]\s*(.+)', linha)
        if padrao_qtd:
            try:
                qtd = int(padrao_qtd.group(1))
                texto = padrao_qtd.group(2).strip()
                return qtd, texto
            except ValueError:
                pass
        return 1, linha.strip()
    
    for linha in descricao_linhas:
        if linha.strip():
            # Extrai quantidade e texto
            quantidade, linha_processada = extrair_quantidade_e_texto(linha)
            
            # Procura por valor R$ na linha
            match = re.search(r'R\$\s*(\d+[.,]\d+)', linha_processada)
            if match:
                valor_str = match.group(1)
                descricao = linha_processada[:match.start()].strip().rstrip(' -')
                try:
                    valor_item = float(valor_str.replace(',', '.'))
                    valor_total_item = valor_item * quantidade
                    total += valor_total_item
                    pdf.cell(20, 6, str(quantidade), border=1, align='C')
                    pdf.cell(140, 6, descricao, border=1)
                    pdf.cell(0, 6, f"R$ {valor_total_item:.2f}", border=1, align='R', ln=True)
                except ValueError:
                    pdf.cell(20, 6, str(quantidade), border=1, align='C')
                    pdf.cell(140, 6, linha_processada, border=1)
                    pdf.cell(0, 6, "", border=1, ln=True)
            else:
                pdf.cell(20, 6, str(quantidade), border=1, align='C')
                pdf.cell(140, 6, linha_processada, border=1)
                pdf.cell(0, 6, "", border=1, ln=True)
    for _ in range(2):
        pdf.cell(20, 6, "", border=1)
        pdf.cell(140, 6, "", border=1)
        pdf.cell(0, 6, "", border=1, ln=True)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(160, 6, "Total:", border=0, align='R')
    pdf.cell(0, 6, f"R$ {total:.2f}", border=0, align='C', ln=True)
    pdf.ln(3)
    pdf.cell(0, 6, "Observações:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 6, "_" * 70 + "\n" + "_" * 70)
    pdf.ln(3)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 6, f"Data de Saída: {dados_os[3]}", ln=True)
    pdf.cell(0, 6, f"Status: {dados_os[6]}", ln=True)
    output_dir = "pdfs"
    os.makedirs(output_dir, exist_ok=True)
    arquivo = os.path.join(output_dir, f"os_{dados_os[0]}.pdf")
    pdf.output(arquivo)
    return arquivo
