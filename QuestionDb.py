
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
    documents =['''
            Install and run Visual Studio Code. In your Terminal (or Command Prompt), type code -s and press Enter. Copy and paste the entire output below.What is the output of code -s?''',

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

        ]
    ids=["W1Q1", "W1Q2", "W1Q3", "W1Q4", "W1Q5","W1Q6","W1Q7","W1Q8","W1Q9","W1Q10", "W1Q11", "W1Q12", "W1Q13", "W1Q14","W1Q15","W1Q16","W1Q17","W1Q18","W2Q1", "W2Q2", "W2Q3", "W2Q4", "W2Q5","W2Q6","W2Q7","W2Q8","W2Q9","W2Q10","W3Q1", "W3Q2", "W3Q3", "W3Q4", "W3Q5","W3Q6","W3Q7","W3Q8","W3Q9"]
    embeddings = model.encode(documents).tolist()

    # Insert documents and vectors
    conn.executemany("""
        INSERT INTO documents (id, text, vector)
        VALUES (?, ?, ?)
    """, [(str(id_), text, embedding)
          for id_, text, embedding in zip(ids, documents, embeddings)])
    
    return  conn, model
    # Search similar documents

