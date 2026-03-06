import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

def load_process_data(path):
    df = pd.read_csv(path)
    required = ["volume_cm3", "surface_area_cm2", "tolerance_mm",
                "material_strength", "material_density", "process_label"]
    for col in required:                                                #Validating presence of required columns in CSV
        if col not in df.columns:
            raise ValueError(f"Missing column '{col}' in process CSV.")
    return df.copy()


def train_process_model(df):
    X = df[["volume_cm3", "surface_area_cm2", "tolerance_mm",
            "material_strength", "material_density"]].astype(float)         #defining feature matrix and target vector
    y = df["process_label"].astype(str)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=150, random_state=42)                   #Using Random Forest Classifier with 150 trees for better accuracy
    model.fit(X_train, y_train)                                         #Training the model, and then evaluating on test set
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Process model trained. Test accuracy: {acc:.3f}")             #Printing model accuracy on test set for the user to know
    return model


def prompt_part_specs():
    def prompt_float(name, min_val=None):                   #using a nested function to prompt for float inputs with validation so that it is easier
        while True:                                 #to call as long as a valid input is given
            try:
                s = input(f"\nEnter {name}: ").strip()
                val = float(s)
                if min_val is not None and val < min_val:
                    print(f"{name} must be >= {min_val}. Try again.")
                    continue
                return val
            except ValueError:
                print("Please enter a numeric value.")

    volume = prompt_float("Part volume (cm^3)", min_val=0.0001)                 #Prompting user for part specifications using previoulsy defined UDF
    surface_area = prompt_float("Surface area (cm^2)", min_val=0.0)
    tolerance = prompt_float("Tolerance (mm)", min_val=0.0)
    qty = int(prompt_float("Quantity (integer)", min_val=1))
    return {
        "volume_cm3": volume,
        "surface_area_cm2": surface_area,
        "tolerance_mm": tolerance,
        "quantity": qty
    }


def predict_processes(model, specs):
    X = pd.DataFrame([{                                                 #Creating a dataframe from user input specifications for prediction
        "volume_cm3": specs["volume_cm3"],
        "surface_area_cm2": specs["surface_area_cm2"],
        "tolerance_mm": specs["tolerance_mm"],
        "material_strength": specs["material_strength_MPa"],
        "material_density": specs["material_density_g_cm3"],
    }])
    proba = model.predict_proba(X)[0]                                   #Predicting process probabilities using the trained model
    classes = model.classes_                                            #Getting the class labels
    pairs = list(zip(classes, proba))                                   #Zipping class labels with their corresponding probabilities
    pairs_sorted = sorted(pairs, key=lambda x: x[1], reverse=True)      #Sorting the pairs based on probabilities in descending order
    predicted_process, confidence = pairs_sorted[0]                     #Getting the process with highest probability and its confidence
    all_probs = {name: float(prob) for name, prob in pairs_sorted}      #Creating a dictionary of all process probabilities
    print(f"\nPredicted process: {predicted_process} (confidence {confidence:.3f})")
    return {"predicted_process": predicted_process, "confidence": float(confidence), "all_probs": all_probs}


def plot_process_probabilities(proc_result, out_path):
    probs = proc_result["all_probs"]                       #Plotting the process prediction probabilities as a horizontal bar chart
    names = list(probs.keys())
    vals = [probs[n] for n in names]

    plt.figure(figsize=(10, 10))
    plt.barh(names, vals, color="C8")
    plt.xlabel("Probability")
    plt.title("Process prediction probabilities")
    plt.xlim(0, 1)
    for i, v in enumerate(vals):
        plt.text(v + 0.01, i, f"{v:.2f}", va="center")          #Adding text labels to each bar indicating the probability value
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)                                 #Saving the plot to the specified output path
    plt.show()
    plt.close()
