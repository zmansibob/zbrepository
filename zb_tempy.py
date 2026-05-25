from pypdf import PdfReader

reader = PdfReader("zblyrics.pdf")
for i in range(1, 10):
    text = reader.pages[i].extract_text()
    if text and "," in text:
        print(f"--- COMMA DETECTED ON PHYSICAL PAGE {i+1} ---")
        print("\n".join(text.split("\n")[:3])) # Print just the first 3 lines of data