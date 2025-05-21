import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from prod_stand import load_and_standardize_production
from plot_utils import colours, plot_monthly_graphs

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Produção e Consumo")
        self.root.geometry("500x400")

        self.ficheiros_consumo = []
        self.ficheiro_producao = None
        self.fig = None  # Store the generated figure for "Guardar"

        self.btn_abrir_consumo = tk.Button(root, text="Selecionar ficheiros Consumo", command=self.abrir_ficheiros_consumo)
        self.btn_abrir_consumo.pack(pady=10)

        self.lbl_consumo = tk.Label(root, text="Nenhum ficheiro de consumo selecionado")
        self.lbl_consumo.pack()

        self.btn_abrir_producao = tk.Button(root, text="Selecionar ficheiro PVsyst", command=self.abrir_ficheiro_producao)
        self.btn_abrir_producao.pack(pady=10)

        self.lbl_producao = tk.Label(root, text="Nenhum ficheiro PVsyst selecionado")
        self.lbl_producao.pack()

        self.btn_processar = tk.Button(root, text="Processar e mostrar gráficos", command=self.processar)
        self.btn_processar.pack(pady=20)

        # Buttons for Guardar and Fechar
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        self.btn_guardar = tk.Button(button_frame, text="Guardar", command=self.guardar_figura)
        self.btn_guardar.pack(side=tk.LEFT, padx=10)

        self.btn_fechar = tk.Button(button_frame, text="Fechar", command=self.root.quit)
        self.btn_fechar.pack(side=tk.LEFT, padx=10)

    def abrir_ficheiros_consumo(self):
        files = filedialog.askopenfilenames(title="Selecionar ficheiros Excel Consumo", 
                                            filetypes=[("Excel files", "*.xlsx *.xls")])
        if files:
            self.ficheiros_consumo = list(files)
            nomes = [f.split("/")[-1] for f in self.ficheiros_consumo]
            self.lbl_consumo.config(text="Consumo: " + ", ".join(nomes))
        else:
            self.lbl_consumo.config(text="Nenhum ficheiro de consumo selecionado")

    def abrir_ficheiro_producao(self):
        file = filedialog.askopenfilename(title="Selecionar ficheiro Excel PVsyst",
                                          filetypes=[("Excel files", "*.xlsx *.xls")])
        if file:
            self.ficheiro_producao = file
            nome = file.split("/")[-1]
            self.lbl_producao.config(text="PVsyst: " + nome)
        else:
            self.lbl_producao.config(text="Nenhum ficheiro PVsyst selecionado")

    def processar(self):
        if not self.ficheiros_consumo:
            messagebox.showwarning("Aviso", "Por favor, selecione pelo menos um ficheiro de consumo.")
            return

        producao_data = None
        if self.ficheiro_producao:
            try:
                producao_data = load_and_standardize_production(self.ficheiro_producao)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar ficheiro PVsyst:\n{e}")
                return

        line_color = colours()

        try:
            plt.close('all')
            self.fig = plot_monthly_graphs(self.ficheiros_consumo, line_color, producao_data)

            grafico_window = tk.Toplevel(self.root)
            grafico_window.title("Gráficos de Produção e Consumo")
            grafico_window.geometry("900x750")

            canvas = FigureCanvasTkAgg(self.fig, master=grafico_window)
            canvas.draw()
            canvas.get_tk_widget().pack()  # No expansion 
            # canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar gráficos:\n{e}")

    def guardar_figura(self):
        if self.fig is None:
            messagebox.showwarning("Aviso", "Por favor, processe os dados antes de guardar o gráfico.")
            return
        try:
            self.fig.savefig("consumo_anual.png", dpi=150)
            messagebox.showinfo("Sucesso", "Gráfico guardado como 'consumo_anual.png'")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao guardar gráfico:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
