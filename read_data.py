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
                elif slope <= 0:
                    delta_y_two = self.voltage[index + 1] - volts
                    delta_x_two = self.time[index + 1] - self.time[index]
                    slope_two = delta_y_two / delta_x_two
                    if slope_two > 1:
                        self.volt_three.append(self.voltage[index])
        # eliminate skewed values at the beginning and end of data set
        self.volt_one.pop(0)
        self.volt_one.pop(-1)
        self.volt_two.pop(0)
        self.v_drop_soc.pop(-1)

    def esr_graph(self):
        esr_drops = []
        esr_list = []
        self.find_voltage_drops()
        new_soc = [s for s in self.v_drop_soc if self.v_drop_soc.index(s) != len(self.v_drop_soc) - 1]
        # compile a list of esr voltage drops
        for n, voltage in enumerate(self.volt_one):
            esr_drop = voltage - self.volt_two[n]
            esr = esr_drop / self.current
            esr_list.append(esr)
        self.graph_data(new_soc, esr_list, "State of Charge", "Equivalent Series Resistance")

    def resistor_one_graph(self):
        r_one_drop_list = []
        for x, volt in enumerate(self.volt_two):
            r_one_drop = volt - self.volt_three[x]
            r_one = r_one_drop / self.current
            r_one_drop_list.append(r_one)
        self.graph_data(self.v_drop_soc, r_one_drop_list, "State of Charge", "Resistance 1")
        
    '''def capacitor_graph(self):'''
        








