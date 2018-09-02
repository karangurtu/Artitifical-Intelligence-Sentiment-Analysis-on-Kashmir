import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import pandas as pd
import matplotlib.patches as mpatches


style.use('ggplot')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    #data = open('twitter-out.txt','r').read()
    #lines = list(data.split('\n'))
    lines = pd.read_csv('twitter-out.csv')
    x_array = []
    y_array = []

    x = 0
    y = 0

    for l in lines.polarity:
        x += 1
        if l >= 0.0:
            y += 10

        elif l < 0.0:
            y -= 10

        x_array.append(x)
        y_array.append(y)
        print y_array


    ax1.clear()
    plt.title('Sentiment Graph')
    plt.xlabel('Polarity')
    plt.ylabel('Time')
    orange_patch = mpatches.Patch(color='red', label='Positivity')
    plt.legend(handles=[orange_patch])
    ax1.plot(x_array,y_array)

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()

