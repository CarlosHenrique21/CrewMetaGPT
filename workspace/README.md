# Conversor Markdown para HTML

## Descrição do Projeto

O Conversor Markdown para HTML é uma ferramenta web que transforma textos escritos em Markdown em HTML de forma rápida, segura e confiável. Ideal para desenvolvedores, redatores, blogueiros e qualquer pessoa que queira converter seus documentos Markdown para HTML para uso em sites, blogs ou projetos web.

## Funcionalidades Principais

- Conversão em tempo real de Markdown para HTML.
- Suporte a títulos (#, ##, ###) convertidos para <h1>, <h2> e <h3>.
- Suporte a listas ordenadas (<ol>) e não ordenadas (<ul>).
- Conversão de links no formato [texto](url) para tags <a href="url">texto</a>.
- Entrada via área de texto ou upload de arquivo Markdown (.md, .markdown).
- Visualização do HTML gerado com sanitização para segurança.
- Exportação do HTML convertido como arquivo gerado pelo navegador.

## Requisitos

- Navegador moderno com suporte a JavaScript.
- Conexão de internet para baixar dependências, se necessário.

## Instalação

1. Clone este repositório:

```bash
git clone https://seu-repositorio/conversor-markdown-html.git
cd conversor-markdown-html
```

2. Instale as dependências:

```bash
npm install
```

3. Execute a aplicação em modo de desenvolvimento:

```bash
npm run dev
```

4. Acesse a aplicação no navegador em `http://localhost:3000` (ou porta indicada).

## Uso

- Digite seu texto Markdown na área de entrada ou faça upload de um arquivo `.md` ou `.markdown`.
- Veja a visualização do HTML gerado atualizada em tempo real.
- Clique em "Exportar HTML" para baixar o resultado como arquivo `output.html`.

### Exemplo Simples

Markdown de entrada:

```
# Título Principal

Este é um texto com uma lista:

- Item 1
- Item 2

[Link Google](https://google.com)
```

HTML gerado:

```html
<h1>Título Principal</h1>
<p>Este é um texto com uma lista:</p>
<ul>
<li>Item 1</li>
<li>Item 2</li>
</ul>
<p><a href="https://google.com">Link Google</a></p>
```

## Estrutura do Projeto

```
/conversor-markdown-html
├── public/               # Arquivo HTML base
│   └── index.html
├── src/
│   ├── components/       # Componentes React (InputArea, OutputArea, Toolbar)
│   ├── utils/            # Funções utilitárias, como parser Markdown
│   ├── App.tsx           # Componente principal
│   └── index.tsx         # Ponto de entrada da aplicação
├── tests/                # Testes unitários e de integração
├── package.json          # Dependências e scripts
├── tsconfig.json         # Configuração TypeScript
└── vite.config.ts        # Configuração do bundler
```

## Como Contribuir

Contribuições são bem-vindas! Siga os passos:

1. Faça um fork do projeto.
2. Crie uma branch para sua feature ou correção: `git checkout -b minha-feature`
3. Faça commits claros e descritivos.
4. Envie um pull request detalhando as mudanças realizadas.

Por favor, mantenha a consistência do código e siga as boas práticas de desenvolvimento.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

---

© 2024 Conversor Markdown para HTML. Todos os direitos reservados.
