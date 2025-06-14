# Lilie - Assistente Virtual IA de Bolso

Lilie é um projeto desenvolvido para a feira de ciências da escola, com o objetivo de criar um assistente virtual compacto, inteligente e acessível. A proposta é oferecer uma IA de bolso, capaz de rodar em dispositivos de baixo custo e fácil de usar.

## Objetivo

O projeto busca prototipar um assistente virtual baseado em IA que possa rodar em dispositivos de baixo custo, como o Raspberry Pi Zero 2 W, tornando-o portátil e prático para uso cotidiano. A ideia é democratizar o acesso a assistentes inteligentes.

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

---

## Sobre o Autor

Fala devs ^^

Tá curioso sobre mim ou sobre o projeto? Vamo lá então...

Eu sou o Athlas (meu nome real é Elder Luiz), tenho 16 anos e comecei a programar tem pouco mais de 1 mês. Se você leu o readme.md da Lilie já entendeu que esse projeto nasceu para uma feira de ciências.

Eu comecei esse projeto sem nem saber o que era o VSCode, não sabia de absolutamente nada de programação, mas eu sabia uma coisa: Pesquisar! Eu nunca gostei de estudar e maximizar o máximo uma nota, mas sempre gostei de aprender, e programar é sobre isso: aprender a resolver problemas.

Esse projeto deixou de ser só um trabalho de escola, a Lilie é meu projeto pessoal que vou aperfeiçoar pelo resto da minha vida, é minha primeira criação e eu tenho orgulho disso. Se você leu até aqui, obrigado por apoiar de alguma forma :)

Athlas, o Dev que programava sem saber uma única linha de código - 14/06/2025
