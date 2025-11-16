import ollama
import lancedb
from pypdf import PdfReader
import os

# --- CONFIGURATION ---
DOC_PATH = "file.pdf"  # Ensure this file exists
DB_PATH = "./lancedb_data"
MODEL_EMBED = "nomic-embed-text"
MODEL_GEN = "llama3"

print("--- 🧠 Building Knowledge Base with LanceDB ---")

# 1. INGESTION: Read PDF
try:
    reader = PdfReader(DOC_PATH)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
except FileNotFoundError:
    print(f"❌ Error: Could not find {DOC_PATH}. Please add a PDF file.")
    exit()

# 2. CHUNKING
chunk_size = 1000
text_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
print(f"📄 Processed {len(text_chunks)} text chunks.")

# 3. EMBEDDING & STORAGE
# LanceDB expects a list of dictionaries (like JSON rows)
data = []
print("⏳ Generating embeddings (this may take a moment)...")

for i, chunk in enumerate(text_chunks):
    # Generate vector using Ollama
    response = ollama.embeddings(model=MODEL_EMBED, prompt=chunk)
    vector = response["embedding"]
    
    # Prepare row for database
    data.append({
        "id": i,
        "text": chunk,
        "vector": vector
    })

# Connect to LanceDB (creates the folder automatically)
db = lancedb.connect(DB_PATH)

# Create (or overwrite) the table
# vector_len depends on the model (nomic-embed-text is usually 768)
try:
    table = db.create_table("resume", data=data, mode="overwrite")
    print("💾 Knowledge stored in LanceDB (Local Disk).")
except Exception as e:
    print(f"⚠️ Database error: {e}")
    exit()

# 4. RETRIEVAL LOOP
while True:
    query = input("\n❓ Ask about the file (or 'quit'): ")
    if query.lower() == 'quit': break

    # Embed the question
    query_vec = ollama.embeddings(model=MODEL_EMBED, prompt=query)["embedding"]

    # Search LanceDB (Find nearest neighbors)
    # .limit(1) = Get the top 1 most relevant chunk
    results = table.search(query_vec).limit(1).to_list()

    if results:
        best_chunk = results[0]["text"]
        print(f"\n🔍 Context Found:\n'...{best_chunk[:100]}...'")

        # 5. GENERATION
        prompt = f"""
        Use the context below to answer the question.
        
        Context: {best_chunk}
        Question: {query}
        """
        
        response = ollama.generate(model=MODEL_GEN, prompt=prompt)
        print(f"\n🤖 Answer: {response['response']}")
    else:
        print("❌ No relevant info found.")