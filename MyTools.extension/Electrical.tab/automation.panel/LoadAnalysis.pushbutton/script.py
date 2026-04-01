# -*- coding: utf-8 -*-
from pyrevit import revit, DB, UI

# Get the active document
doc = revit.doc

# 1. Collect all electrical panels in the project
electrical_panels = DB.FilteredElementCollector(doc)\
                      .OfCategory(DB.BuiltInCategory.OST_ElectricalEquipment)\
                      .WhereElementIsNotElementType()\
                      .ToElements()

# List to store overloaded panels
overloaded_panels = []

# Define a hypothetical maximum load limit (e.g., in Volt-Amperes)
load_limit = 50000.0 

# 2. Iterate through each panel to check its load
for panel in electrical_panels:
    panel_name = panel.Name
    
    # Lookup the total connected load parameter
    load_param = panel.LookupParameter("Total Connected Load")
    
    if load_param:
        # Get the parameter value as a double (number)
        load_value = load_param.AsDouble()
        
        # 3. Check if the load exceeds our defined limit
        if load_value > load_limit:
            overloaded_panels.append("{} (Load: {})".format(panel_name, round(load_value, 2)))

# 4. Display the results in a Revit popup dialog
if overloaded_panels:
    message = "WARNING! Overloaded Panels Detected:\n\n" + "\n".join(overloaded_panels)
    UI.TaskDialog.Show("Load Analysis Report", message)
else:
    UI.TaskDialog.Show("Load Analysis Report", "All electrical panels are within safe load limits.")