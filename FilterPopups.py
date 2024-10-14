import customtkinter as ctk
from Libraries.Primaries import primaries
from Libraries.Secondaries import secondaries
from Libraries.Grenades import grenades
from Libraries.Armors import armors
from Libraries.Boosters import boosters
from Libraries.Stratagems.Sentries import sentries
from Libraries.Stratagems.Vehicles import vehicles

class PrimaryFilterPopup(ctk.CTkToplevel):
    def __init__(self, master, primary_filter_states, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.title("Primary Weapon Filter")
        self.geometry("650x500")
        self.attributes('-topmost', True)
        
        self.primary_filter_vars = {}  # Store variables for each checkbox
        self.primary_subclass_vars = {}  # Store variables for each subclass checkbox
        self.primary_subclass_frames = {}  # Dictionary to hold widgets for each subclass

        # Store a reference to the central state dictionary passed from the main app
        self.primary_checkbox_states = primary_filter_states

        # Create a frame to hold all subclass checkboxes
        grid_frame = ctk.CTkFrame(self)
        grid_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Track grid positions for rows and columns
        current_row = 0
        current_column = 0
        max_columns = 3  # We want 3 columns in total

        # Create sections for each subclass
        primary_subclasses = sorted(set(p.subclass for p in primaries))
        
        for subclass in primary_subclasses:
            # Create a frame for each subclass
            primary_subclass_frame = ctk.CTkFrame(grid_frame)
            primary_subclass_frame.grid(row=current_row, column=current_column, padx=10, pady=5, sticky="nw")

            primary_subclass_var = ctk.BooleanVar()
            primary_subclass_checkbox = ctk.CTkCheckBox(
                primary_subclass_frame, text=subclass, variable=primary_subclass_var,
                command=lambda sv=primary_subclass_var, sf=primary_subclass_frame: self.toggle_primary_section(sv, sf)
            )
            primary_subclass_checkbox.pack(anchor="w")

            self.primary_subclass_vars[subclass] = primary_subclass_var
            self.primary_subclass_frames[subclass] = primary_subclass_frame

            # Add individual weapon checkboxes under the subclass
            for weapon in [p for p in primaries if p.subclass == subclass]:
                primary_weapon_var = ctk.BooleanVar()
                primary_weapon_checkbox = ctk.CTkCheckBox(primary_subclass_frame, text=weapon.name, variable=primary_weapon_var)
                primary_weapon_checkbox.pack(anchor="w", padx=20)

                self.primary_filter_vars[weapon.name] = primary_weapon_var
                
                # Initialize checkbox state from the central dictionary
                primary_weapon_var.set(self.primary_checkbox_states.get(weapon.name, False))

                # Update state on checkbox change
                primary_weapon_var.trace_add("write", lambda *args, name=weapon.name, var=primary_weapon_var: self.update_primary_checkbox_state(name, var))

            # Move to the next column, and if we reach the max number of columns, reset to the first column and move to the next row
            current_column += 1
            if current_column >= max_columns:
                current_column = 0
                current_row += 1

        # Add Confirm button
        confirm_primary_button = ctk.CTkButton(self, text="Confirm", command=self.confirm_primary_selection)
        confirm_primary_button.pack(pady=10)

    # Toggle all checkboxes within a section (subclass) based on the master checkbox state.
    def toggle_primary_section(self, section_var, section_frame):
        for widget in section_frame.winfo_children():
            if isinstance(widget, ctk.CTkCheckBox):
                if section_var.get():
                    widget.select()
                else:
                    widget.deselect()
        
        # Update each individual checkbox state after the toggle
        for name, var in self.primary_filter_vars.items():
            self.primary_checkbox_states[name] = var.get()  # Save the state in the central dictionary

    # Update the state of an individual checkbox and store it in the central dictionary.
    def update_primary_checkbox_state(self, weapon_name, var):
        self.primary_checkbox_states[weapon_name] = var.get()  # Save the state of the individual checkbox

    # Save the state of all checkboxes when the Confirm button is pressed.
    def confirm_primary_selection(self):
        for name, var in self.primary_filter_vars.items():
            self.primary_checkbox_states[name] = var.get()  # Update the central state dictionary
        
        print("Checkbox states saved:", self.primary_checkbox_states)  # Debugging or additional logic
        
        # Close the popup window
        self.destroy()

    def get_selected_primary_weapons(self):
        """
        Return a list of selected weapons based on the checkbox states.
        """
        return [name for name, var in self.primary_filter_vars.items() if var.get()]
    
class SecondaryFilterPopup(ctk.CTkToplevel):
    def __init__(self, master, secondary_filter_states, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.title("Secondary Weapon Filter")
        self.geometry("370x220")
        self.attributes('-topmost', True)
        
        self.secondary_filter_vars = {}  # Store variables for each checkbox
        self.secondary_subclass_vars = {}  # Store variables for each subclass checkbox
        self.secondary_subclass_frames = {}  # Dictionary to hold widgets for each subclass

        # Store a reference to the central state dictionary passed from the main app
        self.secondary_checkbox_states = secondary_filter_states

        # Create a frame to hold all subclass checkboxes
        grid_frame = ctk.CTkFrame(self)
        grid_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Track grid positions for rows and columns
        current_row = 0
        current_column = 0
        max_columns = 3  # We want 3 columns in total

        # Create sections for each subclass
        secondary_subclasses = sorted(set(p.subclass for p in secondaries))
        
        for subclass in secondary_subclasses:
            # Create a frame for each subclass
            secondary_subclass_frame = ctk.CTkFrame(grid_frame)
            secondary_subclass_frame.grid(row=current_row, column=current_column, padx=10, pady=5, sticky="nw")

            secondary_subclass_var = ctk.BooleanVar()
            secondary_subclass_checkbox = ctk.CTkCheckBox(
                secondary_subclass_frame, text=subclass, variable=secondary_subclass_var,
                command=lambda sv=secondary_subclass_var, sf=secondary_subclass_frame: self.toggle_secondary_section(sv, sf)
            )
            secondary_subclass_checkbox.pack(anchor="w")

            self.secondary_subclass_vars[subclass] = secondary_subclass_var
            self.secondary_subclass_frames[subclass] = secondary_subclass_frame

            # Add individual weapon checkboxes under the subclass
            for weapon in [p for p in secondaries if p.subclass == subclass]:
                secondary_weapon_var = ctk.BooleanVar()
                secondary_weapon_checkbox = ctk.CTkCheckBox(secondary_subclass_frame, text=weapon.name, variable=secondary_weapon_var)
                secondary_weapon_checkbox.pack(anchor="w", padx=20)

                self.secondary_filter_vars[weapon.name] = secondary_weapon_var
                
                # Initialize checkbox state from the central dictionary
                secondary_weapon_var.set(self.secondary_checkbox_states.get(weapon.name, False))

                # Update state on checkbox change
                secondary_weapon_var.trace_add("write", lambda *args, name=weapon.name, var=secondary_weapon_var: self.update_secondary_checkbox_state(name, var))

            # Move to the next column, and if we reach the max number of columns, reset to the first column and move to the next row
            current_column += 1
            if current_column >= max_columns:
                current_column = 0
                current_row += 1

        # Add Confirm button
        confirm_secondary_button = ctk.CTkButton(self, text="Confirm", command=self.confirm_secondary_selection)
        confirm_secondary_button.pack(pady=10)

    # Toggle all checkboxes within a section (subclass) based on the master checkbox state.
    def toggle_secondary_section(self, section_var, section_frame):
        for widget in section_frame.winfo_children():
            if isinstance(widget, ctk.CTkCheckBox):
                if section_var.get():
                    widget.select()
                else:
                    widget.deselect()
        
        # Update each individual checkbox state after the toggle
        for name, var in self.secondary_filter_vars.items():
            self.secondary_checkbox_states[name] = var.get()  # Save the state in the central dictionary

    # Update the state of an individual checkbox and store it in the central dictionary.
    def update_secondary_checkbox_state(self, weapon_name, var):
        self.secondary_checkbox_states[weapon_name] = var.get()  # Save the state of the individual checkbox

    # Save the state of all checkboxes when the Confirm button is pressed.
    def confirm_secondary_selection(self):
        for name, var in self.secondary_filter_vars.items():
            self.secondary_checkbox_states[name] = var.get()  # Update the central state dictionary
        
        print("Checkbox states saved:", self.secondary_checkbox_states)  # Debugging or additional logic
        
        # Close the popup window
        self.destroy()

    def get_selected_secondary_weapons(self):
        return [name for name, var in self.secondary_filter_vars.items() if var.get()]

class GrenadeFilterPopup(ctk.CTkToplevel):
    def __init__(self, master, grenade_filter_states, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.title("Grenade Filter")
        self.geometry("210x280")
        self.attributes('-topmost', True)
        
        self.grenade_filter_vars = {}  # Store variables for each checkbox
        self.grenade_subclass_vars = {}  # Store variables for each subclass checkbox
        self.grenade_subclass_frames = {}  # Dictionary to hold widgets for each subclass

        # Store a reference to the central state dictionary passed from the main app
        self.grenade_checkbox_states = grenade_filter_states

        # Create a frame to hold all subclass checkboxes
        grid_frame = ctk.CTkFrame(self)
        grid_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create sections for each subclass
        grenade_subclasses = sorted(set(p.subclass for p in grenades))
        
        for subclass in grenade_subclasses:
            # Create a frame for each subclass
            grenade_subclass_frame = ctk.CTkFrame(grid_frame)
            grenade_subclass_frame.grid(padx=10, pady=5, sticky="nw")

            grenade_subclass_var = ctk.BooleanVar()
            grenade_subclass_checkbox = ctk.CTkCheckBox(
                grenade_subclass_frame, text=subclass, variable=grenade_subclass_var,
                command=lambda sv=grenade_subclass_var, sf=grenade_subclass_frame: self.toggle_grenade_section(sv, sf)
            )
            grenade_subclass_checkbox.pack(anchor="w")

            self.grenade_subclass_vars[subclass] = grenade_subclass_var
            self.grenade_subclass_frames[subclass] = grenade_subclass_frame

            # Add individual weapon checkboxes under the subclass
            for weapon in [p for p in grenades if p.subclass == subclass]:
                grenade_weapon_var = ctk.BooleanVar()
                grenade_weapon_checkbox = ctk.CTkCheckBox(grenade_subclass_frame, text=weapon.name, variable=grenade_weapon_var)
                grenade_weapon_checkbox.pack(anchor="w", padx=20)

                self.grenade_filter_vars[weapon.name] = grenade_weapon_var
                
                # Initialize checkbox state from the central dictionary
                grenade_weapon_var.set(self.grenade_checkbox_states.get(weapon.name, False))

                # Update state on checkbox change
                grenade_weapon_var.trace_add("write", lambda *args, name=weapon.name, var=grenade_weapon_var: self.update_grenade_checkbox_state(name, var))

        # Add Confirm button
        confirm_grenade_button = ctk.CTkButton(self, text="Confirm", command=self.confirm_grenade_selection)
        confirm_grenade_button.pack(pady=10)

    # Toggle all checkboxes within a section (subclass) based on the master checkbox state.
    def toggle_grenade_section(self, section_var, section_frame):
        for widget in section_frame.winfo_children():
            if isinstance(widget, ctk.CTkCheckBox):
                if section_var.get():
                    widget.select()
                else:
                    widget.deselect()
        
        # Update each individual checkbox state after the toggle
        for name, var in self.grenade_filter_vars.items():
            self.grenade_checkbox_states[name] = var.get()  # Save the state in the central dictionary

    # Update the state of an individual checkbox and store it in the central dictionary.
    def update_grenade_checkbox_state(self, weapon_name, var):
        self.grenade_checkbox_states[weapon_name] = var.get()  # Save the state of the individual checkbox

    # Save the state of all checkboxes when the Confirm button is pressed.
    def confirm_grenade_selection(self):
        for name, var in self.grenade_filter_vars.items():
            self.grenade_checkbox_states[name] = var.get()  # Update the central state dictionary
        
        print("Checkbox states saved:", self.grenade_checkbox_states)  # Debugging or additional logic
        
        # Close the popup window
        self.destroy()

    def get_selected_grenade_weapons(self):
        return [name for name, var in self.grenade_filter_vars.items() if var.get()]
    
class ArmorFilterPopup(ctk.CTkToplevel):
    def __init__(self, master, armor_filter_states, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.title("Armor Filter")
        self.geometry("225x380")
        self.attributes('-topmost', True)
        
        self.armor_filter_vars = {}  # Store variables for each checkbox
        self.armor_subclass_vars = {}  # Store variables for each subclass checkbox
        self.armor_subclass_frames = {}  # Dictionary to hold widgets for each subclass

        # Store a reference to the central state dictionary passed from the main app
        self.armor_checkbox_states = armor_filter_states

        # Create a frame to hold all subclass checkboxes
        grid_frame = ctk.CTkFrame(self)
        grid_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create sections for each subclass
        armor_subclasses = sorted(set(p.subclass for p in armors))
        
        for subclass in armor_subclasses:
            # Create a frame for each subclass
            armor_subclass_frame = ctk.CTkFrame(grid_frame)
            armor_subclass_frame.grid(padx=10, pady=5, sticky="nw")

            armor_subclass_var = ctk.BooleanVar()
            armor_subclass_checkbox = ctk.CTkCheckBox(
                armor_subclass_frame, text=subclass, variable=armor_subclass_var,
                command=lambda sv=armor_subclass_var, sf=armor_subclass_frame: self.toggle_armor_section(sv, sf)
            )
            armor_subclass_checkbox.pack(anchor="w")

            self.armor_subclass_vars[subclass] = armor_subclass_var
            self.armor_subclass_frames[subclass] = armor_subclass_frame

            # Add individual weapon checkboxes under the subclass
            for weapon in [p for p in armors if p.subclass == subclass]:
                armor_weapon_var = ctk.BooleanVar()
                armor_weapon_checkbox = ctk.CTkCheckBox(armor_subclass_frame, text=weapon.name, variable=armor_weapon_var)
                armor_weapon_checkbox.pack(anchor="w", padx=20)

                self.armor_filter_vars[weapon.name] = armor_weapon_var
                
                # Initialize checkbox state from the central dictionary
                armor_weapon_var.set(self.armor_checkbox_states.get(weapon.name, False))

                # Update state on checkbox change
                armor_weapon_var.trace_add("write", lambda *args, name=weapon.name, var=armor_weapon_var: self.update_armor_checkbox_state(name, var))

        # Add Confirm button
        confirm_armor_button = ctk.CTkButton(self, text="Confirm", command=self.confirm_armor_selection)
        confirm_armor_button.pack(pady=10)

    # Toggle all checkboxes within a section (subclass) based on the master checkbox state.
    def toggle_armor_section(self, section_var, section_frame):
        for widget in section_frame.winfo_children():
            if isinstance(widget, ctk.CTkCheckBox):
                if section_var.get():
                    widget.select()
                else:
                    widget.deselect()
        
        # Update each individual checkbox state after the toggle
        for name, var in self.armor_filter_vars.items():
            self.armor_checkbox_states[name] = var.get()  # Save the state in the central dictionary

    # Update the state of an individual checkbox and store it in the central dictionary.
    def update_armor_checkbox_state(self, weapon_name, var):
        self.armor_checkbox_states[weapon_name] = var.get()  # Save the state of the individual checkbox

    # Save the state of all checkboxes when the Confirm button is pressed.
    def confirm_armor_selection(self):
        for name, var in self.armor_filter_vars.items():
            self.armor_checkbox_states[name] = var.get()  # Update the central state dictionary
        
        print("Checkbox states saved:", self.armor_checkbox_states)  # Debugging or additional logic
        
        # Close the popup window
        self.destroy()

    def get_selected_armor_weapons(self):
        return [name for name, var in self.armor_filter_vars.items() if var.get()]
    
class BoosterFilterPopup(ctk.CTkToplevel):
    def __init__(self, master, booster_filter_states, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.title("Booster Filter")
        self.geometry("270x400")
        self.attributes('-topmost', True)
        
        self.booster_filter_vars = {}  # Store variables for each checkbox
        self.booster_subclass_vars = {}  # Store variables for each subclass checkbox
        self.booster_subclass_frames = {}  # Dictionary to hold widgets for each subclass

        # Store a reference to the central state dictionary passed from the main app
        self.booster_checkbox_states = booster_filter_states

        # Create a frame to hold all subclass checkboxes
        grid_frame = ctk.CTkFrame(self)
        grid_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create sections for each subclass
        booster_subclasses = sorted(set(p.subclass for p in boosters))
        
        for subclass in booster_subclasses:
            # Create a frame for each subclass
            booster_subclass_frame = ctk.CTkFrame(grid_frame)
            booster_subclass_frame.grid(padx=10, pady=5, sticky="nw")

            booster_subclass_var = ctk.BooleanVar()
            booster_subclass_checkbox = ctk.CTkCheckBox(
                booster_subclass_frame, text=subclass, variable=booster_subclass_var,
                command=lambda sv=booster_subclass_var, sf=booster_subclass_frame: self.toggle_booster_section(sv, sf)
            )
            booster_subclass_checkbox.pack(anchor="w")

            self.booster_subclass_vars[subclass] = booster_subclass_var
            self.booster_subclass_frames[subclass] = booster_subclass_frame

            # Add individual weapon checkboxes under the subclass
            for weapon in [p for p in boosters if p.subclass == subclass]:
                booster_weapon_var = ctk.BooleanVar()
                booster_weapon_checkbox = ctk.CTkCheckBox(booster_subclass_frame, text=weapon.name, variable=booster_weapon_var)
                booster_weapon_checkbox.pack(anchor="w", padx=20)

                self.booster_filter_vars[weapon.name] = booster_weapon_var
                
                # Initialize checkbox state from the central dictionary
                booster_weapon_var.set(self.booster_checkbox_states.get(weapon.name, False))

                # Update state on checkbox change
                booster_weapon_var.trace_add("write", lambda *args, name=weapon.name, var=booster_weapon_var: self.update_booster_checkbox_state(name, var))

        # Add Confirm button
        confirm_booster_button = ctk.CTkButton(self, text="Confirm", command=self.confirm_booster_selection)
        confirm_booster_button.pack(pady=10)

    # Toggle all checkboxes within a section (subclass) based on the master checkbox state.
    def toggle_booster_section(self, section_var, section_frame):
        for widget in section_frame.winfo_children():
            if isinstance(widget, ctk.CTkCheckBox):
                if section_var.get():
                    widget.select()
                else:
                    widget.deselect()
        
        # Update each individual checkbox state after the toggle
        for name, var in self.booster_filter_vars.items():
            self.booster_checkbox_states[name] = var.get()  # Save the state in the central dictionary

    # Update the state of an individual checkbox and store it in the central dictionary.
    def update_booster_checkbox_state(self, weapon_name, var):
        self.booster_checkbox_states[weapon_name] = var.get()  # Save the state of the individual checkbox

    # Save the state of all checkboxes when the Confirm button is pressed.
    def confirm_booster_selection(self):
        for name, var in self.booster_filter_vars.items():
            self.booster_checkbox_states[name] = var.get()  # Update the central state dictionary
        
        print("Checkbox states saved:", self.booster_checkbox_states)  # Debugging or additional logic
        
        # Close the popup window
        self.destroy()

    def get_selected_booster_weapons(self):
        return [name for name, var in self.booster_filter_vars.items() if var.get()]
    
class SentryFilterPopup(ctk.CTkToplevel):
    def __init__(self, master, sentry_filter_states, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.title("Sentry Filter")
        self.geometry("570x280")
        self.attributes('-topmost', True)
        
        self.sentry_filter_vars = {}  # Store variables for each checkbox
        self.sentry_subclass_vars = {}  # Store variables for each subclass checkbox
        self.sentry_subclass_frames = {}  # Dictionary to hold widgets for each subclass

        # Store a reference to the central state dictionary passed from the main app
        self.sentry_checkbox_states = sentry_filter_states

        # Create a frame to hold all subclass checkboxes
        grid_frame = ctk.CTkFrame(self)
        grid_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Track grid positions for rows and columns
        current_row = 0
        current_column = 0
        max_columns = 3  # We want 3 columns in total

        # Create sections for each subclass
        sentry_subclasses = sorted(set(p.subclass for p in sentries))
        
        for subclass in sentry_subclasses:
            # Create a frame for each subclass
            sentry_subclass_frame = ctk.CTkFrame(grid_frame)
            sentry_subclass_frame.grid(row=current_row, column=current_column, padx=10, pady=5, sticky="nw")

            sentry_subclass_var = ctk.BooleanVar()
            sentry_subclass_checkbox = ctk.CTkCheckBox(
                sentry_subclass_frame, text=subclass, variable=sentry_subclass_var,
                command=lambda sv=sentry_subclass_var, sf=sentry_subclass_frame: self.toggle_sentry_section(sv, sf)
            )
            sentry_subclass_checkbox.pack(anchor="w")

            self.sentry_subclass_vars[subclass] = sentry_subclass_var
            self.sentry_subclass_frames[subclass] = sentry_subclass_frame

            # Add individual weapon checkboxes under the subclass
            for weapon in [p for p in sentries if p.subclass == subclass]:
                sentry_weapon_var = ctk.BooleanVar()
                sentry_weapon_checkbox = ctk.CTkCheckBox(sentry_subclass_frame, text=weapon.name, variable=sentry_weapon_var)
                sentry_weapon_checkbox.pack(anchor="w", padx=20)

                self.sentry_filter_vars[weapon.name] = sentry_weapon_var
                
                # Initialize checkbox state from the central dictionary
                sentry_weapon_var.set(self.sentry_checkbox_states.get(weapon.name, False))

                # Update state on checkbox change
                sentry_weapon_var.trace_add("write", lambda *args, name=weapon.name, var=sentry_weapon_var: self.update_sentry_checkbox_state(name, var))

            # Move to the next column, and if we reach the max number of columns, reset to the first column and move to the next row
            current_column += 1
            if current_column >= max_columns:
                current_column = 0
                current_row += 1

        # Add Confirm button
        confirm_sentry_button = ctk.CTkButton(self, text="Confirm", command=self.confirm_sentry_selection)
        confirm_sentry_button.pack(pady=10)

    # Toggle all checkboxes within a section (subclass) based on the master checkbox state.
    def toggle_sentry_section(self, section_var, section_frame):
        for widget in section_frame.winfo_children():
            if isinstance(widget, ctk.CTkCheckBox):
                if section_var.get():
                    widget.select()
                else:
                    widget.deselect()
        
        # Update each individual checkbox state after the toggle
        for name, var in self.sentry_filter_vars.items():
            self.sentry_checkbox_states[name] = var.get()  # Save the state in the central dictionary

    # Update the state of an individual checkbox and store it in the central dictionary.
    def update_sentry_checkbox_state(self, weapon_name, var):
        self.sentry_checkbox_states[weapon_name] = var.get()  # Save the state of the individual checkbox

    # Save the state of all checkboxes when the Confirm button is pressed.
    def confirm_sentry_selection(self):
        for name, var in self.sentry_filter_vars.items():
            self.sentry_checkbox_states[name] = var.get()  # Update the central state dictionary
        
        print("Checkbox states saved:", self.sentry_checkbox_states)  # Debugging or additional logic
        
        # Close the popup window
        self.destroy()

    def get_selected_sentry_weapons(self):
        return [name for name, var in self.sentry_filter_vars.items() if var.get()]
    
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

    # Toggle all checkboxes within a section (subclass) based on the master checkbox state.
    def toggle_vehicle_section(self, section_var, section_frame):
        for widget in section_frame.winfo_children():
            if isinstance(widget, ctk.CTkCheckBox):
                if section_var.get():
                    widget.select()
                else:
                    widget.deselect()
        
        # Update each individual checkbox state after the toggle
        for name, var in self.vehicle_filter_vars.items():
            self.vehicle_checkbox_states[name] = var.get()  # Save the state in the central dictionary

    # Update the state of an individual checkbox and store it in the central dictionary.
    def update_vehicle_checkbox_state(self, weapon_name, var):
        self.vehicle_checkbox_states[weapon_name] = var.get()  # Save the state of the individual checkbox

    # Save the state of all checkboxes when the Confirm button is pressed.
    def confirm_vehicle_selection(self):
        for name, var in self.vehicle_filter_vars.items():
            self.vehicle_checkbox_states[name] = var.get()  # Update the central state dictionary
        
        print("Checkbox states saved:", self.vehicle_checkbox_states)  # Debugging or additional logic
        
        # Close the popup window
        self.destroy()

    def get_selected_vehicle_weapons(self):
        return [name for name, var in self.vehicle_filter_vars.items() if var.get()]