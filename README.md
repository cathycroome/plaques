# Plaques

A small web app that picks you a random UK blue plaque to go and visit, based on the current month, a centre point of your choosing, and how far you're willing to travel.

**Live app:** https://plaques-x80r.onrender.com/

Plaque data comes from [OpenPlaques](https://openplaques.org/), an open dataset of commemorative plaques. This repo currently uses a static CSV snapshot for the United Kingdom (`open-plaques-United-Kingdom-2025-12-14.csv`).

## Logic

For a given plaque location (lat/long) and a centre point (lat/long):

- `relative_location` subtracts the centre point from the plaque location, giving a raw offset in degrees of lat/long.
- `degrees_to_km` converts that offset into an approximate distance in km. Lines of latitude are roughly evenly spaced everywhere, but lines of longitude converge towards the poles — 1° of longitude is about 111 km at the equator and 0 km at the poles, shrinking as roughly `111 km × cos(latitude)`. The code uses `111 km × cos(latitude)` as an approximation (using the plaque's own latitude, not the centre point's, to keep things simple).
- `cartesian_to_polar` turns the resulting (x, y) offset in km into a distance (`km`) and bearing (`theta_deg`).
- `get_filtered_data` selects the relevant columns from the raw OpenPlaques CSV, drops rows missing coordinates/subject/colour, and appends the calculated `km` and `theta_deg` (relative to whichever centre point was supplied), plus a ready-made Google Maps link.
- `get_plaques_for_month` filters that data down to plaques whose bearing falls in the given month's range and whose distance is under a chosen `max_distance`, with an option to restrict to blue plaques only.
- `random_plaque` picks one plaque at random from whatever matches.

Because `km`/`theta_deg` depend on the centre point, they're recalculated per request in the `/random` route rather than once at startup — the raw CSV is still only loaded once.

To test locally, cd to code, run `python app.py` then open http://localhost:5001.
