import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report
import warnings
from imblearn.combine import SMOTETomek
import mlflow
import mlflow.sklearn
import mlflow.xgboost
warnings.filterwarnings('ignore')
# Step 1: Create an imbalanced binary classification dataset
X, y = make_classification(n_samples=1000, n_features=10, n_informative=2, n_redundant=8, weights=[0.9, 0.1], flip_y=0, random_state=42)

np.unique(y, return_counts=True)
# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)
#Handle class imbalance
smt = SMOTETomek(random_state=42)
X_train_res, y_train_res = smt.fit_resample(X_train, y_train)
np.unique(y_train_res, return_counts=True)
#Track Experiments
models = [
    (
        "Logistic Regression", 
        {"C": 1, "solver": 'liblinear'},
        LogisticRegression(), 
        (X_train, y_train),
        (X_test, y_test)
    ),
    (
        "Random Forest", 
        {"n_estimators": 30, "max_depth": 3},
        RandomForestClassifier(), 
        (X_train, y_train),
        (X_test, y_test)
    ),
    (
        "XGBClassifier",
        {"use_label_encoder": False, "eval_metric": 'logloss'},
        XGBClassifier(), 
        (X_train, y_train),
        (X_test, y_test)
    ),
    (
        "XGBClassifier With SMOTE",
        {"use_label_encoder": False, "eval_metric": 'logloss'},
        XGBClassifier(), 
        (X_train_res, y_train_res),
        (X_test, y_test)
    )
]
reports = []

for model_name, params, model, train_set, test_set in models:
    X_train = train_set[0]
    y_train = train_set[1]
    X_test = test_set[0]
    y_test = test_set[1]
    
    model.set_params(**params)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)
    reports.append(report)
# Initialize MLflow
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("Anomaly_Detection")

for i, element in enumerate(models):
    model_name = element[0]
    params = element[1]
    model = element[2]
    report = reports[i]
    
    with mlflow.start_run(run_name=model_name):        
        mlflow.log_params(params)
        mlflow.log_metrics({
            'accuracy': report['accuracy'],
            'recall_class_1': report['1']['recall'],
            'recall_class_0': report['0']['recall'],
            'f1_score_macro': report['macro avg']['f1-score']
        })  
        
        if "XGB" in model_name:
            mlflow.xgboost.log_model(model, "model")
        else:
            mlflow.sklearn.log_model(model, "model")
import mlflow
import mlflow.xgboost

# Register the Model
model_name = 'XGB-Smote'
run_id = input('Enter Run ID:')  # Make sure this is a valid run ID
artifact_path = 'model'  # This should match the path used during log_model()

# Correct model_uri using the actual artifact path
model_uri = f'runs:/{run_id}/{artifact_path}'

# Register the model
result = mlflow.register_model(
    model_uri=model_uri,
    name=model_name
)

# Load the Model
model_version = 1  # Make sure this version exists
model_uri = f"models:/{model_name}/{model_version}"

# Load the model using MLflow's XGBoost loader
loaded_model = mlflow.xgboost.load_model(model_uri)

# Predict (assuming X_test is already defined)
y_pred = loaded_model.predict(X_test)
print(y_pred[:4])

#Transition the Model to Production
current_model_uri = f"models:/{model_name}@challenger"
production_model_name = "anomaly-detection-prod"

client = mlflow.MlflowClient()
client.copy_model_version(src_model_uri=current_model_uri, dst_name=production_model_name)

# Load the Model
model_version = 1
prod_model_uri = f"models:/{production_model_name}@champion"

loaded_model = mlflow.xgboost.load_model(prod_model_uri)
y_pred = loaded_model.predict(X_test)
print(y_pred[:4])
