# FastAPI Base Template For OpenAI with Serverless Config for AWS Lambda

## Setup

1. Clone the repository: 

```bash
git clone https://github.com/chrismaresca/fast-api-base-ai.git
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Clone the `.env.local.sample` file to `.env.local` and populate with your API keys.  

4. Run locally with:

```bash
python -m uvicorn src.main:app --reload      
```

5. Deploy with:

```bash
serverless deploy --stage production   
```


