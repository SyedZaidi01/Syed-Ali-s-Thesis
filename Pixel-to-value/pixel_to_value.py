import pandas as pd
import argparse
import os

def map_pixel_to_data(y_pixel, chart_height, max_data_value, min_data_value, min_pixel):
    """
    Maps a y_pixel value to the corresponding data value using the provided formula.
    """
    data_range = max_data_value - min_data_value
    relative_position = (y_pixel - min_pixel) / chart_height
    data_value = max_data_value - (relative_position * data_range)
    return data_value

def process_csv(input_file, output_file, chart_height, max_data_value, min_data_value, min_pixel):
    """
    Reads the input CSV file, applies the mapping formula to each y_pixel value,
    and writes the results to the output CSV file.
    """
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_file)

    # Check if 'y_pixel' column exists
    if 'y_pixel' not in df.columns:
        print(f"'y_pixel' column not found in {input_file}.")
        return

    # Apply the mapping formula to each y_pixel value
    df['data_value'] = df['y_pixel'].apply(
        lambda y: map_pixel_to_data(y, chart_height, max_data_value, min_data_value, min_pixel)
    )

    # Write the updated DataFrame to the output CSV file
    df.to_csv(output_file, index=False)
    print(f"Processed {input_file} and saved results to {output_file}.")

def main():
    parser = argparse.ArgumentParser(description="Map pixel values to data values in CSV files.")
    parser.add_argument('input_files', nargs='+', help='Input CSV file(s) containing y_pixel values.')
    parser.add_argument('--chart_height', type=float, required=True, help='Vertical range of the chart in pixels.')
    parser.add_argument('--max_data_value', type=float, required=True, help='Maximum data value.')
    parser.add_argument('--min_data_value', type=float, required=True, help='Minimum data value.')
    parser.add_argument('--min_pixel', type=float, required=True, help='Pixel value corresponding to the minimum data value.')
    parser.add_argument('--output_dir', default='output', help='Directory to save output CSV files.')
    args = parser.parse_args()

    # Create the output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    for input_file in args.input_files:
        # Define the output file path
        output_file = os.path.join(args.output_dir, os.path.basename(input_file))
        process_csv(
            input_file,
            output_file,
            args.chart_height,
            args.max_data_value,
            args.min_data_value,
            args.min_pixel
        )

if __name__ == '__main__':
    main()
