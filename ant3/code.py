import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
from cycler import cycler


def readIntensity(photoName, plotName, lamp, surface):
    photo = imageio.imread(photoName)

    # Обрезка по новым координатам
    # x1=969, y1=403 (левый верхний угол)
    # x2=1120, y2=706 (нижний правый угол)

    # Background - используем немного меньшую область для фона (с отступом от краев)
    background_x_start = 969
    background_x_end = 1120
    background_y_start = 403
    background_y_end = 706

    # Cut - основная область для анализа (можно использовать те же координаты или немного уже)
    cut_x_start = 980  # Немного уже для анализа
    cut_x_end = 1110  # Немного уже для анализа
    cut_y_start = 403
    cut_y_end = 706

    # Обрезка изображений
    background = photo[background_y_start:background_y_end,
    background_x_start:background_x_end, 0:3].swapaxes(0, 1)

    cut = photo[cut_y_start:cut_y_end,
    cut_x_start:cut_x_end, 0:3].swapaxes(0, 1)

    rgb = np.mean(cut, axis=(0))
    luma = 0.2989 * rgb[:, 0] + 0.5866 * rgb[:, 1] + 0.1144 * rgb[:, 2]


    plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b'])))

    fig = plt.figure(figsize=(10, 5), dpi=200)

    plt.title('Интенсивность отражённого излучения\n' + '{} / {}'.format(lamp, surface))
    plt.xlabel('Относительный номер пикселя')
    plt.ylabel('Яркость')

    #background_height = background.shape[1]  # высота фона в пикселях
    #max_data_value = max(rgb.max(), luma.max())
    #scale_factor = (background_height * 0.8) / max_data_value
    
    rgb = rgb / 2
    luma = luma /2 

    plt.plot(rgb, label=['r', 'g', 'b'])
    plt.plot(luma, 'w', label='I')
    plt.ylim(0, 150)
    plt.legend()

    background = (background * 0.7).astype(np.uint8)

    plt.imshow(background, origin='lower')

    plt.savefig(plotName)

    return luma

readIntensity("GREEN.jpg", "график_зелёный.png", "Ртутная лампа", "Зелёная поверхность")
#readIntensity("WHITE.jpg", "график_белый.png", "Лампа накаливания", "Белая поверхность")
readIntensity("BLUE.jpg", "график_синий.png", "Лампа накаливания", "Синяя поверхность")
readIntensity("RED.jpg", "график_красный.png", "Лампа накаливания", "Красная поверхность")
readIntensity("RTUT2.jpg", "график_ртуть2.png", "Ртутная лампа", "Эталонная поверхность (Ртуть)")
readIntensity("YELLOW.jpg", "график_желтый.png", "Лампа накаливания", "Жёлтая поверхность")
readIntensity("WHITE_REFERENC.jpg", "график_эталон.png", "Лампа накаливания", "Эталонная белая поверхность")
