import numpy as np
import matplotlib.pyplot as plt

# ====== VALORES DE ENTRADA ======
x = 0.0   # coordenada x do centro
y = 0.0   # coordenada y do centro
a = 5.0   # semieixo maior (vertical)
b = 3.0   # semieixo menor (horizontal)
# =================================


def main():
    if a <= 0 or b <= 0:
        raise ValueError("a e b devem ser positivos.")
    if a <= b:
        raise ValueError("Para eixo maior vertical, é preciso a > b.")

    # Equação: (X - x)^2 / b^2 + (Y - y)^2 / a^2 = 1
    t = np.linspace(0, 2 * np.pi, 400)
    X = x + b * np.cos(t)
    Y = y + a * np.sin(t)

    # Focos (ficam sobre o eixo vertical)
    c = np.sqrt(a**2 - b**2)
    focos = [(x, y + c), (x, y - c)]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(X, Y, color="royalblue", linewidth=2, label="Elipse")
    ax.plot(x, y, "ko", label="Centro")
    ax.plot([f[0] for f in focos], [f[1] for f in focos], "rx", label="Focos")

    # Eixos da elipse
    ax.plot([x, x], [y - a, y + a], "--", color="gray", linewidth=1)
    ax.plot([x - b, x + b], [y, y], "--", color="gray", linewidth=1)

    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(
        f"$\\frac{{(x-{x:g})^2}}{{{b:g}^2}} + \\frac{{(y-{y:g})^2}}{{{a:g}^2}} = 1$"
    )
    ax.legend()
    plt.show()


if __name__ == "__main__":
    main()