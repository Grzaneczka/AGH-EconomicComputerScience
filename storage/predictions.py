from typing import List, Dict
from storage.warehouse import Warehouse, Product, Operation, OperationType
import matplotlib.pyplot as plt
import statistics as st


""" Czesci skladowe na funkcje prognozy """


def only_sales_for_product(wh: Warehouse, product_name: str):
    """ Funkcja wybiera z listy operacji tylko dotyczace sprzedazy oraz ewentualnie okreslonego produktu """
    operations_sales = []
    values = list(wh.operations.values())
    for v in values:
        if product_name is None:
            if v.type == OperationType.SALE:
                operations_sales.append(v)
        else:
            if v.type == OperationType.SALE and v.product.id == product_name:
                operations_sales.append(v)
    return operations_sales


def sales_sum(wh: Warehouse, product_name, only_quantities: bool, monthly: bool):
    """ Sumujemy ilosci sprzedanych produktow w kazdym miesiacu """
    time_series = only_sales_for_product(wh, product_name)
    keys_list = []
    sums_list = []
    sales = {}
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
    if monthly == True:
        k = 12
    else:
        k = 4
    for i in range(0, how_many_years):
        for j in range(0, 12):
            sum = 0
            year = begin_year + i
            month = j + 1
            if 1 <= month <= 3:
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
                quarter_to_compare = 4
            if year == end_year and month > end_month:
                # przerywamy petle, gdy dojdziemy do ostatniego badanego miesiaca
                break
            if k == 4:
                if year == begin_year and quarter_to_compare < begin_quarter:
                    # petla pomija nastepne kroki, jezeli nie dojdziemy do pierwszego kwartalu szeregu czasowego
                    continue
                key = quarter + "_" + str(year)[-2:]
            else:
                if year == begin_year and month < begin_month:
                    # petla pomija nastepne kroki, jezeli nie dojdziemy do pierwszego miesiaca szeregu czasowego
                    continue
                key = str(month) + "_" + str(year)[-2:]
            keys_list.append(key)
            if len(keys_list) > 1 and keys_list[-1] == keys_list[-2]:
                keys_list.remove(key)
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
                    for t in time_series:
                        if t.date.year == year and month <= t.date.month <= month + 2:
                            if only_quantities == True:
                                sum += t.quantity
                            else:
                                whole_sale = t.quantity * float(t.price.amount)
                                sum += whole_sale
                        if t.date.year > year or (t.date.year == year and t.date.month > month + 2):
                            break
                    sums_list.append(sum)
    for i in range(0, len(sums_list)):
        sales[keys_list[i]] = sums_list[i]
    return sales


def linear_trend_parameters(wh: Warehouse, product_name, only_quantities: bool, monthly: bool):
    sales_dict = sales_sum(wh, product_name, only_quantities, monthly)
    t = []
    y = list(sales_dict.values())
    for i in range(0, len(y)):
        t.append(i+1)
    mean_t: float = 0
    mean_y: float = 0
    for i in range(0, len(t)):
        mean_t += t[i]
        mean_y += y[i]
    mean_t /= len(t)
    mean_y /= len(y)
    ratio_ty = []
    square_t = []
    for i in range(0, len(t)):
        dif_t = t[i] - mean_t
        dif_y = y[i] - mean_y
        ratio = dif_t * dif_y
        sq_t = dif_t ** 2
        ratio_ty.append(ratio)
        square_t.append(sq_t)
    sum_ty = 0
    sum_sqt = 0
    for i in range(0, len(ratio_ty)):
        sum_ty += ratio_ty[i]
        sum_sqt += square_t[i]
    a = sum_ty / sum_sqt
    b = mean_y - a * mean_t
    # print("Funkcja trendu: " + str(a) + "*t+" + str(b))
    return [a, b]


def seasonal_indicators_intro(wh: Warehouse, product_name, only_quantities: bool, monthly: bool, additive: bool):
    first_indicators = {}
    sales_dict = sales_sum(wh, product_name, only_quantities, monthly)
    t = []
    t_labels = list(sales_dict)
    y_real = list(sales_dict.values())
    y_trend = []
    parameters = linear_trend_parameters(wh, product_name, only_quantities, monthly)
    a = parameters[0]
    b = parameters[1]
    for i in range(0, len(t_labels)):
        t.append(i+1)
    for i in t:
        new_y = a*i+b
        y_trend.append(new_y)
    indicators_list = []
    keys = []
    if additive == True:
        for i in range(0, len(y_trend)):
            s = y_real[i] - y_trend[i]
            indicators_list.append(s)
    else:
        for i in range(0, len(y_trend)):
            s = y_real[i] / y_trend[i]
            indicators_list.append(s)
    for l in t_labels:
        ind_key = "s"+l
        keys.append(ind_key)
    for i in range(0, len(indicators_list)):
        first_indicators[keys[i]] = indicators_list[i]
    return first_indicators


def cleaning_indicators(wh: Warehouse, product_name, only_quantities: bool, monthly: bool, additive: bool):
    first_indicators = seasonal_indicators_intro(wh, product_name, only_quantities, monthly, additive)
    fi_names = list(first_indicators)
    fi_values = list(first_indicators.values())
    # wskazniki surowe
    strict_indicators = []
    if monthly == True:
        ind_keys = ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "s12"]
        sums = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        how_many = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    else:
        ind_keys = ["s1", "s2", "s3", "s4"]
        sums = [0, 0, 0, 0]
        how_many = [0, 0, 0, 0]
    for i in range(0, len(fi_values)):
        num = fi_names[i][:-3]
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
    for i in range(0, len(sums)):
        ind_mean = sums[i] / how_many[i]
        strict_indicators.append(ind_mean)
    # wskazniki oczyszczone
    cleaned_ind = {}
    main_mean = st.mean(strict_indicators)
    for i in range(0, len(strict_indicators)):
        if additive == True:
            ready_ind = strict_indicators[i]-main_mean
        else:
            ready_ind = strict_indicators[i]/main_mean
        cleaned_ind[ind_keys[i]] = ready_ind
    return cleaned_ind


def counting_prediction(wh: Warehouse, product_name, only_quantities: bool, monthly: bool, additive: bool):
    sales = sales_sum(wh, product_name, only_quantities, monthly)
    parameters = linear_trend_parameters(wh, product_name, only_quantities, monthly)
    a = parameters[0]
    b = parameters[1]
    indicators = cleaning_indicators(wh, product_name, only_quantities, monthly, additive)
    labels = []
    predicted_values = []
    complete_prediction = {}
    num_of_operations = len(sales)
    last_year = int(list(sales)[-1][-2:])
    if monthly == True:
        k = 12
        last_month = int(list(sales)[-1][:-3])
        for j in range(0, k):
            last_month += 1
            if last_month > 12:
                last_month = 1
                last_year += 1
            new_label = str(last_month) + "_" + str(last_year)
            labels.append(new_label)
    else:
        k = 4
        last_quarter = list(sales)[-1][:-3]
        for j in range(0, k):
            if last_quarter == "I":
                next_quarter = "II"
            elif last_quarter == "II":
                next_quarter = "III"
            elif last_quarter == "III":
                next_quarter = "IV"
            else:
                next_quarter = "I"
                last_year += 1
            new_label = next_quarter + "_" + str(last_year)
            labels.append(new_label)
            last_quarter = next_quarter
    for i in range(0, k):
        t = num_of_operations + i + 1
        y = a * t + b
        num = labels[i][:-3]
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
        if additive == True:
            p = y + fluctuations
        else:
            p = y * fluctuations
        if p < 0:
            p = 0
        predicted_values.append(p)
    for i in range(0, len(predicted_values)):
        complete_prediction[labels[i]] = predicted_values[i]
    return complete_prediction


""" Funkcja dla wykresu prognozy """


def prediction_plot(wh: Warehouse, product_name, only_quantities: bool, monthly: bool, additive: bool, only_pred: bool):
    pred = counting_prediction(wh, product_name, only_quantities, monthly, additive)
    sales = sales_sum(wh, product_name, only_quantities, monthly)
    parameters = linear_trend_parameters(wh, product_name, only_quantities, monthly)
    a = parameters[0]
    b = parameters[1]
    sales_names = list(sales)
    sales_values= list(sales.values())
    pred_names = list(pred)
    pred_values = list(pred.values())
    salesandpred_names = sales_names + pred_names
    trend_values = []
    for i in range(0, len(salesandpred_names)):
        t = i + 1
        y = a * t + b
        trend_values.append(y)
    x1 = sales_names
    y1 = sales_values
    x2 = pred_names
    y2 = pred_values
    xt = salesandpred_names
    yt = trend_values
    yt2 = trend_values[-len(pred_values):]

    if only_pred == False:
        plt.plot(x1, y1, c='b', Label='Sale values')
        plt.plot(xt, yt, c='r', Label='Trend')
    else:
        plt.plot(x2, yt2, c='r', Label='Trend')
    plt.plot(x2, y2, c='g', Label='Predicted values')

    plt.title('Prediction for the next year')
    plt.xticks(rotation=90)
    plt.legend()
    plt.show()


# w = Warehouse()
# w.load("../data/categories.csv",
#       "../data/products.csv",
#       "../data/operations.csv")
# test = only_sales_for_product(w, "BHaP01WGry")
# test = sales_sum(w, "BHaP01WGry", True, True)
# test = sales_sum(w, None, False, False)
# test = linear_trend_parameters(w, None, True, True)
# test = seasonal_indicators_intro(w, None, True, True, False)
# test = cleaning_indicators(w, None, True, False, True)
# test = counting_prediction(w, "BHaP01WGry", False, False, False)
# print(test)
# prediction_plot(w, None, True, False, False, False)