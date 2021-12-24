import time
# Время
t1, t2, t3 = time.gmtime(time.time()).tm_mday, time.gmtime(time.time()).tm_mon, time.gmtime(time.time()).tm_year
t4, t5, t6 = time.gmtime(time.time()).tm_hour + 3, time.gmtime(time.time()).tm_min, time.gmtime(time.time()).tm_sec
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import random
# Кол-во чисел
w = 0.3
axisx = [i + w for i in range(1, 11)]
randintnp = [np.random.randint(-100, 100) for _ in axisx]
randintstd = [random.randint(-100, 100) for _ in axisx]
# Случайные числа
while np.random.randint(1, 10) != random.randint(1, 10):
    randintnp = [np.random.randint(-100, 100) for _ in axisx]
    randintstd = [random.randint(-100, 100) for _ in axisx]
# Плот
fig, axs = plt.subplots(1, 3, figsize=(10, 3))
# Случайные числа стандартной библиотеки random
axs[0].bar(axisx, randintstd, width=w * 2, color='grey', label='random')
# Случайные числа библиотеки NumPy
axs[1].bar(axisx, randintnp, width=w * 2, label='NumPy')
# Случайные числа, и NumPy, и random
axs[2].bar(list(map(lambda x: x - w * 2, axisx)), randintstd, width=w, color='grey', label='random')
axs[2].bar(list(map(lambda x: x + w / 2 - w * 1.5, axisx)), randintnp, width=w, label='NumPy')
minimum = min([min(randintnp), min(randintstd)]) - 1
list(map(lambda x: (x.legend(), x.grid(), x.set_ylim(minimum, max([max(randintnp), max(randintstd)]) + 1)), axs))
fig.suptitle('Случайные числа библиотек NumPy и random')
# Окно tkinter
window = tk.Tk()
k = ('Times New Roman', int(window.winfo_screenwidth() // 130))
btn1 = tk.Button(window, font=k, text=f'Получить случайные десятки чисел в виде диаграмм на момент запуска программы ('
                                      f'{t1}.{t2}.{t3} {t4}:{t5}:{t6})', command=lambda: [window.destroy(), plt.show()])
btn1.pack(fill='both')
window.mainloop()
