# Lilie - Assistente Virtual IA de Bolso

Lilie é um projeto desenvolvido para a feira de ciências da escola, com o objetivo de criar um assistente virtual compacto, inteligente e acessível. A proposta é oferecer uma IA de bolso, capaz de interagir com o usuário de forma simples e eficiente, realizando tarefas do dia a dia a partir de comandos de voz ou texto.

## Objetivo

O projeto busca prototipar um assistente virtual baseado em IA que possa rodar em dispositivos de baixo custo, como o Raspberry Pi Zero 2 W, tornando-o portátil e prático para uso cotidiano. A ideia é que, com uma frase, o usuário possa acionar uma ação instantaneamente, tornando a experiência fluida e intuitiva.

## Funcionalidades

- **Interface Simples e Moderna:** Desenvolvida em Python com [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) para uma experiência visual agradável.
- **Integração com IA:** Utiliza modelos de linguagem avançados via API para responder perguntas, conversar e executar comandos.
- **Integração com Google Calendar:** Permite agendar eventos e compromissos por comando de voz ou texto.
- **Extensível:** Estrutura modular para fácil adição de novas integrações, como relógio, Spotify e outros dispositivos.
- **Compatibilidade:** Pensado para rodar em sistemas Windows e, futuramente, em Raspberry Pi Zero 2 W.

## Estrutura do Projeto

```
Lilie4.9/
├── app.py
├── config.json
├── modules/
│   ├── main_window.py
│   ├── settings.py
│   ├── ai_client.py
│   ├── chat_ui.py
│   ├── event_manager.py
│   ├── ui_components.py
│   ├── voice.py
│   ├── calendar_integration.py
│   └── event_parser.py
└── README.md
```

- **app.py:** Inicializa e executa a aplicação.
- **modules/**: Contém todos os módulos responsáveis por interface, integração com IA, voz, calendário, parser de eventos e configurações.

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
     python app.py
     ```

## Futuro do Projeto

- **Portabilidade:** Rodar em Raspberry Pi Zero 2 W.
- **Interação Multidispositivos:** Conexão com relógio, Spotify e outros serviços.
- **Aprimoramento de Ações:** Tornar possível executar qualquer ação com uma frase.
- **Melhorias de Interface e Acessibilidade.**

## Equipe

- **Desenvolvimento Principal:** Athlas (Elder Luiz)
- **Equipe de Apoio:** 3 colegas do colégio, responsáveis por documentação, pesquisa teórica e suporte.

---

Este projeto está em desenvolvimento e aberto a sugestões
