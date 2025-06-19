# 🧠 Technical Approach: RAG Chatbot with n8n, Gemini, and Pinecone

This document outlines the technical design, architecture, and decisions made in building the RAG-based disease-focused chatbot system.

---

## 🏗️ Overall Architecture

```
User Query (Webhook) → AI Agent (n8n) →
 ├── Retrieves context chunks from Pinecone
 ├── Uses Gemini to generate answer
 ├── Logs query & output to Google Sheets
 └── Returns response to user
```

---

## 🔗 Key Technologies Used

| Component      | Tool/Service              | Purpose                              |
|---------------|---------------------------|--------------------------------------|
| Workflow Engine | n8n (cloud)              | Orchestrates RAG pipeline            |
| Embedding Model| Google Gemini (embedding) | Converts query & chunks to vectors   |
| LLM            | Google Gemini 2.0 Flash   | Natural language answer generation   |
| Vector Store   | Pinecone                  | Stores embedded document chunks      |
| Document Input | Google Drive              | Stores source knowledge (PDFs/docs)  |
| Memory         | Redis                     | Maintains chat context               |
| Analytics      | Google Sheets             | Logs queries, IP, country, output    |

---

## 🧩 Document Ingestion Pipeline

1. **Google Drive Triggers** watch for new/updated files
2. Files are downloaded using `Google Drive` node
3. Documents are loaded as binary and parsed via `Default Data Loader`
4. Parsed text is split using `RecursiveCharacterTextSplitter` (chunk size: 800)
5. Chunks are embedded using `Gemini Embedding Model`
6. Embeddings + metadata are stored in Pinecone (namespace: `Diseases`)

---

## 🤖 Query-Time Pipeline

1. User sends query to **Webhook node** (via POST)
2. The **AI Agent** is triggered, configured with:
   - System message (empathy, friendliness)
   - Context tool: Disease Vector Store
   - Memory: Redis
   - Model: Gemini 2.0 Flash
3. Query is embedded → top 5 relevant chunks are retrieved from Pinecone
4. Prompt is auto-generated:
   - Includes retrieved context
   - Includes current + prior conversation history (via Redis)
5. Gemini responds with a warm, informative reply
6. Output is optionally POSTed to a live UI endpoint (ngrok, etc.)
7. Result is logged in Google Sheets:
   - Query, Output, IP, Country, Content-Length

---

## 📊 Analytics and Observability

- Every query interaction is logged to Google Sheets
- Allows usage analysis, sentiment checking, and prompt quality tracking
- IP and country allow basic geographical stats

---

## ✨ Ethical Considerations

- Responses use only vector-retrieved content
- System message promotes empathy and transparency
- Logging helps trace and audit outputs
- No hallucination-prone open-ended prompting

---

## 🧠 Future Improvements

- Add user-facing chat UI (HTML/React)
- Enable user-uploaded documents (admin-only)
- Add feedback buttons for thumbs-up/down
- Link to Supabase or TimescaleDB for deeper analytics

---

## ✅ Summary

This system uses a robust, scalable RAG design built entirely in **n8n** with minimal scripting, leveraging LangChain’s native nodes and Google’s AI ecosystem. It demonstrates both technical fluency and ethical responsibility.
