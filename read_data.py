import pandas
import matplotlib.pyplot as plt


class ReadData:
    def __init__(self, file, current, current_range, time, voltage, soc):
        self.file = pandas.read_csv(file)
        self.current = current
        self.current_range = current_range
        self.time = self.file[time].tolist()
        self.voltage = self.file[voltage].tolist()
        self.soc = self.file[soc].tolist()

    def graph_data(self, x_list, y_list, x_title, y_title):
        fig, ax = plt.subplots()
        plt.plot(x_list, y_list, color='blue', linestyle='-', linewidth=1)
        ax.set_xlabel(x_title, fontsize=14)
        ax.set_ylabel(y_title, fontsize=14)
        ax.set_title(f"{y_title} vs. {x_title} graph ({self.current_range})")
        ax.grid()
        fig.savefig(f"{self.current_range} {y_title} vs. {x_title} plot.png", dpi=600)

    def esr_graph(self):
        volt_zero = []
        volt_one = []
        esr_drop_list = []
        esr_list = []
        soc_list = []
        for index, volts in enumerate(self.voltage):
            # calculate slope
            if index != 0 and index != len(self.voltage) - 1:
                delta_y = volts - self.voltage[index - 1]
                delta_x = self.time[index] - self.time[index - 1]
                slope = delta_y / delta_x
                # check if the point is an esr voltage drop
                if slope < -1:
                    volt_one.append(self.voltage[index - 1])
                    volt_zero.append(volts)
                    soc_list.append(index)
        soc_list.pop(0)
        soc_list.pop(-1)
        # compile a list of esr voltage drops
        for n, voltage in enumerate(volt_one):
            if n != 0 and n != len(volt_one) - 1:
                esr_drop = voltage - volt_zero[n]
                esr_drop_list.append(esr_drop)
        for i, esr_diff in enumerate(esr_drop_list):
            esr = esr_diff / self.current
            esr_list.append(esr)
        self.graph_data(soc_list, esr_list, "State of Charge", "Equivalent Series Resistance")

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
