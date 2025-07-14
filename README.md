🚀 MLflow

This repository contains example scripts demonstrating various features of MLflow — an open-source platform for managing the complete machine learning lifecycle.

📁 Project Structure

├── 📂 mlruns/                          # MLflow tracking folder (auto-generated)
├── 📄 MLflow.py                       # Basic MLflow example
├── 📄 MLflow_model_registry and model_registration.py  # Model registry usage
└── 📄 MLflow_multiple_experiments.py  # Multiple experiments management

📄 File Descriptions

MLflow.py

🔹 A simple example demonstrating how to use MLflow to log parameters, metrics, and artifacts.

MLflow_model_registry and model_registration.py

🗃️ Shows how to register and version models using MLflow’s Model Registry feature.

MLflow_multiple_experiments.py

🧪 Demonstrates how to create and manage multiple MLflow experiments within your workflow.

⚙️ Requirements

Python ≥ 3.6

MLflow

(Other dependencies may be required depending on your scripts.)

Install MLflow using:

pip install mlflow

▶️ How to Run

python MLflow.py

python "MLflow_model_registry and model_registration.py"

python MLflow_multiple_experiments.py

📌 Notes

The mlruns/ directory will be created automatically by MLflow to store local experiment metadata.

For advanced usage (e.g. remote tracking server or model registry), configure your environment as per the MLflow docs.

📚 References

🔗 MLflow Official Documentation
