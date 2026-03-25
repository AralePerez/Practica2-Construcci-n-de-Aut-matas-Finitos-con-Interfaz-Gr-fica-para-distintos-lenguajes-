
import flet as ft

def main(page: ft.Page):
    page.title = "Simulador AFD/AFND FINAL"

    alfabeto = ft.TextField(label="Alfabeto (a,b)")
    estados = ft.TextField(label="Estados (q0,q1)")
    inicial = ft.TextField(label="Inicial")
    finales = ft.TextField(label="Finales")
    transiciones = ft.TextField(label="Transiciones (q0,a,q1; q1,b,q0)")

    cadena = ft.TextField(label="Cadena")
    resultado = ft.Text()
    traza = ft.Text()

    def simular(e):
        trans = {}
        for t in transiciones.value.split(";"):
            if t.strip():
                o,s,d = t.split(",")
                trans[(o,s)] = d

        actual = inicial.value
        recorrido = [actual]

        for c in cadena.value:
            if (actual,c) not in trans:
                resultado.value = "RECHAZADA"
                page.update()
                return
            actual = trans[(actual,c)]
            recorrido.append(actual)

        resultado.value = "ACEPTADA" if actual in finales.value.split(",") else "RECHAZADA"
        traza.value = " -> ".join(recorrido)
        page.update()

    page.add(
        alfabeto, estados, inicial, finales, transiciones,
        cadena,
        ft.ElevatedButton("Simular", on_click=simular),
        resultado, traza
    )

ft.app(target=main)
