import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
from cycler import cycler


def readIntensity(photoName, plotName, lamp, surface):
    x_min=350
    x_max=761
    x_step=50
    """
    x_min, x_max - диапазон значений на оси X (по умолчанию 0-100)
    x_step - шаг меток на оси X (по умолчанию 10)
    """
    photo = imageio.imread(photoName)

    # Обрезка по новым координатам
    background_x_start = 969
    background_x_end = 1120
    background_y_start = 403
    background_y_end = 706

    cut_x_start = 980
    cut_x_end = 1110
    cut_y_start = 403
    cut_y_end = 706

    # Обрезка изображений
    background = photo[background_y_start:background_y_end,
                background_x_start:background_x_end, 0:3].swapaxes(0, 1)

    cut = photo[cut_y_start:cut_y_end,
          cut_x_start:cut_x_end, 0:3].swapaxes(0, 1)

    rgb = np.mean(cut, axis=(0))
    luma = 0.2989 * rgb[:, 0] + 0.5866 * rgb[:, 1] + 0.1144 * rgb[:, 2]

    # ↓↓↓ КЛЮЧЕВЫЕ ИЗМЕНЕНИЯ ↓↓↓
    
    # 1. Создаем новый массив X-координат
    #    Старые координаты: 0, 1, 2, ..., len(luma)-1
    #    Новые координаты: равномерно распределенные от x_min до x_max
    x_coords = np.linspace(x_min, x_max, len(luma))
    
    # 2. Настраиваем метки оси X с нужным шагом
    #    Создаем массив меток: x_min, x_min+x_step, x_min+2*x_step, ..., x_max
    x_ticks = np.arange(x_min, x_max + x_step, x_step)
    
    plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b'])))

    fig = plt.figure(figsize=(10, 5), dpi=200)

    plt.title('Интенсивность отражённого излучения\n' + '{} / {}'.format(lamp, surface))
    plt.xlabel('Длина волны, нм')
    plt.ylabel('Яркость')

    rgb = rgb / 2
    luma = luma / 2

    # 3. Строим график с новыми X-координатами
    plt.plot(x_coords, rgb, label=['r', 'g', 'b'])
    plt.plot(x_coords, luma, 'w', label='I')
    
    plt.ylim(0, 150)
    plt.legend()
    
    # 4. Устанавливаем метки на оси X
    plt.xticks(x_ticks)

    background = (background * 0.7).astype(np.uint8)

    # 5. Растягиваем фон, чтобы он соответствовал новому диапазону X
    #    extent=[x_min, x_max, y_min, y_max] задает границы изображения
    plt.imshow(background, origin='lower', 
               extent=[x_min, x_max, 0, background.shape[1]], 
               aspect='auto')

    plt.savefig(plotName)

    return luma


# Примеры использования с разными диапазонами:
readIntensity("GREEN.jpg", "график_зелёный.png", "Ртутная лампа", 
              "Зелёная поверхность")

readIntensity("BLUE.jpg", "график_синий.png", "Лампа накаливания", 
              "Синяя поверхность")

readIntensity("RED.jpg", "график_красный.png", "Лампа накаливания", 
              "Красная поверхность")

readIntensity("RTUT2.jpg", "график_ртуть2.png", "Ртутная лампа", 
              "Эталонная поверхность (Ртуть)")

readIntensity("YELLOW.jpg", "график_желтый.png", "Лампа накаливания", 
              "Жёлтая поверхность")

readIntensity("WHITE_REFERENC.jpg", "график_эталон.png", "Лампа накаливания", 
              "Эталонная белая поверхность")