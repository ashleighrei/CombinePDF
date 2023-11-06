import streamlit as st
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
from io import BytesIO
import tempfile

# Custom CSS and Streamlit setup
# ... (same as in your previous code)

# Function to combine PDFs using PyPDF2
def combine_pdfs(input_files, output_file):
    pdf_merger = PdfFileWriter()

    try:
        for input_file in input_files:
            pdf_reader = PdfFileReader(input_file)
            for page_num in range(pdf_reader.getNumPages()):
                pdf_merger.addPage(pdf_reader.getPage(page_num))

        # Create a BytesIO buffer to store the combined PDF
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

# Streamlit app (remaining code remains the same as in your previous code)

# ...

# Display a "Combine" button to combine the PDFs
if st.button("Combine") and input_files:
    # Output file where the combined PDF will be saved
    output_file_path = os.path.join(tempfile.gettempdir(), output_file_name)

    # Call the function to combine the PDFs using PyPDF2
    if combine_pdfs(input_files, output_file_path):
        st.success("PDFs successfully combined.")

        # Display a "Download" button for the combined PDF
        with open(output_file_path, "rb") as file:
            st.download_button(
                label="Download",
                data=file.read(),
                file_name=output_file_name,
            )
else:
    st.warning("Please upload at least one PDF file :)")
