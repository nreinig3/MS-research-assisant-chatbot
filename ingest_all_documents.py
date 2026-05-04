# ingest_all_documents.py
import os
import uuid
import pandas as pd
from pypdf import PdfReader
from utils.embeddings import embed_and_store

# ============================================================
# PDF Processing
# ============================================================

def extract_text_from_pdf(pdf_path):
    """Extract all text from a PDF file."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def chunk_text(text, chunk_size=1500, overlap=300):
    """
    Split text into overlapping chunks.
    
    Args:
        text: The text to split
        chunk_size: Maximum characters per chunk
        overlap: Characters to overlap between chunks
    
    Returns:
        List of text chunks
    """
    if not text or len(text) < 100:
        return [text] if text else []
    
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = min(start + chunk_size, text_length)
        
        # Try to break at a sentence or paragraph
        if end < text_length:
            # Look for period followed by space or newline
            last_period = text.rfind('. ', start, end)
            last_newline = text.rfind('\n', start, end)
            break_point = max(last_period + 2, last_newline) if last_period > start else end
            
            if break_point > start and break_point < end:
                end = break_point
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = max(start + chunk_size - overlap, end)
    
    return chunks

def process_pdfs(pdf_dir):
    """Process all PDFs in a directory and return chunks, metadatas, and ids."""
    if not os.path.exists(pdf_dir):
        print(f"   Directory not found: {pdf_dir}")
        return [], [], []
    
    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"   No PDF files found in {pdf_dir}")
        return [], [], []
    
    all_chunks = []
    all_metadatas = []
    all_ids = []
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_dir, pdf_file)
        print(f"   📄 Processing PDF: {pdf_file}")
        
        try:
            text = extract_text_from_pdf(pdf_path)
            if not text.strip():
                print(f"      ⚠️  No text extracted (might be scanned image)")
                continue
            
            chunks = chunk_text(text, chunk_size=1500, overlap=300)
            print(f"      → Split into {len(chunks)} chunks")
            
            for i, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                all_metadatas.append({
                    "source": pdf_file,
                    "type": "pdf",
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                })
                all_ids.append(str(uuid.uuid4()))
                
        except Exception as e:
            print(f"      ❌ Error: {e}")
    
    return all_chunks, all_metadatas, all_ids

# ============================================================
# CSV Processing
# ============================================================

def process_csv(csv_path):
    """Process a CSV file and return chunks, metadatas, and ids."""
    if not os.path.exists(csv_path):
        print(f"   File not found: {csv_path}")
        return [], [], []
    
    print(f"   📊 Processing CSV: {os.path.basename(csv_path)}")
    
    df = pd.read_csv(csv_path)
    print(f"      → Loaded {len(df)} rows")
    
    all_chunks = []
    all_metadatas = []
    all_ids = []
    
    # Display columns for debugging
    print(f"      → Columns: {list(df.columns)[:5]}..." if len(df.columns) > 5 else f"      → Columns: {list(df.columns)}")
    
    for idx, row in df.iterrows():
        # Build a readable text representation
        trial_text_lines = []
        for col in df.columns:
            value = row[col]
            if pd.notna(value) and str(value).strip():
                col_name = col.replace('_', ' ').title()
                trial_text_lines.append(f"{col_name}: {value}")
        
        if trial_text_lines:
            trial_text = "\n".join(trial_text_lines)
            all_chunks.append(trial_text)
            
            # Try to find a trial ID for citation
            trial_id = None
            for id_col in ['NCT Number', 'nct_id', 'Study ID', 'ID', 'NCT']:
                if id_col in df.columns and pd.notna(row[id_col]):
                    trial_id = str(row[id_col])
                    break
            
            all_metadatas.append({
                "source": os.path.basename(csv_path),
                "type": "clinical_trial",
                "trial_id": trial_id or f"row_{idx}",
                "row_index": idx
            })
            all_ids.append(str(uuid.uuid4()))
    
    print(f"      → Created {len(all_chunks)} trial records")
    return all_chunks, all_metadatas, all_ids

# ============================================================
# Main Ingestion Function
# ============================================================

def ingest_all():
    """Ingest all PDFs and CSV files into Chroma DB."""
    print("=" * 60)
    print("📚 Document Ingestion")
    print("=" * 60)
    
    all_chunks = []
    all_metadatas = []
    all_ids = []
    
    # Process PDFs
    print("\n📄 Processing PDFs...")
    pdf_chunks, pdf_metadatas, pdf_ids = process_pdfs("data/raw/pdfs")
    all_chunks.extend(pdf_chunks)
    all_metadatas.extend(pdf_metadatas)
    all_ids.extend(pdf_ids)
    print(f"   ✅ PDFs: {len(pdf_chunks)} chunks")
    
    # Process CSV
    print("\n📊 Processing CSV...")
    csv_chunks, csv_metadatas, csv_ids = process_csv("data/raw/csv/clinical_trials.csv")
    all_chunks.extend(csv_chunks)
    all_metadatas.extend(csv_metadatas)
    all_ids.extend(csv_ids)
    print(f"   ✅ CSV: {len(csv_chunks)} trial records")
    
    # Store everything in Chroma
    if all_chunks:
        print("\n💾 Storing documents in Chroma DB...")
        total = embed_and_store(all_chunks, all_metadatas, all_ids)
        print(f"\n✅ Done! Collection now contains {total} total documents")
    else:
        print("\n❌ No documents to ingest. Check your file paths.")
        
        # Show helpful error
        print("\n📁 Expected file locations:")
        print("   - PDFs: data/raw/pdfs/*.pdf")
        print("   - CSV:  data/raw/csv/clinical_trials.csv")

if __name__ == "__main__":
    ingest_all()