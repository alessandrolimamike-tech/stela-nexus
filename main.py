from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
import requests
from bs4 import BeautifulSoup

# Fundo da tela: lilás escuro
Window.clearcolor = (0.18, 0.06, 0.25, 1)

class StelaTela(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 25
        self.spacing = 18

        # Cabeçalho
        self.add_widget(Label(
            text='STELA NEXUS\nIdealizador: Alessandro Lima\nCriadores: Alessandro Lima e Dola IA',
            font_size='20sp',
            color=(0.9, 0.75, 1, 1),
            halign='center',
            bold=True
        ))

        # Área de respostas
        self.resposta = TextInput(
            text='Olá! Eu sou a Stela Nexus.\nPergunte-me qualquer coisa.',
            font_size='16sp',
            background_color=(0.22, 0.12, 0.3, 1),
            foreground_color=(0.85, 0.7, 1, 1),
            readonly=True,
            size_hint_y=0.6
        )
        self.add_widget(self.resposta)

        # Caixa de pergunta
        self.pergunta = TextInput(
            hint_text='Digite sua pergunta...',
            font_size='16sp',
            background_color=(0.1, 0.18, 0.3, 1),
            foreground_color=(0.7, 0.85, 1, 1),
            size_hint_y=0.12
        )
        self.add_widget(self.pergunta)

        # Botão de envio
        self.botao = Button(
            text='PERGUNTAR',
            font_size='18sp',
            background_color=(0.9, 0.45, 0.15, 1),
            color=(1,1,1,1),
            bold=True,
            size_hint_y=0.1
        )
        self.botao.bind(on_press=self.buscar)
        self.add_widget(self.botao)

    def buscar(self, instancia):
        texto = self.pergunta.text.strip()
        if not texto:
            return
        self.resposta.text = 'Buscando informação...'
        self.pergunta.text = ''

        # Busca na Wikipédia
        try:
            url = f'https://pt.wikipedia.org/w/index.php?search={texto.replace(" ", "+")}'
            cabecalho = {'User-Agent': 'Mozilla/5.0 (Android 14; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36'}
            r = requests.get(url, headers=cabecalho, timeout=15)
            soup = BeautifulSoup(r.text, 'html.parser')
            conteudo = soup.find('div', class_='mw-body-content')
            if conteudo:
                paragrafo = conteudo.find('p')
                if paragrafo:
                    texto_final = paragrafo.get_text(strip=True)[:1200]
                    self.resposta.text = texto_final if texto_final else 'Encontrei o tema, mas não há resumo curto disponível.'
                    return
            self.resposta.text = 'Não encontrei informação sobre esse assunto.'
        except Exception as e:
            self.resposta.text = f'Não consegui buscar no momento: {str(e)}'

class StelaApp(App):
    def build(self):
        return StelaTela()

if __name__ == '__main__':
    StelaApp().run()
