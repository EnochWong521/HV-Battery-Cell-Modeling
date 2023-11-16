from read_data import ReadData

zero_to_forty_amp = ReadData("0A30S-40A20S Cell 1 Run 1.csv", "0A to 40A", "TIME_STAMP", "DMM_VOLTAGE")
zero_to_forty_amp.graph_data()

zero_to_ten_amp = ReadData("0A90S-10A90S Cell 2 Run 1.csv", "0A to 10A", "TIME_STAMP", "DMM_VOLTAGE")
zero_to_ten_amp.graph_data()

twenty_to_ten_amp = ReadData("20A-10A Step 1.csv", "20A to 10A", "TIME_STAMP", "VOLTAGE")
twenty_to_ten_amp.graph_data()

forty_to_thirty_amp = ReadData("40A-30A Step 1.csv", "40A to 30A", "TIME_STAMP", "VOLTAGE")
forty_to_thirty_amp.graph_data()

print(zero_to_forty_amp.esr_graph(40))

