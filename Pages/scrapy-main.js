const puppeteer = require('puppeteer');
const fs = require('fs');
const csv = require('csv-parser');

// Read the CSV file path from the command-line arguments
const csvFilePath = process.argv[2];

if (!csvFilePath) {
  console.error("CSV file path not provided.");
  process.exit(1);
}

(async () => {
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();

  const scrapedData = [];

  // Read URLs from CSV file
  const dataFromCSV = [];
  fs.createReadStream(csvFilePath)
    .pipe(csv())
    .on('data', (row) => {
      // Log the row to inspect column name
      console.log("CSV Row:", row);

      // Check for 'URL' or 'url' column
      const url = row.tool_url;
      const name = row.tool_name;

      console.log("trimmedtool name", name);

      if (url) {
        dataFromCSV.push({ url, name });
      }
    })
    .on('end', async () => {
      // Log the extracted data to inspect
      console.log("Data from CSV:", dataFromCSV);

      // Iterate over each URL
      for (const item of dataFromCSV) {
        try {
          const data = await scrapeUrl(page, item.url);
          scrapedData.push({ tool_name: item.name,tool_url: item.url, user_input: data });
        } catch (error) {
          console.error(`Error scraping URL: ${item.url}`);
          console.error(error);
        }
      }

      // Close the browser
      await browser.close();

      // Write the scraped data to a file
      fs.writeFileSync('Pages/scraped_output.json', JSON.stringify(scrapedData, null, 2));
      console.log(`Scraped data written to 'scraped_output.json'`);

      // Optional: Log the scraped data for debugging
      console.log('Scraped Data:', scrapedData);
    });
})();

async function scrapeUrl(page, url) {
  try {
    // Navigate to the URL
    await page.goto(url);

    // Wait for 5 seconds (adjust as needed)
    await page.waitForTimeout(5000);

    // Get the page content
    const text = await page.evaluate(() => document.body.innerText);

    return text;
  } catch (error) {
    console.error(`Error scraping URL: ${url}`);
    throw error; // Rethrow the error for better error handling in the calling function
  }
}