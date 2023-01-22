import os
from datetime import datetime

import matplotlib.pyplot as plt

from config import Config
from elements.context_manager import ContextManager

config = Config.get_instance()
context_manager = ContextManager.get_instance()


def plot_data():
    if config.PLOT and context_manager.date >= config.SIMULATION_END_DATE:
        current_dir = (config.PLOT_PATH / f'{datetime.now().strftime("%d_%m_%Y__%H_%M")}')
        os.mkdir(current_dir)

        # route quality plot
        fig, ax = plt.subplots(figsize=[10, 5])
        for idx, route_quality in enumerate(context_manager.route_qualities_plot_values):
            ax.plot(route_quality, label=f'Route {idx + 1}')
        ax.legend()
        ax.set_xlabel('Hour')
        ax.set_ylabel('Route quality')
        title = ax.set_title('Routes quality over the time')
        fig.tight_layout()
        title.set_y(1.05)
        plt.show()
        fig.savefig((current_dir / 'route_quality'))

        # budget plot
        plt.figure()
        fig, ax = plt.subplots(figsize=[10, 5])
        ax.plot(context_manager.budget_plot_values)
        ax.set_xlabel('Hours')
        ax.set_ylabel('Money [PLN]')
        title = ax.set_title('Budget over time')
        fig.tight_layout()
        title.set_y(1.05)
        plt.show()
        fig.savefig((current_dir / 'budget'))

        # skiers plot
        plt.figure()
        fig, ax = plt.subplots(figsize=[10, 5])
        ax.bar(list(range(1, len(context_manager.daily_skiers_plot_values) + 1)),
               context_manager.daily_skiers_plot_values)
        ax.set_xlabel('Day')
        ax.set_ylabel('Skiers')
        title = ax.set_title('Skiers over time')
        fig.tight_layout()
        title.set_y(1.05)
        plt.show()
        fig.savefig((current_dir / 'skiers'))

        with open((current_dir / 'config.txt'), 'w') as f:
            f.write(str(config))
