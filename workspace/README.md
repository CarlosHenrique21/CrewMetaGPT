# Conversor Markdown para HTML

## Descrição do Projeto

O Conversor Markdown para HTML é uma ferramenta que permite converter textos escritos em Markdown para código HTML válido e seguro. A aplicação suporta a transformação precisa de títulos (níveis 1 a 3), listas ordenadas e não ordenadas (incluindo listas aninhadas), além de links formatados em Markdown. O projeto é ideal para desenvolvedores, criadores de conteúdo e qualquer usuário que queira visualizar ou publicar documentos Markdown em formato HTML.

## Funcionalidades

- Conversão precisa de títulos Markdown (#, ##, ###) para tags HTML correspondentes (h1, h2, h3).
- Suporte a listas não ordenadas (-, *, +) e ordenadas (1., 2., 3.) com níveis de aninhamento.
- Conversão de links Markdown ([texto](url)) para tags HTML <a href="url">texto</a>.
- Interface Web interativa para edição e visualização em tempo real do HTML gerado.
- Ferramenta de linha de comando (CLI) para conversão offline e integração em scripts.
- API REST para integração com outros sistemas.
- Sanitização do HTML gerado para garantir segurança contra ataques XSS.

## Instalação

### Backend (Python)

1. Certifique-se de ter Python 3.x instalado.
2. Clone o repositório do projeto.
3. Navegue até a pasta `backend/`.
4. Instale as dependências com:

```
pip install -r requirements.txt
```

5. Para rodar a API REST:

```
python api.py
```

A API estará disponível em http://localhost:5000.

### CLI (Node.js)

1. Certifique-se de ter Node.js instalado.
2. Na raiz do projeto, instale as dependências:

```
npm install
```

3. Para usar o CLI:

```
node cli/index.js [input.md] [output.html]
```

- Se nenhum arquivo de entrada for passado, o CLI lerá o Markdown via stdin.
- Se nenhum arquivo de saída for informado, o HTML será impresso no stdout.
- Use `-h` ou `--help` para ver instruções.

### Frontend (React)

1. Acesse a pasta `frontend/`.
2. Instale as dependências:

```
npm install
```

3. Para iniciar a aplicação web:

```
npm run frontend
```

4. Abra o navegador em http://localhost:3000 para acessar a interface.

## Como Usar

### Interface Web
- Digite ou cole Markdown no editor da esquerda.
- Veja o HTML gerado atualizado em tempo real no painel da direita.
- Use o botão "Copiar HTML" para copiar o conteúdo convertido para a área de transferência.
- Use o botão "Exportar HTML" para baixar o conteúdo convertido como arquivo HTML.

### CLI
- Execute a ferramenta passando um arquivo Markdown para convertê-lo para HTML.
- Exemplo:

```
node cli/index.js exemplo.md resultado.html
```

- Ou use via pipeline:

```
echo "# Título" | node cli/index.js
```

### API REST
- Faça requisição POST para `/convert` com JSON:

```json
{
  "markdown": "# Seu Markdown aqui"
}
```

- Receberá JSON com HTML convertido e sanitizado.

## Estrutura do Projeto

```
project-root/
│
├── backend/                 # Código Python para API e conversão
│   ├── converter/           # Módulo de conversão Markdown para HTML
│   ├── api.py               # Servidor REST API Flask
│   └── requirements.txt     # Dependências Python
│
├── cli/                    # Código CLI Node.js
│
├── frontend/                # Aplicação web React
├── docs/                   # Documentação
├── tests/                  # Testes automatizados
├── README.md               # Documentação principal
└── package.json            # Dependências Node.js
```

## Contribuição

Sinta-se à vontade para contribuir! Seguem algumas orientações:

- Abra issues para bugs ou sugestões.
- Faça pull requests com explicações claras sobre suas mudanças.
- Mantenha o padrão de código e inclua testes sempre que possível.
- Utilize Python 3 para backend, JavaScript (Node.js ou React) para frontend e CLI.

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo LICENSE para mais detalhes.

---

Para dúvidas, acesse a seção de Troubleshooting no User Guide ou abra uma issue no repositório.