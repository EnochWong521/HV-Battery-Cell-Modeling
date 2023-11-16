import pandas
import matplotlib.pyplot as plt


class ReadData:
    def __init__(self, file, current_range, x_axis, y_axis, soc):
        self.file_name = file
        data_file = pandas.read_csv(self.file_name)
        self.current = current_range
        self.x = x_axis
        self.y = y_axis
        self.x_axis = data_file[self.x].tolist()
        self.y_axis = data_file[self.y].tolist()
        self.soc = data_file[soc].tolist()
        self.esr_drop_list = []

    def graph_data(self):
        fig, ax = plt.subplots()
        plt.plot(self.x_axis, self.y_axis, color='blue', linestyle='-', linewidth=1)
        ax.set_xlabel(self.x, fontsize=14)
        ax.set_ylabel(self.y, fontsize=14)
        ax.set_title(f"{self.y} vs. {self.x} graph ({self.current})")
        ax.grid()
        fig.savefig(f"{self.current} {self.y} vs. {self.x} plot.png", dpi=600)

    def esr_graph(self, current):
        volt_zero = []
        volt_one = []
        esr_drop_list = []
        esr_list = []
        soc_list = []
        for index, volts in enumerate(self.y_axis):
            # calculate slope
            if index != 0 and index != len(self.y_axis) - 1:
                delta_y = volts - self.y_axis[index - 1]
                delta_x = self.x_axis[index] - self.x_axis[index - 1]
                slope_one = delta_y / delta_x
                # check if the point is an esr voltage drop
                if slope_one < -5:
                    volt_one.append(self.y_axis[index - 1])
                    volt_zero.append(volts)
                    soc_list.append(index)
        # compile a list of esr voltage drops
        for n, voltage in volt_one:
            if n != 0 and n != len(volt_one) - 1:
                esr_drop = voltage - volt_zero[n]
                esr_drop_list.append(esr_drop)
        for i, esr_diff in enumerate(esr_drop_list):
            esr = esr_diff / current
            esr_list.append(esr)
