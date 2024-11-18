import os
import pandas as pd
import json
import subprocess
from vega import VegaLite
import altair as alt

# Folder paths
tables_folder = "chartqa/tables"
vegalite_folder = "chartqa/bar/specs"
svg_folder = "svg_outputs"



# Create necessary folders if they don't exist
os.makedirs(vegalite_folder, exist_ok=True)
os.makedirs(svg_folder, exist_ok=True)

def generate_bar_chart_spec(df):
    """
    Generate a Vega-Lite bar chart specification from a DataFrame.
    Uses the first column as 'x' and the second column as 'y'.
    :param df: DataFrame containing the table.
    :return: A dictionary representing the Vega-Lite specification.
    """
    x_column = df.columns[0]  # Assume first column is X-axis
    y_column = df.columns[1]  # Assume second column is Y-axis

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "Bar chart auto-generated from CSV",
        "data": {
            "values": df.to_dict(orient="records")
        },
        "mark": "bar",
        "encoding": {
            "x": {"field": x_column, "type": "ordinal"},
            "y": {"field": y_column, "type": "quantitative"}
        }
    }

def convert_vegalite_to_svg(vegalite_file, output_file):
    """
    Converts a Vega-Lite spec JSON file to an SVG file using vega-cli.
    """
    try:
        subprocess.run(
            [
                "vega",
                vegalite_file,
                "-o", output_file
            ],
            check=True
        )
        print(f"SVG generated: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to generate SVG for {vegalite_file}: {e}")
    except FileNotFoundError:
        print("Ensure `vega-cli` is installed and available in the PATH.")

# Process each CSV file in the tables folder
for filename in os.listdir(tables_folder):
    if filename.endswith(".csv"):
        table_path = os.path.join(tables_folder, filename)
        df = pd.read_csv(table_path)

        # Ensure there are at least two columns for x and y
        if df.shape[1] < 2:
            print(f"Skipping {filename}: Less than 2 columns.")
            continue

        # Use only the first two columns for x and y
        df = df.iloc[:, :2]

        # Generate Vega-Lite bar chart spec
        spec = generate_bar_chart_spec(df)

        # Save the Vega-Lite spec to a JSON file
        spec_filename = os.path.splitext(filename)[0] + ".json"
        spec_path = os.path.join(vegalite_folder, spec_filename)
        with open(spec_path, "w") as f:
            json.dump(spec, f, indent=2)

        # Convert the Vega-Lite spec to an SVG file
        svg_filename = os.path.splitext(filename)[0] + ".svg"
        svg_path = os.path.join(svg_folder, svg_filename)
        convert_vegalite_to_svg(spec_path, svg_path)

print("All SVG files have been generated.")