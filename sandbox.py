import customtkinter as ctk
from Libraries.Stratagems.Vehicles import vehicles

class VehicleFilterPopup(ctk.CTkToplevel):
    def __init__(self, master, vehicle_filter_states, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.title("Vehicle Filter")
        self.geometry("650x500")
        self.attributes('-topmost', True)
        
        self.vehicle_filter_vars = {}  # Store variables for each checkbox
        self.vehicle_subclass_vars = {}  # Store variables for each subclass checkbox
        self.vehicle_subclass_frames = {}  # Dictionary to hold widgets for each subclass

        # Store a reference to the central state dictionary passed from the main app
        self.vehicle_checkbox_states = vehicle_filter_states

        # Create a frame to hold all subclass checkboxes
        grid_frame = ctk.CTkFrame(self)
        grid_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Track grid positions for rows and columns
        current_row = 0
        current_column = 0
        max_columns = 3  # We want 3 columns in total

        # Create sections for each subclass
        vehicle_subclasses = sorted(set(p.subclass for p in vehicles))
        
        for subclass in vehicle_subclasses:
            # Create a frame for each subclass
            vehicle_subclass_frame = ctk.CTkFrame(grid_frame)
            vehicle_subclass_frame.grid(row=current_row, column=current_column, padx=10, pady=5, sticky="nw")

            vehicle_subclass_var = ctk.BooleanVar()
            vehicle_subclass_checkbox = ctk.CTkCheckBox(
                vehicle_subclass_frame, text=subclass, variable=vehicle_subclass_var,
                command=lambda sv=vehicle_subclass_var, sf=vehicle_subclass_frame: self.toggle_vehicle_section(sv, sf)
            )
            vehicle_subclass_checkbox.pack(anchor="w")

            self.vehicle_subclass_vars[subclass] = vehicle_subclass_var
            self.vehicle_subclass_frames[subclass] = vehicle_subclass_frame

            # Add individual weapon checkboxes under the subclass
            for weapon in [p for p in vehicles if p.subclass == subclass]:
                vehicle_weapon_var = ctk.BooleanVar()
                vehicle_weapon_checkbox = ctk.CTkCheckBox(vehicle_subclass_frame, text=weapon.name, variable=vehicle_weapon_var)
                vehicle_weapon_checkbox.pack(anchor="w", padx=20)

                self.vehicle_filter_vars[weapon.name] = vehicle_weapon_var
                
                # Initialize checkbox state from the central dictionary
                vehicle_weapon_var.set(self.vehicle_checkbox_states.get(weapon.name, False))

                # Update state on checkbox change
                vehicle_weapon_var.trace_add("write", lambda *args, name=weapon.name, var=vehicle_weapon_var: self.update_vehicle_checkbox_state(name, var))

            # Move to the next column, and if we reach the max number of columns, reset to the first column and move to the next row
            current_column += 1
            if current_column >= max_columns:
                current_column = 0
                current_row += 1

        # Add Confirm button
        confirm_vehicle_button = ctk.CTkButton(self, text="Confirm", command=self.confirm_vehicle_selection)
        confirm_vehicle_button.pack(pady=10)

    def toggle_vehicle_section(self, section_var, section_frame):
        """
        Toggle all checkboxes within a section (subclass) based on the master checkbox state.
        This will select/deselect all items but allow them to retain their individual states when
        manually checked or unchecked.
        """
        for widget in section_frame.winfo_children():
            if isinstance(widget, ctk.CTkCheckBox):
                if section_var.get():
                    widget.select()
                else:
                    widget.deselect()
        
        # Update each individual checkbox state after the toggle
        for name, var in self.vehicle_filter_vars.items():
            self.vehicle_checkbox_states[name] = var.get()  # Save the state in the central dictionary

    def update_vehicle_checkbox_state(self, weapon_name, var):
        """
        Update the state of an individual checkbox and store it in the central dictionary.
        This function will ensure that the checkbox state is saved independently of the
        master subclass checkbox state.
        """
        self.vehicle_checkbox_states[weapon_name] = var.get()  # Save the state of the individual checkbox

    def confirm_vehicle_selection(self):
        """
        Save the state of all checkboxes when the Confirm button is pressed.
        Optionally, perform additional actions here.
        """
        for name, var in self.vehicle_filter_vars.items():
            self.vehicle_checkbox_states[name] = var.get()  # Update the central state dictionary
        
        print("Checkbox states saved:", self.vehicle_checkbox_states)  # Debugging or additional logic
        
        # Close the popup window
        self.destroy()

    def get_selected_vehicle_weapons(self):
        """
        Return a list of selected weapons based on the checkbox states.
        """
        return [name for name, var in self.vehicle_filter_vars.items() if var.get()]