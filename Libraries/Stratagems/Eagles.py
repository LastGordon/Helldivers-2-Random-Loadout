from Libraries.InventoryItem import Eagle
from Libraries.Images.ImageLoader import ImageLoader

image_loader = ImageLoader("Libraries/Images")

eagles = [
    Eagle("Strafing Run", ["anti-tank"], "Libraries/Images/Eagle/HD2-ESR.png"),
    Eagle("Airstrike", ["explosive"], "Libraries/Images/Eagle/HD2-EA.png"),
    Eagle("Cluster Bomb", ["none"], "Libraries/Images/Eagle/HD2-ECB.png"),
    Eagle("Napalm Airstrike", ["none"], "Libraries/Images/Eagle/HD2-ENA.png"),
    Eagle("Smoke Strike", ["none"], "Libraries/Images/Eagle/HD2-ESS.png"),
    Eagle("110mm Rocket Pods", ["anti-tank"], "Libraries/Images/Eagle/HD2-ERP.png"),
    Eagle("500kg Bomb", ["explosive", "anti-tank"], "Libraries/Images/Eagle/HD2-E500B.png")
]