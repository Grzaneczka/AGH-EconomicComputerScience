from contextlib import contextmanager
from datetime import date
from typing import Optional, Dict, List, Tuple

import matplotlib.pyplot as plt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from gui.templates.main_window import Ui_main_window
from storage import plots, analysis
from storage.warehouse import Warehouse, Size, Sex


class MainWindow(QMainWindow):

    # ========================================================
    #  SETUP
    # ========================================================
    def __init__(self, warehouse: Warehouse) -> None:
        super().__init__()
        self.warehouse = warehouse

        # setup ui
        self.ui = Ui_main_window()
        self.ui.setupUi(self)

        # setup plot
        self.fig = plt.figure('main')
        self.plot = FigureCanvas(self.fig)
        self.ui.plot_page.layout().addWidget(self.plot)

        # setup table
        self.table = self.ui.table

        # set stock date to today
        self.ui.stock_date.setDate(date.today())

        # connect buttons
        self.ui.comparision_income_button.clicked.connect(self._on_comparision_income_button)
        self.ui.comparision_costs_button.clicked.connect(self._on_comparision_costs_button)
        self.ui.comparision_income_balance_button.clicked.connect(self._on_comparision_income_balance_button)
        self.ui.comparision_sales_button.clicked.connect(self._on_comparision_sales_button)
        self.ui.comparision_resupply_button.clicked.connect(self._on_comparision_resupply_button)
        self.ui.comparision_operations_balance_button.clicked.connect(self._on_comparision_operations_balance_button)
        self.ui.balance_incomes_button.clicked.connect(self._on_balance_incomes_button)
        self.ui.balance_operations_button.clicked.connect(self._on_balance_operations_button)
        self.ui.stock_color_button.clicked.connect(self._on_stock_color_button)
        self.ui.stock_size_button.clicked.connect(self._on_stock_size_button)
        self.ui.analysis_colors_button.clicked.connect(self._on_analysis_colors_button)
        self.ui.analysis_sizes_button.clicked.connect(self._on_analysis_sizes_button)
        self.ui.stocktaking_button.clicked.connect(self._on_stocktaking_button)
        self.ui.stocktaking_file_button.clicked.connect(self._on_stocktaking_file_button)

        # print status
        self.ui.statusbar.showMessage(f"Wczytano {len(self.warehouse.products)} produktów, {len(self.warehouse.categories)} kategori, {len(self.warehouse.operations)} operacji")

    @contextmanager
    def display_plot(self):

        # setup figure
        self.plot.figure.clear()
        plt.figure(self.plot.figure.number)

        # setup widget
        self.ui.main_widget.setCurrentIndex(0)

        # allow for interaction
        yield

        # draw plot
        self.plot.draw()

    @contextmanager
    def display_table(self, columns: int, headers: List[str]):

        # setup table
        self.table.clear()
        self.table.setRowCount(columns)
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        # setup widget
        self.ui.main_widget.setCurrentIndex(1)

        # allow for interaction
        yield

    # ========================================================
    #  HANDLERS
    # ========================================================
    def _on_comparision_income_button(self):
        options = self._get_comparision_options()
        if not options:
            return

        with self.display_plot():
            plots.plot_income_periods(wh=self.warehouse, **options)

        self.ui.statusbar.showMessage("Wyświetlono porównanie przychodów")

    def _on_comparision_costs_button(self):
        options = self._get_comparision_options()
        if not options:
            return

        with self.display_plot():
            plots.plot_costs_periods(wh=self.warehouse, **options)

        self.ui.statusbar.showMessage("Wyświetlono porównanie kosztów")

    def _on_comparision_income_balance_button(self):
        options = self._get_comparision_options()
        if not options:
            return

        with self.display_plot():
            plots.plot_balance_periods(wh=self.warehouse, **options)

        self.ui.statusbar.showMessage("Wyświetlono porównanie bilansów dochodów")

    def _on_comparision_sales_button(self):
        options = self._get_comparision_options()
        if not options:
            return

        with self.display_plot():
            plots.plot_sales_periods(wh=self.warehouse, **options)

        self.ui.statusbar.showMessage("Wyświetlono porównanie sprzedaży")

    def _on_comparision_resupply_button(self):
        options = self._get_comparision_options()
        if not options:
            return

        with self.display_plot():
            plots.plot_resupply_periods(wh=self.warehouse, **options)

        self.ui.statusbar.showMessage("Wyświetlono porównanie dostaw")

    def _on_comparision_operations_balance_button(self):
        options = self._get_comparision_options()
        if not options:
            return

        with self.display_plot():
            plots.plot_products_balance_periods(wh=self.warehouse, **options)

        self.ui.statusbar.showMessage("Wyświetlono porównanie bilansów operacji")

    def _on_balance_incomes_button(self):
        with self.display_plot():
            plots.plot_yearly_balance(
                self.ui.balance_year_from_spinbox.value(),
                self.ui.balance_year_to_spinbox.value(),
                self.warehouse
            )

        self.ui.statusbar.showMessage("Wyświetlono roczny bilans dochodów")

    def _on_balance_operations_button(self):
        with self.display_plot():
            plots.plot_yearly_products_balance(
                self.ui.balance_year_from_spinbox.value(),
                self.ui.balance_year_to_spinbox.value(),
                self.warehouse
            )
        self.ui.statusbar.showMessage("Wyświetlono roczny bilans operacji")

    def _on_stock_color_button(self):
        options = self._get_stock_options()
        if not options:
            return

        with self.display_plot():
            plots.plot_stock_by_color(wh=self.warehouse, **options)

        self.ui.statusbar.showMessage("Wyświetlono stan magazynu według koloru")

    def _on_stock_size_button(self):
        options = self._get_stock_options()
        if not options:
            return

        with self.display_plot():
            plots.plot_stock_by_size(wh=self.warehouse, **options)

        self.ui.statusbar.showMessage("Wyświetlono stan magazynu według rozmiaru")

    def _on_analysis_colors_button(self):
        headers = ['kolor', 'sprzedane sztuki']
        sold_colors = analysis.get_best_selling_colors(
            self.ui.analysis_date_from.date(),
            self.ui.analysis_date_to.date(),
            self.warehouse
        )

        with self.display_table(len(sold_colors), headers):
            for i, (count, color) in enumerate(sold_colors):
                self.table.setItem(i, 0, QTableWidgetItem(color))
                self.table.setItem(i, 1, QTableWidgetItem(str(count)))

        self.ui.statusbar.showMessage("Wyświetlono analizę kolorów")

    def _on_analysis_sizes_button(self):
        headers = ['rozmiar', 'sprzedane sztuki']
        sold_sizes = analysis.get_best_selling_sizes(
            self.ui.analysis_date_from.date(),
            self.ui.analysis_date_to.date(),
            self.warehouse
        )

        with self.display_table(len(sold_sizes), headers):
            for i, (count, size) in enumerate(sold_sizes):
                self.table.setItem(i, 0, QTableWidgetItem(size.name))
                self.table.setItem(i, 1, QTableWidgetItem(str(count)))

        self.ui.statusbar.showMessage("Wyświetlono analizę rozmiarów")

    def _on_stocktaking_button(self):
        headers = ['id', 'nazwa', 'płeć', 'kolor', 'rozmiar', 'w systemie', 'w magazynie', 'różnica']
        stocktaking = analysis.load_stocktaking(self.ui.stocktaking_file_text.text())
        stock = analysis.get_statuses(self.warehouse)

        with self.display_table(len(stock), headers):
            for i, (prod, count) in enumerate(stock.items()):
                self.table.setItem(i, 0, QTableWidgetItem(prod.id))
                self.table.setItem(i, 1, QTableWidgetItem(prod.name))
                self.table.setItem(i, 2, QTableWidgetItem(prod.sex.name))
                self.table.setItem(i, 3, QTableWidgetItem(prod.color))
                self.table.setItem(i, 4, QTableWidgetItem(prod.size.name))
                self.table.setItem(i, 5, QTableWidgetItem(str(count)))
                self.table.setItem(i, 6, QTableWidgetItem(str(stocktaking[prod.id])))
                self.table.setItem(i, 7, QTableWidgetItem(str(count - stocktaking[prod.id])))

                # color row
                if count != stocktaking[prod.id]:
                    for col in range(8):
                        self.table.item(i, col).setBackground(QColor(255, 158, 158))

        self.ui.statusbar.showMessage("Wyświetlono porównanie z inwentaryzacją")

    def _on_stocktaking_file_button(self):
        self.ui.stocktaking_file_text.setText(
            QFileDialog.getOpenFileName(self, 'Inwentaryzacja', filter='*.csv')[0]
        )

    # ========================================================
    #  OPTIONS PARSING
    # ========================================================
    def _parse_filters(self, id_prefixes: str, names: str, categories: str, colors: str, sizes: str, sexes: str) -> Dict:
        """ Generates filters dict from given strings. """

        # prefixes
        if id_prefixes:
            # parse list
            id_prefixes = [pre.strip() for pre in id_prefixes.split(',')]

        # names
        if names:
            # parse list
            names = [name.strip() for name in names.split(',')]

        # categories
        if categories:
            # parse list
            categories_names = [cat.strip() for cat in categories.split(',')]
            # parse categories
            categories = [self.warehouse.get_category_by_name(cat) for cat in categories_names]
            # verify categories
            for name, cat in zip(categories_names, categories):
                assert cat is not None, f'Nieznana kategoria: {name}'

        # colors
        if colors:
            # parse list
            colors = [col.strip() for col in colors.split(',')]

        # sizes
        if sizes:
            # parse list
            sizes = [size.strip().upper() for size in sizes.split(',')]
            # verify sizes
            for size in sizes:
                assert size in Size.__members__, f'Nieznany rozmiar: {size}'
            # parse sizes
            sizes = [Size[size] for size in sizes]

        # sexes
        if sexes:
            # parse list
            sexes = [sex.strip().upper() for sex in sexes.split(',')]
            # verify sexes
            for sex in sexes:
                assert sex in Sex.__members__, f'Nieznana płeć: {sex}'
            # parse sexes
            sexes = [Sex[sex] for sex in sexes]

        return dict(
            id_prefixes=id_prefixes,
            names=names,
            categories=categories,
            colors=colors,
            sizes=sizes,
            sexes=sexes
        )

    def _parse_periods(self, periods: str) -> List[Tuple[date, date]]:
        """ Generates list of periods from text. """

        # parse list
        periods = [per.strip().split(' ') for per in periods.split('\n')]

        # verify periods
        for per in periods:
            assert len(per) == 2, 'Okres musi być w formacie "YYYY-MM-DD YYYY-MM-DD"'

        # parse date
        periods = [(date.fromisoformat(per[0]), date.fromisoformat(per[1])) for per in periods]

        return periods

    def _get_comparision_options(self) -> Optional[Dict]:
        """ Returns parsed options from comparision panel. """
        try:
            options = self._parse_filters(
                self.ui.comparision_filters_prefixes_text.text() or None,
                self.ui.comparision_filters_names_text.text() or None,
                self.ui.comparision_filters_categories_text.text() or None,
                self.ui.comparision_filters_colors_text.text() or None,
                self.ui.comparision_filters_sizes_text.text() or None,
                self.ui.comparision_filters_sexes_text.text() or None
            )
            options['periods'] = self._parse_periods(self.ui.comparision_periods_text.toPlainText())
            return options
        except AssertionError as e:
            self.ui.statusbar.showMessage('[BŁĄD] '+str(e))
        except ValueError as e:
            self.ui.statusbar.showMessage('[BŁĄD] Data musi być w formacie ISO: YYYY-MM-DD')

    def _get_stock_options(self) -> Optional[Dict]:
        """ Returns parsed options from stock panel. """
        try:
            options = self._parse_filters(
                self.ui.stock_filters_prefixes_text.text() or None,
                self.ui.stock_filters_names_text.text() or None,
                self.ui.stock_filters_categories_text.text() or None,
                self.ui.stock_filters_colors_text.text() or None,
                self.ui.stock_filters_sizes_text.text() or None,
                self.ui.stock_filters_sexes_text.text() or None
            )
            options['time'] = self.ui.stock_date.date()
            return options
        except AssertionError as e:
            self.ui.statusbar.showMessage('[BŁĄD] '+str(e))
