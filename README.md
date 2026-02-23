This integration/repository aims to make it simpler to use my scheduler blueprint for the Honeywell T6 thermostat.
However this is not limited to be used with the Honeywell T6 thermostat, other thermostats that use low and high setpoints should work as well.

This project started as a way to better manage my own T6 thermostat with the following requirements
- Wanted to be able to have the thermostat run based on remote sensor (the default location of thermostats in most homes mine included is not ideal)
- Wanted to be able to switch the remote sensor based on time of day which corresponds with different places people find themselves in the house

During the last few years I shared my blueprints in various places and the feedback I got was the extensive use of helpers could be confusing and it did not support temperature settings in both Celsius and Fahrenheit.

So now we are here:
- all the previously manually created helpers are created automatically by the integration
- integration and blueprint handles temperature in either Celsius or Fahrenheit

**Features of the blueprint:**

- four daily schedules for the thermostat (different for weekday vs week-end)
- ability to use remote sensors for the thermostat for each schedule
- ability to change sensors, times, target temperatures in a dashboard
- ability to change target temperatures in the medium term (days/weeks) by modifying tolerance helpers
- ability to change target temperature in the short term (this schedule interval only) by temporarily modifying the target temperature

**HACS**
- Install HACS if you have not already
- Click the button below to auto-add this repository to HACS:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=briodan&repository=Thermostat_scheduler&category=integration)

- If prompted, confirm adding the custom repository as type `Integration`
- In HACS, search for "Thermostat Scheduler" and click `Download`
- Restart Home Assistant
- In Home Assistant go to Settings -> Devices and Services -> Add integration -> Search for Thermostat Scheduler and add
- Configure the device(s)

**Manual Install**
- This integration can be installed by downloading the thermostat_scheduler directory into your Home Assistant /config/custom_components directory and then restart Home Assistant. 

**How to use**
- This integration will create all entities required to run the blueprints
- You will be prompted to set up the initial state of the integration entities during initial setup
- the integration should allow you to set up in either C or F, but the blueprint might need additional testing for F

**Import the blueprints**
- Import both blueprints under Blueprints > Integration bases

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fbriodan%2FThermostat_scheduler%2Fmain%2Fblueprints%2Fintegration%2520based%2FT6%2520-%2520set%2520sensor%2520and%2520temp.yaml)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fbriodan%2FThermostat_scheduler%2Fmain%2Fblueprints%2Fintegration%2520based%2FT6%2520-%2520run%2520based%2520on%2520sensor.yaml)


**Configure the blueprints**
- The blueprints filter entities to only those provided by the integration for easy matching

**Description of entities and what they do:**

**For each of the 4 daily time intervals you need to provide:**
- Time - when the new settings starts (i.e thermostat_scheduler_m_f_time_1 for weekday or thermostat_scheduler_s_s_time_1 for week-end)
- Sensor - the remote sensor to use for the time interval (i.e thermostat_scheduler_m_f_sensor_1 for weekday or thermostat_scheduler_s_s_sensor_1 for week-end)
- Temperature - the target temperature to use for the time interval (i.e thermostat_scheduler_m_f_temperature_1 for weekday or thermostat_scheduler_s_s_temperature_1 for week-end)

**Tolerance cool and tolerance heat**
- These entities offset the target temperature
    - avoids flapping for dual heat/cool systems - by default the min values are 0.5 degrees in Celsius and 1 degrees in Fahrenheit
    - allows medium term temperature adjustment by increasing the offsets
- using the tolerances means the thermostat will never reach the target temperature it will be at most 0.5 degrees cooler/warmer
- tolerances will be different between C and F
    - when configured in C range is 0.5 to 5 C
    - when configured in F range is 0.5 to 10 F - **Need some feedback if this is appropriate from people using this in F**

**Adjusted Cool and Heat Temperature**
- These entities are used to display in a dashboard the true target temperatures after tolerances are applied

**Current Sensor**
- This entity is used to hold the current sensor being used
    - this is used for displaying in a dashboard
    - this is used for the run sensor blueprint to know which sensor to target

**Current Temperature**
- This entity is used to display the current temperature of the current sensor
(TO DO) this entity might go away in the future

**Current Target Temperature**
- This entity is used to hold the current target temperature
    - this is used for displaying in a dashboard
    - this allows for short term changes to temperature until the next scheduled time runs

**Thermostat State**
- This entity shows the historical state on the thermostat
- used mostly for troubleshooting/making sure the program ran as expected

**How does this run**
- The "Thermostat - Set Sensor and Temp" blueprint 
    - this runs every X minutes (TO-DO) at frequency option
    - if it matches one of the times set it changes the current sensor and target temperature to the ones specified for the time interval
- The "Thermostat - Run based on Sensor" blueprint
    - runs every 1/5/10 minutes
    - it turns on the thermostat if current sensor temperature is outside the tolerance ranges
    - on next run it turns the thermostat off.
    - the blueprint turns the thermostat on or off by manipulating the high and low setpoints of the thermostat

**A Sample 2 page dashboard is included**
- copy and paste the contents of the file in the dashboard raw configuration editor
- requires the following additional cards:
    - Mushroom Cards
    - Auto Entities

**Note this Integration is written for the T6 thermostat as such it relies on setting low and high set points to control the temperature and will not work with thermostats that don't have these features**

**Fault tolerance built in**
- Blueprints will default to a user specified default value in case a sensor is not available
- Setpoints are only 2 degrees above target temperature for Celsius and 4 degrees for Fahrenheit

**Larger TO DO:**
- allow user to specify thermostat name during setup and drive entity name from it (allows usage of multiple thermostats)
- look into adjusting the setpoints to reduce the risk of run-off
- look into allowing the use of the blueprint with both Setpoint and Regular thermostats

**Legacy blueprints that might serve as inspiration for others**

The first blueprint - [link](https://gist.github.com/briodan/c4a25ecb376df7ae7995a164100a53a3)
- while that worked I found that I needed to make slight changes to the programs especially in spring/fall to adjust temperature variations

The second set of [blueprints](https://github.com/briodan/Thermostat_Scheduler/tree/main/blueprints/original) (now split into two)
- This allows short term changes of temperature (during current time interval)
- These blueprints had a bit of popularity from others but were missing some key features
    - did not work for people using F as the temperature unit
    - the many helpers that needed to be set up made it confusing to set up
