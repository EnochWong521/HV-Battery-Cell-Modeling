from read_data import ReadData

zero_to_forty_amp = ReadData("0A30S-40A20S Cell 1 Run 1.csv", 40, "TIME_STAMP", "DMM_VOLTAGE", "LOAD_CAPACITY")
zero_to_forty_amp.graph_data(zero_to_forty_amp.time, zero_to_forty_amp.voltage, "Voltage vs. Time graph (40A)", "Time",
                             "Voltage")
zero_to_forty_amp.produce_calc_graphs()

zero_to_ten_amp = ReadData("0A90S-10A90S Cell 2 Run 1.csv", 10, "TIME_STAMP", "DMM_VOLTAGE", "LOAD_CAPACITY")
zero_to_ten_amp.graph_data(zero_to_ten_amp.time, zero_to_ten_amp.voltage, "Voltage vs. Time graph (10A)", "Time",
                           "Voltage")
zero_to_ten_amp.produce_calc_graphs()

one_amp_constant = ReadData("1A Constant Cell 1 Run 1.csv", 1, "TIME_STAMP", "DMM_VOLTAGE", "LOAD_CAPACITY")
one_amp_constant.graph_data(one_amp_constant.all_soc, one_amp_constant.voltage,
                            "Voltage vs. State of Charge graph (1A)", "State of Charge", "Voltage")
