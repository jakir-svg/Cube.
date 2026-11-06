


class adminpanel:
    def __init__(self,vehicles):
        self.vehicles=vehicles
            # add new vehicles
        
    def add_vehicle(self,vid,vtype, vmodel, vyear, vrent):

        self.vehicles[vid] = {
            "vehicle_id": vid,
            "vehicle type": vtype,
            "vehicle model": vmodel,
            "vehicle year": vyear,
            "vehicle rent": vrent,
            "vehicle status": "available"
        }
        print("Vehicle added successfully. {vid} : {vtype}".format(vid=vid, vtype=vtype))
    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)
    def view_inventory(self):
        for vehicle, data in self.vehicles.items():
             print(("Vehicle ID: {vid}, Type: {vtype}, Model: {vmodel}, Year: {vyear}, Rent: {vrent}, Status: {vstatus}".format)(
                  vid=data["vehicle_id"],
                 vtype=data["vehicle type"],
                 vmodel=data["vehicle model"],
                 vyear=data["vehicle year"],
                 vrent=data["vehicle rent"],
                 vstatus=data["vehicle status"]))
        return self.vehicles
if __name__ == "__main__":
    vehicles = {}
    admin = adminpanel(vehicles)
    admin.add_vehicle("V001", "Car", "Toyota", 2020, 100)
    admin.add_vehicle("V002", "Bike", "HOnda", 2021, 50)
    admin.view_inventory()