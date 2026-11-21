
# 🤖 davIA — Assistente Pessoal de Inteligência Artificial

A **davIA** é uma aplicação web de chat com Inteligência Artificial construída com **Streamlit** e integrada à API da **Groq**. Ela conta com interface escura personalizada, gerenciamento de múltiplas conversas e persistência de histórico em arquivo JSON local.

---

## ✨ Funcionalidades

- **Chat interativo em tempo real** com interface estilizada em modo escuro.
- **Gerenciamento de conversas**: crie novas conversas, alterna entre chats anteriores e exclua conversas com facilidade.
- **Título automático**: a primeira mensagem enviada define o título da conversa na barra lateral.
- **Histórico persistente**: as conversas são salvas automaticamente em `historico_davia.json` (com escrita segura via arquivo temporário).
- **Personalidade configurada**: atua como a assistente *davIA*, respondendo em português quando o usuário escreve em português.

---

## 🛠️ Tecnologias Utilizadas

- **Python**
- **Streamlit** (interface web e estado de sessão)
- **Groq Python SDK (`groq`)** (modelo `openai/gpt-oss-20b` via `client.chat.completions.create`)
- **python-dotenv** (carregamento de variáveis de ambiente a partir do `.env`)
- **JSON / UUID / Datetime** (persistência e identificação de conversas)

---

## 📁 Estrutura do Projeto

```text
.
├── app.py                  # Código principal da aplicação Streamlit (ajuste o nome se necessário)
├── historico_davia.json    # Gerado automaticamente para salvar o histórico das conversas
├── .env                    # Variáveis de ambiente (não versionar)
└── README.md               # Documentação do projeto
