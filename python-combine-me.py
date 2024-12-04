import streamlit as st
import os
from PyPDF2 import PdfMerger
from io import BytesIO
import tempfile

# Custom CSS to set the font, colors, and font-weight
css = """
<style>
/* Set the font and font-weight for the title */
.title {
    font-family: 'Poppins', sans-serif;
    font-weight: 700;
}

/* Set the font, colors, and font-weight for the rest of the app */
body {
    font-family: 'Poppins', sans-serif;
}
</style>
"""

st.markdown(css, unsafe_allow_html=True)
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">', unsafe_allow_html=True)

# Function to combine PDFs using PyPDF2
def combine_pdfs(input_files, output_file):
    # Create a PDF merger object
    pdf_merger = PdfMerger()

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

# Streamlit app
st.title('Combine Multiple PDFs App')

# User prompt for the number of files to upload
num_files = st.number_input("How many PDFs would you like to upload? Max of 15 PDF files.", min_value=1, max_value=15, value=1, step=1)

# Initialize the input_files list to store the uploaded PDFs
input_files = []

# File upload widgets for individual PDFs (based on user input)
for i in range(num_files):
    file = st.file_uploader(f"Upload PDF {i + 1}", type=["pdf"], key=f"file_uploader_{i}")
    if file:
        input_files.append(file)

# User input for the output PDF file name
output_file_name = st.text_input("Enter a file name for the combined PDF file (or leave empty for default name)")

# Default output file name
if not output_file_name:
    output_file_name = "combined_file.pdf"
else:
    # Ensure that the output file name has a .pdf extension
    if not output_file_name.lower().endswith(".pdf"):
        output_file_name += ".pdf"

# Display a "Combine" button to combine the PDFs
if st.button("Combine") and input_files:
    # Output file where the combined PDF will be saved
    output_file_path = os.path.join(tempfile.gettempdir(), output_file_name)

    # Call the function to combine the PDFs
    if combine_pdfs(input_files, output_file_path):
        st.success("PDFs successfully combined.")

        # Display a "Download" button for the combined PDF
        with open(output_file_path, "rb") as file:
            st.download_button(
                label="Download",
                data=file.read(),
                file_name=output_file_name,
                mime="application/pdf"
            )
else:
    st.warning("Please upload at least one PDF file :)")
