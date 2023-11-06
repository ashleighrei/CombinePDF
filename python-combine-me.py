import streamlit as st
import os
import PyPDF2
from io import BytesIO
import tempfile

# Custom CSS to set the font, colors, and font-weight
css = f"""
<style>
/* Set the font and font-weight for the title */
.title {{
    font-family: 'Poppins', sans-serif;
    font-weight: 700;
}}

/* Set the font, colors, and font-weight for the rest of the app */
body {{
    font-family: 'Poppins', sans-serif;
}}
</style>
"""

st.markdown(css, unsafe_allow_html=True)

st.markdown('<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">', unsafe_allow_html=True)

# Function to combine PDFs using PyPDF2
def combine_pdfs(input_files, output_file):
    # Create a PDF merger object
    pdf_merger = PyPDF2.PdfFileMerger()

    try:
        # Iterate through input PDF files and append them to the merger
        for input_file in input_files:
            pdf_merger.append(input_file)

        # Write the combined PDF to a BytesIO buffer
        pdf_buffer = BytesIO()
        pdf_merger.write(pdf_buffer)
        pdf_buffer.seek(0)  # Reset the buffer position

        # Save the combined PDF with the specified output file name and PDF extension
        with open(output_file, 'wb') as out_pdf:
            out_pdf.write(pdf_buffer.read())

        return True

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return False

# Rest of your Streamlit app code
# ...
