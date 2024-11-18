import os
from openai import OpenAI
import json

# Initialize the OpenAI client
client = OpenAI(
    base_url="https://api.studio.nebius.ai/v1/",
    api_key="eyJhbGciOiJIUzI1NiIsImtpZCI6IlV6SXJWd1h0dnprLVRvdzlLZWstc0M1akptWXBvX1VaVkxUZlpnMDRlOFUiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMjMxMzA5MjEzMzg2ODQ3MDQ2MSIsInNjb3BlIjoib3BlbmlkIG9mZmxpbmVfYWNjZXNzIiwiaXNzIjoiYXBpX2tleV9pc3N1ZXIiLCJhdWQiOlsiaHR0cHM6Ly9uZWJpdXMtaW5mZXJlbmNlLmV1LmF1dGgwLmNvbS9hcGkvdjIvIl0sImV4cCI6MTg4OTQwNjQ4OCwidXVpZCI6IjU3ZDg3ZGRhLTk5YzMtNDUwZC04ODBjLTQ2YTYzZDYxNjcxNSIsIm5hbWUiOiJUaGVzaXMgRXZhbCIsImV4cGlyZXNfYXQiOiIyMDI5LTExLTE1VDAzOjA4OjA4KzAwMDAifQ.mU9v7jr_TRIVcjLtoc4wQ62g_bhYlT1dJdmV22f6BTo"
)

# Constant prompt
prompt = "Extract the data table from the svg code of a bar chart svg image. Only return the output of a json object with the data within it. "

# Folder containing the SVG files
folder_path = "chartqa/bar/svg_outputs"

# Output text file
output_file = "chartqa/bar/extracted_one_shot/var chart one shot.txt"

# Define a function to process SVG files
def process_svg_files():
    # Get a list of all .svg files in the folder
    svg_files = [f for f in os.listdir(folder_path) if f.endswith('.svg')]
    
    if not svg_files:
        print("No SVG files found in the folder.")
        return

    for svg_file in svg_files:
        svg_path = os.path.join(folder_path, svg_file)

        # Read the content of the SVG file
        with open(svg_path, "r") as file:
            svg_content = file.read()

        # Create the completion request
        completion = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-70B-Instruct",
            messages=[{"role": "user", "content": f"{prompt}\nSVG Chart: {svg_content}"}],
            temperature=0.6,
            max_tokens=512,
            top_p=0.9
        )

     
   # Parse the response into a dictionary
        response_json = json.loads(completion.to_json())

        # Extract the message content
        try:
            message_content = response_json["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            print(f"Error extracting content for file {svg_file}: {e}")
            continue

        print(f"Processed file: {svg_file}")
        
        # Append the results to the output text file
        with open(output_file, "a") as output:
            output.write(f"File: {svg_file}\n")
            output.write(f"Message Content:\n{message_content}\n")
            output.write(f"{'-'*50}\n")
    
    print(f"All SVG files have been processed. Results are saved in {output_file}.")

# Run the script
process_svg_files()
