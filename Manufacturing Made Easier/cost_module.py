PROCESS_COST_MAP = {                            #Process cost per part in USD, a sample mapping based on typical industry costs
    "Sand_Casting": 7.0,            
    "Forging": 18.0,                
    "CNC_Machining": 22.0,          
    "Sheet_Metal_Forming": 10.0,    
    "Additive_Metal": 35.0,         
    "Additive_Polymer": 12.0,       
    "Welding": 8.0,                 
    "Injection_Molding": 5.0,       
    "Extrusion": 6.0,               
    "Laser_Cutting": 14.0,          
    "Composite_Layup": 30.0,        
    "Heat_Treatment": 9.0,          
    "Other": 12.0                   
}



def calculate_mass_kg(volume_cm3, density_g_cm3):
    mass = (float(volume_cm3) * float(density_g_cm3)) / 1000.0          #Calculating mass in kg from volume in cm^3 and density in g/cm^3
    return mass


def estimate_total_cost(material_cost_per_part, process_cost_per_part, quantity):
    total = (float(material_cost_per_part) + float(process_cost_per_part)) * int(quantity)          #Estimating total cost for given quantity
    return total


def display_cost_breakdown(material_name, process_name, quantity,
                           mass_per_part_kg, material_cost_per_part,
                           process_cost_per_part, total_cost):
    print("\n=== COST BREAKDOWN FOR THE PRODUCTION OF THIS PART ===")           #Printing a comprehensive cost breakdown of the cost of making the certain number of parts for the user
    print(f"Material: {material_name}")
    print(f"Mass per part (kg): {mass_per_part_kg:.4f}")
    print(f"Material cost per part: ${material_cost_per_part:.2f}")
    print(f"Process: {process_name}")
    print(f"Process cost per part: ${process_cost_per_part:.2f}")
    print(f"Quantity: {quantity}")
    print("------------------------------------------------------")
    print(f"Estimated total production cost: ${total_cost:.2f}")


def save_cost_breakdown(material_name, process_name, quantity,
                        mass_per_part_kg, material_cost_per_part,               #creating a beautifully formatted cost breakdown report to be written to a text file
                        process_cost_per_part, total_cost, out_path):
    report = f"""                                                       
========================================
        COST BREAKDOWN REPORT
========================================

PROCESS SELECTED:  {process_name}
MATERIAL SELECTED: {material_name}
QUANTITY:          {quantity} parts

========================================
        MATERIAL COST ANALYSIS
========================================
- Unit Material Cost:       ${material_cost_per_part:.2f} per kg
- Part Mass:                {mass_per_part_kg:.3f} kg
- Material Required:        {mass_per_part_kg*quantity:.3f} kg
- Material Subtotal:        ${quantity*material_cost_per_part:.2f}

========================================
        PROCESS COST ANALYSIS
========================================
- Process Cost per Part:    ${process_cost_per_part:.2f} per part
- Processing Subtotal:      ${quantity*process_cost_per_part:.2f}

========================================
              TOTAL COST
========================================
- TOTAL COST:               ${total_cost:.2f}
========================================
    """

    with open(out_path, "w") as f:                                      #Saving the cost breakdown to a text file at the specified output path
        f.write(report)
