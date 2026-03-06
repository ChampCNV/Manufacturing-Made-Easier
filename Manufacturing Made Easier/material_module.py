import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

def prompt_material_constraints():
    while True:
        try:                                                                            #User input with validation, using try except blocks
            strength = float(input("Enter minimum required yield strength (MPa): "))
            if strength <= 0:
                print("Strength must be greater than 0.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    while True:
        try:
            density = float(input("Enter max allowable density (g/cm^3): "))
            if density <= 0:
                print("Density must be greater than 0.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    while True:
        try:
            cost = float(input("Enter maximum cost ($/kg): "))
            if cost <= 0:
                print("Cost must be greater than 0.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    return {                                #Returning constraints as a dictionary
        "target_strength": strength,
        "max_density": density,
        "max_cost": cost
    }



def load_material_data(path):
    df = pd.read_csv(path)
    required = ["name", "density_g_cm3", "yield_strength_MPa", "cost_usd_per_kg",
                "corrosion_rating", "success_score"]
    for col in required:                                        #Checking for required columns in the CSV
        if col not in df.columns:
            raise ValueError(f"Missing column '{col}' in materials CSV.")
    return df.copy()                            #Returning a copy of the dataframe             



def train_material_model(df):
    features = df[["density_g_cm3", "yield_strength_MPa", "cost_usd_per_kg",
                   "corrosion_rating"]].astype(float)                               #Defining features and target variable for model training
    target = df["success_score"].astype(float)

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)       #splits data into train and test
    model = DecisionTreeRegressor(max_depth=5, random_state=42)                     #Creating a decision tree regressor model   
    model.fit(X_train, y_train)                         #Training the decision tree regressor model on training data

    preds = model.predict(X_test)                   #Making predictions on test data
    metrics = {
        "r2": float(r2_score(y_test, preds)),
        "mae": float(mean_absolute_error(y_test, preds))
    }
    print(f"Material model trained. \nR2={metrics['r2']:.3f}(Higher = Better), \nMAE={metrics['mae']:.3f}(Lower = Better)")      #Printing model performance metrics, for user to know accuracy of Model
    return model


def predict_materials(model, df, constraints):
    relaxation_round = 0
    print("\nSearching for materials that meet your constraints... \nConstraints will be relaxed by 10% per round of relaxing the constraints, if no materials meet your constraints.")
    while True:
        #only materials meeting constraints remain
        df = df[
            (df["yield_strength_MPa"] >= constraints["target_strength"]) &
            (df["density_g_cm3"] <= constraints["max_density"]) &
            (df["cost_usd_per_kg"] <= constraints["max_cost"])
            ]

        #If at least one material matches, don't relax constraints
        if not df.empty:
            break

        #If no materials found, then relax constraints

        # asking the user to reconsider their constraints if too many relaxations have occurred
        if relaxation_round > 12:   # roughly 12 relax cycles, should be enough, and if it isnt, the constraints are too tight
            return pd.DataFrame([])  # return empty datafame to indicate no filtering possible, and constraints are too tight
        else:
            relaxation_round += 1
            print(f"Relaxing Constraints -- Round {relaxation_round}...")
            #Relaxation rules
            constraints["target_strength"] *= 0.9       # reduce strength by 10%
            constraints["max_density"] *= 1.1           # increase density by 10%
            constraints["max_cost"] *= 1.1              # increase cost by 10%

    if 12 > relaxation_round > 0:     # Inform user of final relaxed values, if it happens within 12 cycles
            print("\n Constraints relaxed to allow valid materials:")
            print(f"  Final target strength: {constraints["target_strength"]:.2f} MPa")
            print(f"  Final max density:     {constraints["max_density"]:.2f} g/cm³")
            print(f"  Final max cost:        ${constraints["max_cost"]:.2f}/kg")
    
    # Scoring remaining materials with the trained model
    rows = []
    for _, row in df.iterrows():
        # Calculating heuristic scores based on constraints for qualitative aspect of analysis and material recommendation
        # Strength score
        s_strength = min(row["yield_strength_MPa"] / max(1.0, constraints.get("target_strength", 1.0)), 1.0)
        # Cost score
        s_cost = 1 - min(row["cost_usd_per_kg"] / max(1.0, constraints.get("max_cost", row["cost_usd_per_kg"])), 1.0)
        # Density score
        dens_min = df["density_g_cm3"].min()
        dens_max = df["density_g_cm3"].max()
        if dens_max - dens_min > 0:
            s_density = 1 - (row["density_g_cm3"] - dens_min) / (dens_max - dens_min)
        else:
            s_density = 0.5

        # Predicting quantitative score using the trained decision tree regressor model
        X = pd.DataFrame([{
            "density_g_cm3": row["density_g_cm3"],
            "yield_strength_MPa": row["yield_strength_MPa"],
            "cost_usd_per_kg": row["cost_usd_per_kg"],
            "corrosion_rating": row["corrosion_rating"]
        }])
        predicted = model.predict(X)[0]

        # Combining quantitative and qualitative scores for final material recommendation
        heuristic = ((s_strength + s_cost + s_density) / 3.0)*100
        combined_score = 0.7 * predicted + 0.3 * (heuristic)

        rows.append({
            "name": row["name"],
            "density_g_cm3": row["density_g_cm3"],
            "yield_strength_MPa": row["yield_strength_MPa"],
            "cost_usd_per_kg": row["cost_usd_per_kg"],
            "corrosion_rating": row["corrosion_rating"],
            "predicted_score": combined_score,
            "quantitative_analysis_score": predicted,
            "qualitative_analysis_score": heuristic
        })

    out = pd.DataFrame(rows)
    out = out.sort_values("predicted_score", ascending=False).reset_index(drop=True) #Sorting materials by predicted score in descending order
    return out


def display_top_materials(df, n=3):
    print("\nTop recommended materials:")       #Displaying top N recommended materials, keeping n as 3 by default, but changeable as needed
    for i in range(min(n, len(df))):
        r = df.iloc[i]
        print(f"{i+1}. {r['name']} | Score: {r['predicted_score']:.1f} | Cost: ${r['cost_usd_per_kg']}/kg | Density: {r['density_g_cm3']} g/cm3")
