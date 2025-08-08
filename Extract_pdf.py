

import os
import requests

def extract_pdf(pdf_url):
    # Get the folder where this script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(base_dir, "policy.pdf")

    # Download and save
    with open(save_path, "wb") as f:
        f.write(requests.get(pdf_url).content)

    print(f""
          f" Saved PDF to {save_path}")
    return save_path
