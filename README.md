# Manufacturing Made Easier

**Manufacturing Made Easier** is a Python-based **decision-support tool for manufacturing planning**.  
Given part constraints and specifications, the system recommends an **optimal material, manufacturing process, and estimated production cost**.

The project combines **machine learning models, engineering constraints, and cost analysis** to guide early-stage design decisions.

---

## Overview

The system operates through a **three-stage pipeline**:

### 1. Material Recommendation
Uses a **Decision Tree Regressor** trained on material property data to rank viable materials based on strength, density, and cost constraints.

### 2. Manufacturing Process Prediction
A **Random Forest classifier (150 trees)** predicts the most suitable manufacturing process from part geometry and material properties.

### 3. Cost Estimation
Calculates **material cost, processing cost, and total production cost** for the desired quantity.

The result is a **data-driven workflow from design requirements → manufacturable solution**.

---

## Tech Stack

**Languages & Libraries**

- Python  
- Pandas  
- Scikit-learn  
- Matplotlib  

**Machine Learning**

- Decision Tree Regression (material recommendation)  
- Random Forest Classification (process prediction)

**Engineering & Data Concepts**

- Feature engineering from material properties
- Constraint filtering and relaxation
- Model evaluation (R², MAE, classification accuracy)
- Probability visualization of model predictions
- Modular pipeline architecture

---

## Example Workflow

User inputs:

- Minimum yield strength  
- Maximum density  
- Maximum material cost  
- Part volume  
- Surface area  
- Tolerance  
- Production quantity  

The system then:

1. Filters and ranks feasible materials
2. Predicts the best manufacturing process
3. Generates a cost breakdown and process probability visualization

---

## Project Structure
Manufacturing-Made-Easier/
│
├── main.py                # main pipeline
├── material_module.py     # material recommendation model
├── process_module.py      # manufacturing process classifier
├── cost_module.py         # cost estimation logic
│
├── data/
│   ├── materials.csv
│   └── process_train.csv
│
└── output/
    ├── process_probabilities.png
    └── cost_breakdown_report.txt

---

## Running the Project

Clone the repository:
git clone https://github.com/ChampCNV/Manufacturing-Made-Easier.git
cd Manufacturing-Made-Easier

Install dependencies:
pip install pandas scikit-learn matplotlib

Run the program:
python main.py

Follow the CLI prompts to enter part specifications.

## Potential Extensions

- **CAD File Integration**  
  Automatically extract geometry (volume, surface area, features) directly from CAD models.

- **Expanded Manufacturing Dataset**  
  Improve model accuracy with larger real-world manufacturing process data.

- **Process Time Estimation**  
  Estimate machining or fabrication time alongside cost predictions.

- **Web-Based Interface**  
  Build a user-friendly frontend using tools like **Streamlit** or **Flask**.

- **Optimization-Based Process Selection**  
  Integrate optimization algorithms to select manufacturing methods based on cost, speed, and performance trade-offs.
