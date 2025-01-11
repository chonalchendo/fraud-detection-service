# Product & System Design for Real-Time Fraud Detection System

# Intro

Building an ML system is a complex task that involves a mix of business requirements, data, algorithms, infrastructure, and software development. Without thorough scoping of ML product and system design which accounts for all the items listed, it can make building an ML system even harder than it has to be.

As part of my next project, to simulate a real-time fraud detection system, I need to first scope of what the system is, why I am building it, and how I am going to build it. This will provide a reference for my project so I don't end up going down endless rabbit-holes, and keep me focused on building something within the parameters I've set out below.

To develop the product and system requirements, I am using ML product template, create by _Goku Mohandas, creator of [Made With ML](https://madewithml.com/)_. You can find a template copy [here](https://madewithml.com/static/templates/ml-canvas.pdf).

# Product Design

Before building our ML system, we need to scope out _what_ it will be and _why_ we are building it. This involves gathering business requirements and formulating a plan that gives the system the best chance of success.

## Background

_Describe the customer's goals and pains_

For this project, lets say we have been consulted to build a fraud detection system for the fictitious digital payments company called `Nexus Pay`. They are currently missing a high number of fraudulent payments and need a real-time system to quickly detect and flag these payments before the transactions are incorrectly confirmed.

`users`: fraud analysts needing to make quick and accurate decisions on suspicious activity
`goals`: detect and prevent fraudulent transactions before they cause losses
`pains`: high volume of transactions overwhelming the fraud team

## Value Proposition

_Propose the product with the value it creates and the pains it alleviates_

We will build a platform that helps the `Nexus Pay` fraud team detect and flag fraudulent transactions in real-time. This will done by streaming customer transactions and classifying whether the transaction is fraud or not.

`product`: a services that increases the number of fraudulent transactions detected and flagged
`alleviates`: catches fraud in real-time resulting in reduced financial loses
`advantages`: increased customer trust and loyalty through better fraud protection, and providing fraud teams with data driven insight into fraud patterns and trends

## Objectives

_Breakdown the product into key objectives that need to be delivered_

Our key objectives for system include:

- Classify incoming transactions as fraud or not.
- Deny fraudulent transactions in real-time
- Provide an alert system to notify fraud analysts in real-time

## Solution

_Define the solution, including features, integration, constraints, and what's out-of-scope_

`core features`:

- provide real-time binary fraud prediction for each transaction
- model re-training pipeline to adjust to data drift

`integrations`:

- Data dump of `Nexus Pay` transactions

`alternatives`:

- rules based detection system (non-ML solution)

`constraints`:

- maintain low latency (>100ms) for incoming transactions
- customer data privacy (GDPR)

`out of scope`:

- credit risk assessment

## Feasibility

_Discuss the feasibility of the solution and if we have the required resources_

Feasibility is an assessment of whether we have the right resources including data, skillset and infrastructure. In this case, we have data taken from Kaggle and further exploration is needed to see if there is enough signal in the data, and what techniques may need to be applied extra the signal from the noise.

Data sample:

```json
    {
        'trans_date_trans_time': '2019-01-01 00:00:18',
        'customer_id': 'CUST_f198489bae4db7c3'
        'cc_num': 2703186189652095,
        'merchant': 'fraud_Rippin, Kub and Mann',
        'category': 'misc_net',
        'amt': 4.97,
        'first': 'Jennifer',
        'last': 'Banks',
        'gender': 'F',
        'street': '561 Perry Cove',
        'city': 'Moravian Falls',
        'state': 'NC',
        'zip': 28654,
        'lat': 36.0788,
        'long': -81.1781,
        'city_pop': 3495,
        'job': 'Psychologist, counselling',
        'dob': '1988-03-09',
        'trans_num': '0b242abb623afc578575680df30655b9',
        'unix_time': 1325376018,
        'merch_lat': 36.011293,
        'merch_long': -82.048315,
    }
```

# System Design

Now we know the what and the why, we can start to design our ML system to answer _how_ we will build our solution.

![[fraud_detection_system_design.png]]

The system diagram above shows a rough outline of how this system will be deployed (the diagram will likely be subject to change as the project evolves).

## Data

_Identify the training and production data sources, as well as the labelling process and decisions_

The dataset used is the _[Credit Card Transactions Fraud Detection Dataset](https://www.kaggle.com/datasets/kartik2112/fraud-detection/data)_ found on Kaggle, which was generated using the _[Sparkov Data Generation](https://github.com/namebrandon/Sparkov_Data_Generation)_ GitHub repository

The data is split into:

- `fraudTrain.csv`
- `fraudTest.csv`

For the purpose of this exercise, the `fraudTrain.csv` data will be split into the `train`, `validation`, & `test` sets. The `fraudTest.csv` data will be used as the production data which will simulate real-time transactions being streamed into the system.

`training`:

- `fraudTrain.csv` used as `train`, `validation` & `test` data in the initial model training
- the data has been generated from a fraud data simulator

`production`:

- `fraudTest.csv` used as the `production` data source to simulate real-time data ingestion and model prediction

`labels`:

- binary variable indicating whether the transaction is fraudulent (0 for no fraud, 1 for fraud)

`features`:

- combination of numeric and text features that describe the transaction made including location, customer details, and transaction type

# Metrics

_Prioritise key metrics that reflect the objectives_

A metric needs to be chosen that suits our problem. Given that fraudulent transactions are rare, that means our dataset will be imbalanced. Metrics like `accuracy` are useless as if they just predicted every transaction as not fraudulent then an accuracy of 99.9% would be achieved.

The `confusion matrix` is a common way to evaluate classification model performance:

- **True Positive (TP):** correctly identified fraud transaction
- **False Positive (FP):** legitimate transaction _incorrectly_ flagged as fraud
- **True Negative (TN):** correctly identified legitimate transaction
- **False Negative (FN):** fraudulent transaction _incorrectly_ flagged as legitimate

|                        | **Actual Positive** | **Actual Negative** |
| ---------------------- | ------------------- | ------------------- |
| **Predicted Positive** | True Positive       | False Positive      |
| **Predicted Negative** | False Negative      | True Negative       |

Based on the `confusion matrix` we can derive the following metrics:

- **Precision** = TP / (TP + FP)
- **Recall** = TP / (TP + FN)
- **F1** = 2 x (Precision \* Recall) / (Precision + Recall)
- **False Positive Rate** = FP / (FP[+]TN)

Precision tells us the proportion of fraudulent transactions we predicted as fraud. Recall measures the proportion of fraud cases we caught. F1 score provides a balance between precision and recall which is ideal for this system as we want a metric that reflects our accuracy of predicting fraudulent transactions, but also catching as many of them as possible.

# Evaluation

_Design offline and online evaluation criteria_

### Offline Evaluation

Offline evaluation refers to model performance during model training and re-training. Our initial model training will have a holdout set taken from `fraudTrain.csv`.

To evaluate the feature performance we can use SHAP and feature importances visualisations.

### Online Evaluation

Online evaluation refers to how our model performs in production. We need to evaluate transactions predicted as fraud versus whether they actually were fraud. In reality, fraud systems only know if the transaction is fraudulent until a customers complain of unauthorised transactions or further investigation into flagged transactions.

Some steps to evaluate the systems performance could include:

- manually investigating flagged transactions
- monitor customer complaints related to transactions
- send customers emails notifying of transaction made and ask to validate it

However, in this scenario we already have the fraud labels for production data, therefore we can have a running F1 score and false positive rate.

The adapt the system to data drift and performance degradation, new models will be deployed to a _shadow server_ where production traffic will be sent to both models and allow for direct evaluation between them.

As we have a latency requirement of 200ms, we need to evaluate the historical model latency performance.

# Modelling

_List the iterative approach to model the task_

The general modelling approach I want to take it as follows:

1. Explore the data for insight
2. Engineer new features relevant to the task
3. Develop a baseline model to iterate from
4. Predict fraud labels from these features
5. Tune hyperparamters on validation set
6. Evaluate model using offline metrics, SHAP and feature importances
7. Evaluate model in production (if not first model)

`assumption`: ML will be difficult to use given small percentage of fraudulent transactions

`reality`: Data resampling techniques will be needed for our model to learn patterns in the data

`reason`: ML models do not deal with class imbalance well so proper preparation is needed for our modelling framework to be successful

# Inference

_Decide whether we want to do batch (offline) or real-time (online) inference_

Our client `Nexus Pay` need _real-time_ (online) predictions of fraudulent activity so that they can limit financial losses to their customers as quickly as possible.

![[Online Fraud Detection System 1.png]]

The above diagram is a high-level outline of how the online fraud detection system will work.

1. The customer creates a transaction
2. A request is then made from `Nexus Pay` software to the fraud prediction service to predict whether the transaction is fraudulent
3. The real-time data transport (e.g. Kafka) asynchronously sends the customers information to the prediction service and to the data warehouse where the features can be used in future model training and batch feature calculation
4. Pre-computed batch features (e.g. historical spending patterns or merchant fraud rate) are stored in cache (e.g. Redis) for quick retrieval
5. The batch and real-time data are joined together at inference time to return the fraud prediction to the customer
6. The customer gets a transaction approved or denied notification

# Feedback

_Outline sources of feedback from our system to use for iteration_

To gain feedback on model performance we need to setup a robust monitoring service.

**Offline feedback methods:**

- _Model registry_ to log model metadata so allow for easy comparison of experiment performances
- _Data validation_ to create a gold standard holdout set to continually evaluate and have confidence in model re-training.

**Production Feedback methods:**

- _Data drift_ to monitor feature distribution changes
- _Shadow deployment_ to monitor understand how new models will perform in production
- _Alert system_ to notify engineers of fraud transactions
- _Customer complaints_ to monitor any feedback on `Nexus Pay's` ability to catch fraud.

# Summary

This has been a comprehensive overview of my fraud detection ML product, designed to provide real-time fraud predictions for transaction of the fictitious digital payments company, `Nexus Pay`. The ML product template created by `Goku Mohandas` provides an excellent starting point for building ML systems, and challenges you to think about the _what_ and _why_ you are creating this product, and finally _how_ you're going to build it.

To recap the **product design** (what & why):

- **Background:** `Nexus Pay` currently miss a large number of fraudulent transactions and need a system to detect and flag these transactions before being incorrectly confirmed
- **Value Proposition:** To build a real-time fraud detection system that will aid the fraud team in detecting and flagging fraudulent transactions quickly.
- **Objectives:** To screen incoming transaction for fraud, deny if fraudulent, and provide an alert system to fraud team when a fraudulent transaction is made.
- **Solutions:** Provide real-time fraud predictions, and re-train the model frequently to update to evolving data patterns.
- **Feasibility:** We have the feasibility as the data is taken from Kaggle and has been used as source to practice ML for fraud detection.

To recap the **system design** (how):

- **Data:** The `fraudTrain.csv` data will be used for initial model training, validation, and testing. Whereas, `fraudTest.csv` will be used to mimic production data which is streamed in real-time.
- **Metrics:** We will use F1 to score model performance as it provides a tradeoff between precision (correct fraud predictions divided by total fraud prediction made) and recall (proportion of fraud cases predicted correctly).
- **Evaluation:** Offline evaluation will be done with a holdout test set, and features analysed using SHAP and feature importances. Online evaluation includes a running F1 score, model latency monitoring, and shadow server deployment for new model iterations.
- **Modelling:** Explore data -> generate features -> develop baseline model -> predict fraud labels -> tune hyperparameters -> evaluate using offline metrics and shadow deploy to test in production.
- **Inference:** Real-time (online) inference is vital to meet `Nexus Pay's` requirements of prediction on a case by case basis.
- **Feedback:** Offline feedback includes logging of model metadata to track model performance over time and data validation. Online feedback includes data drift monitoring, shadow deployment, and monitoring customer complaints.
