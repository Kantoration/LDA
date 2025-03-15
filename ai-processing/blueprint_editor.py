import ezdxf
import ifcopenshell
import os

def modify_blueprint(file_path, parsed_command):
    """Modifies a blueprint based on an NLP command."""
    file_type = file_path.split(".")[-1].lower()
    updated_file = f"modified_{os.path.basename(file_path)}"

    if file_type in ["dxf", "dwg"]:
        modify_autocad(file_path, parsed_command, updated_file)
    elif file_type == "ifc":
        modify_revit(file_path, parsed_command, updated_file)
    
    return updated_file

def modify_autocad(file_path, parsed_command, updated_file):
    """Edits an AutoCAD DXF/DWG blueprint."""
    doc = ezdxf.readfile(file_path)
    msp = doc.modelspace()

    if parsed_command["action"] == "add" and parsed_command["object"] == "lighting fixture":
        for i in range(parsed_command["quantity"]):
            x, y = i * 2, 0  # Example positioning
            msp.add_circle((x, y), radius=0.2, dxfattribs={"layer": "LIGHTING"})

    doc.saveas(f"uploads/{updated_file}")

def modify_revit(file_path, parsed_command, updated_file):
    """Edits a Revit IFC blueprint."""
    model = ifcopenshell.open(file_path)

    if parsed_command["action"] == "add" and parsed_command["object"] == "lighting fixture":
        new_light = model.create_entity("IfcLightingFixture")
        model.add(new_light)

    model.write(f"uploads/{updated_file}")
