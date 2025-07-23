# Lilie - Assistente Virtual IA de Bolso

Lilie é um projeto desenvolvido para a feira de ciências da escola, com o objetivo de criar um assistente virtual compacto, inteligente e acessível. A proposta é oferecer uma IA de bolso, capaz de rodar em dispositivos de baixo custo e fácil de usar.

## Objetivo

O projeto busca prototipar um assistente virtual baseado em IA que possa rodar em dispositivos de baixo custo, como o Raspberry Pi Zero 2 W, tornando-o portátil e prático para uso cotidiano. A ideia é democratizar o acesso a assistentes inteligentes.

## Funcionalidades

- **Interface Simples e Moderna:** Desenvolvida em Python com [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) para uma experiência visual agradável.
- **Barra Lateral (Sidebar):** Navegação fácil entre Início, Configurações, Sobre e Ajuda.
- **Animação de Carregamento:** Feedback visual enquanto a IA processa respostas.
- **Integração com IA:** Utiliza modelos de linguagem avançados via API para responder perguntas, conversar e executar comandos.
- **Respostas por Voz:** A Lilie lê as respostas em voz alta usando síntese de fala.
- **Integração com Google Calendar:** Permite agendar eventos e compromissos por comando de voz ou texto, com extração inteligente de datas e horários.
- **Busca Online Automática:** Perguntas iniciadas por "quem", "como", "quando", etc. são pesquisadas automaticamente no Google e resumidas pela IA.
- **Extensível:** Estrutura modular para fácil adição de novas integrações, como relógio, Spotify e outros dispositivos.
- **Compatibilidade:** Pensado para rodar em sistemas Windows e, futuramente, em Raspberry Pi Zero 2 W.

## Estrutura do Projeto

```
Lilie5.0/
├── Lilie.py
├── config.json
├── credentials.json
├── modules/
│   ├── main_window.py
│   ├── settings.py
│   ├── ai_client.py
│   ├── chat_ui.py
│   ├── event_manager.py
│   ├── ui_components.py
│   ├── voice.py
│   ├── calendar_integration.py
│   ├── event_parser.py
│   ├── google_search.py
│   └── utils.py
├── lilie.ico
├── send.mp3
├── README.md
├── requirements.txt
└── token.pickle
```

- **Lilie.py:** Inicializa e executa a aplicação.
- **modules/**: Contém todos os módulos responsáveis por interface, integração com IA, voz, calendário, parser de eventos, busca online, configurações e utilidades.

## Como Executar

1. **Pré-requisitos:**  
   - Python 3.10+
   - Instale as dependências:
     ```
     pip install -r requirements.txt
     ```
2. **Configuração:**  
   - Adicione sua chave de API no arquivo `config.json` ou pela interface de configurações do app.
3. **Execução:**  
   - No terminal, execute:
     ```
     python Lilie.py
     ```

## Futuro do Projeto

- **Portabilidade:** Rodar em Raspberry Pi Zero 2 W.
- **Interação Multidispositivos:** Conexão com relógio, Spotify e outros serviços.
- **Aprimoramento de Ações:** Tornar possível executar qualquer ação com uma frase.
- **Melhorias de Interface e Acessibilidade.**

## Equipe

- **Desenvolvimento Principal:** Elder Luiz - Desenvolvedor geral do projeto
- **Equipe de Apoio:** Isabela Pereira e Lígia Luíza - Análise, pesquisas, revisões e controle externo do projeto

---

Este projeto está em desenvolvimento e aberto a sugestões

---

## Sobre o Autor

Fala devs (ou leigos) ^^

Tá curioso sobre mim ou sobre o projeto? Vamo lá então...

Eu sou o Athlas (meu nome real é Elder Luiz), tenho 16 anos e comecei a programar tem pouco mais de 1 mês. Se você leu o readme.md da Lilie já entendeu que esse projeto nasceu para uma feira de ciências.

Eu comecei esse projeto sem nem saber o que era o VSCode, não sabia de absolutamente nada de programação, mas eu sabia uma coisa: Pesquisar! Eu nunca gostei de estudar e maximizar o máximo uma nota, mas sempre gostei de aprender, e programar é sobre isso: aprender a resolver problemas.

Esse projeto deixou de ser só um trabalho de escola, a Lilie é meu projeto pessoal que vou aperfeiçoar pelo resto da minha vida, é minha primeira criação e eu tenho orgulho disso. Se você leu até aqui, obrigado, já é um grande apoio :)

Athlas, o Monarca - 15/06/2025
