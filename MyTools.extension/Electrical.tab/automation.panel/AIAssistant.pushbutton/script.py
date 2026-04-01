# -*- coding: utf-8 -*-
from pyrevit import script, forms, revit, DB
import requests
import json

doc = revit.doc
output = script.get_output()
output.set_title("BIM AI Assistant")
output.print_md("# BIM AI Assistant")
output.print_md("---")

# 1. STEP: COLLECT LIVE DATA FROM REVIT (The AI's Context)
electrical_panels = DB.FilteredElementCollector(doc)\
                      .OfCategory(DB.BuiltInCategory.OST_ElectricalEquipment)\
                      .WhereElementIsNotElementType()\
                      .ToElements()

# Convert collected data into a readable string for the AI prompt
model_context = "Current Electrical Panels and Loads in the Revit Model:\n"

for panel in electrical_panels:
    panel_name = panel.Name
    load_param = panel.LookupParameter("Total Connected Load")
    
    if load_param:
        load_value = round(load_param.AsDouble(), 2)
        model_context += "- Panel: {}, Total Load: {} VA\n".format(panel_name, load_value)

# 2. STEP: LOCAL LLM COMMUNICATION FUNCTION
def ask_ai(user_command, context_data):
    #! Default endpoint for local Ollama server 
    api_url = "http://localhost:11434/api/generate"
    
    # 3. STEP: PROMPT ENGINEERING (Context Injection)    
    system_prompt = "You are an expert Electrical and BIM Engineering assistant. Use the provided Revit model data to answer the user's question accurately and professionally. Do not hallucinate or make up information outside of the provided data.\n\n"
    
    final_prompt = system_prompt + context_data + "\nUser Question: " + user_command
    
    payload = {
        "model": "llama3", 
        "prompt": final_prompt,
        "stream": False
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(api_url, data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            return response.json().get("response", "No response received.")
        else:
            return "API Error: (HTTP Status Code: {})".format(response.status_code)
    except Exception as e:
        return "Connection Error: Local LLM (e.g., Ollama) is not running or accessible. Details: " + str(e)

# 4. STEP: USER INTERFACE AND EXECUTION
user_command = forms.ask_for_string(
    default="Which panels are currently overloaded?",
    prompt="Enter your engineering command or question:",
    title="BIM AI Assistant"
)

if user_command:
    output.print_md("**Your Command:** {}".format(user_command))
    output.print_md("*Analyzing Revit data and querying AI...*")
    
    # Inject both the user command and the live Revit data into the LLM
    ai_response = ask_ai(user_command, model_context)
    
    output.print_md("---")
    output.print_md("**🤖 AI Response:**")
    output.print_md(ai_response)
else:
    output.print_md("*Operation cancelled or empty command provided.*")