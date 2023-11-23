import pandas
import matplotlib.pyplot as plt
import math


class ReadData:
    def __init__(self, file, current, current_range, time, voltage, soc):
        self.file = pandas.read_csv(file)
        self.current = current
        self.current_range = current_range
        self.time = self.file[time].tolist()
        self.voltage = self.file[voltage].tolist()
        self.all_soc = self.file[soc].tolist()
        self.volt_one = []
        self.volt_two = []
        self.volt_three = []
        self.v_drop_soc = []
        self.esr = []
        self.resistance_two = []

    # for testing purposes
    def print_slopes(self):
        slope_list = []
        for index, volts in enumerate(self.voltage):
            # calculate slopes
            if index != 0 and index != len(self.voltage) - 1:
                delta_y = volts - self.voltage[index - 1]
                delta_x = self.time[index] - self.time[index - 1]
                slope_one = delta_y / delta_x
                delta_y_two = self.voltage[index + 1] - volts
                delta_x_two = self.time[index + 1] - self.time[index]
                slope_two = delta_y_two / delta_x_two
                if slope_one <= 0 and slope_two > 1:
                    slope_list.append(slope_one)
                    slope_list.append(slope_two)
        print(slope_list)
        print(len(slope_list))

    # general method for graphing data
    def graph_data(self, x_list, y_list, x_title, y_title):
        fig, ax = plt.subplots()
        plt.plot(x_list, y_list, color='blue', linestyle='-', linewidth=1)
        ax.set_xlabel(x_title, fontsize=14)
        ax.set_ylabel(y_title, fontsize=14)
        ax.set_title(f"{y_title} vs. {x_title} graph ({self.current_range})")
        ax.grid()
        fig.savefig(f"{self.current_range} {y_title} vs. {x_title} plot.png", dpi=600)

    # find all voltage drop points due to esr and resistor two
    def find_voltage_drops(self):
        for index, volts in enumerate(self.voltage):
            # calculate slopes to find voltage drop points
            if index != 0 and index != len(self.voltage) - 1:
                delta_y = volts - self.voltage[index - 1]
                delta_x = self.time[index] - self.time[index - 1]
                slope = delta_y / delta_x
                # check if the point is an esr voltage drop
                if slope < -1:
                    self.volt_one.append(self.voltage[index - 1])
                    self.volt_two.append(volts)
                    self.v_drop_soc.append(self.all_soc[index])
                # check if the point is a voltage drop due to resistor two
                elif slope <= 0:
                    delta_y_two = self.voltage[index + 1] - volts
                    delta_x_two = self.time[index + 1] - self.time[index]
                    slope_two = delta_y_two / delta_x_two
                    if slope_two > 1:
                        self.volt_three.append(self.voltage[index])
        # eliminate skewed values at the beginning/end of data set
        self.volt_one.pop(0)
        self.volt_one.pop(-1)
        self.volt_two.pop(0)
        self.volt_two.pop(-1)
        self.volt_three.pop(0)
        self.v_drop_soc.pop(0)
        self.v_drop_soc.pop(-1)

    # produce esr vs soc graph
    def esr_graph(self):
        # calculate esr
        for n, voltage in enumerate(self.volt_one):
            esr_drop = voltage - self.volt_two[n]
            esr = esr_drop / self.current
            self.esr.append(esr)
        self.graph_data(self.v_drop_soc, self.esr, "State of Charge", "Equivalent Series Resistance")

    # produce resistor two vs soc graph
    def resistor_two_graph(self):
        # calculate resistance of resistor 1
        for x, volt in enumerate(self.volt_two):
            r_two_drop = volt - self.volt_three[x]
            r_two = r_two_drop / self.current
            self.resistance_two.append(r_two)
        self.graph_data(self.v_drop_soc, self.resistance_two, "State of Charge", "Resistance 2")

    # produce capacitance vs soc graph
    def capacitor_graph(self):
        half_lives = []
        capacitance_list = []
        voltage_to_index = {v: index for index, v in enumerate(self.voltage)}
        # find all half lives
        for n, v_final in enumerate(self.volt_three):
            v_initial = self.volt_two[n]
            half_life_v = (v_final + v_initial) / 2
            v_final_index = voltage_to_index.get(v_final)
            v_initial_index = voltage_to_index.get(v_initial)
            new_v_list = [volts for volts in self.voltage if
                          v_initial_index < voltage_to_index.get(volts) < v_final_index]
            new_half_life_v = min(new_v_list, key=lambda volt: abs(volt - half_life_v))
            half_life_index = voltage_to_index[new_half_life_v]
            half_life = self.time[half_life_index]
            half_lives.append(half_life)
        # calculate capacitance
        for i, time in enumerate(half_lives):
            resistance = self.resistance_two[i]
            capacitance = time / (resistance * math.log(2))
            capacitance_list.append(capacitance)
        self.graph_data(self.v_drop_soc, capacitance_list, "State of Charge", "Capacitance")

    # produce all calculated graphs
    def produce_calc_graphs(self):
        self.find_voltage_drops()
        self.esr_graph()
        self.resistor_two_graph()
        self.capacitor_graph()
