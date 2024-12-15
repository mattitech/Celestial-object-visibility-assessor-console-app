import math
from threading import local
from tkinter import CURRENT
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time
from geopy.geocoders import Nominatim
import astropy.units as u
from astroplan import Observer, FixedTarget
from astropy.coordinates import get_body, solar_system_ephemeris    
from astroplan import moon_illumination
import datetime
from astroquery.simbad import Simbad

Simbad.add_votable_fields('ids', 'otype')

def astrodark(altitude):
   #defines a new Time object with the same current date but starts from 17:00

   current_year = datetime.datetime.now().year
   day = datetime.datetime.now().day
   month = datetime.datetime.now().month

   local_time = Time(f"{current_year}-{month}-{day} 16:00:00", scale='utc')
   
   searchHour = local_time.datetime.hour

   while searchHour != 5:
        local_time += 1 * u.minute
        searchHour = local_time.datetime.hour
        sun_radec = get_body(body = "Sun", time = local_time, location = observer_location)
        altaz_frame_sun = AltAz(obstime=local_time, location=observer_location)
        sun_altaz = sun_radec.transform_to(altaz_frame_sun)
        altitude = (sun_altaz.alt).deg

        if altitude > -18:
            continue
        else:
            darktime = local_time
            return darktime
   print("No astronomical darkness in the chosen date")
            
    
        
    

        


def favorites(observer_location, local_time):
    
   
    #put your favorite deep space targets in this array
    dsos = ["M31", "M45", "M33", "M51", "NGC2024", "Orion nebula"]
    #you can also put planets
    planets = ["Jupiter", "Saturn", "Mars", "Venus", "Uranus", "Neptune", "Mercury","Sun"]
    
   
   
    print(" ")
    
    if len(dsos) > 1:
        print("DEEP SPACE OBJECTS")
        print(" ")
        for dso in dsos:
           try:
            dso_position = SkyCoord.from_name(dso)
            altaz_frame = AltAz(obstime=local_time, location=observer_location)
            dso_altaz = dso_position.transform_to(altaz_frame)
    
            print(f"{dso}'s coordinates: |az {dso_altaz.az}, |alt {dso_altaz.alt}", end=" ")
            altitude = dso_altaz.alt.deg
            set_direction_az = rise_set_direction(dso, local_time, observer_location)
            if altitude > 0:
                observer = Observer(location=observer_location)
                target = FixedTarget(coord=dso_position, name=dso)
                set_time = observer.target_set_time(local_time, target, which='nearest')
                set_direction_az = rise_set_direction(dso, set_time.iso, observer_location)
            
                set_direction = cardinal((set_direction_az).deg)
            
                actual_direction = cardinal((dso_altaz.az).deg)
                
                transit_time = observer.target_meridian_transit_time(local_time, target, which='next')
                     

                print(f"|--Visible at {actual_direction}--", end=" ")
                print(f"{dso} transit: {transit_time.iso}', ", end=" ")
                transit_height = max_height(dso, transit_time.iso, observer_location)
                print(f"({transit_height})")

                
                
                print(f"set: {set_time.iso}" , end=" ")
                print(f" {set_direction}")
                print(" ")
        
        
           
            
            else:
                print("|xxUNDER THE HORIZONxx")
            
                observer = Observer(location=observer_location)
                target = FixedTarget(coord=dso_position, name=dso)
                set_time = observer.target_set_time(local_time, target, which='nearest')
                print(f"|rise: {set_time.iso}" , end="")
                set_direction_az = rise_set_direction(dso, set_time.iso, observer_location)
                direction = cardinal((set_direction_az).deg)
                print(f" at {direction}", end=" ")
                transit_time = observer.target_meridian_transit_time(local_time, target, which='next')
                print(f"|{dso} transit: {transit_time.iso}', ", end=" ")
                transit_height = max_height(dso, transit_time.iso, observer_location)
                print(f"({transit_height})") 
        
               
           except:
               print("There was an error with this object:")
    else:
        print("you have no deep space objects in your favorites")
        print(" ")
    
    if len(planets) > 1:
        print(" ")
        print("PLANETS")
        print(" ")
        for plan in planets:
            
            plan_radec = get_body(body = plan, time = local_time, location = observer_location)
            altaz_frame_planets = AltAz(obstime=local_time, location=observer_location)
            planet_altaz = plan_radec.transform_to(altaz_frame_planets)
            altitude = (planet_altaz.alt).deg
            
            actual_direction = cardinal((planet_altaz.az).deg)
            print(f"{plan}'s coordinates - |az:{round(planet_altaz.az.deg, 2)}, |alt:{round(planet_altaz.alt.deg, 2)}", end=" ")
            if(altitude > 0):
                observer = Observer(location=observer_location)
                target = FixedTarget(coord=dso_position, name=dso)
                print(f"|--VISIBLE at {actual_direction}--", end=" ")
                set_time = observer.target_set_time(local_time, plan_radec)
                
                print(f"set:{set_time.iso}, " ,end=" ")
                print(" ")
                
                
            else:
                print("|xxUNDER THE HORIZONxx", end=" ")
                observer = Observer(location=observer_location)
                target = FixedTarget(coord=dso_position, name=dso)
                rise_time = observer.target_rise_time(local_time, plan_radec)
                print(f"rise:{rise_time.iso}")
    else:
        print("you have no planets in your favorites")
    hour_shift_fav(observer_location, local_time)
            
            
   
def city():
     geolocator = Nominatim(user_agent="city_geocoder")
     default_city = "Rome" 
     while True:
     
        city_name = input("type city name: ('d' for default) ")
        try:
            if city_name == "d":
                observer_location = geolocator.geocode(default_city)
                observer_location = EarthLocation(lat=observer_location.latitude, lon=observer_location.longitude)
                city_name = default_city
                print(f"coordinates for {city_name}: LAT: {observer_location.lat}, LON: {observer_location.lon} ")
                break


            else:
                observer_location = geolocator.geocode(city_name)
                print(f"coordinates for {city_name}: LAT: {observer_location.latitude}, LON: {observer_location.longitude} ")
                if observer_location is None:
                    print("city wasn't found")
                    continue
                observer_location = EarthLocation(lat=observer_location.latitude, lon=observer_location.longitude)
                
                break

            print(f"Location for {city_name}: lat={observer_location.latitude}, lon={observer_location.longitude}")
            break
        except Exception as e:
            print(f"Your city wasn't found. Error: {e}")
            continue
    
     return observer_location
def get_time():
     while True:
        print ("------------------------------------------------------------ ")
        date = input("type date YYYY-MM-DD HH:MM:SS ('n' for current or 'd' for default): ")
    
    
        if date == "n":
            specific_time = Time.now()
            local_time = specific_time
            print(f"Time chosen (local time): {local_time}")
            break
        #sets a default time

        elif date == "d":
            cy = Time.now()
            current_year = datetime.datetime.now().year
            local_time = Time(f'{current_year}-{cy.datetime.month}-{cy.datetime.day} 18:00:00', scale='utc') #set default time here 
            print(f"Time chosen (local time): {local_time}")
            break

        else:
            try:
                specific_time = Time(date)
                local_time = specific_time
                print(f"Time chosen (local time): {local_time}")
                break
            except Exception as e:
                print(f"Invalid date format. Error: {e}")
                continue
     return local_time
     
def hour_shift_fav(observer_location, local_time):
    print(" ")
    hour = input("see results for a different hour, select +, - or any other key to reload")
    if(hour == "+"):
        while True:
         try:
            total_shift = int(input("select how many hours: "))
            local_time += total_shift * u.hour
            print(f"showing results for: {local_time}")
            break
         except:
             print("you must type a valid number")
             continue
         
        favorites(observer_location, local_time)
        
        
    elif(hour == "-"):
        while True:
         try:
            total_shift = int(input("select how many hours: "))
            local_time -= total_shift * u.hour
            print(f"showing results for: {local_time}")
            break
         except:
             print("you must type a valid number")
             continue
         
        
        favorites(observer_location, local_time)
        
    else:
        return 
    
def hour_shift_dso(observer_location, dso, local_time):
    print(" ")
    hour = input("see results for a different hour, select +, -, y for yearly visibility or any other key to reload")
    if(hour == "+"):
       while True:
         try:
            total_shift = int(input("select how many hours: "))
            local_time += total_shift * u.hour
            print(f"showing results for: {local_time}")
            break
         except:
             print("you must type a valid number")
             continue
         
        
       repeat(local_time, observer_location, dso)
        
        
    elif(hour == "-"):
       while True:
         try:
            total_shift = int(input("select how many hours: "))
            local_time -= total_shift * u.hour
            print(f"showing results for: {local_time}")
            break
         except:
             print("you must type a valid number")
             continue
       repeat(local_time, observer_location, dso)
    elif(hour == "y"):
        year_visibility(local_time, observer_location, dso)
        
    else:
        return
    
def year_visibility(local_time, observer_location, dso):
    hour = local_time.datetime.hour
    minute = local_time.datetime.minute
    day = datetime.datetime.now().day


    print(" ")
    print(f'showing yearly results for {day}th {hour}:{minute}')
    count = 0
    months = ["January", "February", "March", "April", "May", "June","July", "August", "September", "October", "November", "December"]
    astroposition = SkyCoord.from_name(dso)
    altitudes = []

    while(count < 12):
        current_time = Time.now()
        current_year = datetime.datetime.now().year
        
        timeline = Time(f'{current_year}-{count + 1}-{day} {hour}:{minute}:00', scale= 'utc')
      
        
        altaz_frame = AltAz(obstime=timeline, location=observer_location)
        dso_altaz = astroposition.transform_to(altaz_frame)
        alt = dso_altaz.alt.deg
        az = dso_altaz.az.deg

        print(f'{months[count]}: alt: {round(dso_altaz.alt.deg, 2)}, az: {round(dso_altaz.az.deg, 2)}', end = " ")
        if(alt > 0):
            
            print(f'Visible at {cardinal(az)}')
        else:
            print("**UNDER THE HORIZON**")
        print(" ")

        altitudes.append(alt)
        count += 1

        
        
        




                    


    
def repeat(local_time, observer_location, dso):
    astroposition = SkyCoord.from_name(dso)
    
    altaz_frame = AltAz(obstime=local_time, location=observer_location)

    sun_radec = get_body(body = "Sun", time = local_time, location = observer_location)
    altaz_frame_sun = AltAz(obstime=local_time, location=observer_location)
    sun_altaz = sun_radec.transform_to(altaz_frame_sun)
    sun_altitude = (sun_altaz.alt).deg

    print(" ")

    print(f" Sun altitude: {sun_altitude} ")


    if sun_altitude > -18:
        astronomical_darkness = astrodark(sun_altitude)
        print(f"Astro darkness at: {astronomical_darkness.iso}")
    

    # Transforms the DSO coordinates to Alt/Az
    dso_altaz = astroposition.transform_to(altaz_frame)
    print(" ")
    print("------------------------------------------------------------ ")
    print("RESULTS: ")
    print(f"{dso}'s alt-az coordinates are: Altitude {dso_altaz.alt}, Azimuth {dso_altaz.az}")
    print(" ")
    print("VISIBILITY: ", end=" ")
    altitude = dso_altaz.alt.deg
    if altitude > 0:
        print(f"{dso} is above the horizon,", end=" ")
        warnings = []
        if 20 < altitude < 70:
            print("well visible")
        elif 0 < altitude < 20:
            print("hardly visible")
            warnings.append("LOW!")
        elif 70 < altitude < 85:
            print("visible but Seestar might struggle (very high in the sky)")
            warnings.append("HIGH!")
        elif altitude > 85:
            print("visible but Seestar can't track the object (directly overhead)")
            warnings.append("TRACKING FAIL!")
            
            
        
        
        observer = Observer(location=observer_location)
        target = FixedTarget(coord=astroposition, name=dso)
        
        transit_time = observer.target_meridian_transit_time(local_time, target, which='next')
        print(f"{dso} will transit at {transit_time.iso}', ", end=" ")
        transit_height = max_height(dso, transit_time.iso, observer_location)
        print(f"({transit_height}deg)")

        
        
        
        set_time = observer.target_set_time(local_time, target, which='nearest')
        print(f"{dso} will set on {set_time.iso}", end="")
        
        try:
            set_direction_az = rise_set_direction(dso, set_time.iso, observer_location)
            direction = cardinal((set_direction_az).deg)
            print(f" at {direction}")
        except:
            print("set time could not retrieved")
       
        
        
        print(" ")
        moon_radec = get_body(body = 'Moon', time = local_time, location = observer_location)
        altaz_frame_moon = AltAz(obstime=local_time, location=observer_location)
        moon_altaz = moon_radec.transform_to(altaz_frame_moon)

        
        
       
        
        illumination = moon_illumination(local_time)
        illumination_percentage = illumination * 100
        moon_direction = cardinal((moon_altaz.az).deg)
        
        
        
        azdist = abs((moon_altaz.az - dso_altaz.az).deg)
        altdist = abs((moon_altaz.alt - dso_altaz.alt).deg)
        
        if(moon_altaz.alt > 0):
            print(f"moon is above the horizon(alt: {round(moon_altaz.alt.deg)}, {moon_direction}), ", end= " ")
         
            
                
          


            if(azdist < 15 and altdist < 15):
                print(f"close to {dso}, ", end=" ")
                print(" ")
            elif(altdist > 15 and azdist < 15):
                print(f"in the general sky area of {dso},", end=" ")
                print(" ")

            if(illumination_percentage < 10):
                print(f"but its not very bright ({illumination_percentage:.2f}%)")
            elif(illumination_percentage > 10 and illumination_percentage < 40):
                print(f"and its moderately bright({illumination_percentage:.2f}%)")
                warnings.append("MOON!")
            elif(illumination_percentage > 40 and illumination_percentage < 70):
                print(f"and it is considerably bright({illumination_percentage:.2f}%)")
                warnings.append("MOON!")
            else:
                print(f"and it is very bright({illumination_percentage:.2f}%)")
                warnings.append("MOON!")
            
                
                
        else:
            print(f"the moon is under the horizon ({round(moon_altaz.alt.deg, 2)})")
            
            
             
        
        
        
      
        
    else:
        print(f"{dso} is under the horizon")
        print(" ")
        #calculates rising time 
        observer = Observer(location=observer_location)
        target = FixedTarget(coord=astroposition, name=dso)
        rising_time = observer.target_rise_time(local_time, target, which='nearest')
        print(f"{dso} will rise on {rising_time.iso}")
        
        
        #calculates rising direction
        set_direction_az = rise_set_direction(dso, rising_time.iso, observer_location)
        try:
        
            direction = cardinal((set_direction_az).deg)
            print(f" at {direction}")       
        except:
            print("rising information could not be retrieved")
        transit_time = observer.target_meridian_transit_time(local_time, target, which='next')
        print(f"{dso} will transit at {transit_time.iso}', ", end=" ")
        transit_height = max_height(dso, transit_time.iso, observer_location)
        print(f"({transit_height}deg)")

        print(" ")
       
        hour_shift_dso(observer_location, dso, local_time)
    
    rotation = field_rotation(observer_location, dso_altaz)
    print(rotation)
    
    if rotation == "strong" or rotation == "extreme":
        warnings.append("ROTATION!")
     
    if len(warnings) > 0:
        print(" ")
        print("WARNINGS: ", end=" ")
        for warning in warnings:
            
            print(warning, end=", ")
    else:
        print(" ")
        print("there are no warnings")
        
    print(" ")
    hour_shift_dso(observer_location, dso, local_time)
   
    
    
    
def field_rotation(observer_location, dso_altaz):
    print(" ")
    print("FIELD ROTATION CALCULATE: ")
    print(" ")
    print("general assesment: ")
    
    if((observer_location.lat).deg <= 10):
        print(f"CAUTION: your observing location (lat: {abs(observer_location.lat)}) is close/at the equator, where field rotation is maximum.")
    elif((observer_location.lat).deg >= 60):
        print(f"OPTIMAL: your observing location {abs(observer_location.lat)} is close/at the poles, where field rotation is minimal.")
    else:
        print("")
        

    
    current_direction = cardinal((dso_altaz.az).deg)
    print(f"{dso} is at {current_direction}.", end=" ")
    
    if(current_direction == "N" or current_direction == "NNW" or current_direction == "NNE"):
        print("Caution: the object is almost at/at the north, where field rotation is maximized.", end=" ")
    elif(current_direction == "S" or current_direction == "SSW" or current_direction == "SSE"):
        print("Caution: the object is almost at/ at the south, where field rotation is usually intensified.", end=" ")
    elif(current_direction == "NE" or current_direction == "NW"):
        print("Caution: the object is getting closer to the north, where field rotation is usually intensified.", end=" ")
    elif(current_direction == "SE" or current_direction == "SW"):
        print("Caution: the object is getting closer to the south, where field rotation is usually intensified.", end=" ")
    elif(current_direction == "E" or current_direction == "ESE" or current_direction == "ENE"):
        print("the object is closer/at the east, where field rotation is minimized.", end=" ")
    elif(current_direction == "W" or current_direction == "WSW" or current_direction == "WNW"):
        print("the object is closer/at the west, where field rotation is minimized.", end=" ")
    
    if(dso_altaz.alt.deg < 50):
        print("The object's elevation is less than 50 degrees(the lower, the better)")
    else:
        print("The object's elevation is more than 50 degrees, effects might be intensified")
     
        
        

        
    
    print(" ")
    print("detailed calculations:")
        
        
        
    
    sensor_width = 1096 
    sensor_height = 1936
    #change these values based on the resolution of your image - current values are for the Seestar S50

    exposure = 10  # You can change this value based on the length in seconds of your exposure

    sensor_diagonal = math.sqrt(math.pow(sensor_width, 2) + math.pow(sensor_height, 2))
    earth_rotation = 360 / 23.9344696

    degree_lat = observer_location.lat.deg
    rad_lat = math.radians(degree_lat) 
    rad_azimuth = math.radians(dso_altaz.az.deg)
    rad_alt = math.radians(dso_altaz.alt.deg)

    image_rotation_rate = earth_rotation * math.cos(rad_lat) * math.cos(rad_azimuth) / math.cos(rad_alt)
    print(f"image rotation rate: {round(image_rotation_rate, 2)} Arcseconds/second")

    image_rot_rad = math.radians(image_rotation_rate)

    sensor_movement = math.sin(image_rot_rad / 3600) * sensor_diagonal * exposure
    print(f"max sensor movement({exposure}s): {round(sensor_movement, 2)} pixels -", end=" ")
    
    if(abs(round(sensor_movement, 2)) > 1 and abs(round(sensor_movement, 2)) < 3 ):
        shift = "noticeable"
    elif(abs(round(sensor_movement, 2)) > 3 and abs(round(sensor_movement, 2)) < 5):
        shift = "strong"
    elif(abs(round(sensor_movement, 2)) > 5):
        shift = "extreme"
    else:
        shift = "minimal"
    
    return shift
        
   
        
        
def max_height(object, time, geolocation):
    try:
        astroposition = SkyCoord.from_name(object)
    
        altaz_frame = AltAz(obstime=time, location=geolocation)

        dso_altaz = astroposition.transform_to(altaz_frame)
    
        return dso_altaz.alt
    except:
        print("there was an error retrieving coordinates")
    
    
def rise_set_direction(object, time, geolocation):
    try:
        astroposition = SkyCoord.from_name(object)
    
        altaz_frame = AltAz(obstime=time, location=geolocation)

        dso_altaz = astroposition.transform_to(altaz_frame)
    
        return dso_altaz.az
    except:
        print("there was an error retrieving coordinates")
    
    
def cardinal(az):
    if az >= 337.5 or az <= 22.5:
        cardinal = "N"
    elif az > 22.5 and az <= 45:
        cardinal = "NNE"
    elif az > 45 and az <= 67.5:
        cardinal = "NE"
    elif az > 67.5 and az <= 90:
        cardinal = "ENE"
    elif az > 90 and az <= 112.5:
        cardinal = "E"
    elif az > 112.5 and az <= 135:
        cardinal = "ESE"
    elif az > 135 and az <= 157.5:
        cardinal = "SE"
    elif az > 157.5 and az <= 180:
        cardinal = "SSE"
    elif az > 180 and az <= 202.5:
        cardinal = "S"
    elif az > 202.5 and az <= 225:
        cardinal = "SSW"
    elif az > 225 and az <= 247.5:
        cardinal = "SW"
    elif az > 247.5 and az <= 270:
        cardinal = "WSW"
    elif az > 270 and az <= 292.5:
        cardinal = "W"
    elif az > 292.5 and az <= 315:
        cardinal = "WNW"
    elif az > 315 and az <= 337.5:
        cardinal = "NW"
    else:
        cardinal = "Invalid"
    
    
  
    return cardinal
        

while True:
    
    fav_iteration = 0
    warnings = []

    print("------------------------------------------------------------ ")
    print("CELESTIAL OBJECT VISIBILITY ASSESSOR")

    dso = input("please type identifier for a deep space object, else 'f' to see your favorites or 'help': ")
    if(dso == "help"):
        print("This console app quickly provides the user with Alt/Az coordinates of a given Deep space object and uses that data to assess its overall visibility and to calculate rising/set times, along with the maximum field rotation at a certain exposure. Here's a few tips to use the program:")
        print(" ")
        print(f"1) The Skycoord function uses the SIMBAD database and as input, if you input a DSO's name and it doesn't get recognized, you might want to try typing its identifier(Messier, NGC, Coldwell). If an identifier is typed, such as C20 (north america nebula) and the object is still not found, try to input its alternate identifiers using NGC or Messier ")
        print(f"2) The field rotation calculator is based on the methods discussed in this video 'https://youtu.be/WacU_S_iWHQ?si=iVpUZ4UM7IzRD-78'")
        print("3) Currently the program doesn't really account for time zones, so it might display the wrong time while still providing the correct current coordinates, depending on your system")
        
        continue
    elif(dso == 'f'):
       observer_location = city()
       local_time = get_time()
       favorites(observer_location, local_time)
       continue
       
    else:
        # Pulls Ra/Dec coordinates of the DSO
        try:
            astroposition = SkyCoord.from_name(dso)
            search =  Simbad.query_object(dso)

            object_type = search['OTYPE'][0]  # Extract the object type
            print(f"Object type: {object_type}")

            
            
            try:
             
             alternative_ids = search['IDS'][0]  # The 'IDS' column contains all IDs as a single string
             print(f"Alternative identifiers for {dso}:\n{alternative_ids}")
            except:
             print("no alternative id's found")



        
        except Exception as e:
            print(f"The object {dso} wasn't found in the database. Error: {e}")
            continue
        print(" ---------------------------------------------------------- ")
    observer_location = city()
    local_time = get_time()
   

    # Creates a frame for Ra/Dec - Alt/Az conversion using the input time and the observer location
    altaz_frame = AltAz(obstime=local_time, location=observer_location)

    # Transforms the DSO coordinates to Alt/Az
    dso_altaz = astroposition.transform_to(altaz_frame)
    
    #gets the coordinates of the Sun


    sun_radec = get_body(body = "Sun", time = local_time, location = observer_location)
    altaz_frame_sun = AltAz(obstime=local_time, location=observer_location)
    sun_altaz = sun_radec.transform_to(altaz_frame_sun)
    sun_altitude = (sun_altaz.alt).deg

    print(" ")

    print(f" Sun altitude: {sun_altitude} ")


    if sun_altitude > -18:
        astronomical_darkness = astrodark(sun_altitude)
        print(f"Astro darkness at: {astronomical_darkness.iso}")
    


   


    print(" ")
    print("------------------------------------------------------------ ")
    print("RESULTS: ")
    print(f"{dso}'s alt-az coordinates are: Altitude {dso_altaz.alt}, Azimuth {dso_altaz.az}")
    print(" ")
    print("VISIBILITY: ", end=" ")
    altitude = dso_altaz.alt.deg

    

    


    if altitude > 0:
        print(f"{dso} is above the horizon,", end=" ")
        
        if 20 < altitude < 70:
            print("well visible")
        elif 0 < altitude < 20:
            print("hardly visible")
            warnings.append("LOW!")
            
        elif 70 < altitude < 85:
            print("visible but Seestar might struggle (very high in the sky)")
            warnings.append("HIGH!")
        elif altitude > 85:
            print("visible but Seestar can't track the object (directly overhead)")
            warnings.append("TRACKING FAIL!")
            
        
        
        observer = Observer(location=observer_location)
        target = FixedTarget(coord=astroposition, name=dso)
        
        transit_time = observer.target_meridian_transit_time(local_time, target, which='next')
        print(f"{dso} will transit at {transit_time.iso}', ", end=" ")
        transit_height = max_height(dso, transit_time.iso, observer_location)
        print(f"({transit_height}deg)")

        
        
        
        set_time = observer.target_set_time(local_time, target, which='nearest')
        print(f"{dso} will set on {set_time.iso}", end="")
        
        try:
            set_direction_az = rise_set_direction(dso, set_time.iso, observer_location)
            direction = cardinal((set_direction_az).deg)
            print(f" at {direction}")
        except:
            print("set time could not retrieved")
       
        
        
        print(" ")
        moon_radec = get_body(body = 'Moon', time = local_time, location = observer_location)
        altaz_frame_moon = AltAz(obstime=local_time, location=observer_location)
        moon_altaz = moon_radec.transform_to(altaz_frame_moon)
        
        illumination = moon_illumination(local_time)
        illumination_percentage = illumination * 100
        moon_direction = cardinal((moon_altaz.az).deg)
        
        
        
        azdist = abs((moon_altaz.az - dso_altaz.az).deg)
        altdist = abs((moon_altaz.alt - dso_altaz.alt).deg)
        
        if(moon_altaz.alt > 0):
            print(f"moon is above the horizon(alt: {round(moon_altaz.alt.deg)}, {moon_direction}), ", end= " ")
            if(azdist < 15 and altdist < 15):
                print(f"close to {dso}, ", end=" ")
                
                print(" ")
            elif(altdist > 15 and azdist < 25):
                print(f"in the general sky area of {dso},", end=" ")
                print(" ")

            if(illumination_percentage < 10):
                print(f"but its not very bright ({illumination_percentage:.2f}%)")
            elif(illumination_percentage > 10 and illumination_percentage < 40):
                print(f"and its moderately bright({illumination_percentage:.2f}%)")
                warnings.append("MOON!")
            elif(illumination_percentage > 40 and illumination_percentage < 70):
                print(f"and it is considerably bright({illumination_percentage:.2f}%)")
                warnings.append("MOON!")
            else:
                print(f"and it is very bright({illumination_percentage:.2f}%)")
                warnings.append("MOON!")
                
                
        else:
            print(f"the moon is under the horizon {round(moon_altaz.alt.deg, 2)}")
            print(" ")
             
        
        
        
      
        
    else:
        print(f"{dso} is under the horizon")
        print(" ")
        #calculates rising time 
        observer = Observer(location=observer_location)
        target = FixedTarget(coord=astroposition, name=dso)
        rising_time = observer.target_rise_time(local_time, target, which='nearest')
        print(f"{dso} will rise on {rising_time.iso}")
        
        
        #calculates rising direction
        set_direction_az = rise_set_direction(dso, rising_time.iso, observer_location)
        try:
        
            direction = cardinal((set_direction_az).deg)
            print(f" at {direction}")       
        except:
            print("rising information could not be retrieved")
        transit_time = observer.target_meridian_transit_time(local_time, target, which='next')
        print(f"{dso} will transit at {transit_time.iso}', ", end=" ")
        transit_height = max_height(dso, transit_time.iso, observer_location)
        print(f"({transit_height}deg)")

        print(" ")
        hour_shift_dso(observer_location, dso, local_time)
    
        continue
    
    rotation = field_rotation(observer_location, dso_altaz)
    print(rotation)
    if rotation == "strong" or rotation == "extreme":
        warnings.append("ROTATION!")
        
   

    
    
    if len(warnings) > 0:
        print(" ")
        print("WARNINGS:", end=" ")
        for warning in warnings:
            print(warning, end=", ")
    else:
        print(" ")
        print("there are no warnings")
        
    
    
    print(" ")
    hour_shift_dso(observer_location, dso, local_time)
    
   
        

     
    
   


