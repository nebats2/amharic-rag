
<h1>Amharic Rag</h1>

<p>
AmharicRag is a ready to ship FastAPI application that processes PDF documents, detect amharic and english languages, converts them into vector 
embeddings, and stores them in a Dockerized Qdrant vector database. This enables accurate and
efficient document retrieval to provide context for AI-powered chat prompts.
</p>

<h2>Core Functions are</h2>
<ul>
<li>Configuring OpenAI chat(api key)</li>
<li>Uploading Zip file for PDF traversing, and proccessing</li>
<li>Detecting and splitting Amharic and English texts in the document content</li>
<li>Vectorizing and embedding to a Qdrant Database (on-premises setup)</li>
<li>Retrieval and chat to LLM model(OpenAI)</li>
<li>Caching and embedding QA (question and answers) based on rewards for efficient document retrieval and chat </li>
</ul>
<h4><i>You must set and configure your OpenAI api key and model for chating. Embedding and vector store 
are on-premises ollama and qdrant vector db. please follow the installation steps properly</i></h4>
<hr/>
 
<h3>Authentications</h3>
<p>The API relies on an OAuth2 Jwt token for user authentication. For simplicity, only one root user 
is available, and you can make changes to the username, and hashed and raw password under app/settings/.env. 
</p>
<p>
Once Authentication : Bearer =jwt_token token at the header is required.
</p>

<h3>Uploading Documents</h3>
<p>Documents can only be uploaded as a Zip file with a pdf document type only. The zip file can
 have one or more sub-directories and/or pdf files inside. The uploaded zip files will be 
temporarly stored in the app/data/upload directory for further processing and embedding.</p>

<h3>Vectorizing and Embedding</h3>
<p>Text splitting, vectorization and embedding parameters are configuratble under the app/settings/.env
. You can make changes according to the models, splitting, and embedding requirements. Ollama
 is the emebeddings and qdrant as main vector store, all installed and run inside the docker
 environment (on-premises). Before vectorization, the contents are separated to amharic and english texts 
for better embedding and optimal vectorization. </p>

<h3>OpenAI configuration</h3>
<p>OpenAi is required to be configured with the appropirate api_key from the openAi. Only the 
embedding and vector storage models are on-premises, the chat LLM for OpenAI requires to be configured 
with proper api key. Unless the openAi configuration values are set, chat to the document will  not be 
completed. (please refer the api document on how to configure)</p>

<h2>Installation Steps</h2>
<h3>Downloding and running the app </h3>
<ol>
<li><b>Pull repo :</b> Create a directory and clone the app inside (E.g. C:/Users/documents/talent)</li>
<li> <b>Run docker:</b> Make sure you are Running the docker on your system</li>
<li> <b>Build docker-compose :</b> Redirect to the directory or run the cmd and execute :<br/>
 <b> (> docker-compose up --build -d)</b> </li>
<li><b>Pull Ollama embedding model :</b> Ollama model pulling: the default model for the ollama embedding is <b>nomic-embed-text</b>
 use <br/><b>  > docker exec ollama ollama pull nomic-embed-text </b> <br/>command to pull nomic-embed-text model for 
the ollama inside the docker 
</li>
<li><b>Open on browser and List Api documentation : </b> Once the docker compose build and up complete, open the browser 
 <br/>
       <a href="http://localhost:8071/docs">http://localhost:8071/docs</a>
 <br/>
</li>

</ol>

<h3>Authentication </h3>
<p>Every api response a BaseResponseEntity, which is a customized response object (json)
with status message, status code, body fields.</p>
<h4>Generate jwt token</h4>
<ul>
<li> POST : /auth/login
     payload: 
     {
      "username": "admin",
      "raw_password": "123456"
     }
</li>
<li>Copy the <strong>body</strong> field in the response object and paste to in input box clicking the "authorize", or to your
front-end client  Authentication : Bearer = token_value header</li>
 <img width="1030" height="261" alt="image" src="https://github.com/user-attachments/assets/3b77ee39-5563-450f-bfaf-1abb9498dbcf" />

</ul>

<h3>Configuring OpenAI</h3>
<ul>
<li>POST : /config/openai  : set the openai api_key and prefered model</li>
<li>GET : /config/openai  :  list the available configuration for openai</li>
</ul>

<h3>Document Uploadinig</h3>
<ul>
<li>POST : /upload/upload  : only zip file is accepted. It automatically embed and store to the qdrant after splitting the text contents by language</li>
<li>POST : /upload/list  :   you are list uploaded files </li>
</ul>

<h3>Chat Document (make sure cofiguring the openai setup values</h3>
<ul>
<li>POST : /chat  : enter the question you have from the uploaded document context</li>
<li>GET : /chat/similarity  :  you can list embedded document similar to your query </li>
</ul>

<hr/>
<center>Tsega.B Kum : tsegamtu@gmail.com, +251906137077</center>
