This simple console app allows the user to quickly get information about the position of DSO's, essential for observation, without having to launch a full-fledged sky map software like Stellarium.
The app simply asks for the identifier of a DSO and then for the name of the city or to keep the default one (editable straight from the code), then it asks to set a specific time or get the current one,
(keep in mind the time must be written in the YYYY-MM-DD HH:MM:SS format)

Once time and are set, the program will print the following info: alt/az coordinates - above/under the horizon - rise/set time, transit time -  moon's altitude and possible proximity with the object,
along with the moon's current illumination percentage. Then the program will display a section dedicated to field rotation, that will provide a general assessment firstly based on the object's
general position in the sky(if close to North or observing location is close to the equator/poles or its elevation) and then will run a detailed calculation 
(formulas and method based on this video: https://youtu.be/WacU_S_iWHQ?si=Vcpk1BhZLmokVUyK) that will output the maximum amount of rotation in pixel the object will experience during the course of one exposure
(resolution is set by default for the Seestar S50, if you want to run the calculation for a different camera, then change the "sensor_widht" and "sensor_height" variables), which is set to 10 seconds by default in 
the "exposure" variable.

The only real issue I've encountered with the program is that it seems to have some confusion with time zones, so when I set the current time by writing "now", the programm will say it has selected a time 2 hours
behind the correct one. Same thing happend when setting time manually if you input "21:00:00" then the program really interprets it as "23:00:00). However coordinates are always correct as long as this hour shift 
is kept in mind.
