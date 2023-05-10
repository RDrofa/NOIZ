# NOIZ
Программный инструмент «ПРОГНОЗ НОиЗ» представляет собой набор программных модулей предназначеных для решения следующих аналитических задач, связанных с непроизводительными отборами и закачкой воды (НОиЗ) при разработке нефтяных месторождений. 
1. Автоматизация процесса обработки исходных данных (месячных эксплуатационных рапортов (МЭР), технологических режимов, основных свойств пласта) и загрузки их в БД.
2. Оценка влияния нагнетательных скважин на добывающие скважины окружения.
3. Автоматизация оценки продуктивности нагнетательных скважин, основанной на построении графиков Холла, и оценка технологического и экономического эффекта от ремонтно-изоляционных работ (РИР) на нагнетательном фонде и сокращения непроизводительной закачки.
4. Автоматизация метода анализа источников обводнения, основанного на диагностических графиках Чена, и оценка технологического и экономического эффекта от ремонтно-изоляционных работ (РИР) на добывающем фонде и сокращения непроизводительных отборов.
5. Оптимизация системы поддержания пластового давления (ППД).
6. Повышение качества подбора скважин-кандидатов для проведения ПГИ, ГТМ, РИР, ОПЗ и регулирование режимов работы скважин.

![main](https://github.com/RDrofa/NOIZ/blob/master/docs/main.png?raw=true)

**Модуль «Оценка взаимовлияния скважин»**
* Оценка влияния нагнетательных скважин на добывающие скважины окружения
* Определение пар скважин с хорошей связью и с отсутствием связи

![spear](https://github.com/RDrofa/NOIZ/blob/master/docs/spear.png?raw=true)

**Модуль «Оценка текущих непроизводительных отборов»**
* Анализ характера обводнения (прорыв ФНВ, конусообразование, НЭК, нормальное вытеснение)
* Оценка объема непроизводительных отборов (НО)
* Экономическая оценка потенциала сокращения НО

![chen](https://github.com/RDrofa/NOIZ/blob/master/docs/chen.png?raw=true)
![no](https://github.com/RDrofa/NOIZ/blob/master/docs/no.png?raw=true)

**Модуль «Оценка текущей непроизводительной закачки»**
* Диагностика работы нагнетательных скважин
* Выявление изменений эксплуатационных характеристик, скин-фактора вследствие загрязнения ПЗП, ОПЗ, ГРП и других ГТМ, нарушений
* Оценка доли непроизводительной закачки (НЗ)

![hall](https://github.com/RDrofa/NOIZ/blob/master/docs/hall.png?raw=true)
## Входные данные
В качестве основных входных данных используется выгрузка из NGT Smart c данными МЭР и технологических режимов, а также данные свойств пласта. Входные данные загружаются в программу в виде файла Excel со строго определенными наименованиями столбцов. Порядок следования столбцов в файле значения не имеет.
* Дата
* № скважины
* Месторождение
* Объект
* Объекты работы
* Координата забоя Х
* Координата забоя Y
* Координата X
* Координата Y
* Характер работы
* Состояние
* Дебит жидкости за последний месяц, т/сут
* Дебит нефти за последний месяц, т/сут
* Обводненность за посл.месяц, % (вес)
* Дебит жидкости (ТР), м3/сут
* Дебит нефти (ТР), т/сут
* Обводненность (ТР), % (объём)
* Динамический уровень (ТР), м
* Время работы в добыче, часы
* Забойное давление (ТР), атм
* Приемистость за последний месяц, м3/сут
* Приемистость (ТР), м3/сут
* Диаметр штуцера, мм
* Закачка за посл.месяц, м3
* Время работы под закачкой, часы
* Пластовое давление (ТР), атм
* Нефтенасыщенная толщина, м

[Пример файла входных данных](https://github.com/RDrofa/NOIZ/raw/master/docs/Входные_данные.xlsx?raw=true)

Также можно загрузить в программу дополнительные данные - историю мероприятий (ГТМ)

[Пример файла истории ГТМ](https://github.com/RDrofa/NOIZ/raw/master/docs/ГТМ.xls?raw=true)

## Описание модулей Python
**noiz.py**  -  главный модуль. Реализация классов пользовательского интерфейса

**sql.py**  -  содержит класс для работы с локальной базой данных data.db  (sqlite3)

**mat.py**  -  набор различных вспомогательных функций и данных

**excl.py**  -  реализация отчетов в Excel

**gr_map.py , gr1.py**  -  классы для использования графиков matplotlib в виджетах PyQt5

**data_cls**  -  классы для работы с входными данными

**spearman_cls.py**  -  класс реализуюший метод ранговой корреляции Спирмена. Используется в модуле "Оценка взаимовлияния скважин"

**hall_cls.py**  -  класс для работы с графиками Холла. Используется в модуле "Оценка текущей непроизводительной закачки"

**hall.py**  -  набор функций реализующих метод построения графика Холла

**chen_cls.py**  -  класс для работы с графиками Чена

**chen.py**  -  набор функций реализующих метод построения графика Чена

**NO_cls.py**  -  класс для работы с графиками зависимости логарифма ВНФ от накопленной добычи

**NO.py**  -  набор функций для построения зависимости логарифма ВНФ от накопленной добычи
## Команда для сборки проекта и создания исполняемого файла .exe
    pyinstaller --onedir --noconsole --hidden-import="sklearn.utils._typedefs" main.py
После сборки проекта, в папку с программой необходимо добавить следующие папки и файлы:
* все файлы с расширением .ui  -  окна приложения
* папка "res"  -  ресурсы (иконки и т.д.)
* папка "rdp"  -  библиотека Python
* папка "Отчеты" - здесь будут сохраняться последние сформированные отчеты  
## Разработчики
Дрофа П.М., Мурзакова А.Ф., Дрофа Р.М., Рыбаковская А.А.
