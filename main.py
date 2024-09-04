# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.popup import Popup
import matplotlib.pyplot as plt
from data_manager import DataManager
import calendar
from datetime import datetime  # Asegúrate de importar datetime aquí

data_manager = DataManager()

class InicioScreen(Screen):
    def __init__(self, **kwargs):
        super(InicioScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.total_dinero = Label(text=f"Total Dinero Disponible: ${data_manager.get_total_dinero()}", font_size='20sp')
        layout.add_widget(self.total_dinero)

        btn_ingresos = Button(text="Agregar Ingresos", size_hint=(1, 0.2))
        btn_ingresos.bind(on_press=self.go_to_ingresos)
        layout.add_widget(btn_ingresos)

        btn_egresos = Button(text="Agregar Egresos", size_hint=(1, 0.2))
        btn_egresos.bind(on_press=self.go_to_egresos)
        layout.add_widget(btn_egresos)

        btn_resumen = Button(text="Ver Resumen", size_hint=(1, 0.2))
        btn_resumen.bind(on_press=self.go_to_resumen)
        layout.add_widget(btn_resumen)

        self.add_widget(layout)

    def go_to_ingresos(self, instance):
        self.manager.current = 'ingresos'

    def go_to_egresos(self, instance):
        self.manager.current = 'egresos'

    def go_to_resumen(self, instance):
        self.manager.current = 'resumen'

    def on_pre_enter(self):
        self.total_dinero.text = f"Total Dinero Disponible: ${data_manager.get_total_dinero()}"

class IngresosScreen(Screen):
    def __init__(self, **kwargs):
        super(IngresosScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Label(text="Nombre del Ingreso"))
        self.nombre = TextInput(multiline=False)
        layout.add_widget(self.nombre)

        layout.add_widget(Label(text="Monto"))
        self.monto = TextInput(multiline=False, input_filter='int', hint_text='Ingrese el monto en pesos')
        layout.add_widget(self.monto)

        layout.add_widget(Label(text="Medio de Pago"))
        self.medio_pago = Spinner(
            text='Transferencia',
            values=('Transferencia', 'Efectivo', 'Pago con tarjeta', 'Pago con billetera virtual')
        )
        layout.add_widget(self.medio_pago)

        layout.add_widget(Label(text="Motivo"))
        self.motivo = TextInput(multiline=False)
        layout.add_widget(self.motivo)

        layout.add_widget(Label(text="Estado (Total/Parcial)"))
        self.estado = TextInput(multiline=False)
        layout.add_widget(self.estado)

        btn_submit = Button(text="Guardar Ingreso")
        btn_submit.bind(on_press=self.save_ingreso)
        layout.add_widget(btn_submit)

        btn_inicio = Button(text="Volver al Inicio")
        btn_inicio.bind(on_press=self.go_to_inicio)
        layout.add_widget(btn_inicio)

        self.add_widget(layout)

    def save_ingreso(self, instance):
        if self.monto.text and self.nombre.text and self.motivo.text:
            data_manager.add_ingreso(self.nombre.text, int(self.monto.text), self.medio_pago.text, self.motivo.text, self.estado.text)
            popup = Popup(title='Ingreso Guardado',
                          content=Label(text='El ingreso ha sido guardado con éxito.'),
                          size_hint=(0.6, 0.4))
            popup.open()
            popup.bind(on_dismiss=self.go_to_inicio)
        else:
            popup = Popup(title='Error',
                          content=Label(text='Por favor, complete todos los campos.'),
                          size_hint=(0.6, 0.4))
            popup.open()

    def go_to_inicio(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'inicio'

class EgresosScreen(Screen):
    def __init__(self, **kwargs):
        super(EgresosScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Label(text="Nombre del Egreso"))
        self.nombre = TextInput(multiline=False)
        layout.add_widget(self.nombre)

        layout.add_widget(Label(text="Monto"))
        self.monto = TextInput(multiline=False, input_filter='int', hint_text='Ingrese el monto en pesos')
        layout.add_widget(self.monto)

        layout.add_widget(Label(text="Medio de Pago"))
        self.medio_pago = Spinner(
            text='Transferencia',
            values=('Transferencia', 'Efectivo', 'Pago con tarjeta', 'Pago con billetera virtual')
        )
        layout.add_widget(self.medio_pago)

        layout.add_widget(Label(text="Motivo"))
        self.motivo = TextInput(multiline=False)
        layout.add_widget(self.motivo)

        btn_submit = Button(text="Guardar Egreso")
        btn_submit.bind(on_press=self.save_egreso)
        layout.add_widget(btn_submit)

        btn_inicio = Button(text="Volver al Inicio")
        btn_inicio.bind(on_press=self.go_to_inicio)
        layout.add_widget(btn_inicio)

        self.add_widget(layout)

    def save_egreso(self, instance):
        if self.monto.text and self.nombre.text and self.motivo.text:
            data_manager.add_egreso(self.nombre.text, int(self.monto.text), self.medio_pago.text, self.motivo.text)
            popup = Popup(title='Egreso Guardado',
                          content=Label(text='El egreso ha sido guardado con éxito.'),
                          size_hint=(0.6, 0.4))
            popup.open()
            popup.bind(on_dismiss=self.go_to_inicio)
        else:
            popup = Popup(title='Error',
                          content=Label(text='Por favor, complete todos los campos.'),
                          size_hint=(0.6, 0.4))
            popup.open()

    def go_to_inicio(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'inicio'

class ResumenScreen(Screen):
    def __init__(self, **kwargs):
        super(ResumenScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.add_widget(self.layout)

        self.mes_actual = datetime.now().month

        self.dinero_disponible = Label(text=f"Dinero Disponible: ${data_manager.get_total_dinero()}", font_size='20sp')
        self.layout.add_widget(self.dinero_disponible)

        self.chart_image = Label()  # Placeholder para la imagen del gráfico
        self.layout.add_widget(self.chart_image)

        # Filtro por día, semana, mes, año
        self.filtro = Spinner(
            text='Mes',
            values=('Día', 'Semana', 'Mes', 'Año'),
            size_hint=(None, None),
            size=(100, 44),
        )
        self.filtro.bind(text=self.actualizar_lista)
        self.layout.add_widget(self.filtro)

        # Lista de ingresos y egresos
        self.lista = BoxLayout(orientation='vertical')
        self.layout.add_widget(self.lista)

        btn_inicio = Button(text="Volver al Inicio")
        btn_inicio.bind(on_press=self.go_to_inicio)
        self.layout.add_widget(btn_inicio)

    def on_enter(self):
        self.actualizar_resumen()
        self.actualizar_lista(self.filtro, self.filtro.text)

    def actualizar_resumen(self):
        ingresos, egresos = data_manager.get_ingresos_egresos_por_mes(f'{self.mes_actual:02}')
        dinero_disponible = ingresos - egresos
        self.dinero_disponible.text = f"Dinero Disponible: ${dinero_disponible}"

        labels = ['Ingresos', 'Egresos']
        sizes = [ingresos, egresos]
        colors = ['#4CAF50', '#F44336']

        plt.figure(figsize=(5, 5))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
        plt.axis('equal')
        plt.savefig('resumen_pie_chart.png')
        plt.close()

        self.chart_image.text = 'resumen_pie_chart.png'  # Actualizar la imagen del gráfico

    def actualizar_lista(self, spinner, texto):
        # Limpiar lista actual
        self.lista.clear_widgets()

        # Obtener datos filtrados según la opción seleccionada
        if texto == 'Día':
            registros = data_manager.get_registros_filtrados('dia')
        elif texto == 'Semana':
            registros = data_manager.get_registros_filtrados('semana')
        elif texto == 'Año':
            registros = data_manager.get_registros_filtrados('año')
        else:  # Mes por defecto
            registros = data_manager.get_registros_filtrados('mes')

        for registro in registros:
            icon_color = '#4CAF50' if registro['tipo'] == 'ingreso' else '#F44336'
            item = BoxLayout(orientation='horizontal', spacing=10)
            icon = Label(text='●', color=(1, 0, 0, 1) if icon_color == '#F44336' else (0, 1, 0, 1))
            item.add_widget(icon)
            item.add_widget(Label(text=f"{registro['nombre']}, ${registro['monto']}"))
            self.lista.add_widget(item)

    def on_touch_move(self, touch):
        if touch.x < touch.ox:
            self.mes_actual = (self.mes_actual % 12) + 1  # Cambiar al siguiente mes
            self.on_enter()  # Actualizar el resumen para el nuevo mes
        elif touch.x > touch.ox:
            self.mes_actual = (self.mes_actual - 2) % 12 + 1  # Cambiar al mes anterior
            self.on_enter()  # Actualizar el resumen para el nuevo mes

    def go_to_inicio(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'inicio'

class MiApp(App):
    def build(self):
        sm = ScreenManager()

        self.inicio_screen = InicioScreen(name='inicio')
        self.ingresos_screen = IngresosScreen(name='ingresos')
        self.egresos_screen = EgresosScreen(name='egresos')
        self.resumen_screen = ResumenScreen(name='resumen')

        sm.add_widget(self.inicio_screen)
        sm.add_widget(self.ingresos_screen)
        sm.add_widget(self.egresos_screen)
        sm.add_widget(self.resumen_screen)

        return sm

if __name__ == '__main__':
    MiApp().run()
