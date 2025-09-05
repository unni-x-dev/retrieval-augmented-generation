# 📄 Semantic Document Search with FastAPI & MongoDB Atlas

This project is a **document ingestion and semantic search system** built using:

- [FastAPI](https://fastapi.tiangolo.com/) for API endpoints  
- [SentenceTransformers](https://www.sbert.net/) for generating embeddings  
- [MongoDB Atlas Vector Search](https://www.mongodb.com/atlas/vector-search) for semantic retrieval  

It allows you to:  
1. Upload documents (`PDF`, `DOCX`, `TXT`)  
2. Extract text and split it into overlapping chunks  
3. Generate embeddings for each chunk  
4. Store embeddings + chunks in MongoDB  
5. Query documents semantically using natural language and retrieve the **top 5 most relevant chunks**  

---

## 🚀 Features

- Upload and extract text from documents  
- Chunking of text with overlap handling  
- SentenceTransformer embeddings (`all-MiniLM-L6-v2`)  
- MongoDB Atlas Vector Search integration  
- Query documents with natural language and get relevant context  

---




## 🗄️ MongoDB Setup Guide

This project uses **MongoDB Atlas** as the database with **Vector Search** enabled to store and query document embeddings.  

Follow the steps below to set up your MongoDB environment:

---

### 1. Create a MongoDB Atlas Account
1. Go to [MongoDB Atlas](https://www.mongodb.com/atlas).
2. Sign up (or log in if you already have an account).
3. Create a new project in the Atlas dashboard.

---

### 2. Deploy a Cluster
1. Click **Build a Database**.
2. Choose a **free tier (M0)** for testing or a dedicated cluster for production.
3. Select your preferred cloud provider and region.
4. Click **Create Cluster**.

---

### 3. Configure Database Access
1. Go to **Database Access** in the left-hand menu.
2. Create a new database user:
   - Username: `your-username`
   - Password: `your-password`
3. Assign **Atlas Admin** role (or more restrictive if you prefer).

---

### 4. Network Access
1. Go to **Network Access**.
2. Add your IP address:
   - Option 1: **Add Current IP Address** (for local dev).
   - Option 2: **Allow Access From Anywhere** (`0.0.0.0/0`) — not recommended for production.

---

### 5. Get Your Connection String
1. Go to **Clusters** → **Connect** → **Connect Your Application**.
2. Copy the connection string, e.g.:

   ```bash
   mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/?retryWrites=true&w=majority

---

### 6. Create Vector Search Index

To enable **semantic search**, you need to create a **vector index**:

1. In Atlas, go to your cluster → **Browse Collections** → **Indexes** → **Create Search Index**.
2. Choose **JSON Editor** and add the following definition:

   ```json
   {
     "fields": [
       {
         "type": "vector",
         "path": "embedding",
         "numDimensions": 384,
         "similarity": "cosine"
       }
     ]
   }

