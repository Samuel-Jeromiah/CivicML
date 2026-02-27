# CivicML: Maine Legislative Insights

## Overview
CivicML is a machine learning web application that analyzes legislative bills from the State of Maine. It uses a custom-trained machine learning model (Logistic Regression) built on top of text embeddings to predict which legislative committee a bill belongs to, based on its title and text contents.

## Features
- **Predictive Modeling:** Implements a text classification pipeline to categorize legislative documents.
- **Serverless API:** Uses a FastAPI backend designed to run on Vercel serverless functions, serving model inferences quickly and efficiently.
- **Interactive Frontend:** Features a modern, glassmorphic UI built with Vanilla HTML/CSS/JS for exploring sample bills and viewing AI predictions in real-time.

## Project Structure
- **/api**: Contains `index.py`, the FastAPI backend endpoint for model predictions.
- **/public**: Contains the static frontend files (`index.html`, `styles.css`, `app.js`).
- **/research**: Contains the data exploration, clustering, and model comparison Jupyter Notebooks.
- **`train.py`**: A dedicated script to train the chosen classification pipeline and serialize it for inference.
- **`inference.py`**: A helper module to load the saved `.pkl` model and handle prediction requests securely.

## Local Setup & Development

**Prerequisites:** Python 3.9+

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Samuel-Jeromiah/CivicML.git
   cd CivicML
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the local development server:**
   ```bash
   uvicorn api.index:app --port 8000
   ```

4. Open your browser and navigate to `http://localhost:8000/` to test the UI and API locally.

## Deployment
This project seamlessly deploys to [Vercel](https://vercel.com/). The `vercel.json` configuration routes `/api/*` traffic to the FastAPI python runtime, while serving the static site from the root directory.

---
*Built as a portfolio project demonstrating end-to-end Machine Learning deployment, from Jupyter exploratory data analysis to a serverless production application.*
