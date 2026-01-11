from matplotlib.backends.backend_pdf import PdfPages

def generate_pdf_report(metrics, figures):
    with PdfPages("simulation_report.pdf") as pdf:
        for k in figures:
            pdf.savefig(figures[k])
