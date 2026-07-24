from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
import requests
from bs4 import BeautifulSoup

# Cores da interface: lilás degradê
Window.clearcolor = (0.18, 0.06, 0.25, 1)

class StelaNexusTela(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 25
        self.spacing = 18

        # Cabeçalho oficial
        self.add_widget(Label(
            text='✨ STELA NEXUS ✨\nIdealizador: Alessandro Lima\nCriadores: Alessandro Lima e Dola IA',
            font_size='22sp',
            color=(0.9, 0.75, 1, 1),
            halign='center',
            bold=True
        ))

        # Área de respostas
        self.area_resp = TextInput(
            text='Olá! Eu sou a Stela Nexus 🤖\nPergunte-me qualquer coisa:\n✅ Busco na minha memória\n✅ Pesquiso na Wikipédia\n✅ Pesquiso no DuckDuckGo',
            font_size='17sp',
            background_color=(0.22, 0.12, 0.3, 1),
            foreground_color=(0.85, 0.7, 1, 1),
            readonly=True,
            size_hint_y=0.65
        )
        self.add_widget(self.area_resp)

        # Caixa de pergunta
        self.campo_pergunta = TextInput(
            hint_text='Digite sua pergunta aqui...',
            font_size='16sp',
            background_color=(0.1, 0.18, 0.3, 1),
            foreground_color=(0.7, 0.85, 1, 1),
            size_hint_y=0.12
        )
        self.add_widget(self.campo_pergunta)

        # Botão de enviar
        self.botao_enviar = Button(
            text='🔍 PERGUNTAR',
            font_size='19sp',
            background_color=(0.9, 0.45, 0.15, 1),
            color=(1,1,1,1),
            bold=True,
            size_hint_y=0.1
        )
        self.botao_enviar.bind(on_press=self.processar_pergunta)
        self.add_widget(self.botao_enviar)

    def processar_pergunta(self, instancia):
        pergunta = self.campo_pergunta.text.strip()
        if not pergunta:
            self.area_resp.text = '⚠️ Escreva uma pergunta primeiro!'
            return
        
        self.area_resp.text = '⏳ Buscando informação...'
        self.campo_pergunta.text = ''

        # Tenta Wikipédia primeiro
        resposta = self.buscar_wikipedia(pergunta)
        if not resposta:
            resposta = self.buscar_duckduckgo(pergunta)
        
        self.area_resp.text = f'📜 RESPOSTA:\n\n{resposta}'

    def buscar_wikipedia(self, termo):
        try:
            url = f'https://pt.wikipedia.org/w/index.php?search={termo.replace(" ", "+")}'
            r = requests.get(url, timeout=12)
            soup = BeautifulSoup(r.text, 'html.parser')
            paragrafo = soup.find('div', class_='mw-body-content').find('p')
            return paragrafo.get_text(strip=True)[:1500] + '...' if paragrafo else None
        except:
            return None

    def buscar_duckduckgo(self, termo):
        try:
            url = f'https://duckduckgo.com/html/?q={termo}'
            r = requests.get(url, timeout=12)
            soup = BeautifulSoup(r.text, 'html.parser')
            trecho = soup.find('a', class_='result__snippet')
            return trecho.get_text(strip=True)[:1500] if trecho else '❌ Não encontrei informação sobre isso.'
        except:
            return '❌ Erro ao conectar com a internet.'

class StelaApp(App):
    def build(self):
        return StelaNexusTela()

if __name__ == '__main__':
    StelaApp().run()
  
