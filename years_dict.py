def read_file(path: str) -> dict:
    """
    returns a dictionary with keys that have a year,
    with values the movie name and location
    """
    with open(path, "r", encoding="latin-1") as f:
        data = f.readline()
        while not data.startswith("="):
            data = f.readline()
        year_dict = {}
        for line in f:
            if line.count("(") >= 2:
                continue
            if not line.startswith('\"'):
                break
            if "{" in line:
                continue
            ind = line.find("(") + 1
            year = line[ind: ind+4].strip()
            name_of_film = line[: ind-1].strip()
            location_of_film = (line[ind+5:]).replace("\t", "").strip()
            if year not in year_dict:
                year_dict[year] = [(name_of_film, location_of_film)]
            else:
                year_dict[year].append((name_of_film, location_of_film))
    return year_dict


def films_locations(year_dict: dict, year: str) -> dict:
    """
    returns a dictionary with keys with location and values with movie name.
    Works with appropriately specified year
    """
    film_location = {}
    for i in range(len(year_dict[year])):
        if year_dict[year][i][0] not in film_location:
            film_location[year_dict[year][i][0]] = [year_dict[year][i][1]]
        else:
            film_location[year_dict[year][i][0]].append(year_dict[year][i][1])
    return film_location


YEAR_DICT = read_file('locations.list')
