# assets/

Place your personal files here before running the workflow.

| File | Description |
|------|-------------|
| `resume.pdf` | Your resume — attached manually to each Gmail draft before sending |
| `signature.jpeg` | Your handwritten signature as a JPEG image, used in cover letters |

## Extracting your signature

If you have an existing signed cover letter PDF, run the following to extract the signature:

```python
import fitz  # pip install pymupdf

doc = fitz.open("your_cover_letter.pdf")
page = doc[0]
for img in page.get_images(full=True):
    xref = img[0]
    base_image = doc.extract_image(xref)
    with open(f"assets/signature.{base_image['ext']}", "wb") as f:
        f.write(base_image["image"])
    print("Saved signature")
```
