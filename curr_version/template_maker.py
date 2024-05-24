
import json

def make_new_template():
    print("\n----------NEW TEMPLATE----------\n")
    new_temp = {}
    temp_name = input("Enter the name for new template: ")
    cnt_bd = int(input("Enter amount of objects: "))
    new_temp["temp_name"] = temp_name

    for i in range(cnt_bd):
        bd_name = input(f"Enter the name for object {i+1}: ")
        new_temp[bd_name] = {}
        bd_mass = int(input(f"Enter the mass for object {i+1}(in SM; 1 SM = 1.99e30 kg): "))
        bd_x = int(input(f"Enter the X cord for object {i+1}(from -500 px to 500 px; 1 px = 50000 km): "))
        bd_y = int(input(f"Enter the Y cord for object {i+1}(from -500 px to 500 px; 1 px = 50000 km): "))
        bd_vel = list(map(int, input(f"Enter the velocity vector for object {i+1}(exmpl: \"500, 500\"): ").split()))
        bd_rad = int(input(f"Enter the radius for object {i+1}(in SR; 1 SR = 696340 km): "))
        bd_color = list(map(int, input(f"Enter the color in RGB format for object {i+1}(exmpl: \"255, 255, 255\"): ").split()))

        new_temp[bd_name]["mass"] = bd_mass
        new_temp[bd_name]["x"] = bd_x
        new_temp[bd_name]["y"] = bd_y
        new_temp[bd_name]["vel"] = bd_vel
        new_temp[bd_name]["rad"] = bd_rad
        new_temp[bd_name]["color"] = bd_color

    with open(f"templates\\{temp_name}.json", "w", encoding="utf-8") as file:
        json.dump(new_temp, file)
    
    temp_list = open("templates\\templates_list.txt", "a")
    temp_list.write(f"{temp_name}.json\n")
    temp_list.close()
    print("Template was created successfully")