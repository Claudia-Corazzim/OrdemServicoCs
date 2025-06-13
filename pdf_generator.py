# pdf_generator.py
from fpdf import FPDF
import os

def gerar_pdf_os(dados_os):
    """
    dados_os: tupla com os valores da OS (id, cliente, entrada, saída, descrição, valor, status)
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, f"Ordem de Serviço Nº {dados_os[0]}", ln=True, align="C")

    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Cliente: {dados_os[1]}", ln=True)
    pdf.cell(0, 10, f"Data de Entrada: {dados_os[2]}   |   Saída: {dados_os[3]}", ln=True)
    
    # Converter o valor para float antes de formatar
    valor = float(dados_os[5]) if dados_os[5] else 0.0
    pdf.cell(0, 10, f"Valor Total: R$ {valor:.2f}   |   Status: {dados_os[6]}", ln=True)

    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Descrição do Serviço:\n{dados_os[4]}")

    output_dir = "pdfs"
    os.makedirs(output_dir, exist_ok=True)
    arquivo = os.path.join(output_dir, f"os_{dados_os[0]}.pdf")
    pdf.output(arquivo)
    return arquivo
