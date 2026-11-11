import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button


def ler(texto):
    """Converte o texto digitado em número (aceita vírgula ou ponto)."""
    return float(texto.replace(",", ".").strip())


def calcular_elementos(x, y, a, b):
    """
    Calcula as propriedades da elipse vertical:
      (X - x)^2 / b^2 + (Y - y)^2 / a^2 = 1, com a > b > 0.
    """
    c = np.sqrt(a**2 - b**2)         # Distância focal (do centro aos focos)
    d = a**2 / c                     # Distância do centro às diretrizes
    e = c / a                        # Excentricidade
    lr = (2 * b**2) / a              # Comprimento do Latus Rectum (lado reto)

    # Coeficientes da Forma Geral expandida:
    # a^2(X - x)^2 + b^2(Y - y)^2 = a^2*b^2
    # A*X^2 + B*Y^2 + D*X + E*Y + F = 0
    A = a**2
    B = b**2
    D = -2 * a**2 * x
    E = -2 * b**2 * y
    F = a**2 * x**2 + b**2 * y**2 - a**2 * b**2

    return {
        "centro": (x, y),
        "vertices_maior": [(x, y + a), (x, y - a)],     # Vértices A1, A2
        "vertices_menor": [(x + b, y), (x - b, y)],     # Co-vértices B1, B2
        "focos": [(x, y + c), (x, y - c)],               # Focos F1, F2
        "c": c,
        "d": d,
        "e": e,
        "lr": lr,
        "diretrizes": (y + d, y - d),
        "coef_geral": (A, B, D, E, F)
    }


def gerar_pontos(x, y, a, b):
    # Equação: (X - x)^2 / b^2 + (Y - y)^2 / a^2 = 1
    t = np.linspace(0, 2 * np.pi, 400)
    X = x + b * np.cos(t)
    Y = y + a * np.sin(t)
    return t, X, Y


def salvar_relatorio_txt(caminho, x, y, a, b, elem, t, X, Y):
    """
    Gera e salva tudo em um arquivo .txt
    """
    c = elem["c"]
    d = elem["d"]
    e = elem["e"]
    lr = elem["lr"]
    A, B, D, E, F = elem["coef_geral"]
    d1, d2 = elem["diretrizes"]

    linhas = [
        "=" * 82,
        "           PROJETO DE COMPUTAÇÃO - GAAL (CIÊNCIA DA COMPUTAÇÃO)",
        "             CONSTRUÇÃO ALGORÍTMICA DA ELIPSE COM EIXO VERTICAL",
        "=" * 82,
        "",
        "1. PARÂMETROS DE ENTRADA (Etapa 1)",
        "-" * 82,
        f"   • Coordenada x do Centro:      {x:.6f}",
        f"   • Coordenada y do Centro:      {y:.6f}",
        f"   • Semieixo Maior (a):          {a:.6f}  (vertical)",
        f"   • Semieixo Menor (b):          {b:.6f}  (horizontal)",
        f"   • Condição de existência:      a > b > 0  [VÁLIDA: {a:g} > {b:g} > 0]",
        "",
        "2. EQUAÇÕES MATEMÁTICAS",
        "-" * 82,
        f"   • Forma Reduzida:",
        f"       (x - {x:g})² / {b**2:g} + (y - {y:g})² / {a**2:g} = 1",
        f"       [onde b² = {b**2:g} e a² = {a**2:g}]",
        "",
        f"   • Forma Geral Expandida (Ax² + By² + Dx + Ey + F = 0):",
        f"       {A:g}x² + {B:g}y² + ({D:g})x + ({E:g})y + ({F:g}) = 0",
        "",
        "3. ELEMENTOS NOTÁVEIS IDENTIFICADOS (Etapa 5)",
        "-" * 82,
        f"   • Centro:                   C({x:.6f}, {y:.6f})",
        f"   • Vértice Superior (A1):    ({elem['vertices_maior'][0][0]:.6f}, {elem['vertices_maior'][0][1]:.6f})",
        f"   • Vértice Inferior (A2):    ({elem['vertices_maior'][1][0]:.6f}, {elem['vertices_maior'][1][1]:.6f})",
        f"   • Co-vértice Direito (B1):  ({elem['vertices_menor'][0][0]:.6f}, {elem['vertices_menor'][0][1]:.6f})",
        f"   • Co-vértice Esquerdo (B2): ({elem['vertices_menor'][1][0]:.6f}, {elem['vertices_menor'][1][1]:.6f})",
        f"   • Foco Superior (F1):       ({elem['focos'][0][0]:.6f}, {elem['focos'][0][1]:.6f})",
        f"   • Foco Inferior (F2):       ({elem['focos'][1][0]:.6f}, {elem['focos'][1][1]:.6f})",
        f"   • Distância Semi-focal (c): {c:.6f}  [c = √(a² - b²)]",
        f"   • Distância Focal (2c):     {2*c:.6f}",
        f"   • Excentricidade (e):       {e:.6f}  [e = c/a, onde 0 < e < 1]",
        f"   • Diretrizes (d1 e d2):     d1: y = {d1:.6f}",
        f"                               d2: y = {d2:.6f}",
        f"                               [Equação deduzida: y = y0 ± a²/c = y0 ± a/e (retas horizontais)]",
        f"   • Latus Rectum (corda):     Comprimento LR = {lr:.6f}  [LR = 2b²/a]",
        f"   • Comprimento Eixo Maior:   2a = {2*a:.6f}",
        f"   • Comprimento Eixo Menor:   2b = {2*b:.6f}",
        f"   • Raio:                     Não aplicável a elipses (possui semieixos a e b;",
        f"                               raio único r ocorre apenas na circunferência, quando a = b)",
        f"   • Assíntotas:               Não existem na elipse (a curva é fechada e limitada no R²;",
        f"                               assíntotas só existem em curvas abertas, como a hipérbole)",
        "",
        "4. ARMAZENAMENTO DOS PONTOS (x, y) DA CURVA (Etapa 3)",
        "-" * 82,
        f"   Total de pontos calculados e armazenados: {len(X)}",
        f"   {'Índice':<8} | {'Parâmetro t (rad)':<18} | {'Coordenada X':<18} | {'Coordenada Y':<18}",
        "-" * 82,
    ]

    for i in range(len(X)):
        linhas.append(f"   {i+1:<8d} | {t[i]:<18.6f} | {X[i]:<18.6f} | {Y[i]:<18.6f}")

    linhas.append("=" * 82)
    linhas.append("Arquivo gerado.")

    with open(caminho, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas) + "\n")


def main():
    fig, ax = plt.subplots(figsize=(7.5, 8.8))
    fig.subplots_adjust(bottom=0.28, top=0.92, left=0.10, right=0.95)

    #Inputs iniciais
    nomes = ["x", "y", "a", "b"]
    iniciais = ["0", "0", "4", "3"]
    posicoes = [0.06, 0.19, 0.32, 0.45]
    caixas = []
    for nome, ini, pos in zip(nomes, iniciais, posicoes):
        eixo_caixa = fig.add_axes([pos, 0.07, 0.09, 0.05])
        caixas.append(TextBox(eixo_caixa, f"{nome}: ", initial=ini))

    #botao que gera a figura
    eixo_botao_gerar = fig.add_axes([0.58, 0.07, 0.17, 0.05])
    botao_gerar = Button(eixo_botao_gerar, "Gerar", color="#d0e1fd", hovercolor="#adcaf7")

    #botao que gera o arquivo txt
    eixo_botao_txt = fig.add_axes([0.77, 0.07, 0.17, 0.05])
    botao_txt = Button(eixo_botao_txt, "Salvar TXT", color="#d4edda", hovercolor="#b7e4c2")

    info = fig.text(0.06, 0.14, "", fontsize=8, color="dimgray", va="bottom")
    status_msg = fig.text(0.06, 0.02, "", fontsize=8, color="navy", va="bottom")


    #Inicialização de um dicionario "vazio" para armazenamento dos parametros da elipse 
    estado = {
        "x": 0.0, "y": 0.0, "a": 4.0, "b": 3.0,
        "elem": None, "t": None, "X": None, "Y": None
    }

    def marcar(px, py, texto, cor, dx, dy, ha="left"):
        ax.plot(px, py, "o", color=cor, markersize=5, zorder=5)
        ax.annotate(texto, (px, py), xytext=(dx, dy), textcoords="offset points",
                    fontsize=8, color=cor, zorder=6, ha=ha, fontweight="bold")

    def desenhar(_=None):
        status_msg.set_text("")
        try:
            x, y, a, b = [ler(c.text) for c in caixas]
        except ValueError:
            ax.set_title("Valores inválidos: digite apenas números.", color="red", fontsize=10)
            fig.canvas.draw_idle()
            return
        if a <= 0 or b <= 0:
            ax.set_title("a e b devem ser estritamente positivos.", color="red", fontsize=10)
            fig.canvas.draw_idle()
            return
        if a <= b:
            ax.set_title("Para eixo maior vertical, é necessário a > b.", color="red", fontsize=10)
            fig.canvas.draw_idle()
            return

        # 1. Cálculos matemáticos
        elem = calcular_elementos(x, y, a, b)
        t, X, Y = gerar_pontos(x, y, a, b)

        # 2. Armazenamento em memória
        estado["x"], estado["y"], estado["a"], estado["b"] = x, y, a, b
        estado["elem"], estado["t"], estado["X"], estado["Y"] = elem, t, X, Y

        # 3. Visualização e Identificação Gráfica
        c = elem["c"]
        d = elem["d"]
        e = elem["e"]
        lr = elem["lr"]
        d1, d2 = elem["diretrizes"]
        margem = max(a * 1.3, min(d * 1.15, a * 3))

        ax.clear()

        # Curva da elipse
        ax.plot(X, Y, color="royalblue", linewidth=2.2, label="Elipse")

        # Eixos: maior vertical e menor horizontal
        ax.plot([x, x], [y - a, y + a], "--", color="gray", linewidth=1.2)
        ax.plot([x - b, x + b], [y, y], "--", color="gray", linewidth=1.2)
        ax.text(x + 0.02 * margem, y - a * 0.55, "eixo maior (2a)", rotation=90,
                fontsize=8, color="gray", va="center")
        ax.text(x - b * 0.5, y - 0.05 * margem, "eixo menor (2b)",
                fontsize=8, color="gray", ha="center", va="top")

        # Semieixos a e b
        ax.text(x + 0.02 * margem, y + a * 0.5, f"a = {a:g}", fontsize=8, color="gray")
        ax.text(x + b * 0.5, y + 0.02 * margem, f"b = {b:g}", fontsize=8, color="gray", ha="center")

        # Latus Rectum nos dois focos
        semi_lr = lr / 2
        ax.plot([x - semi_lr, x + semi_lr], [y + c, y + c], color="purple", linestyle="-.", linewidth=1)
        ax.plot([x - semi_lr, x + semi_lr], [y - c, y - c], color="purple", linestyle="-.", linewidth=1)

        # Diretrizes: retas horizontais y = y0 ± a²/c
        ax.axhline(d1, color="forestgreen", linestyle=":", linewidth=1.4)
        ax.axhline(d2, color="forestgreen", linestyle=":", linewidth=1.4)
        ax.text(x - margem * 0.96, d1, f"diretriz d1: y = {d1:.4g}", fontsize=8, color="forestgreen", va="bottom")
        ax.text(x - margem * 0.96, d2, f"diretriz d2: y = {d2:.4g}", fontsize=8, color="forestgreen", va="top")

        # Pontos Notáveis
        marcar(x, y, f"C ({x:g}, {y:g})", "black", 6, -12)
        marcar(x, y + a, f"A1 ({x:g}, {y + a:g})", "crimson", 6, 4)
        marcar(x, y - a, f"A2 ({x:g}, {y - a:g})", "crimson", 6, -12)
        marcar(x + b, y, f"B1 ({x + b:g}, {y:g})", "darkorange", 5, 5)
        marcar(x - b, y, f"B2 ({x - b:g}, {y:g})", "darkorange", -65, 5)
        marcar(x, y + c, f"F1 ({x:g}, {y + c:.3g})", "purple", -6, -12, "right")
        marcar(x, y - c, f"F2 ({x:g}, {y - c:.3g})", "purple", -6, 4, "right")

        ax.set_xlim(x - margem, x + margem)
        ax.set_ylim(y - margem, y + margem)
        ax.set_aspect("equal")
        ax.grid(True, alpha=0.3, linestyle="--")
        ax.axhline(0, color="black", linewidth=0.6)
        ax.axvline(0, color="black", linewidth=0.6)
        ax.set_xlabel("x")
        ax.set_ylabel("y")

        A_c, B_c, D_c, E_c, F_c = elem["coef_geral"]
        ax.set_title(
            f"$\\frac{{(x-{x:g})^2}}{{{b:g}^2}} + \\frac{{(y-{y:g})^2}}{{{a:g}^2}} = 1$\n"
            f"Forma Geral: ${A_c:g}x^2 + {B_c:g}y^2 {D_c:+g}x {E_c:+g}y {F_c:+g} = 0$",
            fontsize=11, pad=10
        )

        info.set_text(
            f"C = centro | A = vértices maiores | B = co-vértices | F = focos | d = diretrizes | Latus Rectum = {lr:.4g}\n"
            f"c = {c:.4g} | excentricidade e = c/a = {e:.3f} | eixo maior = 2a = {2 * a:g} | eixo menor = 2b = {2 * b:g}\n"
            f"Raio: a e b são os semieixos (raio único apenas no círculo) | "
            f"Assíntotas: não existem na elipse (curva compacta)"
        )
        fig.canvas.draw_idle()

    def salvar_txt(_=None):
        if estado["elem"] is None:
            status_msg.set_text("Gere o gráfico primeiro antes de salvar os dados.")
            fig.canvas.draw_idle()
            return

        caminho_arquivo = os.path.abspath("dados_elipse_vertical.txt")
        try:
            salvar_relatorio_txt(
                caminho_arquivo,
                estado["x"], estado["y"], estado["a"], estado["b"],
                estado["elem"], estado["t"], estado["X"], estado["Y"]
            )
            nome_curto = os.path.basename(caminho_arquivo)
            status_msg.set_text(f"✓ Dados salvos com sucesso em '{nome_curto}'!")
        except Exception as err:
            status_msg.set_text(f"Erro ao salvar arquivo: {err}")
        fig.canvas.draw_idle()

    for c in caixas:
        c.on_submit(desenhar)
    botao_gerar.on_clicked(desenhar)
    botao_txt.on_clicked(salvar_txt)

    desenhar()
    plt.show()


if __name__ == "__main__":
    main()
