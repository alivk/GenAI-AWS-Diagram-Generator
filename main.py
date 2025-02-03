import streamlit as st
import subprocess
import tempfile
import os
import re
from PIL import Image

import bedrock_utils

# Set up the Streamlit app
st.set_page_config(page_title="Best AWS Diagram Generator", layout="wide")
st.title("Best AWS Diagram Generator")
st.markdown("Write your diagram code and export to draw.io format")

# Add Graphviz installation instructions
st.sidebar.markdown("""
### Prerequisites
1. Install Graphviz:
   - **macOS**: `brew install graphviz`
   - **Linux**: `sudo apt-get install graphviz`
   - **Windows**: Download from [graphviz.org](https://graphviz.org/download/)
2. Make sure `dot` is in your PATH
""")

# ---------------------------
# SECTION: Auto-generate Diagram Code using Bedrock API
# ---------------------------
st.subheader("Auto Generate Diagram Code using Bedrock API")

diagram_prompt = st.text_area(
    "Please describe the diagram you want to create",
    value="Generate diagram code for a web service with ELB, EC2, and RDS using the diagrams library."
)

model_options = bedrock_utils.list_available_models()
model_selection = st.selectbox(
    "Select a model",
    options=model_options,
    format_func=lambda x: x[1]
)

def filter_generated_code(generated_text):
    """
    Extract only the Python code for a diagrams model from the generated response.
    
    Tries to pull out the code enclosed in triple backticks (optionally with a 'python' specifier).
    If no codeblock is found, it will return only the lines starting at the first occurrence of "from diagrams".
    """
    # Try to search for a markdown code-block
    match = re.search(r"```(?:python)?\n(.*?)```", generated_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        # Fallback: return only lines starting from "from diagrams"
        lines = generated_text.splitlines()
        filtered_lines = []
        code_started = False
        for line in lines:
            if not code_started and "from diagrams" in line:
                code_started = True
            if code_started:
                filtered_lines.append(line)
        return "\n".join(filtered_lines).strip()

if st.button("Review Diagram Code"):
    creds = bedrock_utils.get_bedrock_credentials()
    if creds is not None:
        with st.spinner("Generating diagram code using Bedrock API..."):
            wrapped_prompt = (
                "Please generate python code using the diagrams module according to this prompt. "
                "You should start with 'from diagrams'.\n\nPrompt: " + diagram_prompt
            )
            response = bedrock_utils.invoke_bedrock_model(
                prompt=wrapped_prompt,
                access_key=creds["aws_access_key_id"],
                secret_key=creds["aws_secret_access_key"],
                model_id=model_selection[0]
            )
        if response:
            # Filter the output to extract only the generated Python code
            filtered_code = filter_generated_code(response)
            # Replace occurrences of "DynamoDB" with "Dynamodb"
            filtered_code = filtered_code.replace("DynamoDB", "Dynamodb")
            # Additionally, replace occurrences of "ApiGateway" with "APIGateway"
            filtered_code = filtered_code.replace("ApiGateway", "APIGateway")
            st.session_state.generated_diagram_code = filtered_code
            st.success("Diagram code generated successfully!")
        else:
            st.error("Failed to generate diagram code.")

# ---------------------------
# SECTION: Diagram Code (Editable)
# ---------------------------
default_code = """from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

with Diagram("Grouped Workers", show=False, outformat="png"):
    ELB("lb") >> EC2("web") >> RDS("userdb")
"""

# Use the auto-generated code if available, otherwise the default
diagram_code = st.text_area(
    "Diagram Code (You can edit this code)",
    height=300,
    value=st.session_state.get("generated_diagram_code", default_code)
)

st.info("Click **Edit** to manually modify the diagram code if desired.")

# Additionally display the diagram code in a formatted code block
st.code(diagram_code, language="python")

# ---------------------------
# SECTION: Generate Diagram Image
# ---------------------------
def generate_diagram_image(code):
    """Generate a diagram image from the provided code."""
    # Write code to temporary Python file
    with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as tmp_py:
        tmp_py.write(code.encode())
        tmp_py_path = tmp_py.name

    try:
        # Execute the diagram code
        result = subprocess.run(['python', tmp_py_path], capture_output=True, text=True)
        st.text(f"STDOUT: {result.stdout}")
        st.text(f"STDERR: {result.stderr}")

        if result.returncode != 0:
            if "ExecutableNotFound" in result.stderr:
                st.error("Graphviz not found. Please install Graphviz and ensure 'dot' is in your PATH.")
            else:
                st.error(f"Error executing code:\n{result.stderr}")
            return None

        # Ensure the diagram uses the fixed output name "example_diagram.png"
        img_path = "example_diagram.png"
        if not os.path.exists(img_path):
            st.error("Failed to generate the diagram image.")
            return None

        return img_path
    finally:
        os.unlink(tmp_py_path)

if st.button("Generate Diagram"):
    with st.spinner("Generating diagram..."):
        # Update the diagram code, forcing the Diagram name to "example_diagram"
        updated_code = re.sub(r'with Diagram\(".*?"', 'with Diagram("example_diagram"', diagram_code)
        img_path = generate_diagram_image(updated_code)
        if img_path:
            st.success("Diagram generated successfully!")
            image = Image.open(img_path)
            st.image(image, caption="Generated Diagram", use_column_width=True)
            os.remove(img_path)
