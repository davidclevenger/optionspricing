import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class OptionValuation:
    def __init__(self):
        pass

    def run(self, data, n_days, side, type, strike, premium, n_runs = 500):
        premium = np.abs(premium)
        transformed = []

        for i in range(1, len(data)):
            transformed.append(data[i] / data[i-1])

        mean = np.mean(transformed)
        std = np.std(transformed)

        runs = []
        for _ in range(n_runs):
            curr = [data[len(data)-1]]
            syn = np.random.normal(mean, std, n_days)
            #syn = np.random.choice(transformed, n_days)
            for i in range(n_days):
                curr.append(curr[i] * syn[i])
            runs.append(curr)

        itm_cnt = 0
        profits = []
        for run in runs:
            last = run[len(run)-1]
            if side == 'LONG' or side == 'BUY':
                if type == 'CALL':
                    if last > strike:
                        itm_cnt += 1
                        plt.plot(run, color='black')
                        profits.append( ((last - strike) * 100) - premium )

                    else:  # less than or equal
                        plt.plot(run, color='red')
                        profits.append( -premium )

                elif type == 'PUT':
                    if last >= strike:
                        plt.plot(run, color='red')
                        profits.append( -premium )

                    else:  # strictly less than
                        itm_cnt += 1
                        plt.plot(run, color='black')
                        profits.append( ((strike - last) * 100) - premium )

            elif side == 'SHORT' or side == 'SELL' or side == 'WRITE':
                if type == 'CALL':
                    if last > strike:
                        plt.plot(run, color='red')
                        profits.append( ((strike - last) * 100) + premium )

                    else:  # less than or equal
                        itm_cnt += 1
                        plt.plot(run, color='black')
                        profits.append(premium)

                elif type == 'PUT':
                    if last >= strike:
                        itm_cnt += 1
                        plt.plot(run, color='black')
                        profits.append(premium)

                    else:  # strictly less than
                        plt.plot(run, color='red')
                        profits.append( ((last - strike) * 100) + premium )

        print('pct profit: ', len([x for x in profits if x > 0]) / len(profits))
        print('avg profit: ', np.mean(profits))
        plt.show()

df = pd.read_csv('path/to/csv')
adjusted = df['Adj Close']

model = OptionValuation()
model.run(adjusted, 5, 'SELL', 'CALL', 7.5, 22)


