# 🧠 RAG Chatbot for Disease FAQs using n8n, Pinecone, and Google Gemini

This project implements a **Retrieval-Augmented Generation (RAG)** based chatbot to answer disease-related questions. It integrates **n8n**, **Google Drive**, **LangChain**, **Google Gemini**, **Redis**, **Pinecone**, and **Google Sheets** to form a complete pipeline from document ingestion to intelligent, empathetic chatbot response.

---

## 🚀 Features

- Semantic search with Pinecone and Gemini embeddings  
- Automatic PDF ingestion and chunking from Google Drive  
- Conversational memory using Redis  
- Intelligent response generation via Gemini Chat API  
- Query logging and analytics using Google Sheets  
- Webhook endpoint for easy chatbot integration (e.g., frontend, Postman, UI)

---

## 🧩 Stack

| Component         | Tech Used                       |
|------------------|----------------------------------|
| Workflow engine  | n8n (cloud)                      |
| Embeddings       | Google Gemini (text-embedding-004) |
| Vector DB        | Pinecone                         |
| LLM              | Gemini 2.0 Flash                 |
| Memory           | Redis                            |
| Storage/Input    | Google Drive                     |
| Analytics        | Google Sheets                    |

---

## 📁 Folder Structure

```
runtime-docs/           ← Any uploaded Google Docs/PDFs (triggered via Google Drive folder)
webhook/                ← Accepts user queries
query-logs-sheet/       ← Google Sheet where all inputs + outputs are logged
```

---

## ⚙️ Setup Instructions

### 1. ✅ Import into n8n
- Log into [n8n.cloud](https://n8n.io)
- Import `rag-chatbot-workflow.json`
- Connect credentials:
  - Google Drive OAuth
  - Google Sheets OAuth
  - Google Gemini API
  - Pinecone API
  - Redis (for chat memory)

### 2. 📥 Connect Google Drive folder
- Upload disease documents to the connected folder
- n8n watches for new/updated files

### 3. 🔄 Embedding & Indexing
- Trigger loads file → chunks → embeds → sends to Pinecone (namespace: `Diseases`)

### 4. 💬 Chatbot usage
- Send a `POST` to the webhook:
```json
{
  "query": "What are the symptoms of dengue?"
}
```
- Response is generated and returned
- The query, output, IP, and country are logged in Google Sheets

---

## 📊 Analytics

- Google Sheet logs:
  - Query
  - Output
  - IP (from header)
  - Country (from Cloudflare header)
  - Content Length

Use Google Sheets charts or connect to **Looker Studio** for visual dashboards.

---

## 💡 Example

**Request**:
```json
{ "query": "How is malaria different from dengue?" }
```

**Response**:
> "Malaria is caused by Plasmodium parasites while dengue is caused by a virus..."

---

