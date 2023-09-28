# Pelusa Server

## Description
Pelusa (Predictive Engine for Legitimate & Unverified Site Assessment) is a machine learning
based application that predicts the legitimacy of a website based on the URL provided. It is
built using FastAPI and PostgreSQL, deployed with Docker Compose.

## Installation
To get started, clone the repository and run with Docker Compose.

```bash
git clone
cd pelusa-server
docker-compose up
```

That should run the application on [http://localhost:8000](http://localhost:8000).

## Usage
You can get a more detailed reference of the API by visiting [http://localhost:8000/docs](http://localhost:8000/docs). But mainly it consists of an endpoint `api/v1/analysis` that accepts an URL and returns the legitimacy of the website (1 means bad, 0 means good).

Those results are stored in a PostgreSQL database.

## Dataset
The dataset used for training the model is handmade and available under the path `backend/app/ml/data/phishing_dataset.csv` 

## Training
The model is trained using a Random Forest Classifier with an accuracy of 94% and is available as a Jupyter Notebook under the path `backend/app/ml/train.ipynb`.

## Credits

This project was made keeping in mind [FastAPI Starter](https://github.com/gaganpreet/fastapi-starter) as a reference, but bundling the frontend in a different repository, which is available in [Pelusa React](https://github.com/javi-aranda/pelusa-react).

