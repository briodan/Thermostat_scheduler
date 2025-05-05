DOMAIN = "t6_program"

MF_TIMES = [f"m_f_time_{i}" for i in range(1, 5)]
SS_TIMES = [f"s_s_time_{i}" for i in range(1, 5)]
MF_TEMPS = [f"m_f_temperature_{i}" for i in range(1, 5)]
SS_TEMPS = [f"s_s_temperature_{i}" for i in range(1, 5)]

ALL_INPUT_DATETIMES = MF_TIMES + SS_TIMES
ALL_INPUT_NUMBERS = MF_TEMPS + SS_TEMPS

# Option keys
OPTION_COOL_TOLERANCE = "cool_tolerance"
OPTION_HEAT_TOLERANCE = "heat_tolerance"
