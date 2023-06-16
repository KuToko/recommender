# FastAPI Based Recommendation System Deployment

This repository contains the code for deploying the recommendation system model developed using Collaborative Filtering and Natural Language Processing (NLP) techniques on a FastAPI server.

## Project Overview

This project is part of the larger KuToko app project, which helps users find nearby MSMEs that match their interests and needs. This repository specifically handles the deployment of the recommendation system model on a FastAPI server.

## Table of Contents

1. [Installation](#installation)
2. [File Descriptions](#file-descriptions)
3. [Usage](#usage)
4. [Contributing](#contributing)

## Installation

To run the server in this repository, you will need Python 3.x and the following Python libraries installed:

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [TensorFlow](https://www.tensorflow.org/)
- [Scikit-learn](https://scikit-learn.org/stable/)

You can install these packages with the following command:

```
pip install -r requirements.txt
```

Before running the server, you need to set up your environment variables. You can do this by creating a `.env` file in the root directory of the project and filling it with your configuration:

```
DB_CONNECTION=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_DATABASE=kutoko
DB_USERNAME=postgres
DB_PASSWORD=your_password
API_KEY=your_api_key
```

Replace `your_password` with your actual PostgreSQL password and `your_api_key` with your random API key.

## File Descriptions

- `main.py`: This file contains the FastAPI application.
- `saved_model/s`: This directory contains the trained recommendation system model.
- `gunicorn_conf.py`: This file contains the configuration for the Gunicorn server.
- `models.py`: This file contains the database models.

## Usage

To start the FastAPI server, navigate to the repository directory and run the following command:

```
uvicorn main:app --reload
```

This will start the server at `http://localhost:8000/`.
