const fs = require("fs");
const path = require("path");
const csv = require("csv-parser");
const vega = require("vega");
const vl = require("vega-lite");

// Folder paths
const tablesFolder = "chartqa/tables";
const specsFolder = "chartqa/scatter/specs";
const svgFolder = "svg_outputs";

// Create output folders if they don't exist
if (!fs.existsSync(specsFolder)) {
  fs.mkdirSync(specsFolder);
}
if (!fs.existsSync(svgFolder)) {
  fs.mkdirSync(svgFolder);
}

// Function to read a CSV file and return its data
function readCSV(filepath) {
  return new Promise((resolve, reject) => {
    const data = [];
    fs.createReadStream(filepath)
      .pipe(csv())
      .on("data", (row) => data.push(row))
      .on("end", () => resolve(data))
      .on("error", (err) => reject(err));
  });
}

// Function to generate Vega-Lite specification for a scatter plot
function generateVegaLiteSpec(data, xField, yField) {
  return {
    $schema: "https://vega.github.io/schema/vega-lite/v5.json",
    description: "Scatter plot auto-generated from CSV",
    data: { values: data },
    mark: "point", // Scatter plots use point marks
    encoding: {
      x: { field: xField, type: "quantitative" }, // X-axis is quantitative
      y: { field: yField, type: "quantitative" }, // Y-axis is quantitative
    }
  };
}

// Function to convert a Vega-Lite spec to SVG and save it
async function saveSVG(spec, outputFilePath) {
  try {
    const compiledSpec = vl.compile(spec).spec; // Convert Vega-Lite to Vega
    const view = new vega.View(vega.parse(compiledSpec), { renderer: "none" });
    const svg = await view.toSVG(); // Generate SVG
    fs.writeFileSync(outputFilePath, svg); // Save SVG to file
    console.log(`SVG saved: ${outputFilePath}`);
  } catch (error) {
    console.error(`Error generating SVG for ${outputFilePath}:`, error.message);
  }
}

// Main function to process all CSV files in the tables folder
async function processCSVFiles() {
  const files = fs.readdirSync(tablesFolder).filter((file) => file.endsWith(".csv"));

  for (const file of files) {
    const filepath = path.join(tablesFolder, file);
    console.log(`Processing: ${file}`);

    try {
      // Read CSV data
      const data = await readCSV(filepath);

      if (data.length === 0) {
        console.warn(`Skipping ${file}: No data found.`);
        continue;
      }

      // Use the first column as X and the second column as Y
      const xField = Object.keys(data[0])[0];
      const yField = Object.keys(data[0])[1];

      if (!xField || !yField) {
        console.warn(`Skipping ${file}: Less than 2 columns.`);
        continue;
      }

      // Generate Vega-Lite specification for scatter plot
      const spec = generateVegaLiteSpec(data, xField, yField);

      // Save the Vega-Lite specification as JSON
      const specFilePath = path.join(specsFolder, `${path.parse(file).name}.json`);
      fs.writeFileSync(specFilePath, JSON.stringify(spec, null, 2));
      console.log(`Vega-Lite spec saved: ${specFilePath}`);

      // Save the SVG
      const svgFilePath = path.join(svgFolder, `${path.parse(file).name}.svg`);
      await saveSVG(spec, svgFilePath);
    } catch (error) {
      console.error(`Error processing ${file}:`, error.message);
    }
  }

  console.log("All files processed.");
}

// Run the script
processCSVFiles();
