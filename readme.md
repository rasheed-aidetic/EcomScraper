<html lang="en">
<head>
    
</head>
<body>

<h1>EcomScraper</h1>
<p>EcomScraper is a Python project designed for scraping data from various e-commerce platforms like Shopify, Wix, WooCommerce, and more. This project is structured into multiple modules to organize the scrapers, database management, utilities, and configuration files.</p>

<h2>Project Structure</h2>

<pre>
EcomScraper/
├── custom_scrappers/
│   ├── bobbi_brown_scrapper.py
│   └── scraper.py
├── db/
│   ├── database.py
│   └── images/
├── shopify_scraper/
│   └── scraper.py
├── utils/
│   └── utils.py
├── wix_scrapper/
│   └── scraper.py
├── woocommerce_scrapper/
│   └── scraper.py
├── .env
├── .env.sample
├── .gitignore
├── config.py
├── database.sqlite3
├── main.py
└── requirements.txt
</pre>

<h2>Folders and Files</h2>

<h3>1. <code>custom_scrappers/</code></h3>
<p>This folder contains custom scrapers for specific websites.</p>
<ul>
    <li><code>bobbi_brown_scrapper.py</code>: A scraper tailored for the Bobbi Brown e-commerce site.</li>
    <li><code>scraper.py</code>: General scraper script for custom websites.</li>
</ul>

<h3>2. <code>db/</code></h3>
<p>Database management module for handling and storing scraped data.</p>
<ul>
    <li><code>database.py</code>: Database connection and query functions.</li>
    <li><code>images/</code>: Directory to store downloaded product images.</li>
</ul>

<h3>3. <code>shopify_scraper/</code></h3>
<p>Contains scripts specific to scraping Shopify-based websites.</p>
<ul>
    <li><code>scraper.py</code>: Script for scraping Shopify products, categories, etc.</li>
</ul>

<h3>4. <code>utils/</code></h3>
<p>Utility functions used across the project for various helper tasks.</p>
<ul>
    <li><code>utils.py</code>: General utility functions to support scraping tasks.</li>
</ul>

<h3>5. <code>wix_scrapper/</code></h3>
<p>Module designed for scraping data from Wix-based websites.</p>
<ul>
    <li><code>scraper.py</code>: Wix scraper for extracting products and related data.</li>
</ul>

<h3>6. <code>woocommerce_scrapper/</code></h3>
<p>Contains scripts to scrape data from WooCommerce-based websites.</p>
<ul>
    <li><code>scraper.py</code>: WooCommerce scraper script.</li>
</ul>

<h3>7. <code>main.py</code></h3>
<p>Main entry point of the project that initiates the scraping process. It includes the following key components:</p>
<ul>
    <li><code>initialize_db()</code>: Initializes the database for storing scraped data.</li>
    <li><code>process_website()</code>: Determines the platform type (Shopify, WooCommerce, Wix, or custom) and calls the appropriate scraper function.</li>
    <li>Uses <code>concurrent.futures</code> for parallel processing of multiple websites.</li>
</ul>

<h3>8. <code>config.py</code></h3>
<p>Configuration file that defines the list of websites to scrape and the database path.</p>
<ul>
    <li><code>WEBSITES</code>: List of URLs to be scraped. Add or remove URLs in this list as required.</li>
    <li><code>DB_PATH</code>: Path to the SQLite database. The path is fetched from the environment variable <code>SQLITE_DB_PATH</code>.</li>
</ul>

<h3>9. <code>.env</code> & <code>.env.sample</code></h3>
<p>Environment configuration files:</p>
<ul>
    <li><code>.env</code>: Contains sensitive environment variables (e.g., <code>SQLITE_DB_PATH</code> for database path).</li>
    <li><code>.env.sample</code>: Sample environment file to set up necessary variables.</li>
</ul>

<h3>10. <code>requirements.txt</code></h3>
<p>File listing all the required Python packages to run the project.</p>

<h2>Setup Instructions</h2>
<ol>
    <li>Clone the repository:
        <pre><code>git clone https://github.com/yourusername/EcomScraper.git</code></pre>
    </li>
    <li>Navigate to the project directory:
        <pre><code>cd EcomScraper</code></pre>
    </li>
    <li>Install the dependencies:
        <pre><code>pip install -r requirements.txt</code></pre>
    </li>
    <li>Set up environment variables:
        <ul>
            <li>Rename <code>.env.sample</code> to <code>.env</code>.</li>
            <li>In the <code>.env</code> file, define <code>SQLITE_DB_PATH</code> with the path to your SQLite database.</li>
        </ul>
    </li>
    <li>Update <code>config.py</code>:
        <ul>
            <li>Add URLs of e-commerce websites to the <code>WEBSITES</code> list.</li>
        </ul>
    </li>
    <li>Run the main script to start scraping:
        <pre><code>python main.py</code></pre>
    </li>
</ol>

<h2>Usage</h2>
<p>To initiate scraping, simply run <code>main.py</code>. The script will check each website’s platform and use the appropriate scraper function. The scraping progress and any errors will be displayed in the console output.</p>

<h2>License</h2>
<p>This project is licensed under the MIT License.</p>

</body>
</html>
