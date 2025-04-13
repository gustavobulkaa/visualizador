import kivy
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
import os
import random

kivy.require('1.11.1')

class Visualizador(BoxLayout):
    def __init__(self, **kwargs):
        super(Visualizador, self).__init__(orientation='vertical', **kwargs)

        self.casos_total = 26
        self.casos_vistos = []
        self.resposta_mostrada = False
        self.imagem_atual = None
        self.index_atual = -1

        self.image_widget = Image(allow_stretch=True, keep_ratio=True)
        self.add_widget(self.image_widget)

        botoes = BoxLayout(size_hint=(1, 0.1))
        self.botao_voltar = Button(text="◀ Voltar", background_color=(1, 0.6, 0, 1))
        self.botao_resposta = Button(text="Mostrar Resposta", background_color=(1, 0, 0, 1))
        self.botao_proximo = Button(text="Próxima ▶", background_color=(0, 1, 0, 1))

        self.botao_voltar.bind(on_release=self.voltar)
        self.botao_resposta.bind(on_release=self.mostrar_resposta)
        self.botao_proximo.bind(on_release=self.mostrar_proximo)

        botoes.add_widget(self.botao_voltar)
        botoes.add_widget(self.botao_resposta)
        botoes.add_widget(self.botao_proximo)

        self.add_widget(botoes)

        self.mostrar_proximo()

    def mostrar_imagem(self, caminho):
        if os.path.exists(caminho):
            self.image_widget.source = caminho
            self.image_widget.reload()
        else:
            self.popup_mensagem("Imagem não encontrada:\n" + caminho)

    def mostrar_proximo(self, *args):
        if len(self.casos_vistos) >= self.casos_total:
            self.popup_mensagem("Todos os casos foram vistos.")
            return

        while True:
            numero = random.randint(1, self.casos_total)
            if numero not in self.casos_vistos:
                break

        self.index_atual = numero
        self.casos_vistos.append(numero)
        self.resposta_mostrada = False
        caminho = f"imagens/caso {numero}.jpg"
        self.mostrar_imagem(caminho)

    def voltar(self, *args):
        if len(self.casos_vistos) > 1:
            self.casos_vistos.pop()
            self.index_atual = self.casos_vistos[-1]
            self.resposta_mostrada = False
            caminho = f"imagens/caso {self.index_atual}.jpg"
            self.mostrar_imagem(caminho)

    def mostrar_resposta(self, *args):
        if self.index_atual == -1 or self.resposta_mostrada:
            return
        caminho = f"imagens/caso {self.index_atual} resposta.jpg"
        self.resposta_mostrada = True
        self.mostrar_imagem(caminho)

    def popup_mensagem(self, mensagem):
        popup = Popup(title='Aviso',
                      content=Label(text=mensagem),
                      size_hint=(0.8, 0.3))
        popup.open()


class VisualizadorApp(App):
    def build(self):
        return Visualizador()


if __name__ == '__main__':
    VisualizadorApp().run()