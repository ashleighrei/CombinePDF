import streamlit as st
import os
import PyPDF2
from io import BytesIO
import tempfile

# Custom CSS and Streamlit setup
# ... (same as in your previous code)

# Function to combine PDFs using PyPDF2
def combine_pdfs(input_files, output_file):
    pdf_merger = PyPDF2.PdfFileMerger()

    try:
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

# Streamlit app (remaining code remains the same as in your previous code)

# ...

# Display a "Combine" button to combine the PDFs
if st.button("Combine") and uploaded_files:
    # Output file where the combined PDF will be saved
    output_file_path = os.path.join(tempfile.gettempdir(), output_file_name)

    # Call the function to combine the PDFs using PyPDF2
    if combine_pdfs(uploaded_files, output_file_path):  # Use uploaded_files, not input_files
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
