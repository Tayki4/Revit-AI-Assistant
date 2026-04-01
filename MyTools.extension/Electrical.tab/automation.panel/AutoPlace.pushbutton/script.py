# -*- coding: utf-8 -*-
from pyrevit import revit, DB, UI

# Get the active document
doc = revit.doc

# 1. Collect all Rooms in the project
rooms = DB.FilteredElementCollector(doc)\
          .OfCategory(DB.BuiltInCategory.OST_Rooms)\
          .ToElements()

# Stop the script if no rooms exist
if not rooms:
    UI.TaskDialog.Show("Error", "No rooms found in the current project.")
    import sys
    sys.exit()

# 2. Collect an Electrical Fixture to place
# We grab the first available family symbol (type) in the Electrical Fixtures category
symbols = DB.FilteredElementCollector(doc)\
            .OfCategory(DB.BuiltInCategory.OST_ElectricalFixtures)\
            .OfClass(DB.FamilySymbol)\
            .ToElements()

if not symbols:
    UI.TaskDialog.Show("Error", "No electrical fixture families loaded.")
    import sys
    sys.exit()

symbol_to_place = symbols[0]

# 3. Start the Database Transaction (Crucial for writing data)
t = DB.Transaction(doc, "Auto-Place Elements in Rooms")
t.Start()

# A symbol must be active in the document before placing an instance of it
if not symbol_to_place.IsActive:
    symbol_to_place.Activate()

placed_count = 0

# 4. Iterate through rooms, calculate the center, and place the element
for room in rooms:
    # Get the bounding box of the room to calculate its geometric center
    bbox = room.get_BoundingBox(None)
    
    if bbox:
        # Calculate X and Y center points
        center_x = (bbox.Min.X + bbox.Max.X) / 2.0
        center_y = (bbox.Min.Y + bbox.Max.Y) / 2.0
        center_z = bbox.Min.Z # Z coordinate (Floor level)
        
        # Create a Revit XYZ point object
        center_point = DB.XYZ(center_x, center_y, center_z)
        
        # Place the family instance at the calculated center point
        doc.Create.NewFamilyInstance(center_point, symbol_to_place, DB.Structure.StructuralType.NonStructural)
        
        placed_count += 1

# 5. Commit the Transaction to save changes to the model
t.Commit()

# 6. Display Success Message
UI.TaskDialog.Show("Success", "Successfully placed {} elements at room centers.".format(placed_count))