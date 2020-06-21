from PIL import Image, ImageDraw, ImageColor
import numpy as np
import time

def print_waypoints(waypoints, cost, expanded_nodes):
    print(f'Planned path: {waypoints}')
    print(f'Path length: {len(waypoints)}')
    print(f'Total path cost: {cost}')
    print(f'Total nodes expanded: {expanded_nodes}')

class PathPlanPrinter():
    def __init__(self, plan=[], input_file="",
                 output_file="", grid_size=[]):
        '''
            :param plan: list representing the points in the
            path.
            :param input_file: path to the input map.
            :param output_file: optional. path in which to store
            the result.
            :param grid_size: size of the grid.
        '''
        if not plan:
            raise ValueError("Provided plan is empty.")
        if type(plan[0]) is not tuple\
           and type(plan[0]) is not list:
            raise TypeError("Type of points in plan must be"+\
                            " tuple or list.\n"+\
                            "Current type is "+str(type(plan[0])))
        if input_file == "" or type(input_file) is not str:
            raise ValueError("No input file was provided.\n"+\
                             "Unable to print plan.")
        if type(output_file) is not str:
            raise TypeError("Type of output file must be a string.\n"+\
                            "Type of argument provided: "+\
                            str(type(output_file)))
        if output_file == "":
            output_file = '../out/'+input_file.split('/')[-1].split('\\')[-1].split(".")[-2].split('/')[-1]+\
                  '_'+str(time.time())+".png"
        self.plan = plan
        self.img = Image.open(input_file)
        self.img.load()
        self.output_file = output_file
        self.grid_size = grid_size
        self.__plan_drawn = False

    def draw_plan(self):
        if self.__plan_drawn:
            return
        img_d = ImageDraw.Draw(self.img)
        if self.grid_size:
            img = self.img.copy()
            img = img.convert('L')
            npdata = np.asarray(img, dtype='int32')
            grid_color = (150, 150, 150)
            font_size = round((self.grid_size[0]+self.grid_size[1]) // 2)
            if font_size > min(self.grid_size):
                font_size = int(min(self.grid_size))
            tolerance = 12
            offset_x = round(self.grid_size[0]/4)
            offset_y = round(self.grid_size[1]/4)
            for i in range(round(npdata.shape[0]/self.grid_size[0])+1):
                liCoord = round(i * self.grid_size[0])
                img_d.line(((0, liCoord), (self.img.size[0], liCoord)),
                           fill=grid_color)
                if ((self.grid_size[0] < tolerance and i%5 == 0)\
                or self.grid_size[0] >= tolerance) and\
                int(i * self.grid_size[0] + self.grid_size[0]//2) - 2 <npdata.shape[0]:
                    if npdata.item(int(i * self.grid_size[0] + self.grid_size[0]//2) - 2,
                                int(self.grid_size[1]//2) - 2) is 0:
                        font_color = (255, 255, 255)
                    else:
                        font_color = (0, 0, 0)
                    img_d.text((int(i * self.grid_size[1] + offset_x), int(offset_y)),
                               str(i), fill=font_color)
            for j in range(round(npdata.shape[1]/self.grid_size[1])+1):
                colCoord = round(j * self.grid_size[1])
                img_d.line(((colCoord, 0), (colCoord, self.img.size[1])),
                           fill=grid_color)
                if ((self.grid_size[1] < tolerance and j%5 == 0)\
                or self.grid_size[1] >= tolerance) and\
                int(self.grid_size[1]*j+self.grid_size[1]/2) - 20 < npdata.shape[1]:
                    if npdata.item(int(self.grid_size[0]/2) - 2,
                                int(self.grid_size[1]*j+self.grid_size[1]/2) - 20) is 0:
                        font_color = (255, 255, 255)
                    else:
                        font_color = (0, 0, 0)
                    img_d.text((offset_x, int(j * self.grid_size[0] + offset_y)),
                               str(j), fill=font_color)
        img_d.line(self.plan, fill=(155, 0, 100), width=3)
        start = self.plan[0]
        img_d.ellipse([(start[0]-5, start[1]-5),(start[0]+5, start[1]+5)], fill="red")
        img_d.text((start[0]+20, start[1]), "Start", fill="yellow")
        finish = self.plan[-1]
        img_d.ellipse([(finish[0]-5, finish[1]-5),(finish[0]+5, finish[1]+5)], fill="blue")
        img_d.text((finish[0]+20, finish[1]), "Finish", fill="yellow")
        del img_d
        self.__plan_draw = True

    def print_plan(self):
        if not self.__plan_drawn:
            self.draw_plan()
        print("Outputting result to "+self.output_file+".")
        self.img.save(self.output_file, "PNG")
        
        
