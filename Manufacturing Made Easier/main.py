import os

from material_module import (
    prompt_material_constraints,
    load_material_data,
    train_material_model,
    predict_materials,
    display_top_materials,
)
from process_module import (
    prompt_part_specs,
    load_process_data,
    train_process_model,
    predict_processes,
    plot_process_probabilities,
)
from cost_module import (
    calculate_mass_kg,
    estimate_total_cost,
    display_cost_breakdown,
    save_cost_breakdown,
    PROCESS_COST_MAP,
)



def prompt_select_material(top3_df):                
    while True:                               #Prompting user to select one of the top 3 recommended materials, using try except and an infinite loop until we get a valid value.
        try:
            choice = input("Select material to use (1, 2 or 3): ").strip()
            if choice not in ("1", "2", "3"):
                print("Please enter 1, 2, or 3.")
                continue
            id = int(choice) - 1
            selected = top3_df.iloc[id]
            return selected
        except Exception as e:
            print("Invalid choice:", e)



def main():
    OUTPUT_DIR = "output"
    os.makedirs(OUTPUT_DIR, exist_ok=True)                  #Creating output directory if it doesn't exist, so that I can store the process probability plots there
    print("====== Manufacturing Made Easier (Material, Process, and Cost Estimator) ======")        
    #collecting user constraints for material selection
    constraints = prompt_material_constraints()
    #loading material data and training material selection model
    mat_df = load_material_data("data/materials.csv")
    mat_model = train_material_model(mat_df)
    #predicting materials based on user constraints and displaying the top recommendations
    mat_predictions = predict_materials(mat_model, mat_df, constraints)
    if mat_predictions.empty:
        print("\nNo materials found even after relaxation. Please try again with different constraints.")   #handling case where no materials are found even after constraint relaxation
    else:
        display_top_materials(mat_predictions)
        #prompting user to select one of the top 3 materials and then printing the selected material and its properties
        top3 = mat_predictions.head(3)
        selected_material = prompt_select_material(top3)
        print("\nSelected material:")
        print(selected_material.to_string())
        #collecting part specifications from user and adding material properties to it
        part_specs = prompt_part_specs()
        part_specs["material_name"] = selected_material["name"]
        part_specs["material_density_g_cm3"] = float(selected_material["density_g_cm3"])
        part_specs["material_strength_MPa"] = float(selected_material["yield_strength_MPa"])
        part_specs["material_cost_usd_per_kg"] = float(selected_material["cost_usd_per_kg"])
        #loading process data, training process model, predicting processes for the part, and plotting the process probabilities
        proc_df = load_process_data("data/process_train.csv")
        proc_model = train_process_model(proc_df)
        proc_result = predict_processes(proc_model, part_specs)
        proc_plot_path = os.path.join(OUTPUT_DIR, "process_probabilities.png")
        plot_process_probabilities(proc_result, proc_plot_path)
        #calculating mass, costs, and displaying & saving cost breakdown
        mass_kg = calculate_mass_kg(part_specs["volume_cm3"], part_specs["material_density_g_cm3"])
        process_name = proc_result["predicted_process"]
        material_cost_per_part = part_specs["material_cost_usd_per_kg"] * mass_kg
        process_cost_per_part = PROCESS_COST_MAP.get(process_name, PROCESS_COST_MAP["Other"])
        total_cost = estimate_total_cost(material_cost_per_part, process_cost_per_part, part_specs["quantity"])
        display_cost_breakdown(
            selected_material["name"],
            process_name,
            part_specs["quantity"],
            mass_kg,
            material_cost_per_part,
            process_cost_per_part,
            total_cost
        )
        out_report_path = os.path.join(OUTPUT_DIR, "cost_breakdown_report.txt")
        save_cost_breakdown(
            selected_material["name"],
            process_name,
            part_specs["quantity"],
            mass_kg,
            material_cost_per_part,
            process_cost_per_part,
            total_cost,
            out_report_path
        )
        #ends with a thank you message
        print("\nProcess probability chart and Cost Breakdown Report saved to output folder.")
        print("All done. Thank you for using Manufacturing Made Easier!")

if __name__ == "__main__":
    main()
