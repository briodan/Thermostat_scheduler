This integration/repository aims to make it simpler to use my scheduler blue print for the Honeywell T6 thermostat

**Features of the blueprint:**

- four daily schedules for the thermostat (differant for weekday vs week-end)
- ability to use remote sensor for the thermostat
- ability to change sensors, times, target temperatures in a dashbaord
- ability to change target temperatures in the mediaum term (days/weeks) by modifying tolerance helpers
- ability to change target temperature in the short term (this schedule interval ony) by temporarily modifying the target temperature

**HACS**
- Install HACS if you have not already
- Open HACS and click three dots in right corner -> Custom Repositories -> then paste https://github.com/briodan/t6_program/ in 'Repository' and choose type 'Integration' then click 'Add'
- Now search for 'T6 Program' in HACS
- Click "Add" to confirm, and then click "Download" to download and install the integration Restart Home Assistant
- Search for "T6 Program" in HACS and install then restart
- In Home Assistant go to Settings -> Devices and Services -> Add integration -> Search for T6 and add
- Configure the device(s)

**Manual Install**
- This integration can be installed by downloading the view_assist directory into your Home Assistant /config/custom_components directory and then restart Home Assistant. We have plans to make this easier through HACS but are waiting for acceptance.

**How to use**
- This integration will create all entities required to run the blueprint
   - (TO DO) add a sample dashboard for integration entities
   - (TO DO) add a sample dashboard for Thermostat control
- You will be prompted to setup the initial state of the integration entities during initial setup

**Import the blueprints**
- Import both blueprints under Blueprints > Integration bases
   - (TO DO) add import links

**Configure the blueprints**
- The blueprints filter entities to only those provided by the integration for easy matching

**Description of entities and what they do:**

**For each of the 4 daily time intervals you need to provide:**
- Time - when the new settings stats (i.e t6_program_m_f_time_1 for weekday or t6_program_s_s_time_1 for week-end)
- Sensor - the remote sensor to use for the time interval (i.e t6_program_m_f_sensor_1 for weekday or t6_program_s_s_sensor_1 for week-end)
- Temperature - the target temperature to use for the time interval (i.e t6_program_m_f_temperature_1 for weekday or t6_program_s_s_temperature_1 for week-end)

**Tolerance cool and tolerance heat**
- These entities offset the target temperature
    - avoids flapping for dual heat/cool systems - by default the min values are 0.5 degrees
    - allows medium term temperature adjustement by increasing the offsets
- using the tolerances means the thermostat will never reach the target temperature it will be at most 0.5 degrees cooler/warmer

**Adjusted Cool and Heat Temeprature**
- These entities are used to display in a dashboard the true target temperatures after tolerances are applied

**Current Sensor**
- This entities is used to hold the current sensor being used
    - this is used for displaying in a dashbaord
    - this is used for the run sensor blueprint to know which sensor to target

Current Temperature
- This entitie is used to display the current temperature of the current sensor
(TO DO) this entity might go away in the future

Current Target Temperature
- This entity is used to told the current target temeperature
    - this is used for displaying in a dashbaord
    - this allows for short term changes to temeprature until the next scheduled time runs

Thermostat State
- This entity show the historical state on the termostat
- used mostly for troubleshooting/making sure the program ran as expected

Note this Integration is written for the T6 thermostat as such it relies on setting low and high set points to control the temperature and will not work with thermostats that don't have this features

Additional notes:
- blueprint used a default temeprature as a fallback in case there are issues with a sensors
- blueprint setpoint are set to 2 degrees above target to avoid run-off (TO DO) this might change to match the target temperature

Larger TO DO:
- allow user to specify temeprature ranges manually for the temperature entities (will allow usage with C or F)
- check into an other changes required to support both C and F in the integration or blueprint
- allow user to specify thermostat name during setup and drive entity name from it (allows usage of multiple thermostats)
- look into adjusting the setpoints to reduce the risk of run-off
- look into allowing the use of this with both T6 and Regular thermostats

