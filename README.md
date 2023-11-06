# Project-III.
## Overview
As part of a company in the gaming industry, you have to find a new place to move the office considering the preferences of everyone in the staff.
The company has this following scheme and expressed needs:
- Everyone in the company is between 25 and 40 and want to party.
- 29 people have at least one kid.
- 20 Designers would like to work near other companies that also do design.
- 20 Account Managers: they need to travel a lot.
- 15 Data Engineers.
- 10 Frontend Developers, 5 Backend Developers: they like to be near successful tech startups that have raised at least 1 million dollars.
- 10 Executives: love Starbucks.
- 5 UI/UX Engineers
- 1 Maintenance manager who loves basketball. He will not have a stadium to play, but we'll make sure there are basketball courts close to the office.
- 1 CEO/President, vegan.
- Dog of the office, they need a trim once a month.


## Datasets
[companies.json](data/companies.json).

From the webscrapping I created:
- A [dataset](data/officesSF.csv) with the offices available for rent.
- A MongoDB collection with the geometry of all the neighborhoods.


## Scrapping
[squarefoor.com](https://www.squarefoot.com/office-space/m/ca/san_francisco/1aee3919-edd5-4fad-b301-76f335aae568?minOccupancy=87&maxOccupancy=120&&activeSizeFilter=SEATS&groupByBuilding=false), from page 1 to page 9 (almost 100 offices for rent).


## Workflow
1. First of all, I checked all the companies in the dataset to filter only those companies that have less than 100 employees -as startups, they are medium size companies-, and those that have raised more than one million dolars.

    Once filtered, I checked the countries and cities where there are more companies with these characteristics.

2. After choosing the city, I scrapped a rental estate webpage to know where this new office could be located considering the size of the company and city. I got the addresses and coordinates of these offices, and the coordinates of the neighborhoods that appeared on the webpage. According to the density of offered offices for rent, I had a list of three possible neighborhoods.

3. Prioritisation:
    - Everyone in the company is between 25 and 40 and want to party.

    From those three neighborhoods I chose the one that has more night life according to the [internet](https://www.viajarsanfrancisco.com/salir-de-fiesta-ocio-nocturno.php).

    - 29 people have at least one kid.

    I requested a list of 20 schools close to that neighbourhood. A lot of them had to be ignored, because they weren't eductation institutions for kids or they have closed.

    From the remaining list I checked the distance from every school to each available office, and selected only those offices that weren't further than half a kilometer.

    This process left me with only two possible offices. 

    - 20 Designers would like to work near other companies that also do design.

    There was no company in the category "design" that complied with the rest of the conditions of a startup, and there was only one company tagged with the word "design".

    I chose the office closest to this company.

4. Map creation:

I made requests for the rest of the expressed needs from the staff, only considering those that remain active and open, and only the one that was closest to the office.


## Libraries Used:
- os
- pandas
- requests
- BeautifulSoup, from bs4
- json
- MongoClient, from pymongo 
- load_dotenv, from dotenv
- geopandas
- folium
- Choropleth, Circle, Marker, Icon, Map, from folium
- time
- math


## Results
### Find startup companies and their countries
These were the top five countries and the number of companies they have with the required characteristics.
| country |  count  | 
|---------|---------|
| USA     | 1067    |
| GBR     | 121     |
| ISR     | 43      |
| CAN     | 40      |
| FRA     | 36      |

These are the five top cities in the USA and the amount of companies with the required characteristics.
| city          |  count  | 
|---------------|---------|
| San Francisco | 181     |
| New York      | 120     |
| London        | 72      |
| Seattle       | 42      |
| Palo Alto     | 40      |

### San Francisco rental estate for offices and coworking places
Coordinates and addresses of the offices in the first pages of the site scrapped, ordered by number of employees.

|     | employees | lat       | lon         | address
|-----|-----------|-----------|-------------|-----------
| 114 | 87	      | 37.791582 | -122.394000 | 135 Main Street
| 163 |	87	      | 37.788891 | -122.398100 | 535 Mission Street
| 147 |	87	      | 37.794792 | -122.403684 | 601 Montgomery Street
| 151 | 87	      | 37.791582 | -122.394000 | 135 Main Street
| 1   | 87	      | 37.784463 | -122.242628 | 1830 Embarcadero
| ... |	...	      | ...       | ...         | ...
| 121 | 119	      | 37.790913 | -122.396728 | 350 Mission Street
| 120 | 119	      | 37.790913 | -122.396728 | 350 Mission Street
| 9   | 119	      | 37.795014 | -122.399435 | 1 Embarcadero Center
| 181 | 119	      | 37.790913 | -122.396728 | 350 Mission Street
| 93  | 119	      | 37.790965 | -122.401688 | 225 Bush Street


Most of the offices for rent are located in the Financial District, followed by South Of Market (SoMa) and Mission Bay.
| neighborhoods      |  count  | 
|--------------------|---------|
| Financial District | 137     |
| South Of Market    | 13      |
| Mission Bay        | 7       |
| Downtown           | 4       |
| North San Jose     | 4       |

SoMa is the most recommended neighborhood to go out and party, so I selected the **13 offices placed there**.

### Selection through priorities
1. Schools:
After requesting to foursquare schools near SoMa -20 requests, within a radius of 3700 meters, which is the longest distance this neighborhood has-, and cleaning the results, these where the remaining schools, their names and coordinates:

|     | school_name                         | school_categ      | school_lat | school_lon
|-----|-------------------------------------|-------------------|------------|----------
| 1   | KinderCare Learning Center          | Preschool         | 37.779426  | -122.411882
| 3   | C5 Children's School                | Daycare           | 37.780990  | -122.419214
| 6   | Bessie Carmichael Elementary School | Elementary School | 37.776344  | -122.406468
| 11  | Love & Learn Nursery School         | Daycare           | 37.773386  | -122.414823

There were only **two offices** in less than half a kilometer from some of the schools.

2. Design companies:
For these two remaining offices there was **one that was closer to the only design startup company** with more than 1 million dollars raised.

#### Final office:
|     | employees | lat       | lon         | address           | positions
|-----|-----------|-----------|-------------|-------------------|----------------------
| 143 | 112       | 37.783521 | -122.408109	| 901 Market Street | [-122.408109, 37.783521]

Once the office was chosen all the other requirements were checked using foursquare, to know which were the closest venues for each necessity. 


## Conclusions
The office is located in South Of Market (SoMa) in San Francisco. Its address is [901 Market Street, Suite 500](https://www.squarefoot.com/building/ca/san-francisco/901-market-street/e7cadee9-829c-46b9-8942-109d10b2bd28?listingId=1037813) (price inquiry required).

![Building](image.png)

Every venue is close to the office except for the design company, which is more than a kilometer away, as can be seen in the [map](images/mapa.html).

![Map](image-1.png)