import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button


def ler(texto):
    """Converte o texto digitado em número (aceita vírgula ou ponto)."""
    return float(texto.replace(",", ".").strip())


def main():
    fig, ax = plt.subplots(figsize=(7, 8))
    fig.subplots_adjust(bottom=0.28, top=0.92)

    # ---- Campos de entrada ----
    nomes = ["x", "y", "a", "b"]
    iniciais = ["0", "0", "4", "3"]
    posicoes = [0.07, 0.25, 0.43, 0.61]
    caixas = []
    for nome, ini, pos in zip(nomes, iniciais, posicoes):
        eixo_caixa = fig.add_axes([pos, 0.07, 0.10, 0.06])
        caixas.append(TextBox(eixo_caixa, f"{nome}: ", initial=ini))

    eixo_botao = fig.add_axes([0.79, 0.07, 0.15, 0.06])
    botao = Button(eixo_botao, "Gerar")

    info = fig.text(0.07, 0.15, "", fontsize=8, color="dimgray", va="bottom")

    def desenhar(_=None):
        # Lê e valida os valores
        try:
            x, y, a, b = [ler(c.text) for c in caixas]
        except ValueError:
            ax.set_title("Valores inválidos: digite apenas números.", color="red", fontsize=10)
            fig.canvas.draw_idle()
            return
        if a <= 0 or b <= 0:
            ax.set_title("a e b devem ser positivos.", color="red", fontsize=10)
            fig.canvas.draw_idle()
            return
        if a <= b:
            ax.set_title("Para eixo maior vertical, é preciso a > b.", color="red", fontsize=10)
            fig.canvas.draw_idle()
            return

        # Equação: (X - x)^2 / b^2 + (Y - y)^2 / a^2 = 1
        t = np.linspace(0, 2 * np.pi, 400)
        X = x + b * np.cos(t)
        Y = y + a * np.sin(t)
        c = np.sqrt(a**2 - b**2)  # distância do centro aos focos
        d = a**2 / c              # distância do centro às diretrizes
        e = c / a                 # excentricidade
        margem = max(a * 1.3, min(d * 1.15, a * 3))

        def marcar(px, py, texto, cor, dx, dy, ha="left"):
            ax.plot(px, py, "o", color=cor, markersize=6, zorder=5)
            ax.annotate(texto, (px, py), xytext=(dx, dy), textcoords="offset points",
                        fontsize=8, color=cor, zorder=6, ha=ha)

        ax.clear()
        ax.plot(X, Y, color="royalblue", linewidth=2)

        # Eixos (maior vertical e menor horizontal)
        ax.plot([x, x], [y - a, y + a], "--", color="gray", linewidth=1)
        ax.plot([x - b, x + b], [y, y], "--", color="gray", linewidth=1)
        ax.text(x + 0.02 * margem, y - a * 0.55, "eixo maior", rotation=90,
                fontsize=8, color="gray", va="center")
        ax.text(x - b * 0.5, y - 0.05 * margem, "eixo menor",
                fontsize=8, color="gray", ha="center", va="top")

        # Raios (semieixos)
        ax.text(x + 0.02 * margem, y + a * 0.5, f"a = {a:g}", fontsize=8, color="gray")
        ax.text(x + b * 0.5, y + 0.02 * margem, f"b = {b:g}",
                fontsize=8, color="gray", ha="center")

        # Diretrizes: y = y0 ± a²/c
        for sinal, nome in ((1, "d1"), (-1, "d2")):
            yd = y + sinal * d
            ax.axhline(yd, color="green", linestyle=":", linewidth=1.3)
            ax.text(x - margem * 0.97, yd, f"diretriz {nome}: y = {yd:.4g}",
                    fontsize=8, color="green", va="bottom")

        # Pontos notáveis
        marcar(x, y, f"C ({x:g}, {y:g})", "black", 6, -12)
        marcar(x, y + a, f"V1 ({x:g}, {y + a:g})", "crimson", 6, 4)
        marcar(x, y - a, f"V2 ({x:g}, {y - a:g})", "crimson", 6, -12)
        marcar(x + b, y, f"B1 ({x + b:g}, {y:g})", "darkorange", 4, 6)
        marcar(x - b, y, f"B2 ({x - b:g}, {y:g})", "darkorange", -70, 6)
        marcar(x, y + c, f"F1 ({x:g}, {y + c:.3g})", "purple", -6, -12, "right")
        marcar(x, y - c, f"F2 ({x:g}, {y - c:.3g})", "purple", -6, 4, "right")

        ax.set_xlim(x - margem, x + margem)
        ax.set_ylim(y - margem, y + margem)
        ax.set_aspect("equal")
        ax.grid(True, alpha=0.3)
        ax.axhline(0, color="black", linewidth=0.5)
        ax.axvline(0, color="black", linewidth=0.5)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(
            f"$\\frac{{(x-{x:g})^2}}{{{b:g}^2}} + \\frac{{(y-{y:g})^2}}{{{a:g}^2}} = 1$",
            fontsize=14,
        )
        info.set_text(
            f"C = centro | V = vértices | B = co-vértices | F = focos | d = diretrizes\n"
            f"c = {c:.4g} | excentricidade e = c/a = {e:.3f} | "
            f"eixo maior = 2a = {2 * a:g} | eixo menor = 2b = {2 * b:g}\n"
            f"Raio: a e b são os semieixos (raio único só no círculo) | "
            f"Assíntotas: não existem na elipse (só na hipérbole)"
        )
        fig.canvas.draw_idle()

    # Enter em qualquer campo ou clique no botão redesenham o gráfico
    for c in caixas:
        c.on_submit(desenhar)
    botao.on_clicked(desenhar)

    desenhar()
    plt.show()


if __name__ == "__main__":
    main()