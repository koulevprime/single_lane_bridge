#UI.py
#
#Written by Madeline Cameron and Doug McGeehan
#CS 384 - Distributed Operating Systems
#Spring 2014


import cocos
from VehicleManager import *
from cocos.director import director
from cocos.draw import Line
from cocos.scene import Scene
from pyglet.window import key


class RoadPoints:
    SW = 100, 100
    NW = 100, 400
    SE = 500, 100
    NE = 500, 400

    # Intersections of the road with the bridge.
    W = 200, 250
    E = 400, 250

    ROADMAP = [
        [W, NW],
        [NW, SW],
        [SW, W],
        [W, E],
        [E, SE],
        [SE, NE],
        [NE, E],
    ]

class UI:
    class Canvas(cocos.draw.Canvas):
        def render(self):
            print("Creating canvas...")
            x, y = director.get_window_size()
            color = 255, 255, 255, 255 #Color of lines / roads
            width = 3 #How wide the roads are drawn

            for start, end in RoadPoints.ROADMAP:
                self.set_color(color)
                self.set_stroke_width(width)
                self.move_to(start)
                self.line_to(end)
            print("Road map drawn!")

    class Layer(cocos.layer.Layer):
        def __init__(self, vehicleManager):
            super(UI.Layer, self).__init__()

            self.label_pos_y = 450
            self.label_step = 20
            self.label_color = (255, 255, 255, 255)
            self._vehManage = vehicleManager

            print("Creating layer...")

            self.add(UI.Canvas())
            self.schedule(lambda x: 0)
            print("Canvas added!")

            print("Adding vehicles...")
            for vehicle in vehicleManager.vehicleList:
                self.add(vehicle.sprite)
                print("Vehicle " + str(vehicle.index) + " added!")

            print("Layer created!")

        def redraw_speed(self, vehicle):
            vehicle.speed_label.element.text = str(vehicle.speed)

        def create_speed_label(self, vehicle=None, vehManage=None):
            to_create_list = []
            if vehManage is not None:
                for vehicle in vehManage.vehicleList:
                    to_create_list.append(vehicle)
            else:
                to_create_list.append(vehicle)

            for vehicle in to_create_list:
                print("Creating speed label for vehicle" + str(vehicle.index) + "...")
                speedLabel = cocos.text.Label("Vehicle " + str(vehicle.index) + "'s speed: ", position=(460, self.label_pos_y),
                                          color=self.label_color)
                speedText = cocos.text.Label(str(vehicle.speed), position=(600, self.label_pos_y),
                                               color=self.label_color)
                self.add(speedLabel)
                self.add(speedText)

                self.label_pos_y -= self.label_step

                vehicle.speed_label = speedText

        def create_vehicle_label(self, vehicle=None, vehManage=None):
            to_create_list = []
            if vehManage is not None:
                for vehicle in vehManage.vehicleList:
                    to_create_list.append(vehicle)
            else:
                to_create_list.append(vehicle)

            for vehicle in to_create_list:
                index = self._vehManage.vehicleList.index(vehicle)
                vehicleLabel = cocos.text.Label(str(index), position=(vehicle.sprite.position[0] + 10,
                                                                      vehicle.sprite.position[1] + 10),
                                                color=self.label_color)
                vehicle.label = vehicleLabel
                self.add(vehicleLabel)

        def add_vehicle(self, vehicle):
            self.add(vehicle.sprite)
            print("Vehicle " + str(vehicle.index) + " added!")

    class Event_Handler(cocos.layer.Layer):
        is_event_handler = True
        def __init__(self, vehicleManage):
            super(UI.Event_Handler, self).__init__()

            self.vehManage = vehicleManage

        def on_close(self):
            self.vehManage.stop()

        def on_key_press(self, keyp, mod):
            if keyp == key.NUM_ADD: #Set positive speed modifier
                self._modifier = 1
            if keyp == key.NUM_SUBTRACT: #Set negative speed modifier
                self._modifier = -1
            if (keyp >= 65456 and keyp <= 65465): #Numpad 1 - 9. Modify vehicle speed
                index = keyp - 65456 #Get vehicleList index
                if self._modifier != None:
                    new_speed = self.vehManage.vehicleList[index].speed + (10 * self._modifier)
                    print("Modifying vehicle speed by " + str(new_speed))
                    self.vehManage.vehicleList[index].speed = new_speed
                    self.vehManage.layer.redraw_speed(vehicle=self.vehManage.vehicleList[index])
                else:
                    print("Please use a modifier before attempting to modify speed!")

            if keyp == key.ENTER: #Begin / stop simulation
                print("Starting simulation...")
                self.vehManage.start()
                #for vehicle in self.vehManage.vehicleList:
                #    vehicle.move()

            if keyp == key.F1: #Add new vehicle
                if len(self.vehManage.vehicleList) < 10:
                    print("Adding new car...")

                    self.vehManage.add_vehicle("left")

            if keyp == key.SPACE: #Switch bridge modes
                self.vehManage.bridge_mode = ~self.vehManage.bridge_mode + 1 #Complement + 1

            if keyp == key.ESCAPE: #Exit application gracefully
                self.vehManage.stop()
                print("Goodbye!")
                sys.exit(384) #;D



def main():
    cocos.director.director.init(caption="CS 384 Project")

    directions = ["left", "right"]
    vehManage = VehicleManager(
      vehicleNum=2,
      speed=10, 
      directions=directions,
      mode=Bridge_Mode.One_at_a_Time
    )
    layer = UI.Layer(vehManage)
    print("Setting layer object...")
    vehManage.layer = layer
    layer.create_speed_label(vehManage=vehManage)
    layer.create_vehicle_label(vehManage=vehManage)
    eventHandler = UI.Event_Handler(vehManage)

    color_layer = cocos.layer.ColorLayer(0,104,10, 0)
    print("Starting scene...")
    scene = Scene(eventHandler, color_layer, layer)
    print("Running scene...")
    # I don't think we need threading.
    #UIThread = threading.Thread(group=None,target=cocos.director.director.run(scene))
    #UIThread.start()
    cocos.director.director.run(scene)


if __name__ == "__main__":
    # If you run this python script from the command line, then this
    #  if-statement will evaluate to true, in which the main() function
    #  will be executed.
    main()
