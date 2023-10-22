# Pelusa Server

![GitHub last commit (branch)](https://img.shields.io/github/last-commit/javi-aranda/pelusa-server/master)
[![Build and test](https://github.com/javi-aranda/pelusa-server/actions/workflows/test.yaml/badge.svg)](https://github.com/javi-aranda/pelusa-server/actions/workflows/test.yaml)


## Description
Pelusa (Predictive Engine for Legitimate & Unverified Site Assessment) is a machine learning
based application that predicts the legitimacy of a website based on the URL provided. It is
built using FastAPI and PostgreSQL, deployed with Docker Compose.

## Installation
To get started, clone the repository and run with Docker Compose.

```bash
git clone https://github.com/javi-aranda/pelusa-server
cd pelusa-server
docker-compose up  # add flag -d to run detached
docker-compose exec -T backend alembic upgrade head  # run SQLAlchemy migrations
```

That should run the application on [http://localhost:8000](http://localhost:8000).

## Usage
You can get a more detailed reference of the API by visiting [http://localhost:8000/docs](http://localhost:8000/docs).
But mainly it consists of an endpoint `api/v1/analysis` that accepts JSON body with `{"input": "<URL_TO_CHECK>"}`
and returns the legitimacy of the website (1 means potentially bad, 0 means potentially safe).

Those results are stored in a PostgreSQL database, which could be useful to train the model in a future
or as persistence mechanism in case an URL is submitted multiple times in a short period of time.

## Dataset
The dataset used for training the model is handmade, it consists on 30000 URLs, 50% legitimate and 50% malicious.

Malicious websites were randomly sampled from [PhishTank active threats](http://data.phishtank.com/data/online-valid.csv)
and legitimate URLs were sampled from multiple [Kaggle datasets](https://www.kaggle.com/search?q=urls+in%3Adatasets).
After extracting features for both types, the resulting dataset is [phishing_dataset.csv](https://github.com/javi-aranda/pelusa-server/blob/master/backend/app/ml/data/phishing_dataset.csv)

## Training
The model is trained using a Random Forest Classifier with an accuracy of 94% over the training dataset
and the code is available as a Jupyter Notebook in [train.ipynb](https://github.com/javi-aranda/pelusa-server/blob/master/backend/app/ml/notebooks/train.ipynb)

## Credits

This project was made keeping in mind [FastAPI Starter](https://github.com/gaganpreet/fastapi-starter) as a reference,
but bundling the frontend in a different repository, which is available in [Pelusa React](https://github.com/javi-aranda/pelusa-react).
