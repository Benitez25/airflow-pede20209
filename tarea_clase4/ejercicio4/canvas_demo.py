from celery import Celery, chain, group, chord

app = Celery(
    "canvas_demo",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)


@app.task
def sumar(a, b):
    return a + b


@app.task
def multiplicar(valor, factor):
    return valor * factor


@app.task
def cuadrado(valor):
    return valor ** 2


@app.task
def cubo(valor):
    return valor ** 3


@app.task
def resumir(resultados):
    return {"resultados": resultados, "suma_total": sum(resultados)}


if __name__ == "__main__":
    print("=== CHAIN ===")
    resultado_chain = chain(
        sumar.s(2, 3),
        multiplicar.s(10),
        cuadrado.s(),
    ).apply_async()
    print("Resultado chain:", resultado_chain.get(timeout=30))

    print("\n=== GROUP ===")
    resultado_group = group(
        cuadrado.s(2),
        cuadrado.s(3),
        cubo.s(2),
        sumar.s(10, 5),
    ).apply_async()
    print("Resultado group:", resultado_group.get(timeout=30))

    print("\n=== CHORD ===")
    resultado_chord = chord(
        group(
            cuadrado.s(2),
            cuadrado.s(3),
            cubo.s(2),
            sumar.s(10, 5),
        ),
        resumir.s(),
    ).apply_async()
    print("Resultado chord:", resultado_chord.get(timeout=30))
