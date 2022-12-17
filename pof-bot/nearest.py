import numpy as np
import csv


POST_OFFICES = {}
POST_OFFICES_LOCATIONS = []

def init_data():
    with open("Post_offices.csv", 'r', newline="") as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|')

        for row in reader:
            lat = float(row["lat"])
            lng = float(row["lng"])

            key = f"{lat}:{lng}"

            POST_OFFICES.update({
                key: row
            })

    for post_office in POST_OFFICES.values():
        lat = float(post_office["lat"])
        lng = float(post_office["lng"])

        POST_OFFICES_LOCATIONS.append((lat, lng))


def get_nearest(lat, lng):
    A = np.array(POST_OFFICES_LOCATIONS)

    leftbottom = np.array((lat, lng))

    distances = np.linalg.norm(A-leftbottom, axis=1)
    min_index = np.argmin(distances)
    
    lat, lng = A[min_index]

    key = f"{lat}:{lng}"
    return POST_OFFICES[key]

init_data()
