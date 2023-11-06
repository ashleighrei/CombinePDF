import streamlit as st
import os
import PyPDF2
import tempfile
from io import BytesIO
import base64

import streamlit as st


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

# Rest of your Streamlit app code
# ...

st.markdown('<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap" rel="stylesheet">', unsafe_allow_html=True)


# Function to combine PDFs
def combine_pdfs(input_files, output_file):
    # Create a PDF merger object
    pdf_merger = PyPDF2.PdfMerger()

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

# File upload widgets for individual PDFs (based on user input)
uploaded_files = []
for i in range(num_files):
    file = st.file_uploader(f"Upload PDF {i + 1}", type=["pdf"])
    if file:
        uploaded_files.append(file)

# User input for the output PDF file name
output_file_name = st.text_input("Enter a file name for the combined PDF file (or leave empty for default name)")

# Default output file name
if not output_file_name:
    output_file_name = "incognito_noname_combined_file.pdf"
else:
    # Ensure that the output file name has a .pdf extension
    if not output_file_name.lower().endswith(".pdf"):
        output_file_name += ".pdf"

# Display a "Combine" button to combine the PDFs
if st.button("Combine") and uploaded_files:
    # Temporary directory to store uploaded files
    temp_dir = 'temp'
    
    # Create the temporary directory if it doesn't exist
    os.makedirs(temp_dir, exist_ok=True)

    # Save uploaded files to the temporary directory
    for i, uploaded_file in enumerate(uploaded_files):
        with open(os.path.join(temp_dir, f"file_{i + 1}.pdf"), 'wb') as f:
            f.write(uploaded_file.read())

    # List all PDF files in the temporary directory
    input_files = [os.path.join(temp_dir, filename) for filename in os.listdir(temp_dir) if filename.endswith(".pdf")]

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
            )

        # Remove the temporary directory and its contents
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)
else:
    st.warning("Please upload at least one PDF file :)")
