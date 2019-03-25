#! python3

import requests
import argparse
import sys
import turtle
import time


def get_astronauts():
    astro_data = requests.get("http://api.open-notify.org/astros.json")
    return astro_data.json()


def get_coordinates():
    coord_data = requests.get("http://api.open-notify.org/iss-now.json")
    return coord_data.json()

def indy_time():
    coords = {'lat': 39.7684, 'lon': -86.1581}
    request = requests.get("http://api.open-notify.org/iss-pass.json", params=coords)
    passover = time.ctime(request.json()['response'][0]['risetime'])
    return passover

def world_map():
    data = get_coordinates()
    position = data['iss_position']
    longitude = position['longitude']
    latitude = position['latitude']
    world = turtle.Screen()
    world.bgpic('map.gif')
    world.setup(720, 360)
    world.setworldcoordinates(-180, -90, 180, 90)
    world.register_shape('iss.gif')

    iss = turtle.Turtle()
    iss.shape('iss.gif')
    iss.setheading(90)
    iss.penup()
    iss.goto(float(longitude), float(latitude))

    indy = turtle.Turtle()
    indy.penup()
    indy.color('yellow')
    indy.goto(-86.1581, 39.7684)
    indy.shape('circle')
    indy.shapesize(0.2)
    indy.write(indy_time())
    world.exitonclick()

def create_parser():
    """Creates an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--astro', help='finds astronauts', action='store_true')
    parser.add_argument('-c', '--coords', help='finds coordinates', action='store_true')
    parser.add_argument('-m', '--map', help='displays world map', action='store_true')
    return parser


def main(args):
    parser = create_parser()
    parsed_args = parser.parse_args(args)

    if parsed_args.astro:
        astronauts = get_astronauts()
        for astronaut in astronauts['people']:
            print("Astronaut {} is aboard the {}".format(astronaut['name'], astronaut['craft']))
        print("Number of astronauts in space: {}".format(astronauts['number']))
    elif parsed_args.coords:
        coordinates = get_coordinates()
        print("The ISS is located at latitude {} and longitude {} on {}"
              .format(coordinates['iss_position']['latitude'],
                      coordinates['iss_position']['longitude'],
                      time.ctime(coordinates['timestamp'])))
    elif parsed_args.map:
        date = indy_time()
        world_map()
        print("The ISS will pass over Indianapolis, IN on {}".format(date))


if __name__ == '__main__':
    main(sys.argv[1:])
