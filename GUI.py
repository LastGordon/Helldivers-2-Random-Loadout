import customtkinter as ctk
import json
import os
from Libraries.Images.ImageLoader import ImageLoader
from Randomizer import randomize_items
from PIL import Image
from FilterPopups import PrimaryFilterPopup
from FilterPopups import SecondaryFilterPopup
from FilterPopups import GrenadeFilterPopup
from FilterPopups import ArmorFilterPopup
from FilterPopups import BoosterFilterPopup
from FilterPopups import SentryFilterPopup
from FilterPopups import VehicleFilterPopup
# from FilterPopups import SuperstoreFilterPopup





# Initialize the CTk window
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class LoadoutRandomizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Helldivers 2 Loadout Randomizer")
        self.geometry("1000x650")

        # Initialize ImageLoader
        self.image_loader = ImageLoader("Libraries/Images")

        self.helldiver_image = self.image_loader.load_generic_helldiver_image()
        self.helldiver_image_tk = ctk.CTkImage(self.helldiver_image, size=(372, 343))

        self.default_stratagem1_image = self.image_loader.load_images("blank", "HD2-blank-blue.png")
        self.default_stratagem1_image_tk = ctk.CTkImage(self.default_stratagem1_image,size=(60, 60))
        self.default_stratagem2_image = self.image_loader.load_images("blank", "HD2-blank-green.png")
        self.default_stratagem2_image_tk = ctk.CTkImage(self.default_stratagem2_image,size=(60, 60))
        self.default_stratagem3_image = self.image_loader.load_images("blank", "HD2-blank-red.png")
        self.default_stratagem3_image_tk = ctk.CTkImage(self.default_stratagem3_image,size=(60, 60))
        self.default_stratagem4_image = self.image_loader.load_images("blank", "HD2-blank-red.png")
        self.default_stratagem4_image_tk = ctk.CTkImage(self.default_stratagem4_image,size=(60, 60))

        # Dictionaries to store checkbox states from their associated filter buttons.
        self.primary_filter_states = {}
        self.secondary_filter_states = {}
        self.grenade_filter_states = {}
        self.armor_filter_states = {}
        self.booster_filter_states = {}
        self.sentry_filter_states = {}
        self.vehicle_filter_states = {}

        # self.superstore_states = {}

        # Initialize checkbox variables
        self.primary_var = ctk.BooleanVar(value=False)
        self.secondary_var = ctk.BooleanVar(value=False)
        self.grenade_var = ctk.BooleanVar(value=False)
        self.armor_var = ctk.BooleanVar(value=False)
        self.booster_var = ctk.BooleanVar(value=False)

        self.stratagem_var = ctk.BooleanVar(value=False)

        self.one_support_var = ctk.BooleanVar(value=False)
        self.g_support_var = ctk.BooleanVar(value=False)
        self.one_backpack_var = ctk.BooleanVar(value=False)
        self.g_backpack_var = ctk.BooleanVar(value=False)
        self.g_sentry_var = ctk.BooleanVar(value=False)
        self.g_tank_var = ctk.BooleanVar(value=False)
        self.g_explosive_var = ctk.BooleanVar(value=False)
        self.one_vehicle_var = ctk.BooleanVar(value=False)
        self.g_vehicle_var = ctk.BooleanVar(value=False)

        self.deluxe_var = ctk.BooleanVar(value=False)
        self.steeled_veterans_var = ctk.BooleanVar(value=False)
        self.cutting_edge_var = ctk.BooleanVar(value=False)
        self.democratic_detonation_var = ctk.BooleanVar(value=False)
        self.polar_patriots_var = ctk.BooleanVar(value=False)
        self.viper_commandos_var = ctk.BooleanVar(value=False)
        self.freedoms_flame_var = ctk.BooleanVar(value=False)
        self.chemical_agents_var = ctk.BooleanVar(value=False)
        self.truth_enforcers_var = ctk.BooleanVar(value=False)
        self.urban_legends_var = ctk.BooleanVar(value=False)

        self.warbond_states = {
            "Deluxe" : self.deluxe_var,
            "Steeled Veterans": self.steeled_veterans_var,
            "Cutting Edge": self.cutting_edge_var,
            "Democratic Detonation": self.democratic_detonation_var,
            "Polar Patriots": self.polar_patriots_var,
            "Viper Commandos": self.viper_commandos_var,
            "Freedoms Flame": self.freedoms_flame_var,
            "Chemical Agents": self.chemical_agents_var,
            "Truth Enforcers": self.truth_enforcers_var,
            "Urban Legends": self.urban_legends_var
        }

        # Load saved warbond states
        self.load_warbonds()
        # self.superstore_popup = SuperstoreFilterPopup(self, self.superstore_states)
        # self.superstore_popup.load_superstore()  # Load states without displaying the popup

        # # Withdraw the popup to keep it hidden initially
        # self.superstore_popup.withdraw()

        # Configure Grid Layout: 2 rows, 2 columns
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0), weight=0)
        self.grid_rowconfigure((1), weight=0)

        # Top Section: Randomizer Options
        self.randomizer_frame = ctk.CTkFrame(self)
        self.randomizer_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        
        # Title Label for Randomizer Options
        self.randomizer_label = ctk.CTkLabel(self.randomizer_frame, text="Randomizer Options", font=ctk.CTkFont(size=16, weight="bold"))
        self.randomizer_label.grid(row=0, column=0, sticky="w", padx=10 ,pady=(0, 10))

        # Find Loadout Button
        self.find_loadout_button = ctk.CTkButton(self.randomizer_frame, text="Find Loadout", command=self.find_loadout)
        self.find_loadout_button.grid(row=0, column=3, sticky="w")

        # Gear Section with Master Checkbox
        self.randomize_gear_master_check = ctk.CTkCheckBox(self.randomizer_frame, text="Randomize Gear", command=self.toggle_gear_options)
        self.randomize_gear_master_check.grid(row=1, column=0, sticky="w", padx=10 ,pady=(0, 10))

        # Sub-checkboxes for Gear Randomization (inset)
        self.primary_check = ctk.CTkCheckBox(self.randomizer_frame, text="Primary", state="disabled", command=self.toggle_primary, variable=self.primary_var)
        self.primary_check.grid(row=2, column=0, sticky="w", padx=35)
        self.primary_filter_button = ctk.CTkButton(self.randomizer_frame, text="Primary Filter", state="disabled", command=self.open_primary_filter_popup)
        self.primary_filter_button.grid(row=2, column=1, sticky="e")

        self.secondary_check = ctk.CTkCheckBox(self.randomizer_frame, text="Secondary", state="disabled", command=self.toggle_secondary,variable=self.secondary_var)
        self.secondary_check.grid(row=3, column=0, sticky="w", padx=35)
        self.secondary_filter_button = ctk.CTkButton(self.randomizer_frame, text="Secondary Filter", state="disabled", command=self.open_secondary_filter_popup)
        self.secondary_filter_button.grid(row=3, column=1, sticky="e")

        self.grenade_check = ctk.CTkCheckBox(self.randomizer_frame, text="Grenade", state="disabled", command=self.toggle_grenade,variable=self.grenade_var)
        self.grenade_check.grid(row=4, column=0, sticky="w", padx=35)
        self.grenade_filter_button = ctk.CTkButton(self.randomizer_frame, text="Grenade Filter", state="disabled", command=self.open_grenade_filter_popup)
        self.grenade_filter_button.grid(row=4, column=1, sticky="e")

        self.armor_check = ctk.CTkCheckBox(self.randomizer_frame, text="Armor", state="disabled", command=self.toggle_armor,variable=self.armor_var)
        self.armor_check.grid(row=5, column=0, sticky="w", padx=35)
        self.armor_filter_button = ctk.CTkButton(self.randomizer_frame, text="Armor Filter", state="disabled", command=self.open_armor_filter_popup)
        self.armor_filter_button.grid(row=5, column=1, sticky="e")

        self.booster_check = ctk.CTkCheckBox(self.randomizer_frame, text="Booster", state="disabled", command=self.toggle_booster,variable=self.booster_var)
        self.booster_check.grid(row=6, column=0, sticky="w", padx=35)
        self.booster_filter_button = ctk.CTkButton(self.randomizer_frame, text="Booster Filter", state="disabled", command=self.open_booster_filter_popup)
        self.booster_filter_button.grid(row=6, column=1, sticky="e")

        # Stratagem Section with Master Checkbox (added to the right)
        self.randomize_stratagem_master_check = ctk.CTkCheckBox(self.randomizer_frame, text="Randomize Stratagems", command=self.toggle_stratagem_options, variable=self.stratagem_var)
        self.randomize_stratagem_master_check.grid(row=1, column=2, sticky="w", padx=25)

        # First column of Stratagem options (indented one checkbox width further)
        self.limit_support_check = ctk.CTkCheckBox(self.randomizer_frame, text="Limit to One Support", state="disabled",variable=self.one_support_var,)
        self.limit_support_check.grid(row=2, column=2, sticky="w", padx=50)
        self.guarantee_support_check = ctk.CTkCheckBox(self.randomizer_frame, text="Guarantee Support", state="disabled", variable=self.g_support_var)
        self.guarantee_support_check.grid(row=3, column=2, sticky="w", padx=50)
        self.limit_backpack_check = ctk.CTkCheckBox(self.randomizer_frame, text="Limit to One Backpack", state="disabled", variable=self.one_backpack_var)
        self.limit_backpack_check.grid(row=4, column=2, sticky="w", padx=50)
        self.guarantee_backpack_check = ctk.CTkCheckBox(self.randomizer_frame, text="Guarantee Backpack", state="disabled", variable=self.g_backpack_var)
        self.guarantee_backpack_check.grid(row=5, column=2, sticky="w", padx=50)

        # Second column of Stratagem options (indented one checkbox width further)
        self.sentry_check = ctk.CTkCheckBox(self.randomizer_frame, text="Guarantee Sentry", state="disabled", variable=self.g_sentry_var)
        self.sentry_check.grid(row=1, column=3, sticky="w", padx=0)
        self.anti_tank_check = ctk.CTkCheckBox(self.randomizer_frame, text="Guarantee Anti-Tank", state="disabled", variable=self.g_tank_var)
        self.anti_tank_check.grid(row=2, column=3, sticky="w", padx=0)
        self.explosive_check = ctk.CTkCheckBox(self.randomizer_frame, text="Guarantee Explosive", state="disabled", variable=self.g_explosive_var)
        self.explosive_check.grid(row=3, column=3, sticky="w", padx=0)
        self.limit_vehicle_check = ctk.CTkCheckBox(self.randomizer_frame, text="Limit to One Vehicle", state="disabled",variable=self.one_vehicle_var,)
        self.limit_vehicle_check.grid(row=4, column=3, sticky="w", padx=0)
        self.vehicle_check = ctk.CTkCheckBox(self.randomizer_frame, text="Guarantee Vehicle", state="disabled", variable=self.g_vehicle_var)
        self.vehicle_check.grid(row=5, column=3, sticky="w", padx=0)

        self.sentry_filter_button = ctk.CTkButton(self.randomizer_frame, text="Sentry Filter", state="disabled", command=self.open_sentry_filter_popup)
        self.sentry_filter_button.grid(row=6, column=2, sticky="w", padx=50)
        self.vehicle_filter_button = ctk.CTkButton(self.randomizer_frame, text="Vehicle Filter", state="disabled", command=self.open_vehicle_filter_popup)
        self.vehicle_filter_button.grid(row=6, column=3, sticky="w")

        # Add Spacer Row
        self.randomizer_frame.grid_rowconfigure(7, weight=0, minsize=10)  # Adjust minsize as needed

        # Bottom Section: Output Section
        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        fixed_label_width = 220

        self.loadout_label = ctk.CTkLabel(self.output_frame, text="Final Loadout", font=ctk.CTkFont(size=16, weight="bold"))
        self.loadout_label.grid(row=0, column=0, sticky="w", padx= 10)

        #  Load generic helldiver image
        self.image_label = ctk.CTkLabel(self.output_frame,text="" , image=self.helldiver_image_tk)
        self.image_label.grid(row=1, column=0, rowspan=10,columnspan=2, sticky="w", padx=10, pady=10)

        self.primary_label = ctk.CTkLabel(self.output_frame, text="Primary:", font=ctk.CTkFont(size=20))
        self.primary_label.grid(row=1, column=0, sticky="w", padx=10)
        self.output_primary_sub = ctk.CTkLabel(self.output_frame, text="Subclass:", font=ctk.CTkFont(size=20), width=fixed_label_width, justify="left")
        self.output_primary_sub.grid(row=1, column=1, sticky="w", padx=25)
        self.output_primary = ctk.CTkLabel(self.output_frame, text="Primary Output", font=ctk.CTkFont(size=20), width=fixed_label_width, justify="left")
        self.output_primary.grid(row=2, column=1, sticky="w", padx=25)

        self.secondary_label = ctk.CTkLabel(self.output_frame, text="Secondary:", font=ctk.CTkFont(size=20))
        self.secondary_label.grid(row=3, column=0, sticky="w", padx=10)
        self.output_secondary_sub = ctk.CTkLabel(self.output_frame, text="Subclass:", font=ctk.CTkFont(size=20), width=fixed_label_width, justify="left")
        self.output_secondary_sub.grid(row=3, column=1, sticky="w", padx=25)
        self.output_secondary = ctk.CTkLabel(self.output_frame, text="Secondary Output", font=ctk.CTkFont(size=20), width=fixed_label_width, justify="left")
        self.output_secondary.grid(row=4, column=1, sticky="w", padx=25)

        self.grenade_label = ctk.CTkLabel(self.output_frame, text="Grenade:", font=ctk.CTkFont(size=20))
        self.grenade_label.grid(row=5, column=0, sticky="w", padx=10)
        self.output_grenade = ctk.CTkLabel(self.output_frame, text="Grenade Output", font=ctk.CTkFont(size=20), width=fixed_label_width, justify="left")
        self.output_grenade.grid(row=5, column=1, sticky="w", padx=25)

        self.armor_label = ctk.CTkLabel(self.output_frame, text="Armor:", font=ctk.CTkFont(size=20))
        self.armor_label.grid(row=6, column=0, sticky="w", padx=10)
        self.output_armor = ctk.CTkLabel(self.output_frame, text="Armor Output", font=ctk.CTkFont(size=20), width=fixed_label_width, justify="left")
        self.output_armor.grid(row=6, column=1, sticky="w", padx=25, columnspan=2)
        self.output_armor_des = ctk.CTkLabel(self.output_frame, text="Description\n", font=ctk.CTkFont(size=16), width=340,justify="left")
        self.output_armor_des.grid(row=7, column=0, sticky="w", padx=35, columnspan=3)

        self.booster_label = ctk.CTkLabel(self.output_frame, text="Booster:", font=ctk.CTkFont(size=20))
        self.booster_label.grid(row=8, column=0, sticky="w", padx=10)
        self.output_booster = ctk.CTkLabel(self.output_frame, text="Booster Output", font=ctk.CTkFont(size=18), width=fixed_label_width, justify="left")
        self.output_booster.grid(row=8, column=1, sticky="w", padx=25, columnspan=2)
        self.output_booster_des = ctk.CTkLabel(self.output_frame, text="Description", font=ctk.CTkFont(size=14), width=340,justify="left")
        self.output_booster_des.grid(row=9, column=0, sticky="w", padx=35, columnspan=3)

        self.loadout_label = ctk.CTkLabel(self.output_frame, text="Stratagems", font=ctk.CTkFont(size=20, weight="bold"))
        self.loadout_label.grid(row=1, column=2, sticky="w", columnspan= 2)

        self.output_Stratagem1_image = ctk.CTkLabel(self.output_frame, text="", image=self.default_stratagem1_image_tk)
        self.output_Stratagem1_image.grid(row=2, column=2, sticky="w", rowspan=2)
        self.output_stratagem1_output = ctk.CTkLabel(self.output_frame, text="Stratagem Selection", font=ctk.CTkFont(size=22))
        self.output_stratagem1_output.grid(row=2, column=3, sticky="w", padx=10, rowspan=2)

        self.output_Stratagem2_image = ctk.CTkLabel(self.output_frame, text="", image=self.default_stratagem2_image_tk)
        self.output_Stratagem2_image.grid(row=4, column=2, sticky="w", rowspan=2)
        self.output_stratagem2_output = ctk.CTkLabel(self.output_frame, text="Stratagem Selection", font=ctk.CTkFont(size=22))
        self.output_stratagem2_output.grid(row=4, column=3, sticky="w", padx=10, rowspan=2)

        self.output_Stratagem3_image = ctk.CTkLabel(self.output_frame, text="", image=self.default_stratagem3_image_tk)
        self.output_Stratagem3_image.grid(row=6, column=2, sticky="w", rowspan=2)
        self.output_stratagem3_output = ctk.CTkLabel(self.output_frame, text="Stratagem Selection", font=ctk.CTkFont(size=22))
        self.output_stratagem3_output.grid(row=6, column=3, sticky="w", padx=10, rowspan=2)

        self.output_Stratagem4_image = ctk.CTkLabel(self.output_frame, text="", image=self.default_stratagem4_image_tk)
        self.output_Stratagem4_image.grid(row=8, column=2, sticky="w", rowspan=2)
        self.output_stratagem4_output = ctk.CTkLabel(self.output_frame, text="Stratagem Selection", font=ctk.CTkFont(size=22))
        self.output_stratagem4_output.grid(row=8, column=3, sticky="w", padx=10, rowspan=2)

        # Right Side Section: Warbonds
        self.warbond_states_frame = ctk.CTkFrame(self)
        self.warbond_states_frame.grid(row=0, column=2, rowspan=2, sticky="ns", padx=10, pady=10)  # Span whole height of window
        
        self.warbond_states_label = ctk.CTkLabel(self.warbond_states_frame, text="Warbonds Owned", font=ctk.CTkFont(size=16, weight="bold"))
        self.warbond_states_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        self.deluxe_check = ctk.CTkCheckBox(self.warbond_states_frame, text="Super Citizen Edition", variable=self.deluxe_var, command= self.save_warbonds)
        self.deluxe_check.grid(row=1, column=0, sticky="w", padx=10, pady=(0,5))
        self.steeled_veterans_check = ctk.CTkCheckBox(self.warbond_states_frame, text="Steeled Veterans", variable=self.steeled_veterans_var, command= self.save_warbonds)
        self.steeled_veterans_check.grid(row=2, column=0, sticky="w", padx=10, pady=(0,5))
        self.cutting_edge_check = ctk.CTkCheckBox(self.warbond_states_frame, text="Cutting Edge", variable=self.cutting_edge_var, command= self.save_warbonds)
        self.cutting_edge_check.grid(row=3, column=0, sticky="w", padx=10, pady=(0,5))
        self.democratic_detonation_check = ctk.CTkCheckBox(self.warbond_states_frame, text="Democratic Detonation", variable=self.democratic_detonation_var, command= self.save_warbonds)
        self.democratic_detonation_check.grid(row=4, column=0, sticky="w", padx=10, pady=(0,5))
        self.polar_patriots_check = ctk.CTkCheckBox(self.warbond_states_frame, text="Polar Patriots", variable=self.polar_patriots_var, command= self.save_warbonds)
        self.polar_patriots_check.grid(row=5, column=0, sticky="w", padx=10, pady=(0,5))
        self.viper_commandos_check = ctk.CTkCheckBox(self.warbond_states_frame, text="Viper Commandos", variable=self.viper_commandos_var, command= self.save_warbonds)
        self.viper_commandos_check.grid(row=6, column=0, sticky="w", padx=10, pady=(0,5))
        self.freedoms_flame_check = ctk.CTkCheckBox(self.warbond_states_frame, text="Freedoms Flame", variable=self.freedoms_flame_var, command= self.save_warbonds)
        self.freedoms_flame_check.grid(row=7, column=0, sticky="w", padx=10, pady=(0,5))
        self.chemical_agents_check = ctk.CTkCheckBox(self.warbond_states_frame, text="Chemical Agents", variable=self.chemical_agents_var, command= self.save_warbonds)
        self.chemical_agents_check.grid(row=8, column=0, sticky="w", padx=10, pady=(0,5))
        self.truth_enforcers_check = ctk.CTkCheckBox(self.warbond_states_frame, text="Truth Enforcers", variable=self.truth_enforcers_var, command= self.save_warbonds)
        self.truth_enforcers_check.grid(row=9, column=0, sticky="w", padx=10, pady=(0,5))
        self.urban_legends_check = ctk.CTkCheckBox(self.warbond_states_frame, text="Urban Legends", variable=self.urban_legends_var, command= self.save_warbonds)
        self.urban_legends_check.grid(row=10, column=0, sticky="w", padx=10, pady=(0,5))

        # self.superstore_button = ctk.CTkButton(self.warbond_states_frame, text="Superstore Purchases", command=self.open_superstore_filter_popup)
        # self.superstore_button.grid(column=0, sticky="S")


    # Enable or disable gear options based on master checkbox state
    def toggle_gear_options(self):
        # Enable or disable all gear options based on the master checkbox state
        state = "normal" if self.randomize_gear_master_check.get() else "disabled"
        self.primary_check.configure(state=state)
        self.secondary_check.configure(state=state)
        self.grenade_check.configure(state=state)
        self.armor_check.configure(state=state)
        self.booster_check.configure(state=state)

        # If disabling, uncheck all options and trigger their respective toggles
        if state == "disabled":
            print("=== Disabling Gear Randomization ===")
            self.primary_check.deselect()
            self.toggle_primary()
            self.secondary_check.deselect()
            self.toggle_secondary()
            self.grenade_check.deselect()
            self.toggle_grenade()
            self.armor_check.deselect()
            self.toggle_armor()
            self.booster_check.deselect()
            self.toggle_booster()
            print("===================")
            
        else:
            print("=== Enabling Gear Randomization ===")

        
    def toggle_primary(self):
        state = "normal" if self.primary_var.get() else "disabled"
        self.primary_filter_button.configure(state=state)
        # Debug message
        print(f"Primary Randomization: {'Enabled' if self.primary_var.get() else 'Disabled'}")

    def toggle_secondary(self):
        state = "normal" if self.secondary_var.get() else "disabled"
        self.secondary_filter_button.configure(state=state)
        print(f"Secondary Randomization: {'Enabled' if self.secondary_var.get() else 'Disabled'}")

    def toggle_grenade(self):
        state = "normal" if self.grenade_var.get() else "disabled"
        self.grenade_filter_button.configure(state=state)
        print(f"Grenade Randomization: {'Enabled' if self.grenade_var.get() else 'Disabled'}")

    def toggle_armor(self):
        state = "normal" if self.armor_var.get() else "disabled"
        self.armor_filter_button.configure(state=state)
        print(f"Armor Randomization: {'Enabled' if self.armor_var.get() else 'Disabled'}")

    def toggle_booster(self):
        state = "normal" if self.booster_var.get() else "disabled"
        self.booster_filter_button.configure(state=state)
        print(f"Booster Randomization: {'Enabled' if self.booster_var.get() else 'Disabled'}")

    # Enable or disable stratagem options based on master checkbox state
    def toggle_stratagem_options(self):
        state = "normal" if self.randomize_stratagem_master_check.get() == 1 else "disabled"
        self.limit_support_check.configure(state=state)
        self.guarantee_support_check.configure(state=state)
        self.limit_backpack_check.configure(state=state)
        self.guarantee_backpack_check.configure(state=state)
        self.sentry_check.configure(state=state)
        self.anti_tank_check.configure(state=state)
        self.explosive_check.configure(state=state)
        self.limit_vehicle_check.configure(state=state)
        self.vehicle_check.configure(state=state)
        self.sentry_filter_button.configure(state=state)
        self.vehicle_filter_button.configure(state=state)
        if state== "disabled":
            print("=== Disabling Stratagem Options ===")
            self.limit_support_check.deselect()
            self.guarantee_support_check.deselect()
            self.limit_backpack_check.deselect()
            self.guarantee_backpack_check.deselect()
            self.sentry_check.deselect()
            self.anti_tank_check.deselect()
            self.explosive_check.deselect()
            self.limit_vehicle_check.deselect()
            self.vehicle_check.deselect()
            print("===================")
        else:
            print("=== Enabling Stratagem Options ===")



        # Example function to show the filter popup
    def open_primary_filter_popup(self):
        PrimaryFilterPopup(self, self.primary_filter_states)
    def open_secondary_filter_popup(self):
        SecondaryFilterPopup(self, self.secondary_filter_states)
    def open_grenade_filter_popup(self):
        GrenadeFilterPopup(self, self.grenade_filter_states)
    def open_armor_filter_popup(self):
        ArmorFilterPopup(self, self.armor_filter_states)
    def open_booster_filter_popup(self):
        BoosterFilterPopup(self, self.booster_filter_states)
    def open_sentry_filter_popup(self):
        SentryFilterPopup(self, self.sentry_filter_states)
    def open_vehicle_filter_popup(self):
        VehicleFilterPopup(self, self.vehicle_filter_states)

    # def open_superstore_filter_popup(self):
    #     if self.superstore_popup is None or not self.superstore_popup.winfo_exists():
    #         # Create a new instance if it doesn't exist or has been destroyed
    #         self.superstore_popup = SuperstoreFilterPopup(self, self.superstore_states)
        
    #     self.superstore_popup.deiconify()  # Show the popup

        # method for generating loadout
    def find_loadout(self):
        # Call the randomizer function, passing the necessary variables
        loadout = randomize_items(
            primary_var=self.primary_var.get(),
            secondary_var=self.secondary_var.get(),
            grenade_var=self.grenade_var.get(),
            armor_var=self.armor_var.get(),
            booster_var=self.booster_var.get(),
            stratagem_var=self.stratagem_var.get(),
            one_support_var=self.one_support_var.get(),
            g_support_var=self.g_support_var.get(),
            one_backpack_var=self.one_backpack_var.get(),
            g_backpack_var=self.g_backpack_var.get(),
            g_sentry_var=self.g_sentry_var.get(),
            g_tank_var=self.g_tank_var.get(),
            g_explosive_var=self.g_explosive_var.get(),
            one_vehicle_var=self.one_vehicle_var.get(),
            g_vehicle_var=self.g_vehicle_var.get(),
            primary_filter_states=self.primary_filter_states,
            secondary_filter_states=self.secondary_filter_states,
            grenade_filter_states=self.grenade_filter_states,
            armor_filter_states=self.armor_filter_states,
            booster_filter_states=self.booster_filter_states,
            sentry_filter_states=self.sentry_filter_states,
            vehicle_filter_states=self.vehicle_filter_states,
            warbond_states=self.warbond_states,
            # superstore_states=self.superstore_states
            )

        # Update output labels with loadout data using class attributes
        if 'Primary Weapon' in loadout:
            self.output_primary.configure(text=f"{loadout['Primary Weapon'].name}")
            self.output_primary_sub.configure(text=f"{loadout['Primary Weapon'].subclass}")
        else:
            self.output_primary.configure(text=f"Primary Output")
            self.output_primary_sub.configure(text=f"Subclass:")

        if 'Secondary Weapon' in loadout:
            self.output_secondary.configure(text=f"{loadout['Secondary Weapon'].name}")
            self.output_secondary_sub.configure(text=f"{loadout['Secondary Weapon'].subclass}")
        else:
            self.output_secondary.configure(text=f"Secondary Output")
            self.output_secondary_sub.configure(text=f"Subclass:")
        
        if 'Grenade' in loadout:
            self.output_grenade.configure(text=f"{loadout['Grenade'].name}")
        else:
            self.output_grenade.configure(text=f"Grenade Output")
        
        if 'Armor' in loadout:
            self.output_armor.configure(text=f"{loadout['Armor'].name}")
            self.output_armor_des.configure(text=f"{loadout['Armor'].description}")
        else:
            self.output_armor.configure(text="Armor Output")
            self.output_armor_des.configure(text="Description\n")

        if 'Booster' in loadout:
            self.output_booster.configure(text=f"{loadout['Booster'].name}")
            self.output_booster_des.configure(text=f"{loadout['Booster'].description}")
        else:
            self.output_booster.configure(text=f"Booster Output")
            self.output_booster_des.configure(text=f"Description")

        # Update stratagems section with images and descriptions
        if 'Stratagems' in loadout:
            self.update_all_stratagems(loadout['Stratagems'])
        else:
            self.output_Stratagem1_image.configure(image=self.default_stratagem1_image_tk)
            self.output_stratagem1_output.configure(text=f"Stratagem Selection")
            self.output_Stratagem2_image.configure(image=self.default_stratagem2_image_tk)
            self.output_stratagem2_output.configure(text=f"Stratagem Selection")
            self.output_Stratagem3_image.configure(image=self.default_stratagem3_image_tk)
            self.output_stratagem3_output.configure(text=f"Stratagem Selection")
            self.output_Stratagem4_image.configure(image=self.default_stratagem4_image_tk)
            self.output_stratagem4_output.configure(text=f"Stratagem Selection")


    def update_stratagem(self, label_image, label_text, stratagem):
        # Use the image path directly from the stratagem object
        stratagem_image_path = stratagem.image_name  # This is already the full path
        support_subclass = "Support"
        sentry_subclass = ["Sentry", "Emplacement", "Mines", "Exosuit"]
        special_exception = ["Shield Generator Relay", "Tesla Tower", "HMG Emplacement"]

        try:
            # Load the image using PIL directly from the path
            stratagem_image = Image.open(stratagem_image_path)
            # Convert it to CTkImage for display
            stratagem_image_tk = ctk.CTkImage(stratagem_image, size=(60, 60))
            label_image.configure(image=stratagem_image_tk)

            # Save the image reference to the instance to prevent garbage collection
            self.current_stratagem_image_tk = stratagem_image_tk
        except FileNotFoundError:
            print(f"Error: Image {stratagem_image_path} not found.")
        
        # Update the label text with stratagem details
        if stratagem.name in special_exception:
            label_text.configure(text=f"{stratagem.name}")
        elif stratagem.subclass == support_subclass:
            label_text.configure(text=f"{stratagem.name}")
        elif stratagem.subclass in sentry_subclass:
            label_text.configure(text=f"{stratagem.name} {stratagem.subclass}")
        else:   
            label_text.configure(text=f"{stratagem.subclass} {stratagem.name}")
        
    
    def update_all_stratagems(self, stratagems):
        self.update_stratagem(self.output_Stratagem1_image, self.output_stratagem1_output, stratagems[0])
        self.update_stratagem(self.output_Stratagem2_image, self.output_stratagem2_output, stratagems[1])
        self.update_stratagem(self.output_Stratagem3_image, self.output_stratagem3_output, stratagems[2])
        self.update_stratagem(self.output_Stratagem4_image, self.output_stratagem4_output, stratagems[3])

    def toggle_section(self, subclass_var, subclass_frame):
        # Toggle all checkboxes in the section based on the section checkbox
        for widget in subclass_frame.winfo_children():
            if isinstance(widget, ctk.CTkCheckBox):
                widget.select() if subclass_var.get() else widget.deselect()

    def save_warbonds(self):
        data = {name: var.get() for name, var in self.warbond_states.items()}
        
        with open("Warbonds.json", "w") as file:
            json.dump(data, file, indent=4)

    def load_warbonds(self):
        if os.path.exists("Warbonds.json"):
            with open("Warbonds.json", "r") as file:
                data = json.load(file)

            for name, var in self.warbond_states.items():
                var.set(data.get(name, False))

    # def load_superstore(self):
    #     # Create an instance of SuperstoreFilterPopup to call load_superstore_data
    #     popup = SuperstoreFilterPopup(self, self.superstore_states)
    #     popup.load_superstore()

# Run the application
if __name__ == "__main__":
    app = LoadoutRandomizerApp()
    app.mainloop()
