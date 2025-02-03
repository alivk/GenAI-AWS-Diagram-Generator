# Best AWS Diagram Generator

Welcome to the **Best AWS Diagram Generator**! This Streamlit application enables you to design AWS architecture diagrams using the [Diagrams](https://diagrams.mingrammer.com/) Python library. It leverages AWS Bedrock (e.g., using Claude models) so you can simply describe your desired architecture in plain English and automatically generate the corresponding diagram code.

## Features

- **Auto-generate Diagram Code:**  
  Describe the diagram you want to create (for example, "Generate diagram code for a web service with ELB, EC2, and RDS using the diagrams library."). Your prompt is automatically wrapped with instructions (ensuring the generated code starts with `from diagrams`) and sent to AWS Bedrock.  
  The response is then filtered to extract only the valid Python code, and any necessary naming adjustments (e.g., replacing `"DynamoDB"` with `"Dynamodb"` and `"ApiGateway"` with `"APIGateway"`) are applied.

- **Editable Code:**  
  The generated code is pre-populated in an editable text area. You can modify it as needed. The code is also displayed in a formatted code block for clarity.

- **Diagram Generation:**  
  Once you verify or edit the diagram code, click **Generate Diagram**. The app forces the output file name to be `"example_diagram.png"`, executes the code, and then displays the resulting diagram image directly on the website.

## Prerequisites

### Software Requirements

- **Python 3.7+**
- **Graphviz:**  
  The Diagrams library depends on Graphviz to render images. Ensure Graphviz is installed and the `dot` command is available in your system's PATH.
  - **macOS:**  
    ```bash
    brew install graphviz
    ```
  - **Linux:**  
    ```bash
    sudo apt-get install graphviz
    ```
  - **Windows:**  
    Download from [Graphviz](https://graphviz.org/download/)

### Python Dependencies

Install the required Python packages:
```bash
pip install streamlit diagrams boto3 pillow
```

## AWS Bedrock API Configuration

The application integrates with AWS Bedrock to generate diagram code using natural language prompts. To enable this functionality, the app retrieves credentials from AWS Secrets Manager. Ensure that your AWS Secrets Manager contains a secret named **`bedrocksecrets`** with these keys:
- `AWS_REGION`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_KENDRA_INDEX_ID`
- `SESSION_SECRET`
- `SESSION_SECRET_BDM1`
- `SESSION_SECRET_BMD2`
- `SESSION_SECRET_INSTRUCTOR1`
- `SESSION_SECRET_INSTRUCTOR2`

The helper functions to manage AWS credentials and invoke the Bedrock API are provided in the **`bedrock_utils.py`** file.

## Usage

1. **Launch the Application**  
   Start the app with the following command:
   ```bash
   streamlit run main.py
   ```

2. **Auto-generate Diagram Code**
   - At the top of the app, enter your description in the prompt area labeled **"Please describe the diagram you want to create"**.
   - Click the **"Review Diagram Code"** button. The app wraps your prompt with extra instructions (ensuring the response starts with `from diagrams`), invokes the Bedrock API, and then filters the response to produce clean, valid Python code. Any instances of `"DynamoDB"` or `"ApiGateway"` are automatically replaced with `"Dynamodb"` and `"APIGateway"` respectively.
   
3. **Edit Diagram Code**
   - The filtered code appears in an editable text area as well as a formatted code block. You can manually tweak this code if required.

4. **Generate the Diagram Image**
   - Click **Generate Diagram**. The application updates the code to force the diagram to be named `"example_diagram"`, runs the code to generate the diagram image, and then displays the image on the website. The temporary image file is automatically removed afterward.

## Project Structure

```
project/
├── main.py             # Main Streamlit application for diagram generation
├── bedrock_utils.py    # Utility functions for accessing AWS Bedrock and credentials
├── README.md           # This documentation file
└── requirements.txt    # (Optional) List of Python dependencies
```

## Customization

- **Prompt Wrapping:**  
  Your natural language prompt is wrapped with specific instructions to ensure the LLM output is valid Python code starting with `from diagrams`.

- **Code Filtering & Replacement:**  
  The application filters the raw LLM response to extract only the necessary Python code, applying text replacements to correct naming conventions.

## Troubleshooting

- **Graphviz Issues:**  
  Verify that Graphviz is installed and that the `dot` executable is on your system's PATH if you encounter related errors.

- **AWS Credentials:**  
  Ensure the secret named `bedrocksecrets` in AWS Secrets Manager has the needed keys and values. If there's an error retrieving credentials, the app will display an error message.

## License

This project is distributed under the [MIT License](LICENSE).

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the interactive web interface.
- [Diagrams](https://diagrams.mingrammer.com/) for AWS diagram generation.
- AWS Bedrock and associated LLMs for code generation capabilities.