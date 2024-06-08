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

def favorites():
    #put your favorite deep space targets in this array
    dsos = ["M31", "M45", "M33", "M51", "NGC2024", "Orion nebula"]
    #you can also put planets
    planets = ["Jupiter", "Saturn", "Mars", "Venus", "Uranus", "Neptune", "Mercury"]
    
    while True:
     
        city_name = input("type city name: ('d' for default) ")
        try:
            if city_name == "d":
                observer_location = geolocator.geocode(default_city)
                observer_location = EarthLocation(lat=observer_location.latitude, lon=observer_location.longitude)
                city_name = default_city
                break


            else:
                observer_location = geolocator.geocode(city_name)
                if observer_location is None:
                    print("Your city wasn't found")
                    continue
                observer_location = EarthLocation(lat=observer_location.latitude, lon=observer_location.longitude)
                print(f"You chose the city: {city_name}")
                break

            print(f"Location for {city_name}: lat={observer_location.lat}, lon={observer_location.lon}")
            break
        except Exception as e:
            print(f"Your city wasn't found. Error: {e}")
            continue
    while True:
        print ("------------------------------------------------------------ ")
        date = input("type date YYYY-MM-DD HH:MM:SS (or 'now'): ")
    
    
        if date == "now":
            specific_time = Time.now()
            local_time = specific_time
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
                set_time = observer.target_set_time(specific_time, target, which='nearest')
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
                set_time = observer.target_set_time(specific_time, target, which='nearest')
                print(f"|rise: {set_time.iso}" , end="")
                transit_time = observer.target_meridian_transit_time(local_time, target, which='next')
                print(f"{dso} transit: {transit_time.iso}', ", end=" ")
                transit_height = max_height(dso, transit_time.iso, observer_location)
                print(f"({transit_height})") 
        
                set_direction_az = rise_set_direction(dso, set_time.iso, observer_location)
                direction = cardinal((set_direction_az).deg)
                print(f" at {direction}")
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
            
            
    return
           
    
        
   
        
        
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
    # Initializes geocoder
    geolocator = Nominatim(user_agent="city_geocoder")
    default_city = "Rome"

    print("------------------------------------------------------------ ")
    print("CELESTIAL OBJECT VISIBILITY ASSESSOR")

    dso = input("please type identifier for a deep space object, else 'f' to see your favorites or 'help': ")
    if(dso == "help"):
        print("This console app quickly provides the user with Alt/Az coordinates of a given Deep space object and uses that data to assess its overall visibility and to calculate rising/set times, along with the maximum field rotation at a certain exposure. Here's a few tips to use the program:")
        print(" ")
        print(f"1) The Skycoord function uses the SIMBAD database and as input, if you input a DSO's name and it doesn't get recognized, you might want to try typing its identifier(Messier, NGC, Coldwell). If an identifier is typed, such as C20 (north america nebula) and the object is still not found, try to input its alternate identifiers using NGC or Messier ")
        print(f"2) The field rotation calculator is based on the methods discussed in this video 'https://youtu.be/WacU_S_iWHQ?si=iVpUZ4UM7IzRD-78'")
        print("3) Currently the program doesn't really account for time zones, so it might display the wrong time while still providing the correct current coordinates, depending on your system")
        print(f"4) You can change the default city in the code, look for the variable named 'default_city'. Your current default city is  - {default_city} - ")
        continue
    elif(dso == 'f'):
        favorites()
        continue
    else:
        # Pulls Ra/Dec coordinates of the DSO
        try:
            astroposition = SkyCoord.from_name(dso)
        
        except Exception as e:
            print(f"The object {dso} wasn't found in the database. Error: {e}")
            continue
        print(" ---------------------------------------------------------- ")
 
    
    # Finds the city
    while True:
     
        city_name = input("type city name: ('d' for default) ")
        try:
            if city_name == "d":
                observer_location = geolocator.geocode(default_city)
                observer_location = EarthLocation(lat=observer_location.latitude, lon=observer_location.longitude)
                city_name = default_city
            else:
                observer_location = geolocator.geocode(city_name)
                if observer_location is None:
                    print("Your city wasn't found")
                    continue
                observer_location = EarthLocation(lat=observer_location.latitude, lon=observer_location.longitude)
                print(f"You chose the city: {city_name}")

            print(f"Location for {city_name}: lat={observer_location.lat}, lon={observer_location.lon}")
            break
        except Exception as e:
            print(f"Your city wasn't found. Error: {e}")
            continue
    print ("------------------------------------------------------------ ")
    date = input("type date YYYY-MM-DD HH:MM:SS (or 'now'): ")

    if date == "now":
        specific_time = Time.now()
        local_time = specific_time
     
       
    else:
        try:
            specific_time = Time(date)
            local_time = specific_time
        except Exception as e:
            print(f"Invalid date format. Error: {e}")
            continue
    print(f"Time chosen (local time): {local_time}")

    # Creates a frame for Ra/Dec - Alt/Az conversion using the input time and the observer location
    altaz_frame = AltAz(obstime=local_time, location=observer_location)

    # Transforms the DSO coordinates to Alt/Az
    dso_altaz = astroposition.transform_to(altaz_frame)
    print(" ")
    print("------------------------------------------------------------ ")
    print("RESULTS: ")
    print(f"{dso}'s alt-az coordinates are: Altitude {dso_altaz.alt}, Azimuth {dso_altaz.az}, at {city_name}")
    print(" ")
    print("VISIBILITY: ", end=" ")
    altitude = dso_altaz.alt.deg
    if altitude > 0:
        print(f"{dso} is above the horizon,", end=" ")
        
        if 20 < altitude < 70:
            print("well visible")
        elif 0 < altitude < 20:
            print("hardly visible")
        elif 70 < altitude < 85:
            print("visible but Seestar might struggle (very high in the sky)")
        elif altitude > 85:
            print("visible but Seestar can't track the object (directly overhead)")
        
        observer = Observer(location=observer_location)
        target = FixedTarget(coord=astroposition, name=dso)
        
        transit_time = observer.target_meridian_transit_time(local_time, target, which='next')
        print(f"{dso} will transit at {transit_time.iso}', ", end=" ")
        transit_height = max_height(dso, transit_time.iso, observer_location)
        print(f"({transit_height}deg)")

        
        
        
        set_time = observer.target_set_time(specific_time, target, which='nearest')
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
        
        
        
        azdist = abs((moon_altaz.az - dso_altaz.az).deg)
        altdist = abs((moon_altaz.alt - dso_altaz.alt).deg)
        
        if(moon_altaz.alt > 0):
            print(f"moon is above the horizon(alt: {round(moon_altaz.alt.deg)}), ", end= " ")
            if(azdist < 15 and altdist < 15):
                print(f"close to {dso}, ", end=" ")
                print(" ")
            elif(altdist > 15 and azdist < 15):
                print(f"in the general sky area of {dso},", end=" ")
                print(" ")

            if(illumination_percentage < 10):
                print(f"but its not very bright ({illumination_percentage:.2}%)")
            elif(illumination_percentage > 40 and illumination_percentage < 70):
                print(f"and it is considerably bright({illumination_percentage:.2}%)")
            else:
                print(f"and it is very bright({illumination_percentage:.2f}%)")
                
        else:
            print(f"the moon is under the horizon {round(moon_altaz.alt.deg, 2)}")
            print(" ")
             
        
        
        
      
        
    else:
        print(f"{dso} is under the horizon")
        print(" ")
        #calculates rising time 
        observer = Observer(location=observer_location)
        target = FixedTarget(coord=astroposition, name=dso)
        rising_time = observer.target_rise_time(specific_time, target, which='nearest')
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
       
        continue


    
    print(" ")
    print("FIELD ROTATION CALCULATE: ")
    print(" ")
    print("general assesment: ")
    
    if((observer_location.lat).deg <= 10):
        print(f"your observing location {observer_location.lat} is close/at the equator, where field rotation is maximum.")
    elif((observer_location.lat).deg >= 75):
        print(f"your observing location {observer_location.lat} is close/at to the poles, where field rotation is minimal.")
    else:
        print("")
        

    
    current_direction = cardinal((dso_altaz.az).deg)
    print(f"{dso} is at {current_direction}", end=" ")
    
    if(current_direction == "N"):
        print("which means field rotation might be intensified,", end=" " )
        if(altitude > 50):
            print("the object's elevation is also more than 50 degrees, which can increase the effects further ")
        else:
            print("your object's elevation is less than 50 degrees, the closer it is to the horizon, the better")
    elif(current_direction == "NNE"):
        print("which means field rotation might be intensified,", end=" " )
        if(altitude > 50):
            print("the object's elevation is also more than 50 degrees, which can increase the effects further ")
        else:
            print("your object's elevation is less than 50 degrees, the closer it is to the horizon, the better")
    elif(current_direction == "NE"):
        print("which means field rotation might be intensified,", end=" " )
        if(altitude > 50):
            print("the object's elevation is also more than 50 degrees, which can increase the effects further ")
        else:
            print("your object's elevation is less than 50 degrees, the closer it is to the horizon, the better")
    elif(current_direction == "NNW"):
        print("which means field rotation might be intensified,", end=" " )
        if(altitude > 50):
            print("the object's elevation is also more than 50 degrees, which can increase the effects further ")
        else:
            print("your object's elevation is less than 50 degrees, the closer it is to the horizon, the better")
    elif(current_direction == "NW"):
        print("which means field rotation might be intensified,", end=" " )
        if(altitude > 50):
            print("the object's elevation is also more than 50 degrees, which can increase the effects further ")
        else:
            print("your object's elevation is less than 50 degrees, the closer it is to the horizon, the better")
    elif(current_direction == "WNW"):
        print("which means field rotation might be intensified,", end=" " )
        if(altitude > 50):
            print("the object's elevation is also more than 50 degrees, which can increase the effects further ")
        else:
            print("your object's elevation is less than 50 degrees, the closer it is to the horizon, the better")
    
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
    print(f"max sensor movement: {round(sensor_movement, 2)} pixels -", end=" ")
    
    if(abs(round(sensor_movement, 2)) > 1 and abs(round(sensor_movement, 2)) < 3 ):
        print("noticeable")
    elif(abs(round(sensor_movement, 2)) > 3 and abs(round(sensor_movement, 2)) < 5):
        print("strong")
    elif(abs(round(sensor_movement, 2)) > 5):
        print("extreme")
    else:
        print("minimal")
