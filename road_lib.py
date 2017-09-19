#!/usr/bin/env/python
"""
Title:
    Python script for simulating road

Assumption:
    1. All the python packages are installed
    2. You are using python==2.7.11
    3. Any more assumptions <>

Description:
    1. Describe the class

"""
import csv
import logging
import matplotlib.pyplot as plt
import math

# import log_lib
from math import pi

# For logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class RoadPoint(object):
    def __init__(self, x1, y1, x2, y2, lw, speed, curvature=0):
        """
        Class to store road points
        Stores the location of left/right lane point

        Args:
            x (float): Location of x co-ordinate of left lane in meters
            y (float): Location of y co-ordinate of left lane in meters
            lw (float): Lane width in meters
            speed (float): Speed of car in meters second at that point
            curvature (float): Curvature of road in degrees
        """
        self.x1 = float(x1)
        self.y1 = float(y1)
        self.x2 = x2
        self.y2 = y2

        self.lane_width = float(lw)
        self.speed = speed
        self.curvature = curvature

    @property
    def curve_radians(self):
        """float: returns the angle of road in radians"""
        return math.radians(self.curvature)

    @property
    def coordinates(self):
        """tuple: returns the road location of let and right lane points as x1, y1, x2, y2"""
        return self.x1, self.y1, self.x2, self.y2

    def __str__(self):
        return "({self.x1}, {self.y1})({self.x2}, {self.y2})".format(**locals())

    def __repr__(self):
        return self.__str__()


class Road(list):
    def __init__(self, values=None, name=None):
        """
        To store road points in a list

        Args:
            name (str): Name of the road
            values (list): The values with to initialise the road
        """
        values = values if values is not None else list()
        super(Road, self).__init__(values)
        self.name = name

    @property
    def coordinates(self):
        """list: returns list of road points as left lane(x,y) then right lane"""
        coords = []
        for item in self:
           coords.append(item.coordinates)
        return coords

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


def read_centre_lane(file_path):
    """
        To read road from a csv file
        Column format -  X,Y,Lane_width,v
        where x and y are location of left lane point and v is the speed of car at that point

        Args:
            file_path (str): Path of the file
        """

    logger.info("Loading file {file_path}".format(**locals()))
    with open(file_path) as f:
        reader = csv.reader(f)

        road_info = []

        for idx, row in enumerate(reader):
            logger.info(row)
            # Skip first two rows, first row is header
            # To calc curvature u need to speed 1st row
            if idx < 1:
                continue
            try:
                x, y, lw, speed = row
                road_info.append([float(x), float(y), float(lw), float(speed)])

            except Exception as e:
                logger.exception("Ignoring row number - {i}".format(i=idx + 1))

    return road_info


def read_road(centre_lane):
    """
    To read road from a csv file
    Column format -  X,Y,Lane_width,v
    where x and y are location of left lane point and v is the speed of car at that point

    Args:
        file_path (str): Path of the file
    """

    # logger.info("Loading file {file_path}".format(**locals()))

    # road_info = read_centre_lane(file_path)
    road_info = centre_lane

    # Arrays
    road = Road(name="Sample_Road")

    calc_lw_arr = []

    # Go through all points
    for idx, row in enumerate(road_info[1:], 1):
        # Get the current road point
        # To calc curvature u need to skip 1st row
        curr_x, curr_y = row

        curr_lane_width, curr_speed = 0.3, 1

        # Get previous point
        prev_x, prev_y = road_info[idx - 1]

        prev_lane_width, prev_speed = 0.3, 1

        # Calculate curvature
        curve = math.atan2(float(curr_y - prev_y), float(curr_x - prev_x))
        curve_deg = math.degrees(curve)

        # Calculate lw curve (90 - curve)
        lw_curve_deg = 90.0 - curve_deg
        lw_curve_rad = math.radians(lw_curve_deg)

        # Left lane x
        left_x = curr_x - (math.cos(lw_curve_rad) * (curr_lane_width/2))
        left_y = curr_y + (math.sin(lw_curve_rad) * (curr_lane_width/2))

        # Right lane x
        right_x = curr_x + (math.cos(lw_curve_rad) * (curr_lane_width / 2))
        right_y = curr_y - (math.sin(lw_curve_rad) * (curr_lane_width / 2))

        road_point = RoadPoint(left_x, left_y, right_x, right_y, curr_lane_width, curr_speed, lw_curve_deg)
        road.append(road_point)
        calc_lw = math.sqrt((left_x - right_x) ** 2 + (left_y - right_y) ** 2)
        calc_lw_arr.append(calc_lw)

    return road


def control_simulator(car_loc, speed, steer_angle):
    """
    To simulate a control dll

    Args:
        car_loc (tuple): Tuple of x/y coordinate
        speed (float): Speed of the car in m/s
        steer_angle (int): Angle in degree, absolute angle and not the angle of the steering wheel
    """

    # Calculate the new location of the car using speed/old_car location and steer angle
    car_x1, car_y1 = car_loc
    steer_radians = math.radians(steer_angle)
    car_x2 = car_x1 + (speed * math.cos(steer_radians))
    car_y2 = car_y1 + (speed * math.sin(steer_radians))

    return car_x2, car_y2


def lane_dist(road_point, car_loc):
    """
    To calculate lane distance

    Args:
        road_point (tuple): Tuple of road points x1,y1,x2,y2 , 1 for left and 2 for right point, where car
        car_loc (tuple): Tuple of x/y coordinate
    """

    left_x1, left_y1, right_x1, right_y1 = road_point

    car_x1, car_y1 = car_loc

    # Apply pythagoras theorem to find the shortest distance to the left lane point
    # TODO: Do we calculate from the line equation as the above is a generous approx
    left_lane_dist = math.sqrt((left_x1 - car_x1) ** 2 + (left_y1 - car_y1) ** 2)
    right_lane_dist = math.sqrt((right_x1 - car_x1) ** 2 + (right_y1 - car_y1) ** 2)

    return left_lane_dist, right_lane_dist


def plot_road(road_points, car_loc_points, lane_dist_array=None, scatter=True):
    """
    To plot road and location of car in the road

    Args:
        lane_dist_array (list): Dist from left lane and right lane as tuple. Should be of same length as road points
        and car loc
        car_loc_points (list): Location of car as x,y
        road_points (List[tuple]): Tuple of road points x1,y1,x2,y2 , 1 for left and 2 for right point, where car
    """
    max_x = max([max(a[0], a[2]) for a in road_points])
    max_y = max([max(a[1], a[3]) for a in road_points])

    min_x = min([min(a[0], a[2]) for a in road_points])
    min_y = min([min(a[1], a[3]) for a in road_points])

    # Lets keep absolute minimum so axes are of same length so no viewing error
    abs_min = min(min_y, min_x)
    abs_max = max(max_y, max_x)

    # Using -1 and +1 as min/max so we can see origin/end clearly
    plt.axis([abs_min - 1, abs_max + 1, abs_min - 1, abs_max + 1])
    plt.ion()

    # Plot the road
    left_lane_x = [a[0] for a in road_points]
    left_lane_y = [a[1] for a in road_points]
    right_lane_x = [a[2] for a in road_points]
    right_lane_y = [a[3] for a in road_points]

    # Plot lanes
    plt.plot(left_lane_x, left_lane_y)
    plt.plot(right_lane_x, right_lane_y)

    # For lane distance text
    if lane_dist_array:
        right_dist = left_dist = 0
        first_lane_dist = True

    for idx, point in enumerate(car_loc_points):
        plt.pause(0.001)

        if scatter:
            point_x1, point_y1 = point
            plt.scatter(point_x1, point_y1)
        else:
            car_x_arr = [a[0] for a in car_loc_points[:idx]]
            car_y_arr = [a[1] for a in car_loc_points[:idx]]
            plt.plot(car_x_arr, car_y_arr)

        if lane_dist_array:
            # Plot lane distance only if value changes
            if first_lane_dist:
                left_dist, right_dist = lane_dist_array[idx]
                first_lane_dist = False
            else:
                if lane_dist_array[idx - 1] == lane_dist_array[idx]:
                    continue
                left_dist, right_dist = lane_dist_array[idx]

            # For lane distance just scatter slightly away from car location point by some value
            # Hit and tried based on the value being printed
            plt.text(point_x1 - 1, point_y1, "{0:.2f} m".format(left_dist))
            plt.text(point_x1 + 0.1, point_y1, "{0:.2f} m".format(left_dist))

    # Now connect line of car points
    car_loc_x = [a[0] for a in car_loc_points]
    car_loc_y = [a[1] for a in car_loc_points]
    plt.plot(car_loc_x, car_loc_y)

    plt.ioff()
    plt.show()
    a = 23


def write_circular_road(radius, num_points=100, speed=1, lw=3, name="circle.csv"):
    """To write a circular road for testing road parsing"""
    points = [(math.cos(2 * pi / num_points * x) * radius, math.sin(2 * pi / num_points * x) * radius)
              for x in xrange(0, num_points + 1)]

    with open(name, 'w') as f:
        f.write("X,Y,Lane_width,v")
        for point in points:
            f.write(",".join([str(point[0]), str(point[1]), str(lw), str(speed)]) + "\n")
    return True


if __name__ == '__main__':
    logger = log_lib.console_logger(__name__, logging.DEBUG)
    logger.setLevel(logging.INFO)

    # Generate a circular road of radius 10 m
    write_circular_road(10)

    file_path = "sample_road_curve4.csv"
    road = read_road(file_path)

    centre_lane = read_centre_lane(file_path)
    car_loc_points = [[i[0], i[1]] for i in centre_lane]

    plot_road(road.coordinates, car_loc_points, scatter=False)

