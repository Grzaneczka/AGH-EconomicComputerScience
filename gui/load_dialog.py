from PyQt5.QtWidgets import QDialog, QFileDialog

from gui.templates.load_dialog import Ui_load_dialog
from storage.warehouse import Warehouse


class LoadDialog(QDialog):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.warehouse = None

        # setup ui
        self.ui = Ui_load_dialog()
        self.ui.setupUi(self)

        self.ui.load_error.setStyleSheet("color: red;")

        # wire buttons
        self.ui.load_categories_button.clicked.connect(self._on_categories_button)
        self.ui.load_operations_button.clicked.connect(self._on_operations_button)
        self.ui.load_products_button.clicked.connect(self._on_products_button)
        self.ui.load_button.clicked.connect(self._on_submit)

        # # FIXME REMOVE: only for development
        # self.ui.load_operations_text.setText('/home/grzaneczka/PycharmProjects/AGH-EconomicComputerScience/data/operations.csv')
        # self.ui.load_categories_text.setText('/home/grzaneczka/PycharmProjects/AGH-EconomicComputerScience/data/categories.csv')
        # self.ui.load_products_text.setText('/home/grzaneczka/PycharmProjects/AGH-EconomicComputerScience/data/products.csv')
        #

    def _on_submit(self):
        # TODO: handle exceptions
        try:
            self.warehouse = Warehouse()
            self.warehouse.load(
                self.ui.load_categories_text.text(),
                self.ui.load_products_text.text(),
                self.ui.load_operations_text.text()
            )
        except FileNotFoundError as e:
            self.warehouse = None
            return self.ui.load_error.setText(f'Błędna ścierzka:\n{e.filename}')
        except:
            self.warehouse = None
            return self.ui.load_error.setText('Błędny format danych')

        self.close()

    def _on_products_button(self):
        self.ui.load_products_text.setText(
            QFileDialog.getOpenFileName(self, 'Produkty', self.ui.load_products_text.text(), filter='*.csv')[0]
        )

    def _on_operations_button(self):
        self.ui.load_operations_text.setText(
            QFileDialog.getOpenFileName(self, 'Operacje', self.ui.load_operations_text.text(), filter='*.csv')[0]
        )

    def _on_categories_button(self):
        self.ui.load_categories_text.setText(
            QFileDialog.getOpenFileName(self, 'Kategorie', self.ui.load_categories_text.text(), filter='*.csv')[0]
        )
