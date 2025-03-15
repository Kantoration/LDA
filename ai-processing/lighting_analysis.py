import ezdxf
import ifcopenshell
import os

def identify_file_type(file_path):
    """Identifies if a file is AutoCAD (DXF/DWG) or Revit (IFC)."""
    if file_path.lower().endswith(".dxf") or file_path.lower().endswith(".dwg"):
        return "AutoCAD"
    elif file_path.lower().endswith(".ifc"):
        return "Revit"
    return "Unknown"

def extract_autocad_data(file_path):
    """Extracts data from AutoCAD files to check for lighting elements."""
    try:
        doc = ezdxf.readfile(file_path)
        msp = doc.modelspace()
        lighting_layers = ["LIGHTING", "FIXTURES", "ELECTRICAL"]
        
        lighting_data = []
        for entity in msp:
            if entity.dxf.layer in lighting_layers:
                lighting_data.append({
                    "type": entity.dxftype(),
                    "layer": entity.dxf.layer
                })
        
        return {"lighting_found": len(lighting_data) > 0, "details": lighting_data}
    except Exception as e:
        print(f"Error reading AutoCAD file: {e}")
        return {"lighting_found": False, "error": str(e)}

def extract_revit_data(file_path):
    """Extracts data from Revit (IFC) files to check for lighting fixtures."""
    try:
        model = ifcopenshell.open(file_path)
        lights = model.by_type("IfcLightingFixture")

        lighting_data = [{"name": light.Name, "type": light.is_a()} for light in lights]
        return {"lighting_found": len(lights) > 0, "details": lighting_data}
    except Exception as e:
        print(f"Error reading Revit file: {e}")
        return {"lighting_found": False, "error": str(e)}

def analyze_file(file_path):
    """Main function to analyze AutoCAD or Revit files for lighting schemes."""
    file_type = identify_file_type(file_path)

    if file_type == "AutoCAD":
        return extract_autocad_data(file_path)
    elif file_type == "Revit":
        return extract_revit_data(file_path)
    else:
        return {"error": "Unsupported file format"}
