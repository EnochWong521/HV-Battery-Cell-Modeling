import pandas
import matplotlib.pyplot as plt


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

    # for testing purposes
    def print_slopes(self):
        slope_list = []
        for index, volts in enumerate(self.voltage):
            # calculate slope
            if index != 0 and index != len(self.voltage) - 1:
                delta_y = volts - self.voltage[index - 1]
                delta_x = self.time[index] - self.time[index - 1]
                slope_one = delta_y / delta_x
                slope_list.append(slope_one)
        slope_list.sort()
        for n in slope_list:
            if slope_list.index(n) <= 30:
                print(n)

    def graph_data(self, x_list, y_list, x_title, y_title):
        fig, ax = plt.subplots()
        plt.plot(x_list, y_list, color='blue', linestyle='-', linewidth=1)
        ax.set_xlabel(x_title, fontsize=14)
        ax.set_ylabel(y_title, fontsize=14)
        ax.set_title(f"{y_title} vs. {x_title} graph ({self.current_range})")
        ax.grid()
        fig.savefig(f"{self.current_range} {y_title} vs. {x_title} plot.png", dpi=600)

    def find_voltage_drops(self):
        for index, volts in enumerate(self.voltage):
            # calculate slope
            if index != 0 and index != len(self.voltage) - 1:
                delta_y = volts - self.voltage[index - 1]
                delta_x = self.time[index] - self.time[index - 1]
                slope = delta_y / delta_x
                # check if the point is an esr voltage drop
                if slope < -1:
                    self.volt_one.append(self.voltage[index - 1])
                    self.volt_two.append(volts)
                    self.v_drop_soc.append(self.all_soc[index])
        self.v_drop_soc.pop(0)
        self.v_drop_soc.pop(-1)

    def esr_graph(self):
        esr_drop_list = []
        esr_list = []
        self.find_voltage_drops()
        # compile a list of esr voltage drops
        for n, voltage in enumerate(self.volt_one):
            if n != 0 and n != len(self.volt_two) - 1:
                esr_drop = voltage - self.volt_two[n]
                esr_drop_list.append(esr_drop)
        for i, esr_diff in enumerate(esr_drop_list):
            esr = esr_diff / self.current
            esr_list.append(esr)
        self.graph_data(self.v_drop_soc, esr_list, "State of Charge", "Equivalent Series Resistance")

    # def resistor_one_graph(self):



