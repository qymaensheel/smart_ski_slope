import pickle

from matplotlib import pyplot as plt

path_dumb = r'C:\Users\bbart\PycharmProjects\smart_ski_slope\outputs\22_01_2023__23_25 - dumb\dump_slope_data.pickle'
path_smart = r'C:\Users\bbart\PycharmProjects\smart_ski_slope\outputs\22_01_2023__23_34 - smart\dump_slope_data.pickle'


with open(path_dumb, 'rb') as f:
    data_dumb = pickle.load(f)

with open(path_smart, 'rb') as f:
    data_smart = pickle.load(f)


# budget comparison

plt.figure()
fig, ax = plt.subplots(figsize=[10, 5])
ax.plot(data_dumb["budget_plot_values"], label='Dumb')
ax.plot(data_smart["budget_plot_values"], label='Smart')
ax.set_xlabel('Hours')
ax.set_ylabel('Money [PLN]')
title = ax.set_title('Budget over time comparison')
fig.tight_layout()
title.set_y(1.05)
ax.legend()
plt.show()
fig.savefig(r'C:\Users\bbart\PycharmProjects\smart_ski_slope\outputs' + r'\budget_comparison')
