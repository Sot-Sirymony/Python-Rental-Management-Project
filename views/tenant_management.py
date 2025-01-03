
# from PyQt6.QtWidgets import (
#     QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel, QComboBox, QWidget, QHeaderView
# )
# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QFont

# class TenantManagement(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Tenant Management")
#         self.layout = QVBoxLayout()

#         # Search Bar
#         self.search_input = QLineEdit()
#         self.search_input.setPlaceholderText("Search Tenant by Name or Contact")
#         self.search_input.setStyleSheet("font-size: 14px; padding: 8px;")
#         self.search_input.textChanged.connect(self.search_tenants)
#         self.layout.addWidget(self.search_input)

#         # Tenant Table
#         self.tenant_table = QTableWidget()
#         self.tenant_table.setColumnCount(5)  # ID, Name, Contact, Actions (Edit, Delete)
#         self.tenant_table.setHorizontalHeaderLabels(["ID", "Name", "Contact", "Rental History", "Actions"])
#         self.layout.addWidget(self.tenant_table)

#         # Enable horizontal scrolling
#         self.tenant_table.setHorizontalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
#         self.tenant_table.setSizeAdjustPolicy(QTableWidget.SizeAdjustPolicy.AdjustToContents)
#         self.tenant_table.horizontalScrollBar().setVisible(True)

#         # Apply table styling
#         self.tenant_table.setStyleSheet(
#             """
#             QTableWidget::item { font-size: 14px; text-align: center; }
#             QHeaderView::section { font-size: 16px; font-weight: bold; text-align: center; }
#             """
#         )
#         self.tenant_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

#         # Buttons
#         self.add_tenant_btn = QPushButton("Add Tenant")
#         self.add_tenant_btn.setStyleSheet("font-size: 14px; padding: 10px;")
#         self.add_tenant_btn.clicked.connect(self.open_add_tenant_view)
#         self.layout.addWidget(self.add_tenant_btn)

#         self.refresh_btn = QPushButton("Refresh")
#         self.refresh_btn.setStyleSheet("font-size: 14px; padding: 10px;")
#         self.refresh_btn.clicked.connect(self.load_tenants)
#         self.layout.addWidget(self.refresh_btn)

#         self.setLayout(self.layout)
#         self.load_tenants()

#     def load_tenants(self):
#         """Fetch and display tenant data."""
#         from controllers.tenant_controller import fetch_tenants
#         tenants = fetch_tenants()
#         self.tenant_table.setRowCount(0)

#         row_font = QFont()
#         row_font.setPointSize(14)  # Set font size for row values

#         for tenant in tenants:
#             row = self.tenant_table.rowCount()
#             self.tenant_table.insertRow(row)
#             for col, data in enumerate(tenant[:3]):  # ID, Name, Contact
#                 item = QTableWidgetItem(str(data))
#                 item.setFont(row_font)  # Apply font size to row values
#                 self.tenant_table.setItem(row, col, item)

#             # Add View Rental History Button
#             history_btn = QPushButton("View History")
#             history_btn.setStyleSheet("font-size: 14px; padding: 5px;")
#             history_btn.clicked.connect(lambda _, t=tenant: self.view_rental_history(t))
#             self.tenant_table.setCellWidget(row, 3, history_btn)

#             # Add Edit Button
#             edit_btn = QPushButton("Edit")
#             edit_btn.setStyleSheet("font-size: 14px; padding: 5px;")
#             edit_btn.clicked.connect(lambda _, t=tenant: self.open_edit_tenant_view(t))
#             self.tenant_table.setCellWidget(row, 4, edit_btn)

#     def search_tenants(self, search_text):
#         """Search tenants by name or contact."""
#         from controllers.tenant_controller import fetch_tenants
#         tenants = fetch_tenants()
#         filtered_tenants = [
#             tenant for tenant in tenants if search_text.lower() in tenant[1].lower() or search_text.lower() in tenant[2].lower()
#         ]
#         self.tenant_table.setRowCount(0)

#         row_font = QFont()
#         row_font.setPointSize(14)  # Set font size for row values

#         for tenant in filtered_tenants:
#             row = self.tenant_table.rowCount()
#             self.tenant_table.insertRow(row)
#             for col, data in enumerate(tenant[:3]):  # ID, Name, Contact
#                 item = QTableWidgetItem(str(data))
#                 item.setFont(row_font)  # Apply font size to row values
#                 self.tenant_table.setItem(row, col, item)

#             # Add View Rental History Button
#             history_btn = QPushButton("View History")
#             history_btn.setStyleSheet("font-size: 14px; padding: 5px;")
#             history_btn.clicked.connect(lambda _, t=tenant: self.view_rental_history(t))
#             self.tenant_table.setCellWidget(row, 3, history_btn)

#             # Add Edit Button
#             edit_btn = QPushButton("Edit")
#             edit_btn.setStyleSheet("font-size: 14px; padding: 5px;")
#             edit_btn.clicked.connect(lambda _, t=tenant: self.open_edit_tenant_view(t))
#             self.tenant_table.setCellWidget(row, 4, edit_btn)

#     def open_add_tenant_view(self):
#         """Open add tenant view."""
#         from views.add_tenant import AddTenantView
#         dialog = AddTenantView(self)
#         if dialog.exec():
#             self.load_tenants()

#     def open_edit_tenant_view(self, tenant_data):
#         """Open edit tenant view."""
#         from views.edit_tenant import EditTenantView
#         dialog = EditTenantView(tenant_data, self)
#         if dialog.exec():
#             self.load_tenants()

#     def view_rental_history(self, tenant_data):
#         """View rental history of a tenant."""
#         print(f"Opening Rental History for tenant: {tenant_data}")  # Debug: Print tenant data
#         from views.rental_history import RentalHistoryView
#         dialog = RentalHistoryView(tenant_data, self)
#         dialog.exec()






from PyQt6.QtWidgets import (
    QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel, QComboBox, QWidget, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class TenantManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tenant Management")
        self.layout = QVBoxLayout()

        # Search Bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search Tenant by Name or Contact")
        self.search_input.setStyleSheet("font-size: 14px; padding: 8px;")
        self.search_input.textChanged.connect(self.search_tenants)
        self.layout.addWidget(self.search_input)

        # Tenant Table
        self.tenant_table = QTableWidget()
        self.tenant_table.setColumnCount(5)  # ID, Name, Contact, Actions (Edit, Delete)
        self.tenant_table.setHorizontalHeaderLabels(["ID", "Name", "Contact", "Rental History", "Actions"])
        self.layout.addWidget(self.tenant_table)

        # Enable horizontal scrolling
        self.tenant_table.setHorizontalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        self.tenant_table.setSizeAdjustPolicy(QTableWidget.SizeAdjustPolicy.AdjustToContents)
        self.tenant_table.horizontalScrollBar().setVisible(True)

        # Apply column size and styling
        self.tenant_table.horizontalHeader().setDefaultSectionSize(200)  # Default column width
        self.tenant_table.setStyleSheet(
            """
            QTableWidget::item { font-size: 14px; text-align: center; }
            QHeaderView::section { font-size: 16px; font-weight: bold; text-align: center; }
            """
        )

        # Manually set specific column widths (optional)
        self.tenant_table.setColumnWidth(0, 100)  # ID
        self.tenant_table.setColumnWidth(1, 400)  # Name
        self.tenant_table.setColumnWidth(2, 200)  # Contact
        self.tenant_table.setColumnWidth(3, 150)  # Rental History
        self.tenant_table.setColumnWidth(4, 150)  # Actions

        # Buttons
        self.add_tenant_btn = QPushButton("Add Tenant")
        self.add_tenant_btn.setStyleSheet("font-size: 14px; padding: 10px;")
        self.add_tenant_btn.clicked.connect(self.open_add_tenant_view)
        self.layout.addWidget(self.add_tenant_btn)

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setStyleSheet("font-size: 14px; padding: 10px;")
        self.refresh_btn.clicked.connect(self.load_tenants)
        self.layout.addWidget(self.refresh_btn)

        self.setLayout(self.layout)
        self.load_tenants()

    def load_tenants(self):
        """Fetch and display tenant data."""
        from controllers.tenant_controller import fetch_tenants
        tenants = fetch_tenants()
        self.tenant_table.setRowCount(0)

        row_font = QFont()
        row_font.setPointSize(14)  # Set font size for row values

        for tenant in tenants:
            row = self.tenant_table.rowCount()
            self.tenant_table.insertRow(row)
            for col, data in enumerate(tenant[:3]):  # ID, Name, Contact
                item = QTableWidgetItem(str(data))
                item.setFont(row_font)  # Apply font size to row values
                self.tenant_table.setItem(row, col, item)

            # Add View Rental History Button
            history_btn = QPushButton("View History")
            history_btn.setStyleSheet("font-size: 14px; padding: 5px;")
            history_btn.clicked.connect(lambda _, t=tenant: self.view_rental_history(t))
            self.tenant_table.setCellWidget(row, 3, history_btn)

            # Add Edit Button
            edit_btn = QPushButton("Edit")
            edit_btn.setStyleSheet("font-size: 14px; padding: 5px;")
            edit_btn.clicked.connect(lambda _, t=tenant: self.open_edit_tenant_view(t))
            self.tenant_table.setCellWidget(row, 4, edit_btn)

    def search_tenants(self, search_text):
        """Search tenants by name or contact."""
        from controllers.tenant_controller import fetch_tenants
        tenants = fetch_tenants()
        filtered_tenants = [
            tenant for tenant in tenants if search_text.lower() in tenant[1].lower() or search_text.lower() in tenant[2].lower()
        ]
        self.tenant_table.setRowCount(0)

        row_font = QFont()
        row_font.setPointSize(14)  # Set font size for row values

        for tenant in filtered_tenants:
            row = self.tenant_table.rowCount()
            self.tenant_table.insertRow(row)
            for col, data in enumerate(tenant[:3]):  # ID, Name, Contact
                item = QTableWidgetItem(str(data))
                item.setFont(row_font)  # Apply font size to row values
                self.tenant_table.setItem(row, col, item)

            # Add View Rental History Button
            history_btn = QPushButton("View History")
            history_btn.setStyleSheet("font-size: 14px; padding: 5px;")
            history_btn.clicked.connect(lambda _, t=tenant: self.view_rental_history(t))
            self.tenant_table.setCellWidget(row, 3, history_btn)

            # Add Edit Button
            edit_btn = QPushButton("Edit")
            edit_btn.setStyleSheet("font-size: 14px; padding: 5px;")
            edit_btn.clicked.connect(lambda _, t=tenant: self.open_edit_tenant_view(t))
            self.tenant_table.setCellWidget(row, 4, edit_btn)

    def open_add_tenant_view(self):
        """Open add tenant view."""
        from views.add_tenant import AddTenantView
        dialog = AddTenantView(self)
        if dialog.exec():
            self.load_tenants()

    def open_edit_tenant_view(self, tenant_data):
        """Open edit tenant view."""
        from views.edit_tenant import EditTenantView
        dialog = EditTenantView(tenant_data, self)
        if dialog.exec():
            self.load_tenants()

    def view_rental_history(self, tenant_data):
        """View rental history of a tenant."""
        print(f"Opening Rental History for tenant: {tenant_data}")  # Debug: Print tenant data
        from views.rental_history import RentalHistoryView
        dialog = RentalHistoryView(tenant_data, self)
        dialog.exec()

