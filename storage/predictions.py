from typing import List, Dict
from storage.warehouse import Warehouse, Product, Operation, OperationType
import matplotlib.pyplot as plt
import statistics as st


""" Czesci skladowe na funkcje prognozy """


def only_sales_for_product(wh: Warehouse, product_name: str):
    """ Funkcja wybiera z listy operacji tylko dotyczace sprzedazy oraz ewentualnie okreslonego produktu """
    # wh - magazyn, z ktorego pobieramy operacje
    # product_name - id produktu, dla ktorego sprzedaze badamy; jesli nie interesuje nas konkretny produkt, tylko
    # wszystko, wpisujemy w to miejsce None
    operations_sales = []  # pusta lista operacji dot. sprzedazy
    values = list(wh.operations.values())  # lista pobranych wartosci z operacji
    for v in values:  # wypelniamy liste
        if product_name is None:  # jesli None, to dodajemy wszystkie operacje typu Sale
            if v.type == OperationType.SALE:
                operations_sales.append(v)
        else:  # dodajemy operacje jednoczescnie typu Sale i dot. konkretnego produktu
            if v.type == OperationType.SALE and v.product.id == product_name:
                operations_sales.append(v)
    return operations_sales


def sales_sum(wh: Warehouse, product_name, only_quantities: bool, monthly: bool):
    """ Sumujemy ilosci sprzedanych produktow w kazdym okresie; tworzymy dane historyczne """
    # only_quantities: True - prognoza tylko dla ilosci sprzedanych produktow; False - prognoze sprzedazy (ilosc*cena)
    # monthly: True - sezonowosc miesieczna; False - sezonowosc kwartalna
    time_series = only_sales_for_product(wh, product_name)  # szereg czasowy sprzedazy
    keys_list = []  # lista identyfikatorow dla sprzedazy w poszczegolnych okresach
    sums_list = []  # lista wielkosci sprzedazy w poszczegolnych okresach
    sales = {}  # slownik dla wielkosci sprzedazy
    # uniwersalizacja danych
    whole_data = list(wh.operations.values())
    begin_year = time_series[0].date.year
    begin_month = time_series[0].date.month
    # do prognozy brane beda pod uwage okresy, odkad zaczelismy sprzedarz produktu (pierwszy rok/miesiac w szeregu cz.)
    # ten punkt do przemyslenia; potrzeba konsultacji
    end_year = whole_data[-1].date.year
    end_month = whole_data[-1].date.month
    # prognozujemy do ostatniego mierzonego w ogole okresu, nawet jezeli nie bylo wtedy zadnej sprzedazy
    if 1 <= begin_month <= 3:
        begin_quarter = 1
    elif 4 <= begin_month <= 6:
        begin_quarter = 2
    elif 7 <= begin_month <= 9:
        begin_quarter = 3
    else:
        begin_quarter = 4
    # do jakiego kwartalu nalezy pierwszy miesiac szeregu czasowego
    how_many_years = end_year - begin_year + 1
    # liczba lat dla danych historycznych
    if monthly == True:  # liczba okresow w ciagu roku
        k = 12
    else:
        k = 4
    for i in range(0, how_many_years):  # petla reprezentujaca kolejne lata
        for j in range(0, 12):  # petla reprezentujaca kolejne miesiace
            sum = 0
            year = begin_year + i  # rok dla iteracji i
            month = j + 1  # miesiac dla iteracji j
            if 1 <= month <= 3:  # kwartal dla kolejnych trzech iteracji j
                quarter = "I"
                quarter_to_compare = 1
            elif 4 <= month <= 6:
                quarter = "II"
                quarter_to_compare = 2
            elif 7 <= month <= 9:
                quarter = "III"
                quarter_to_compare = 3
            else:
                quarter = "IV"
                quarter_to_compare = 4  # zmienna pomocnicza
            if year == end_year and month > end_month:
                # przerywamy petle, gdy dojdziemy do ostatniego badanego miesiaca
                break
            if k == 4:
                if year == begin_year and quarter_to_compare < begin_quarter:
                    # petla pomija nastepne kroki, jezeli nie dojdziemy do pierwszego kwartalu szeregu czasowego
                    continue
                key = quarter + "_" + str(year)[-2:]  # postac identyfikatora welkosci sprzedarzy dla roku i kwartalu
            else:
                if year == begin_year and month < begin_month:
                    # petla pomija nastepne kroki, jezeli nie dojdziemy do pierwszego miesiaca szeregu czasowego
                    continue
                key = str(month) + "_" + str(year)[-2:]  # postac identyfikatora welkosci sprzedarzy dla roku i miesiaca
            keys_list.append(key)
            if len(keys_list) > 1 and keys_list[-1] == keys_list[-2]:
                keys_list.remove(key)  # jesli id sie powtarza, to go usuwamy (zdarza sie dla sez. kwartalnej)
            if k == 12:
                for t in time_series:
                    # sumowanie sprzedarzy zgodnie z danym rokiem i miesiacem
                    if t.date.year == year and t.date.month == month:
                        if only_quantities == True:
                            sum += t.quantity
                        else:
                            whole_sale = t.quantity * float(t.price.amount)
                            sum += whole_sale
                    # jesli program przejdzie do operacji dotyczacych nastepnego miesiaca/roku, to przerywamy petle
                    if t.date.year > year or (t.date.year == year and t.date.month > month):
                        break
                sums_list.append(sum)
            else:
                if month == 1 or month == 4 or month == 7 or month == 10:
                    # liczymy sumy, gdy month odpowiada pierwszemu miesiacowi w kwartale
                    for t in time_series:
                        # sumowanie sprzedarzy zgodnie z danym rokiem i kwartalem
                        if t.date.year == year and month <= t.date.month <= month + 2:
                            if only_quantities == True:
                                sum += t.quantity
                            else:
                                whole_sale = t.quantity * float(t.price.amount)
                                sum += whole_sale
                        # jesli program przejdzie do operacji dotyczacych nastepnego kwartalu/roku, to przerywamy petle
                        if t.date.year > year or (t.date.year == year and t.date.month > month + 2):
                            break
                    sums_list.append(sum)
    for i in range(0, len(sums_list)):
        sales[keys_list[i]] = sums_list[i]
    return sales


def linear_trend_parameters(wh: Warehouse, product_name, only_quantities: bool, monthly: bool):
    """ Funkcja obliczajaca parametry funkcji trendu liniowego """
    sales_dict = sales_sum(wh, product_name, only_quantities, monthly)  # dane historyczne
    t = []  # nr-y operacji od 1 do len(sales_dict)
    y = list(sales_dict.values())  # pobrane wartosci danych historycznych
    # wypelniamy liste t
    for i in range(0, len(y)):
        t.append(i+1)
    # obliczamy srednie dla t i y
    mean_t: float = st.mean(t)
    mean_y: float = st.mean(y)
    ratio_ty = []  # lista iloczynow roznic (t - t_sr) i (y - y_sr)
    square_t = []  # lista kwadratow roznic (t - t_sr)
    # wypelnianie list
    for i in range(0, len(t)):
        dif_t = t[i] - mean_t
        dif_y = y[i] - mean_y
        ratio = dif_t * dif_y
        sq_t = dif_t ** 2
        ratio_ty.append(ratio)
        square_t.append(sq_t)
    # sumowanie wartosci tych list
    sum_ty = sum(ratio_ty)
    sum_sqt = sum(square_t)
    # obliczanie parametrow
    a = sum_ty / sum_sqt
    b = mean_y - a * mean_t
    # print("Funkcja trendu: " + str(a) + "*t+" + str(b))
    return [a, b]


def seasonal_indicators_intro(wh: Warehouse, product_name, only_quantities: bool, monthly: bool, additive: bool):
    """ Funkcja liczaca wskazniki sezonowosci dla poszczegolnych okresow"""
    # additive: True - model addytywny; False - model multiplikatywny
    first_indicators = {}  # zbior wskaznikow
    sales_dict = sales_sum(wh, product_name, only_quantities, monthly)  # dane historyczne
    t = []  # # nr-y operacji od 1 do len(sales_dict)
    t_labels = list(sales_dict)  # identyfikatory danych historycznych
    y_real = list(sales_dict.values())  # wartosci danych historycznych; rzeczywiste wartosci sprzedazy
    y_trend = []  # teoretyczne wartosci sprzedazy wg funkcji trendu
    parameters = linear_trend_parameters(wh, product_name, only_quantities, monthly)  # parametry funkcji trendu
    a = parameters[0]
    b = parameters[1]
    # wypelnianie listy t
    for i in range(0, len(t_labels)):
        t.append(i+1)
    # obliczanie wartosci teoretycznych
    for i in t:
        new_y = a*i+b
        y_trend.append(new_y)
    # puste listy na wskazniki i ich identyfikatory
    indicators_list = []
    keys = []
    # obliczanie wskaznikow dla modelu addytywnego lub multiplikatywnego
    if additive == True:
        for i in range(0, len(y_trend)):
            s = y_real[i] - y_trend[i]
            indicators_list.append(s)
    else:
        for i in range(0, len(y_trend)):
            s = y_real[i] / y_trend[i]
            indicators_list.append(s)
    # tworzenie identyfikatorow dla wskaznikow
    for l in t_labels:
        ind_key = "s"+l
        keys.append(ind_key)
    for i in range(0, len(indicators_list)):
        first_indicators[keys[i]] = indicators_list[i]
    return first_indicators


def cleaning_indicators(wh: Warehouse, product_name, only_quantities: bool, monthly: bool, additive: bool):
    """ Funkcja obliczajaca wskazniki surowe i oczyszczone """
    first_indicators = seasonal_indicators_intro(wh, product_name, only_quantities, monthly, additive)  # zbior wsk.
    fi_names = list(first_indicators)  # id wskaznikow
    fi_values = list(first_indicators.values())  # wartosci wskaznikow
    # wskazniki surowe
    strict_indicators = []
    if monthly == True:  # tworzenie list id wskaznikow surowych oraz danych potrzebnych do ich obliczenia
        ind_keys = ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "s12"]
        sums = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        how_many = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    else:
        ind_keys = ["s1", "s2", "s3", "s4"]
        sums = [0, 0, 0, 0]
        how_many = [0, 0, 0, 0]
    # uzupelnianie list sums i how_many
    for i in range(0, len(fi_values)):
        num = fi_names[i][:-3]  # fragment id wskaznika "normalnego", decydujacy o jego "przynaleznosci"
        if monthly == True:
            if num == "s1":
                sums[0] = sums[0] + fi_values[i]
                how_many[0] += 1
            elif num == "s2":
                sums[1] = sums[1] + fi_values[i]
                how_many[1] += 1
            elif num == "s3":
                sums[2] = sums[2] + fi_values[i]
                how_many[2] += 1
            elif num == "s4":
                sums[3] = sums[3] + fi_values[i]
                how_many[3] += 1
            elif num == "s5":
                sums[4] = sums[4] + fi_values[i]
                how_many[4] += 1
            elif num == "s6":
                sums[5] = sums[5] + fi_values[i]
                how_many[5] += 1
            elif num == "s7":
                sums[6] = sums[6] + fi_values[i]
                how_many[6] += 1
            elif num == "s8":
                sums[7] = sums[7] + fi_values[i]
                how_many[7] += 1
            elif num == "s9":
                sums[8] = sums[8] + fi_values[i]
                how_many[8] += 1
            elif num == "s10":
                sums[9] = sums[9] + fi_values[i]
                how_many[9] += 1
            elif num == "s11":
                sums[10] = sums[10] + fi_values[i]
                how_many[10] += 1
            else:
                sums[11] = sums[11] + fi_values[i]
                how_many[11] += 1
        else:
            if num == "sI":
                sums[0] = sums[0] + fi_values[i]
                how_many[0] += 1
            elif num == "sII":
                sums[1] = sums[1] + fi_values[i]
                how_many[1] += 1
            elif num == "sIII":
                sums[2] = sums[2] + fi_values[i]
                how_many[2] += 1
            else:
                sums[3] = sums[3] + fi_values[i]
                how_many[3] += 1
    # obliczanie wskaznikow surowych
    for i in range(0, len(sums)):
        ind_mean = sums[i] / how_many[i]
        strict_indicators.append(ind_mean)
    # wskazniki oczyszczone
    cleaned_ind = {}
    main_mean = st.mean(strict_indicators)  # srednia wskaznikow surowych
    # "czyszczenie" wkaznikow
    for i in range(0, len(strict_indicators)):
        if additive == True:
            ready_ind = strict_indicators[i]-main_mean
        else:
            ready_ind = strict_indicators[i]/main_mean
        cleaned_ind[ind_keys[i]] = ready_ind
    return cleaned_ind


def counting_prediction(wh: Warehouse, product_name, only_quantities: bool, monthly: bool, additive: bool):
    """ Funkcja obliczajaca prognoze na nastepne 12 miesiecy / 4 kwartaly """
    sales = sales_sum(wh, product_name, only_quantities, monthly)  # dane historyczne
    parameters = linear_trend_parameters(wh, product_name, only_quantities, monthly)  # parametry funkcji trendu
    a = parameters[0]
    b = parameters[1]
    indicators = cleaning_indicators(wh, product_name, only_quantities, monthly, additive)  # wskazniki oczyszczone
    labels = []  # identyfikatory dla prognozowanych wartosci
    predicted_values = []  # zbior prognozowanych wartosci
    complete_prediction = {}  # slownik zbudowany z dwoch poprzednich list
    num_of_operations = len(sales)  # ile mamy danych historycznych
    # jaki byl rok dla ostatniej wartosci historycznej
    last_year = int(list(sales)[-1][-2:])
    if monthly == True:
        k = 12
        last_month = int(list(sales)[-1][:-3])  # jaki byl ostatni miesiac dla ostatniej wartosci historycznej
        # tworzenie id dla prognoz
        for j in range(0, k):
            last_month += 1
            if last_month > 12:  # jesli dojdziemy do stycznia nastepnego roku:
                last_month = 1
                last_year += 1
            new_label = str(last_month) + "_" + str(last_year)
            labels.append(new_label)
    else:
        k = 4
        last_quarter = list(sales)[-1][:-3]  # jaki byl ostatni kwartal dla ostatniej wartosci historycznej
        for j in range(0, k):
            if last_quarter == "I":
                next_quarter = "II"  # kwartal po poprzednim
            elif last_quarter == "II":
                next_quarter = "III"
            elif last_quarter == "III":
                next_quarter = "IV"
            else:  # jesli dojdziemy do pierwszego kwartalu nastepnego roku
                next_quarter = "I"
                last_year += 1
            new_label = next_quarter + "_" + str(last_year)
            labels.append(new_label)
            last_quarter = next_quarter  # "nowy' kwartal staje sie "starym" w nastepnej iteracji
    # liczenie prognozy
    for i in range(0, k):
        t = num_of_operations + i + 1  # nr-y kolejnych prognoz wzgledem danych historycznych
        y = a * t + b  # teoretyczna wartosc prognozy wg funkcji trendu
        num = labels[i][:-3]  # fragment id prognozy, ktory bedzie decydowal o wyborze wskaznika sezonowosci
        # wybor odpowiedniego wskaznika
        if k == 12:
            if num == "1":
                fluctuations = indicators["s1"]
            elif num == "2":
                fluctuations = indicators["s2"]
            elif num == "3":
                fluctuations = indicators["s3"]
            elif num == "4":
                fluctuations = indicators["s4"]
            elif num == "5":
                fluctuations = indicators["s5"]
            elif num == "6":
                fluctuations = indicators["s6"]
            elif num == "7":
                fluctuations = indicators["s7"]
            elif num == "8":
                fluctuations = indicators["s8"]
            elif num == "9":
                fluctuations = indicators["s9"]
            elif num == "10":
                fluctuations = indicators["s10"]
            elif num == "11":
                fluctuations = indicators["s11"]
            else:
                fluctuations = indicators["s12"]
        else:
            if num == "I":
                fluctuations = indicators["s1"]
            elif num == "II":
                fluctuations = indicators["s2"]
            elif num == "III":
                fluctuations = indicators["s3"]
            else:
                fluctuations = indicators["s4"]
        # uzupelnienie teoretycznej wartosci prognozy o wybrany wskaznik
        if additive == True:
            p = y + fluctuations
        else:
            p = y * fluctuations
        if p < 0:  # jesli prognoza wyjdzie ujemna, podstawiamy 0
            p = 0
        predicted_values.append(p)
    for i in range(0, len(predicted_values)):
        complete_prediction[labels[i]] = predicted_values[i]
    return complete_prediction


""" Funkcja dla wykresu prognozy """


def prediction_plot(wh: Warehouse, product_name, only_quantities: bool, monthly: bool, additive: bool, only_pred: bool):
    # only_pred: True - wykresy tylko dla prognozy; False - wykresy takze dla wartosci historycznych
    pred = counting_prediction(wh, product_name, only_quantities, monthly, additive)  # prognoza
    sales = sales_sum(wh, product_name, only_quantities, monthly)  # dane historyczne
    parameters = linear_trend_parameters(wh, product_name, only_quantities, monthly)  # parametry funkcji trendu
    a = parameters[0]
    b = parameters[1]
    sales_names = list(sales)  # nazwy dla poszczegolnych danych historycznych
    sales_values = list(sales.values())  # wartosci danych historycznych
    pred_names = list(pred)  # nazwy dla poszczegolnych prognoz
    pred_values = list(pred.values())  # wartosci prognozy
    salesandpred_names = sales_names + pred_names  # wszystkie id (id dla d. hist. oraz prognozy)
    trend_values = []  # wartosci funkcji trendu
    # obliczanie wartosci funkcji trendu
    for i in range(0, len(salesandpred_names)):
        t = i + 1
        y = a * t + b
        trend_values.append(y)
    # ustalanie osi x i y dla wykresow: 1 - dane historyczne; 2 - prognoza; t - trend
    x1 = sales_names
    y1 = sales_values
    x2 = pred_names
    y2 = pred_values
    xt = salesandpred_names
    yt = trend_values  # wartosci funkcji trendu dla wszystkich danych
    yt2 = trend_values[-len(pred_values):]  # wartosci funkcji trendu dla danych prognozowanych

    if only_pred == False:
        plt.plot(x1, y1, c='b', Label='Historical data')
        plt.plot(xt, yt, c='r', Label='Trend')
    else:
        plt.plot(x2, yt2, c='r', Label='Trend')
    plt.plot(x2, y2, c='g', Label='Prediction')

    plt.title('Prediction for the next year')
    plt.xticks(rotation=90)  # nazwy dla pozycji na osi x beda pionowo
    plt.legend()
    plt.show()
