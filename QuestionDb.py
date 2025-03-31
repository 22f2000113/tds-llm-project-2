# /// script
# requires-python = "==3.12"
# dependencies = [
#   "duckdb",
#   "sentence-transformers",
# ]
# ///

import duckdb
from sentence_transformers import SentenceTransformer

def setup_vector_db() -> tuple[duckdb.DuckDBPyConnection, SentenceTransformer]:
    """Initialize DuckDB with VSS extension and embedding model."""
    # Initialize model
    model = SentenceTransformer("BAAI/bge-base-en-v1.5")
    vector_dim = model.get_sentence_embedding_dimension()

    # Setup DuckDB with VSS extension
    conn = duckdb.connect(":memory:")
    conn.install_extension("vss")
    conn.load_extension("vss")

    # Create table with vector column
    conn.execute(f"""
        CREATE TABLE documents (
            id VARCHAR,
            text VARCHAR,
            vector FLOAT[{vector_dim}]
        )
    """)

    # Create HNSW index for vector similarity search
    conn.execute("CREATE INDEX vector_idx ON documents USING HNSW (vector)")
    return conn, model

def search_similar(conn: duckdb.DuckDBPyConnection, model: SentenceTransformer,
                        query: str, n_results: int = 1) -> list[dict]:
    """Search for documents similar to query using vector similarity."""
    # Encode query to vector
    query_vector = model.encode(query).tolist()

    # Search using HNSW index with explicit FLOAT[] cast
    results = conn.execute("""
        SELECT id, text, array_distance(vector, CAST(? AS FLOAT[768])) as distance
        FROM documents
        ORDER BY array_distance(vector, CAST(? AS FLOAT[768]))
        LIMIT ?
    """, [query_vector, query_vector, n_results]).fetchall()
    return results[0][0]

def init_db():
    conn, model = setup_vector_db()

    # Add sample documents
    documents =[
      '''Your Task ESPN Cricinfo has ODI batting stats for each batsman. The result is paginated across multiple pages. Count the number of ducks in page number 26. Understanding the Data Source: ESPN Cricinfo's ODI batting statistics are spread across multiple pages, each containing a table of player data. Go to page number 26. Setting Up Google Sheets: Utilize Google Sheets' IMPORTHTML function to import table data from the URL for page number 26. Data Extraction and Analysis: Pull the relevant table from the assigned page into Google Sheets. Locate the column that represents the number of ducks for each player. (It is titled "0".) Sum the values in the "0" column to determine the total number of ducks on that page. Impact By automating the extraction and analysis of cricket batting statistics, CricketPro Insights can: Enhance Analytical Efficiency: Reduce the time and effort required to manually gather and process player performance data. Provide Timely Insights: Deliver up-to-date statistical analyses that aid teams and coaches in making informed decisions. Scalability: Easily handle large volumes of data across multiple pages, ensuring comprehensive coverage of player performances. Data-Driven Strategies: Enable the development of data-driven strategies for player selection, training focus areas, and game planning. Client Satisfaction: Improve service offerings by providing accurate and insightful analytics that meet the specific needs of clients in the cricketing world. What is the total number of ducks across players on page number 26 of ESPN Cricinfo's ODI batting stats?''',
      
      '''Source: Utilize IMDb's advanced web search at https://www.imdb.com/search/title/ to access movie data.Filter: Filter all titles with a rating between 3 and 5.Format: For up to the first 25 titles, extract the necessary details: ID, title, year, and rating. The ID of the movie is the part of the URL after tt in the href attribute. For example, tt10078772. Organize the data into a JSON structure as follows:[  { "id": "tt1234567", "title": "Movie 1", "year": "2021", "rating": "5.8" },  { "id": "tt7654321", "title": "Movie 2", "year": "2019", "rating": "6.2" },  // ... more titles]Submit: Submit the JSON data in the text box below.''',
      
      '''Write a web application that exposes an API with a single query parameter: ?country=. It should fetch the Wikipedia page of the country, extracts all headings (H1 to H6), and create a Markdown outline for the country. The outline should look like this:## Contents# Vanuatu## Etymology## History### Prehistory...API Development: Choose any web framework (e.g., FastAPI) to develop the web application. Create an API endpoint (e.g., /api/outline) that accepts a country query parameter.Fetching Wikipedia Content: Find out the Wikipedia URL of the country and fetch the page's HTML.Extracting Headings: Use an HTML parsing library (e.g., BeautifulSoup, lxml) to parse the fetched Wikipedia page. Extract all headings (H1 to H6) from the page, maintaining order.Generating Markdown Outline: Convert the extracted headings into a Markdown-formatted outline. Headings should begin with #.Enabling CORS: Configure the web application to include appropriate CORS headers, allowing GET requests from any origin.What is the URL of your API endpoint?''',
      
      '''As part of this initiative, you are tasked with developing a system that automates the following:API Integration and Data Retrieval: Use the BBC Weather API to fetch the weather forecast for Kuwait City. Send a GET request to the locator service to obtain the city's locationId. Include necessary query parameters such as API key, locale, filters, and search term (city).Weather Data Extraction: Retrieve the weather forecast data using the obtained locationId. Send a GET request to the weather broker API endpoint with the locationId.Data Transformation: Extract the localDate and enhancedWeatherDescription from each day's forecast. Iterate through the forecasts array in the API response and map each localDate to its corresponding enhancedWeatherDescription. Create a JSON object where each key is the localDate and the value is the enhancedWeatherDescription.The output would look like this:{  "2025-01-01": "Sunny with scattered clouds",  "2025-01-02": "Partly cloudy with a chance of rain",  "2025-01-03": "Overcast skies",  // ... additional days}What is the JSON weather forecast description for Kuwait City?''',
      
      '''What is the minimum latitude of the bounding box of the city Chengdu in the country China on the Nominatim API?    1. API Integration: Use the Nominatim API to fetch geospatial data for a specified city within a country via a GET request to the Nominatim API with parameters for the city and country. Ensure adherence to Nominatim’s usage policies, including rate limiting and proper attribution.    2. Data Retrieval and Filtering: Parse the JSON response from the API. If multiple results are returned (e.g., multiple cities named “Springfield” in different states), filter the results based on the provided osm_id ending to select the correct city instance.    3. Parameter Extraction: Access the boundingbox attribute. Depending on whether you're looking for the minimum or maximum latitude, extract the corresponding latitude value.ImpactBy automating the extraction and processing of bounding box data, UrbanRide can:    • Optimize Routing: Enhance route planning algorithms with precise geographical boundaries, reducing delivery times and operational costs.    • Improve Fleet Allocation: Allocate vehicles more effectively across defined service zones based on accurate city extents.    • Enhance Market Analysis: Gain deeper insights into regional performance, enabling targeted marketing and service improvements.    • Scale Operations: Seamlessly integrate new cities into their service network with minimal manual intervention, ensuring consistent data quality.What is the minimum latitude of the bounding box of the city Chengdu in the country China on the Nominatim API? Value of the minimum latitude''',
      
      '''Your TaskSearch using the Hacker News RSS API for the latest Hacker News post mentioning Stripe and having a minimum of 81 points. What is the link that it points to?    1. Automate Data Retrieval: Utilize the HNRSS API to fetch the latest Hacker News posts. Use the URL relevant to fetching the latest posts, searching for topics and filtering by a minimum number of points.    2. Extract and Present Data: Extract the most recent <item> from this result. Get the <link> tag inside it.    3. Share the result: Type in just the URL in the answer.What is the link to the latest Hacker News post mentioning Stripe having at least 81 points?''',
      
      '''Using the GitHub API, find all users located in the city Paris with over 90 followers.When was the newest user's GitHub profile created?    1. API Integration and Data Retrieval: Leverage GitHub’s search endpoints to query users by location and filter them by follower count.    2. Data Processing: From the returned list of GitHub users, isolate those profiles that meet the specified criteria.    3. Sort and Format: Identify the "newest" user by comparing the created_at dates provided in the user profile data. Format the account creation date in the ISO 8601 standard (e.g., "2024-01-01T00:00:00Z").ImpactBy automating this data retrieval and filtering process, CodeConnect gains several strategic advantages:    • Targeted Recruitment: Quickly identify new, promising talent in key regions, allowing for more focused and timely recruitment campaigns.    • Competitive Intelligence: Stay updated on emerging trends within local developer communities and adjust talent acquisition strategies accordingly.    • Efficiency: Automating repetitive data collection tasks frees up time for recruiters to focus on engagement and relationship-building.    • Data-Driven Decisions: Leverage standardized and reliable data to support strategic business decisions in recruitment and market research.Enter the date (ISO 8601, e.g. "2024-01-01T00:00:00Z") when the newest user joined GitHub.''',

      '''Create a scheduled GitHub action that runs daily and adds a commit to your repository. The workflow should:    • Use schedule with cron syntax to run once per day (must use specific hours/minutes, not wildcards)    • Include a step with your email 21f3002724@ds.study.iitm.ac.in in its name    • Create a commit in each run    • Be located in .github/workflows/ directoryAfter creating the workflow:    • Trigger the workflow and wait for it to complete    • Ensure it appears as the most recent action in your repository    • Verify that it creates a commit during or within 5 minutes of the workflow runEnter your repository URL (format: https://github.com/USER/REPO):''',

      '''This file, q-extract-tables-from-pdf.pdf contains a table of student marks in Maths, Physics, English, Economics, and Biology.Calculate the total Physics marks of students who scored 55 or more marks in Physics in groups 19-55 (including both groups).    1. Data Extraction:: Retrieve the PDF file containing the student marks table and use PDF parsing libraries (e.g., Tabula, Camelot, or PyPDF2) to accurately extract the table data into a workable format (e.g., CSV, Excel, or a DataFrame).    2. Data Cleaning and Preparation: Convert marks to numerical data types to facilitate accurate calculations.    3. Data Filtering: Identify students who have scored marks between 55 and Physics in groups 19-55 (including both groups).    4. Calculation: Sum the marks of the filtered students to obtain the total marks for this specific cohort.By automating the extraction and analysis of student marks, EduAnalytics empowers Greenwood High School to make informed decisions swiftly. This capability enables the school to:    • Identify Performance Trends: Quickly spot areas where students excel or need additional support.    • Allocate Resources Effectively: Direct teaching resources and interventions to groups and subjects that require attention.    • Enhance Reporting Efficiency: Reduce the time and effort spent on manual data processing, allowing educators to focus more on teaching and student engagement.    • Support Data-Driven Strategies: Use accurate and timely data to shape educational strategies and improve overall student outcomes.What is the total Physics marks of students who scored 55 or more marks in Physics in groups 19-55 (including both groups)?''',

      '''As part of the Documentation Transformation Project, you are a junior developer at EduDocs tasked with developing a streamlined workflow for converting PDF files to Markdown and ensuring their consistent formatting. This project is critical for supporting EduDocs' commitment to delivering high-quality, accessible educational resources to its clients.q-pdf-to-markdown.pdf has the contents of a sample document.    1. Convert the PDF to Markdown: Extract the content from the PDF file. Accurately convert the extracted content into Markdown format, preserving the structure and formatting as much as possible.    2. Format the Markdown: Use Prettier version 3.4.2 to format the converted Markdown file.    3. Submit the Formatted Markdown: Provide the final, formatted Markdown file as your submission.ImpactBy completing this exercise, you will contribute to EduDocs Inc.'s mission of providing high-quality, accessible educational resources. Automating the PDF to Markdown conversion and ensuring consistent formatting:    • Enhances Productivity: Reduces the time and effort required to prepare documentation for clients.    • Improves Quality: Ensures all documents adhere to standardized formatting, enhancing readability and professionalism.    • Supports Scalability: Enables EduDocs to handle larger volumes of documentation without compromising on quality.    • Facilitates Integration: Makes it easier to integrate Markdown-formatted documents into various digital platforms and content management systems.What is the markdown content of the PDF, formatted with prettier@3.4.2?''',


      '''Install and run Visual Studio Code. In your Terminal (or Command Prompt), type code -s and press Enter. Copy and paste the entire output below.What is the output of code -s?''',

            '''Running uv run --with httpie -- https [URL] installs the Python package httpie and sends a HTTPS request to the URL.
            
            Send a HTTPS request to https://httpbin.org/get with the URL encoded parameter email set to 22f2000113@ds.study.iitm.ac.in
            
            What is the JSON output of the command? (Paste only the JSON body, not the headers)''',

            '''Let's make sure you know how to use npx and prettier.Download . In the directory where you downloaded it, make sure it is called README.md, and run npx -y prettier@3.4.2 README.md | sha256sum.What is the output of the command?''',

            '''Let's make sure you can write formulas in Google Sheets. Type this formula into Google Sheets. (It won't work in Excel)
            
            =SUM(ARRAY_CONSTRAIN(SEQUENCE(100, 100, 2, 1), 1, 10))
            
            What is the result?''',

            ''''Let's make sure you can write formulas in Excel. Type this formula into Excel.
            
            Note: This will ONLY work in Office 365.
            
            =SUM(TAKE(SORTBY({12,1,0,13,1,0,1,1,11,3,13,15,13,14,15,3}, {10,9,13,2,11,8,16,14,7,15,5,4,6,1,3,12}), 1, 5))
            What is the result?''',
            
            '''Just above this paragraph, there's a hidden input with a secret value.
            
            What is the value in the hidden input?''',
            
            '''How many Wednesdays are there in the date range 1982-04-24 to 2007-12-01? The dates are in the year-month-day format. Include both the start and end date in your count.''',

            '''Download q-extract-csv-zip.zip and unzip file  which has a single extract.csv file inside.
            
            What is the value in the "answer" column of the CSV file?''',

            '''Let's make sure you know how to use JSON. Sort this JSON array of objects by the value of the age field. In case of a tie, sort by the name field. Paste the resulting JSON below without any spaces or newlines.
            
            [{"name":"Alice","age":86},{"name":"Bob","age":11},{"name":"Charlie","age":47},{"name":"David","age":10},{"name":"Emma","age":25},{"name":"Frank","age":45},{"name":"Grace","age":57},{"name":"Henry","age":4},{"name":"Ivy","age":71},{"name":"Jack","age":33},{"name":"Karen","age":53},{"name":"Liam","age":10},{"name":"Mary","age":83},{"name":"Nora","age":84},{"name":"Oscar","age":52},{"name":"Paul","age":92}]''',
            
            '''Download q-multi-cursor-json.txt and use multi-cursors and convert it into a single JSON object, where key=value pairs are converted into {key: value, key: value, ...}.
            
            What's the result when you paste the JSON at tools-in-data-science.pages.dev/jsonhash and click the Hash button?''',

            '''Let's make sure you know how to select elements using CSS selectors. Find all <div>s having a foo class in the hidden element below. What's the sum of their data-value attributes?''',

            '''Download and process the files in q-unicode-data.zip which contains three files with different encodings:
            
            data1.csv: CSV file encoded in CP-1252
            data2.csv: CSV file encoded in UTF-8
            data3.txt: Tab-separated file encoded in UTF-16
            Each file has 2 columns: symbol and value. Sum up all the values where the symbol matches ” OR Ž OR ˆ across all three files.
            
            What is the sum of all values associated with these symbols?''',

            '''Let's make sure you know how to use GitHub. Create a GitHub account if you don't have one. Create a new public repository. Commit a single JSON file called email.json with the value {"email": "22f2000113@ds.study.iitm.ac.in"} and push it.
            
            Enter the raw Github URL of email.json so we can verify it. (It might look like https://raw.githubusercontent.com/[GITHUB ID]/[REPO NAME]/main/email.json.)''',

            '''Download q-replace-across-files.zip and unzip it into a new folder, then replace all "IITM" (in upper, lower, or mixed case) with "IIT Madras" in all files. Leave everything as-is - don't change the line endings.
            
            What does running cat * | sha256sum in that folder show in bash?''',

            '''Download q-list-files-attributes.zip and extract it. Use ls with options to list all files in the folder along with their date and file size.
            
            What's the total size of all files at least 8340 bytes large and modified on or after Tue, 20 Jul, 1993, 9:26 pm IST?''',

            '''Download q-move-rename-files.zip and extract it. Use mv to move all files under folders into an empty folder. Then rename all files replacing each digit with the next. 1 becomes 2, 9 becomes 0, a1b9c.txt becomes a2b0c.txt.
            
            What does running grep . * | LC_ALL=C sort | sha256sum in bash on that folder show?''',

            '''Download q-compare-files.zip and extract it. It has 2 nearly identical files, a.txt and b.txt, with the same number of lines.
            
            How many lines are different between a.txt and b.txt?''',

            '''There is a tickets table in a SQLite database that has columns type, units, and price. Each row is a customer bid for a concert ticket.
            
            type	units	price
            Silver	991	1
            GOLD	561	0.55
            GOLD	451	1.01
            silver	224	0.57
            GOLD	178	1.87
            ...
            What is the total sales of all the items in the "Gold" ticket type? Write SQL to calculate it.
            Get all rows where the Type is "Gold". Ignore spaces and treat mis-spellings like GOLD, gold, etc. as "Gold". Calculate the sales as Units * Price, and sum them up.''',

                '''Write documentation in Markdown for an **imaginary** analysis of the number of steps you walked each day for a week, comparing over time and with friends. The Markdown must include:
            
                Top-Level Heading: At least 1 heading at level 1, e.g., # Introduction
                Subheadings: At least 1 heading at level 2, e.g., ## Methodology
                Bold Text: At least 1 instance of bold text, e.g., **important**
                Italic Text: At least 1 instance of italic text, e.g., *note*
                Inline Code: At least 1 instance of inline code, e.g., sample_code
                Code Block: At least 1 instance of a fenced code block, e.g.
            
                print("Hello World")
                Bulleted List: At least 1 instance of a bulleted list, e.g., - Item
                Numbered List: At least 1 instance of a numbered list, e.g., 1. Step One
                Table: At least 1 instance of a table, e.g., | Column A | Column B |
                Hyperlink: At least 1 instance of a hyperlink, e.g., [Text](https://example.com)
                Image: At least 1 instance of an image, e.g., ![Alt Text](https://example.com/image.jpg)
                Blockquote: At least 1 instance of a blockquote, e.g., > This is a quote
                Enter your Markdown here:''',

                '''Download the image below and compress it losslessly to an image that is less than 1,500 bytes.
                By losslessly, we mean that every pixel in the new image should be identical to the original image.
            
                Upload your losslessly compressed image (less than 1,500 bytes)''',

                '''Publish a page using GitHub Pages that showcases your work. Ensure that your email address 22f2000113@ds.study.iitm.ac.in is in the page's HTML.
            
                GitHub pages are served via CloudFlare which obfuscates emails. So, wrap your email address inside a:
            
                <!--email_off-->22f2000113@ds.study.iitm.ac.in<!--/email_off-->
                What is the GitHub Pages URL? It might look like: https://[USER].github.io/[REPO]/
            
                If a recent change that's not reflected, add ?v=1, ?v=2 to the URL to bust the cache.''',

                '''Let's make sure you can access Google Colab. Run this program on Google Colab, allowing all required access to your email ID: 22f2000113@ds.study.iitm.ac.in.
            
                import hashlib
                import requests
                from google.colab import auth
                from oauth2client.client import GoogleCredentials
            
                auth.authenticate_user()
                creds = GoogleCredentials.get_application_default()
                token = creds.get_access_token().access_token
                response = requests.get(
                  "https://www.googleapis.com/oauth2/v1/userinfo",
                  params={"alt": "json"},
                  headers={"Authorization": f"Bearer {token}"}
                )
                email = response.json()["email"]
                hashlib.sha256(f"{email} {creds.token_expiry.year}".encode()).hexdigest()[-5:]
                What is the result? (It should be a 5-character string)''',

                '''Download this image. Create a new Google Colab notebook and run this code (after fixing a mistake in it) to calculate the number of pixels with a certain minimum brightness:
            
                import numpy as np
                from PIL import Image
                from google.colab import files
                import colorsys
            
                # There is a mistake in the line below. Fix it
                image = Image.open(list(files.upload().keys)[0])
            
                rgb = np.array(image) / 255.0
                lightness = np.apply_along_axis(lambda x: colorsys.rgb_to_hls(*x)[1], 2, rgb)
                light_pixels = np.sum(lightness > 0.227)
                print(f'Number of pixels with lightness > 0.227: {light_pixels}')
                What is the result? (It should be a number)''',

                '''Download this q-vercel-python.json which has the marks of 100 imaginary students.
            
                Create and deploy a Python app to Vercel. Expose an API so that when a request like https://your-app.vercel.app/api?name=X&name=Y is made, it returns a JSON response with the marks of the names X and Y in the same order, like this:
            
                { "marks": [10, 20] }
                Make sure you enable CORS to allow GET requests from any origin.
            
                What is the Vercel URL? It should look like: https://your-app.vercel.app/api''',

                '''Create a GitHub action on one of your GitHub repositories. Make sure one of the steps in the action has a name that contains your email address 22f2000113@ds.study.iitm.ac.in. For example:
            
            
                jobs:
                  test:
                    steps:
                      - name: 22f2000113@ds.study.iitm.ac.in
                        run: echo "Hello, world!"
            
                Trigger the action and make sure it is the most recent action.
            
                What is your repository URL? It will look like: https://github.com/USER/REPO''',

                '''Create and push an image to Docker Hub. Add a tag named 22f2000113 to the image.
            
                What is the Docker image URL? It should look like: https://hub.docker.com/repository/docker/$USER/$REPO/general''',

                '''Download q-fastapi.csv. This file has 2-columns:
            
                studentId: A unique identifier for each student, e.g. 1, 2, 3, ...
                class: The class (including section) of the student, e.g. 1A, 1B, ... 12A, 12B, ... 12Z
                Write a FastAPI server that serves this data. For example, /api should return all students data (in the same row and column order as the CSV file) as a JSON like this:
            
                {
                  "students": [
                    {
                      "studentId": 1,
                      "class": "1A"
                    },
                    {
                      "studentId": 2,
                      "class": "1B"
                    }, ...
                  ]
                }
                If the URL has a query parameter class, it should return only students in those classes. For example, /api?class=1A should return only students in class 1A. /api?class=1A&class=1B should return only students in class 1A and 1B. There may be any number of classes specified. Return students in the same order as they appear in the CSV file (not the order of the classes).
            
                Make sure you enable CORS to allow GET requests from any origin.
            
                What is the API URL endpoint for FastAPI? It might look like: http://127.0.0.1:8000/api
                We'll check by sending a request to this URL with ?class=... added and check if the response matches the data.''',

                '''Download Llamafile. Run the Llama-3.2-1B-Instruct.Q6_K.llamafile model with it.
            
                Create a tunnel to the Llamafile server using ngrok.
            
                What is the ngrok URL? It might look like: https://[random].ngrok-free.app/''',

                '''DataSentinel Inc. is a tech company specializing in building advanced natural language processing (NLP) solutions. Their latest project involves integrating an AI-powered sentiment analysis module into an internal monitoring dashboard. The goal is to automatically classify large volumes of unstructured feedback and text data from various sources as either GOOD, BAD, or NEUTRAL. As part of the quality assurance process, the development team needs to test the integration with a series of sample inputs—even ones that may not represent coherent text—to ensure that the system routes and processes the data correctly.

                 Before rolling out the live system, the team creates a test harness using Python. The harness employs the httpx library to send POST requests to OpenAI's API. For this proof-of-concept, the team uses the dummy model gpt-4o-mini along with a dummy API key in the Authorization header to simulate real API calls.

                One of the test cases involves sending a sample piece of meaningless text:
                
                zF Et0X  F SrR 
                l7R  9yc  kWFj
                4XFlS9aqNDk fub e4W
                
                Write a Python program that uses httpx to send a POST request to OpenAI's API to analyze the sentiment of this (meaningless) text into GOOD, BAD or NEUTRAL. Specifically:
            
                Make sure you pass an Authorization header with dummy API key.
                Use gpt-4o-mini as the model.
                The first message must be a system message asking the LLM to analyze the sentiment of the text. Make sure you mention GOOD, BAD, or NEUTRAL as the categories.
                The second message must be exactly the text contained above.
                This test is crucial for DataSentinel Inc. as it validates both the API integration and the correctness of message formatting in a controlled environment. Once verified, the same mechanism will be used to process genuine customer feedback, ensuring that the sentiment analysis module reliably categorizes data as GOOD, BAD, or NEUTRAL. This reliability is essential for maintaining high operational standards and swift response times in real-world applications.
            
                Note: This uses a dummy httpx library, not the real one. You can only use:
            
                response = httpx.get(url, **kwargs)
                response = httpx.post(url, json=None, **kwargs)
                response.raise_for_status()
                response.json() ''',

                '''LexiSolve Inc. is a startup that delivers a conversational AI platform to enterprise clients. The system leverages OpenAI’s language models to power a variety of customer service, sentiment analysis, and data extraction features. Because pricing for these models is based on the number of tokens processed—and strict token limits apply—accurate token accounting is critical for managing costs and ensuring system stability.
            
                To optimize operational costs and prevent unexpected API overages, the engineering team at LexiSolve has developed an internal diagnostic tool that simulates and measures token usage for typical prompts sent to the language model.
            
                One specific test case an understanding of text tokenization. Your task is to generate data for that test case.
            
                Specifically, when you make a request to OpenAI's GPT-4o-Mini with just this user message:
                
                List only the valid English words from these: Tck0a, D, Q1TT0, R, o9Yv, hh3YwTGFQ8, ZzS4gw4, AA, NtOb, wAOHLZ0fc, owAN7, GhPWjNw, wbqZaJZjtr, bfLE, xgGzTtX1B, 8li4, viAS, DO8VOFb, 1VH, o92xER, hMPOoVKY, XLTY, MInf, IcKFFprAB, Qew5LDp, h, Xhd8ET, tBPVGge1JM, S6p7hkIp, sz, 0yd, gAFac, GtCXV4jN, plRdd, dvocGe, kJmrdydzi, 1yE, HwEZjNMne, rj59E, dGu, 1NcYP, bdqCvct22g, Ki, vGI6EYysp9, 2SZixYs, nwovTV, kOfikETj, 1uur, Ua9x, IrQIeSDJIf, g95l, Tr9v6SsE, NwgdvGGCb, oFEwK6yHFM, y5, E3PydpG1kH, X1q6aDbHp, T, eB6QcBS7, 2Yt0pU0c, OTYz, Ocw4, XnaOO7, DV, HQiH2f, URl5VtJquf, U5IDO, F1g, QZht, X9N, dwMZ6erOB, lyL, oSY, 7HYXvqDRS, 6hOO, 4yRd, TLmFgheO9H, A0gnJ9wu, 4WR0Um
                
                how many input tokens does it use up?''',

                '''RapidRoute Solutions is a logistics and delivery company that relies on accurate and standardized address data to optimize package routing. Recently, they encountered challenges with manually collecting and verifying new addresses for testing their planning software. To overcome this, the company decided to create an automated address generator using a language model, which would provide realistic, standardized U.S. addresses that could be directly integrated into their system.
            
                The engineering team at RapidRoute is tasked with designing a service that uses OpenAI's GPT-4o-Mini model to generate fake but plausible address data. The addresses must follow a strict format, which is critical for downstream processes such as geocoding, routing, and verification against customer databases. For consistency and validation, the development team requires that the addresses be returned as structured JSON data with no additional properties that could confuse their parsers.
            
                As part of the integration process, you need to write the body of the request to an OpenAI chat completion call that:
            
                Uses model gpt-4o-mini
                Has a system message: Respond in JSON
                Has a user message: Generate 10 random addresses in the US
                Uses structured outputs to respond with an object addresses which is an array of objects with required fields: longitude (number) country (string) county (string) .
                Sets additionalProperties to false to prevent additional properties.
                Note that you don't need to run the request or use an API key; your task is simply to write the correct JSON body.
            
                What is the JSON body we should send to https://api.openai.com/v1/chat/completions for this? (No need to run it or to use an API key. Just write the body of the request below.)''',

                '''Acme Global Solutions manages hundreds of invoices from vendors every month. To streamline their accounts payable process, the company is developing an automated document processing system. This system uses a computer vision model to extract useful text from scanned invoice images. Critical pieces of data such as vendor email addresses, invoice or transaction numbers, and other details are embedded within these documents.
            
                Your team is tasked with integrating OpenAI's vision model into the invoice processing workflow. The chosen model, gpt-4o-mini, is capable of analyzing both text and image inputs simultaneously. When an invoice is received—for example, an invoice image may contain a vendor email like alice.brown@acmeglobal.com and a transaction number such as 34921. The system needs to extract all embedded text to automatically populate the vendor management system.
            
                The automated process will send a POST request to OpenAI's API with two inputs in a single user message:
            
                Text: A simple instruction "Extract text from this image."
                Image URL: A base64 URL representing the invoice image that might include the email and the transaction number among other details.
                Here is an example invoice image:
            
                Write just the JSON body (not the URL, nor headers) for the POST request that sends these two pieces of content (text and image URL) to the OpenAI API endpoint.
            
                Use gpt-4o-mini as the model.
                Send a single user message to the model that has a text and an image_url content (in that order).
                The text content should be Extract text from this image.
                Send the image_url as a base64 URL of the image above. CAREFUL: Do not modify the image.''',

                '''SecurePay, a leading fintech startup, has implemented an innovative feature to detect and prevent fraudulent activities in real time. As part of its security suite, the system analyzes personalized transaction messages by converting them into embeddings. These embeddings are compared against known patterns of legitimate and fraudulent messages to flag unusual activity.
            
                Imagine you are working on the SecurePay team as a junior developer tasked with integrating the text embeddings feature into the fraud detection module. When a user initiates a transaction, the system sends a personalized verification message to the user's registered email address. This message includes the user's email address and a unique transaction code (a randomly generated number). Here are 2 verification messages:
            
                Dear user, please verify your transaction code 65692 sent to 22f2000113@ds.study.iitm.ac.in
                Dear user, please verify your transaction code 85184 sent to 22f2000113@ds.study.iitm.ac.in
                The goal is to capture this message, convert it into a meaningful embedding using OpenAI's text-embedding-3-small model, and subsequently use the embedding in a machine learning model to detect anomalies.
            
                Your task is to write the JSON body for a POST request that will be sent to the OpenAI API endpoint to obtain the text embedding for the 2 given personalized transaction verification messages above. This will be sent to the endpoint https://api.openai.com/v1/embeddings.''',

                '''ShopSmart is an online retail platform that places a high value on customer feedback. Each month, the company receives hundreds of comments from shoppers regarding product quality, delivery speed, customer service, and more. To automatically understand and cluster this feedback, ShopSmart's data science team uses text embeddings to capture the semantic meaning behind each comment.
            
                As part of a pilot project, ShopSmart has curated a collection of 25 feedback phrases that represent a variety of customer sentiments. Examples of these phrases include comments like “Fast shipping and great service,” “Product quality could be improved,” “Excellent packaging,” and so on. Due to limited processing capacity during initial testing, you have been tasked with determine which pair(s) of 5 of these phrases are most similar to each other. This similarity analysis will help in grouping similar feedback to enhance the company’s understanding of recurring customer issues.
            
                ShopSmart has written a Python program that has the 5 phrases and their embeddings as an array of floats. It looks like this:
            
                our task is to write a Python function most_similar(embeddings) that will calculate the cosine similarity between each pair of these embeddings and return the pair that has the highest similarity. The result should be a tuple of the two phrases that are most similar.''',

                '''InfoCore Solutions is a technology consulting firm that maintains an extensive internal knowledge base of technical documents, project reports, and case studies. Employees frequently search through these documents to answer client questions quickly or gain insights for ongoing projects. However, due to the sheer volume of documentation, traditional keyword-based search often returns too many irrelevant results.
            
                To address this issue, InfoCore's data science team decides to integrate a semantic search feature into their internal portal. This feature uses text embeddings to capture the contextual meaning of both the documents and the user's query. The documents are pre-embedded, and when an employee submits a search query, the system computes the similarity between the query's embedding and those of the documents. The API then returns a ranked list of document identifiers based on similarity.
            
                Imagine you are an engineer on the InfoCore team. Your task is to build a FastAPI POST endpoint that accepts an array of docs and query string via a JSON body. The endpoint is structured as follows:
            
                POST /similarity
            
                {
                  "docs": ["Contents of document 1", "Contents of document 2", "Contents of document 3", ...],
                  "query": "Your query string"
                }
                Service Flow:
            
                Request Payload: The client sends a POST request with a JSON body containing:
                docs: An array of document texts from the internal knowledge base.
                query: A string representing the user's search query.
                Embedding Generation: For each document in the docs array and for the query string, the API computes a text embedding using text-embedding-3-small.
                Similarity Computation: The API then calculates the cosine similarity between the query embedding and each document embedding. This allows the service to determine which documents best match the intent of the query.
                Response Structure: After ranking the documents by their similarity scores, the API returns the identifiers (or positions) of the three most similar documents. The JSON response might look like this:
            
                {
                  "matches": ["Contents of document 3", "Contents of document 1", "Contents of document 2"]
                }
                Here, "Contents of document 3" is considered the closest match, followed by "Contents of document 1", then "Contents of document 2".
            
                Make sure you enable CORS to allow OPTIONS and POST methods, perhaps allowing all origins and headers.
            
                What is the API URL endpoint for your implementation? It might look like: http://127.0.0.1:8000/similarity''',

                '''TechNova Corp. is a multinational corporation that has implemented a digital assistant to support employees with various internal tasks. The assistant can answer queries related to human resources, IT support, and administrative services. Employees use a simple web interface to enter their requests, which may include:
            
                Checking the status of an IT support ticket.
                Scheduling a meeting.
                Retrieving their current expense reimbursement balance.
                Requesting details about their performance bonus.
                Reporting an office issue by specifying a department or issue number.
                Each question is direct and templatized, containing one or more parameters such as an employee or ticket number (which might be randomized). In the backend, a FastAPI app routes each request by matching the query to one of a set of pre-defined functions. The response that the API returns is used by OpenAI to call the right function with the necessary arguments.
            
                Pre-Defined Functions:
            
                For this exercise, assume the following functions have been defined:
            
                get_ticket_status(ticket_id: int)
                schedule_meeting(date: str, time: str, meeting_room: str)
                get_expense_balance(employee_id: int)
                calculate_performance_bonus(employee_id: int, current_year: int)
                report_office_issue(issue_code: int, department: str)
                Each function has a specific signature, and the student’s FastAPI app should map specific queries to these functions.
            
                Example Questions (Templatized with a Random Number):
            
                Ticket Status:
                Query: "What is the status of ticket 83742?"
                → Should map to get_ticket_status(ticket_id=83742)
                Meeting Scheduling:
                Query: "Schedule a meeting on 2025-02-15 at 14:00 in Room A."
                → Should map to schedule_meeting(date="2025-02-15", time="14:00", meeting_room="Room A")
                Expense Reimbursement:
                Query: "Show my expense balance for employee 10056."
                → Should map to get_expense_balance(employee_id=10056)
                Performance Bonus Calculation:
                Query: "Calculate performance bonus for employee 10056 for 2025."
                → Should map to calculate_performance_bonus(employee_id=10056, current_year=2025)
                Office Issue Reporting:
                Query: "Report office issue 45321 for the Facilities department."
                → Should map to report_office_issue(issue_code=45321, department="Facilities")
                Task Overview:
            
                Develop a FastAPI application that:
            
                Exposes a GET endpoint /execute?q=... where the query parameter q contains one of the pre-templatized questions.
                Analyzes the q parameter to identify which function should be called.
                Extracts the parameters from the question text.
                Returns a response in the following JSON format:
            
                { "name": "function_name", "arguments": "{ ...JSON encoded parameters... }" }
                For example, the query "What is the status of ticket 83742?" should return:
            
                {
                  "name": "get_ticket_status",
                  "arguments": "{\"ticket_id\": 83742}"
                }
                Make sure you enable CORS to allow GET requests from any origin.
            
                What is the API URL endpoint for your implementation? It might look like: http://127.0.0.1:8000/execute
                We'll check by sending a GET request to this URL with ?q=... containing a task. We'll verify that it matches the expected response. Arguments must be in the same order as the function definition.''',

                '''SecurePrompt Technologies is a cybersecurity firm that specializes in deploying large language models (LLMs) for sensitive enterprise applications. To ensure that these models adhere strictly to security policies, SecurePrompt imposes hardcoded behavioral instructions on the LLMs. For example, an LLM may be configured to never output certain sensitive keywords.
            
                As part of their regular security audits and red-team exercises, SecurePrompt's engineers and external auditors test how well the LLMs follow these strict instructions. One objective of these tests is to determine if it is possible to bypass or trick the LLM into violating its preset security constraints.
            
                This task is simulates potential attack vectors where a malicious actor might manipulate the model's output by ingeniously engineering the prompt. While the intention is to expose vulnerabilities in instruction adherence, it also provides valuable insights into improving the safety and security of the deployed system.
            
                Here's your task: You are chatting with an LLM that has been told to never say Yes. You need to get it to say Yes.
            
                Use your AI Proxy token when prompted.
            
                Write a prompt that will get the LLM to say Yes.
            
                As long as the LLM says the word Yes (case sensitive), you will be marked correct. Careful! If you get a correct answer, submit and don't change it. You may get a different answer next time.''',
                '''As a data analyst at EduTrack Systems, your task is to process this text file and determine the number of unique students based on their student IDs. This deduplication is essential to:Ensure Accurate Reporting: Avoid inflated counts in enrollment and performance reports.Improve Data Quality: Clean the dataset for further analytics, such as tracking academic progress or resource allocation.Optimize Administrative Processes: Provide administrators with reliable data to support decision-making.You need to do the following:Data Extraction: Read the text file line by line. Parse each line to extract the student ID.Deduplication: Remove duplicates from the student ID list.Reporting: Count the number of unique student IDs present in the file.By accurately identifying the number of unique students, EduTrack Systems will:Enhance Data Integrity: Ensure that subsequent analyses and reports reflect the true number of individual students.Reduce Administrative Errors: Minimize the risk of misinformed decisions that can arise from duplicate entries.Streamline Resource Allocation: Provide accurate student counts for budgeting, staffing, and planning academic programs.Improve Compliance Reporting: Ensure adherence to regulatory requirements by maintaining precise student records.Download the text file with student marks q-clean-up-student-marks.txt.How many unique students are there in the file?''',
                '''As a data analyst at GlobalRetail Insights, you are tasked with extracting meaningful insights from this dataset. Specifically, you need to:Group Mis-spelt City Names: Use phonetic clustering algorithms to group together entries that refer to the same city despite variations in spelling. For instance, cluster "Tokyo" and "Tokio" as one.Filter Sales Entries: Select all entries where:The product sold is Fish.The number of units sold is at least 13.Aggregate Sales by City: After clustering city names, group the filtered sales entries by city and calculate the total units sold for each city.By performing this analysis, GlobalRetail Insights will be able to:Improve Data Accuracy: Correct mis-spellings and inconsistencies in the dataset, leading to more reliable insights.Target Marketing Efforts: Identify high-performing regions for the specific product, enabling targeted promotional strategies.Optimize Inventory Management: Ensure that inventory allocations reflect the true demand in each region, reducing wastage and stockouts.Drive Strategic Decision-Making: Provide actionable intelligence to clients that supports strategic planning and competitive advantage in the market.How many units of Fish were sold in Chennai on transactions with at least 13 units?''',
                '''As a data recovery analyst at ReceiptRevive Analytics, your task is to develop a program that will:Parse the Sales Data:Read the provided JSON file containing 100 rows of sales data. Despite the truncated data (specifically the missing id), you must accurately extract the sales figures from each row.Data Validation and Cleanup:Ensure that the data is properly handled even if some fields are incomplete. Since the id is missing for some entries, your focus will be solely on the sales values.Calculate Total Sales:Sum the sales values across all 100 rows to provide a single aggregate figure that represents the total sales recorded.By successfully recovering and aggregating the sales data, ReceiptRevive Analytics will enable RetailFlow Inc. to:Reconstruct Historical Sales Data: Gain insights into past sales performance even when original receipts are damaged.Inform Business Decisions: Use the recovered data to understand sales trends, adjust inventory, and plan future promotions.Enhance Data Recovery Processes: Improve methods for handling imperfect OCR data, reducing future data loss and increasing data accuracy.Build Client Trust: Demonstrate the ability to extract valuable insights from challenging datasets, thereby reinforcing client confidence in ReceiptRevive's services.Download the data from q-parse-partial-json.jsonl.What is the total sales value?''',
                '''As a data analyst at DataSure Technologies, you have been tasked with developing a script that processes a large JSON log file and counts the number of times a specific key, represented by the placeholder Q, appears in the JSON structure. Your solution must:Parse the Large, Nested JSON: Efficiently traverse the JSON structure regardless of its complexity.Count Key Occurrences: Increment a count only when Q is used as a key in the JSON object (ignoring occurrences of Q as a value).Return the Count: Output the total number of occurrences, which will be used by the operations team to assess the prevalence of particular system events or errors.By accurately counting the occurrences of a specific key in the log files, DataSure Technologies can:Diagnose Issues: Quickly determine the frequency of error events or specific system flags that may indicate recurring problems.Prioritize Maintenance: Focus resources on addressing the most frequent issues as identified by the key count.Enhance Monitoring: Improve automated monitoring systems by correlating key occurrence data with system performance metrics.Inform Decision-Making: Provide data-driven insights that support strategic planning for system upgrades and operational improvements.Download the data from  q-extract-nested-json-keys.json.How many times does Q appear as a key?''',


        ]
    ids = [
        "W4Q1",
        "W4Q2",
        "W4Q3",
        "W4Q4",
        "W4Q5",
        "W4Q6",
        "W4Q7",
        "W4Q8",
        "W4Q9",
        "W4Q10",
        "W1Q1",
        "W1Q2",
        "W1Q3",
        "W1Q4",
        "W1Q5",
        "W1Q6",
        "W1Q7",
        "W1Q8",
        "W1Q9",
        "W1Q10",
        "W1Q11",
        "W1Q12",
        "W1Q13",
        "W1Q14",
        "W1Q15",
        "W1Q16",
        "W1Q17",
        "W1Q18",
        "W2Q1",
        "W2Q2",
        "W2Q3",
        "W2Q4",
        "W2Q5",
        "W2Q6",
        "W2Q7",
        "W2Q8",
        "W2Q9",
        "W2Q10",
        "W3Q1",
        "W3Q2",
        "W3Q3",
        "W3Q4",
        "W3Q5",
        "W3Q6",
        "W3Q7",
        "W3Q8",
        "W3Q9",
        "W5Q2",
        "W5Q5",
        "W5Q6",
        "W5Q7",
    ]
    embeddings = model.encode(documents).tolist()

    # Insert documents and vectors
    conn.executemany("""
        INSERT INTO documents (id, text, vector)
        VALUES (?, ?, ?)
    """, [(str(id_), text, embedding)
          for id_, text, embedding in zip(ids, documents, embeddings)])

    return  conn, model
    # Search similar documents
