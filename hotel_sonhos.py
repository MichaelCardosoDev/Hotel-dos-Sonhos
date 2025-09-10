import flet as ft
from datetime import datetime
import json

class Cliente:
    def __init__(self, nome, telefone, email, id_unico):
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.id_unico = id_unico

class Quarto:
    def __init__(self, numero, tipo, preco_diaria, disponivel=True):
        self.numero = numero
        self.tipo = tipo
        self.preco_diaria = preco_diaria
        self.disponivel = disponivel

class Reserva:
    def __init__(self, cliente, quarto, checkin, checkout):
        self.cliente = cliente
        self.quarto = quarto
        self.checkin = checkin
        self.checkout = checkout
        self.status = "Ativa"

    def to_dict(self):
        return {
            "cliente": vars(self.cliente),
            "quarto": vars(self.quarto),
            "checkin": self.checkin,
            "checkout": self.checkout,
            "status": self.status
        }

class GerenciadorDeReservas:
    def __init__(self):
        self.reservas = []

    def verificar_disponibilidade(self, tipo_quarto):
        for quarto in quartos:
            if quarto.tipo == tipo_quarto and quarto.disponivel:
                return quarto
        return None

    def criar_reserva(self, cliente, tipo_quarto, checkin, checkout):
        quarto_disponivel = self.verificar_disponibilidade(tipo_quarto)
        if quarto_disponivel:
            reserva = Reserva(cliente, quarto_disponivel, checkin, checkout)
            quarto_disponivel.disponivel = False
            self.reservas.append(reserva)
            return reserva
        return None

    def cancelar_reserva(self, id_cliente):
        for reserva in self.reservas:
            if reserva.cliente.id_unico == id_cliente and reserva.status == "Ativa":
                reserva.status = "Cancelada"
                reserva.quarto.disponivel = True
                return reserva
        return None

    def salvar_reservas_json(self, caminho="reservas.json"):
        with open(caminho, "w") as f:
            json.dump([r.to_dict() for r in self.reservas], f, indent=4)

quartos = [
    Quarto(101, "single", 100),
    Quarto(102, "double", 150),
    Quarto(201, "suite", 250)
]
gerenciador = GerenciadorDeReservas()

def main(page: ft.Page):
    page.title = "Sistema de Reservas de Hotel"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.ALWAYS
    page.padding = 25

    def criar_textfield(label):
        return ft.TextField(label=label, expand=True, border_radius=10, border_color=ft.colors.BLUE_GREY_100)

    nome = criar_textfield("Nome do Cliente")
    telefone = criar_textfield("Telefone")
    email = criar_textfield("Email")
    id_unico = criar_textfield("ID Único")
    tipo_quarto = ft.Dropdown(
        label="Tipo de Quarto",
        options=[ft.dropdown.Option("single"), ft.dropdown.Option("double"), ft.dropdown.Option("suite")],
        expand=True,
        border_radius=10,
        filled=True,
        bgcolor=ft.colors.BLUE_GREY_50
    )
    checkin = criar_textfield("Check-in (DD/MM/AAAA)")
    checkout = criar_textfield("Check-out (DD/MM/AAAA)")
    resultado = ft.Text("", size=16, weight="bold", color=ft.colors.BLUE_600)

    reservas_listagem = ft.Column(spacing=5, scroll=ft.ScrollMode.ALWAYS)

    def atualizar_reservas():
        reservas_listagem.controls.clear()
        for r in gerenciador.reservas:
            reservas_listagem.controls.append(
                ft.Container(
                    content=ft.Text(
                        f"{r.cliente.nome} • Quarto {r.quarto.numero} • {r.checkin} até {r.checkout} • {r.status}",
                        size=14
                    ),
                    bgcolor=ft.colors.BLUE_GREY_50,
                    border_radius=8,
                    padding=10
                )
            )
        page.update()

    def reservar(e):
        cliente = Cliente(nome.value, telefone.value, email.value, id_unico.value)
        try:
            checkin_dt = datetime.strptime(checkin.value, "%d/%m/%Y").strftime("%d/%m/%Y")
            checkout_dt = datetime.strptime(checkout.value, "%d/%m/%Y").strftime("%d/%m/%Y")
        except:
            resultado.value = "Datas inválidas! Use DD/MM/AAAA"
            page.update()
            return

        reserva = gerenciador.criar_reserva(cliente, tipo_quarto.value, checkin_dt, checkout_dt)
        if reserva:
            resultado.value = f"✅ Reserva criada! Quarto {reserva.quarto.numero}"
            atualizar_reservas()
        else:
            resultado.value = "❌ Nenhum quarto disponível!"
        page.update()

    id_cancelar = criar_textfield("ID para Cancelar")
    cancelar_resultado = ft.Text("", size=14, weight="bold", color=ft.colors.RED_400)

    def cancelar(e):
        cancelada = gerenciador.cancelar_reserva(id_cancelar.value)
        if cancelada:
            cancelar_resultado.value = f"Reserva cancelada para {cancelada.cliente.nome}."
            atualizar_reservas()
        else:
            cancelar_resultado.value = "Reserva não encontrada."
        page.update()

    def salvar(e):
        gerenciador.salvar_reservas_json()
        resultado.value = "📁 Reservas salvas com sucesso!"
        page.update()

    page.add(
        ft.Column([
            ft.Text("🛎️ Sistema de Reserva de Hotel", size=26, weight="bold", color=ft.colors.BLUE_800),
            ft.Container(
                content=ft.Column([
                    nome, telefone, email, id_unico,
                    tipo_quarto, checkin, checkout,
                    ft.ElevatedButton("Reservar", on_click=reservar, bgcolor=ft.colors.BLUE_600),
                    resultado
                ]),
                bgcolor=ft.colors.BLUE_50,
                border_radius=12,
                padding=20,
                margin=10
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("❌ Cancelar Reserva", size=18, weight="bold", color=ft.colors.RED_600),
                    id_cancelar,
                    ft.ElevatedButton("Cancelar", on_click=cancelar, bgcolor=ft.colors.RED_400),
                    cancelar_resultado
                ]),
                bgcolor=ft.colors.RED_50,
                border_radius=12,
                padding=20,
                margin=10
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("📋 Lista de Reservas", size=18, weight="bold"),
                    reservas_listagem
                ]),
                bgcolor=ft.colors.GREEN_50,
                border_radius=12,
                padding=20,
                margin=10,
                height=300
            ),
            ft.ElevatedButton("💾 Salvar em JSON", on_click=salvar, bgcolor=ft.colors.GREEN_500)
        ])
    )

ft.app(target=main)
