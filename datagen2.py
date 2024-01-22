import numpy as np
import matplotlib.pyplot as plt
import random, math, statistics

# Seed
seed = 42069
np.random.seed(seed)
random.seed(seed)

# Init fig
fig, axs = plt.subplots(2,2)
ts = axs[0,0]
mov_a3 = axs[0,1]
mov_a7 = axs[1,0]
# Try to reverse engineer time series to generate random number that reflects more on the pattern of real world ts


# Cumsum
def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def time_series(base = 0, trend = 0, random_amp = 0, random_base = 0, sin_amp = 0, sin_base = 0, sin_period = 0, ts_size = 0, iteration = 0):
    if ts_size < 4:
        ts_size = 4
    
    if sin_period == 0:
        sin_period = 1
    return base + (iteration*trend) + (random_amp * np.random.random() + random_base) + (sin_amp * math.sin(0.5*math.pi*iteration/((ts_size//4)/sin_period)) + sin_base)

def draw(base, trend, random_amp, random_base, sin_amp, sin_period, sin_base, size, rule, i, rpm, x, yl, tsc):
    # You cant put the loop inside here directly due to a bug
    random_spike = False
    rule2_spike = False
    rule3_spike = False
    rule4_spike = False
    rule5 = False
    rule6 = False
    rule7 = False
    rule8 = False


    if rule == 1:
        random_spike = True
    elif rule == 2:
        rule2_spike = True
    elif rule == 3:
        rule3_spike = True
    elif rule == 4:
        rule4_spike = True
    elif rule == 5:
        rule5 = True
    elif rule == 6:
        rule6 = True
    elif rule == 7:
        rule7 = True
    elif rule == 8:
        rule8 = True
    
    # TS = base+trend+randomnoise+sinusodialseasonality
    y = round(time_series(base=base, trend=trend, random_amp=random_amp, random_base=random_base, sin_amp=sin_amp, sin_period=sin_period, sin_base=sin_base, ts_size=size, iteration=i))
    # print(y)

    x.append(i)

    if random_spike:
        # Trigger spike that can satisfy rule 1 
        if i == rpm:
            yl.append(y*2)
        else:
            yl.append(y)
    elif rule2_spike:
        # Trigger spike that can satisfy rule 2   
        if i == rpm or i == rpm + 1:
            yl.append(y*1.5)
        else:
            yl.append(y)
    elif rule3_spike:
        # Trigger spike that can satisfy rule 3 
        if i in range(rpm, rpm+4):
            yl.append(y*1.5)
        else:
            yl.append(y)
    elif rule4_spike:
        # Trigger spike that can satisfy rule 4 
        if i in range(rpm, rpm+8):
            yl.append(y*1.2)
        else:
            yl.append(y)
    elif rule5:
        # Trigger pattern that can satisfy rule 5 
        # This is deliberately designed to only hit the pattern for exactly 6 points as stipulated in the rules
        if i in range(rpm-1, rpm+7):
            if i == (rpm-1): # One point before the data points
                yl.append(y + (base//rpm))
            elif i == (rpm+6): # One point after the data points
                yl.append(y - (base//rpm))
            else:
                yl.append(base + random_amp // 2 + (i-rpm))
        else:
            yl.append(y)
    elif rule6:
        # Trigger pattern that can satisfy rule 6 
        if i in range(rpm, rpm+15):
            # You know I gotta do it to em
            # Run the time series function and deamplify the noise
            yl.append(round(random.randint((base + 3*(random_amp//8) + random_base), (base + 6*(random_amp//8) + random_base))))
        else:
            yl.append(y)
    elif rule7:
        # Trigger pattern that can satisfy rule 7 
        if i in range(rpm, rpm+14):
            if i % 2 == 0:
                yl.append(base + (random_amp//2) + (i-rpm))
            else:
                yl.append(base - (random_amp//4) + (i-rpm))
        else:
            yl.append(y)
    elif rule8:
        # Trigger pattern that can satisfy rule 7 
        if i in range(rpm, rpm+8):
            if i % 4 == 1 or i % 4 == 2:
                yl.append(random.randint(base + (random_amp//2) + 10, base + (random_amp//2) + 25))
            else:
                yl.append(random.randint(base + (random_amp//2) - 25, base + (random_amp//2) - 10))
        else:
            yl.append(y)
    else:
        yl.append(y)
    

    tsc.plot(x, yl, c="blue", marker = ".")
    plt.draw()
    plt.pause(0.01)

def main(base, trend, random_amp, random_base, sin_amp, sin_period, sin_base, size, tsc, spc_rule, mov3 = None, mov7 = None):
    x = []
    yl = []
    tsc.axis([0, size, None, None])
    # Had to put this outside so that the number does not change with each iteration
    rand_pos_mid = random.randint(size//4, (3*(size//4))) # Select between inter quartile range (add math form 5)
    print(rand_pos_mid)
    # Animation loop
    # qe = (-5 * (i - 50) ** 2) + (1 * (i - 50)) + 100

    # This will add values to x and yl
    for i in range(size+1):
        draw(base=base, trend=trend, random_amp=random_amp, random_base=random_base, sin_amp=sin_amp, sin_period=sin_period, sin_base=sin_base, size=size, rule=spc_rule, i=i, rpm=rand_pos_mid, x=x, yl=yl, tsc=tsc)

    avg = np.nanmean(yl)
    stdev = statistics.stdev(yl)
    ucl = avg + (stdev * 3)
    lcl = avg - (stdev * 3)
    print(avg, stdev)

    # Sigma lines
    tsc.axhline(y=avg + stdev, c="0.6", linestyle='dashed')
    tsc.axhline(y=avg - stdev, c="0.6", linestyle='dashed')
    tsc.axhline(y=avg + stdev + stdev, c="0.3", linestyle='dashed')
    tsc.axhline(y=avg - stdev - stdev, c="0.3", linestyle='dashed')
    tsc.axhline(y=avg - stdev - stdev - stdev, c="0", linestyle='dashed')
    tsc.axhline(y=avg + stdev + stdev + stdev, c="0", linestyle='dashed')
    tsc.axhline(y=avg, c="red", linestyle='dashed')
    tsc.text(0, math.ceil(avg), f"Median: {avg}")

    if mov3:
        mov3.plot(moving_average(yl,3))

    if mov7:
        mov7.plot(moving_average(yl,7))

    # Check for SPC rules
    # Rule 1
    for x,y in enumerate(yl):
        if y > ucl or y < lcl:
            tsc.scatter(x,y, c="red", zorder=2)

    # Rule 2
    for x,y in enumerate(yl):
        if x < len(yl) - 1:
            if (yl[x] > avg + (stdev * 2) or yl[x] < avg - (stdev * 2)) and (yl[x+1] > avg + (stdev * 2) or yl[x+1] < avg - (stdev * 2)):
                tsc.scatter(x,yl[x], c="green", zorder=2)
                tsc.scatter([x+1], yl[x+1], c="green", zorder=2)

    # Rule 3
    # Need to create a variable to store the streak which will be reset if its broken
    r3_streak = {}
    r3_streaks = []
    for x,y in enumerate(yl):
        if x < len(yl) - 1:
            if (y < (avg - stdev) and yl[x+1] < avg) or (y > (avg + stdev) and yl[x+1] > avg):
                r3_streak[x] = yl[x]
            else:
                r3_streaks.append(r3_streak)
                r3_streak = {}


    for st in r3_streaks:
        if st is not {} and len(st) == 4:
            for k,v in st.items():
                tsc.scatter(k,v, c="cyan", zorder=2)

    # Rule 4
    #
    r4_streak = {}
    r4_streaks = []
    for x,y in enumerate(yl):
        if x < len(yl) - 1:
            if y < avg:
                r4_streak[x] = yl[x]
                if yl[x+1] > avg:
                    r4_streaks.append(r4_streak)
                    r4_streak = {}
            else:
                r4_streak[x] = yl[x]
                if yl[x+1] < avg:
                    r4_streaks.append(r4_streak)
                    r4_streak = {}
            
    # print(r4_streaks)
    for st in r4_streaks:
        if st is not {} and len(st) == 8:
            for k,v in st.items():
                tsc.scatter(k,v, c="orange", zorder=2)

    # Rule 5
    r5_streak_a = {}
    r5_streaks_a = []
    # Loop through each value in the list

    for x, y in enumerate(yl):
        if x < len(yl) - 1:
            if yl[x+1] > y:
                r5_streak_a[x] = y
                if yl[x+1] < y:
                    r5_streak_a[x+1] = yl[x+1]
                    r5_streaks_a.append(r5_streak_a)
                    r5_streak_a = {}
            elif yl[x+1] < y:
                r5_streak_a[x] = y
                r5_streaks_a.append(r5_streak_a)
                r5_streak_a = {}
            else:
                r5_streaks_a.append(r5_streak_a)
                r5_streak_a = {}

    # Create another set of dict and list to make it detectable the other way around (descending)
    r5_streak_b = {}
    r5_streaks_b = []
    # Loop through each value in the list
    for x, y in enumerate(yl):
        if x < len(yl) - 1:
            if yl[x+1] < y:
                r5_streak_b[x] = y
                if yl[x+1] > y:
                    r5_streak_b[x+1] = yl[x+1]
                    r5_streaks_b.append(r5_streak_b)
                    r5_streak_b = {}
            elif yl[x+1] > y:
                r5_streak_b[x] = y
                r5_streaks_b.append(r5_streak_b)
                r5_streak_b = {}
            else:
                r5_streaks_b.append(r5_streak_b)
                r5_streak_b = {}

    r5_streaks = r5_streaks_a + r5_streaks_b
    for st in r5_streaks:
        if st is not {} and len(st) >= 6:
            for k,v in st.items():
                tsc.scatter(k,v, c="yellow", zorder=2)

    # Rule 6
    r6_streak = {}
    r6_streaks = []
    for x,y in enumerate(yl):
        # if x < len(yl) - 1:
            if y < (avg+stdev) and y > (avg-stdev):
                r6_streak[x] = yl[x]
            else:
                r6_streaks.append(r6_streak)
                r6_streak = {}
    
    for st in r6_streaks:
        if st is not {} and len(st) >= 15:
            for k,v in st.items():
                tsc.scatter(k,v, c="black", zorder=2)

    # Rule 7
    r7_streak = {}
    r7_streaks = []
    up = False
    for x,y in enumerate(yl):
        if x < len(yl) - 1:
            if up:
                if y < yl[x+1]:
                    r7_streak[x] = y
                    up = False
                else:
                    r7_streaks.append(r7_streak)
                    r7_streak = {}
            else:
                if y > yl[x+1]:
                    r7_streak[x] = y
                    up = True
                else:
                    r7_streaks.append(r7_streak)
                    r7_streak = {}
    
    # print(r7_streaks)
    for st in r7_streaks:
        if st is not {} and len(st) >= 14:
            print(st, end=' ')
            for k,v in st.items():
                tsc.scatter(k,v, c="magenta", zorder=2)

    # Rule 8
    # Need to create a variable to store the streak which will be reset if its broken
    r8_streak = {}
    r8_streaks = []
    for x,y in enumerate(yl):
        if x < len(yl) - 1:
            if (y < (avg - stdev)) or (y > (avg + stdev)):
                r8_streak[x] = yl[x]
            else:
                r8_streaks.append(r8_streak)
                r8_streak = {}


    for st in r8_streaks:
        if st is not {} and len(st) >= 8:
            for k,v in st.items():
                tsc.scatter(k,v, c="gold", zorder=2)

size = 100
base = 50
trend = 0
random_amp = 20
random_base = 0
sin_amp = 0
sin_period = 0
sin_base = 0
main(base, trend, random_amp, random_base, sin_amp, sin_period, sin_base, size, tsc=ts, spc_rule=8, mov3=mov_a3, mov7=mov_a7)
plt.draw()
plt.show()