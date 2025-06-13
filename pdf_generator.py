#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from fpdf import FPDF
import re
from datetime import datetime

def gerar_pdf_os(dados_os):
    """
    Gera um PDF para uma ordem de serviço
    dados_os: tupla com os valores da OS (id, cliente, entrada, saída, descrição, valor, status, telefone, endereco, veiculo, placa)
    """
    pdf = FPDF()
    pdf.add_page()
    
    # Logo 10% maior
    logo_path = os.path.join("images", "logo.png")
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=10, y=8, w=49.5)
    
    # Informações da empresa - centralizadas verticalmente com o logo
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
    
    # Veículo e Placa - usando os valores da ordem de serviço
    veiculo = dados_os[9] if dados_os[9] and dados_os[9] != "Veículo" else "_________________"
    placa = dados_os[10] if dados_os[10] and dados_os[10] != "Placa" else "_________"
    pdf.cell(130, 6, f"Veículo: {veiculo}", border=1)
    pdf.cell(0, 6, f"Placa: {placa}", border=1, ln=True)
    pdf.ln(5)
    
    # Tabela de Serviços
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(20, 6, "Qtd", border=1, align='C')
    pdf.cell(140, 6, "Descrição", border=1, align='C')
    pdf.cell(0, 6, "Valor", border=1, align='C', ln=True)
    pdf.set_font("Arial", '', 11)
    descricao_linhas = dados_os[4].split('\n')
    total = 0
    
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
            match = re.search(r'R\$\s*(\d+[.,]\d+|\d+)', linha_processada)
            valor_str = ""
            valor_total_item = 0
            
            if match:
                valor_str = match.group(1)
                # Remove o valor da descrição
                linha_processada = linha_processada.replace(match.group(0), "").strip()
                # Remove traço após descrição se existir
                linha_processada = re.sub(r'\s*-\s*$', '', linha_processada)
                
                try:
                    valor_item = float(valor_str.replace(',', '.'))
                    valor_total_item = valor_item * quantidade
                    total += valor_total_item
                except ValueError:
                    valor_total_item = 0
            
            # Imprime a linha na tabela
            pdf.cell(20, 6, str(quantidade), border=1, align='C')
            pdf.cell(140, 6, linha_processada, border=1)
            
            if valor_total_item > 0:
                pdf.cell(0, 6, f"R$ {valor_total_item:.2f}", border=1, align='C', ln=True)
            else:
                pdf.cell(0, 6, "", border=1, ln=True)
    
    # Linhas adicionais em branco para serviços extras
    for _ in range(5):  # 5 linhas extras
        pdf.cell(20, 6, "", border=1)
        pdf.cell(140, 6, "", border=1)
        pdf.cell(0, 6, "", border=1, ln=True)
    
    # Total
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(160, 6, "Total:", align='R')
    pdf.cell(0, 6, f"R$ {total:.2f}", align='C', ln=True)
    
    # Observações
    pdf.ln(5)
    pdf.cell(0, 6, "Observações:", ln=True)
    for _ in range(3):  # 3 linhas para observações
        pdf.cell(0, 6, "_" * 90, ln=True)
    
    # Data de Saída e Status
    pdf.ln(5)
    pdf.cell(95, 6, f"Data de Saída: {dados_os[3] or '_____________'}")
    pdf.cell(0, 6, f"Status: {dados_os[6]}", ln=True)
    
    # Diretório para salvar PDFs
    pdf_dir = "pdfs"
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    
    # Nome do arquivo com timestamp para evitar sobreposição
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(pdf_dir, f"OS_{dados_os[0]}_{timestamp}.pdf")
    pdf.output(filename)
    
    return filename