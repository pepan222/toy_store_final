import os
import shutil
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QFont, QIcon, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QDateEdit,
    QDialog,
    QFileDialog,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from db import get_connection

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(os.path.dirname(BASE_DIR), "resources")
PHOTOS_DIR = os.path.join(RESOURCES_DIR, "photos")
ICON_ICO = os.path.join(RESOURCES_DIR, "icon.ico")
ICON_PNG = os.path.join(RESOURCES_DIR, "icon.png")
PICTURE_PNG = os.path.join(RESOURCES_DIR, "picture.png")

# Цвета по руководству стиля
COLOR_WHITE = "#FFFFFF"
COLOR_BG_SECOND = "#F5DEB3"    # дополнительный фон
COLOR_ACCENT = "#DEB887"       # акцент
COLOR_DISCOUNT_ROW = "#FFDEAD" # скидка > 17%
COLOR_ZERO_STOCK = "#ADD8E6"   # голубой (нет на складе)

@dataclass
class UserInfo:
    user_id: int | None
    full_name: str
    role_name: str

def show_error(parent, text):
    QMessageBox.critical(parent, "Ошибка", text)

def show_warn(parent, text):
    QMessageBox.warning(parent, "Предупреждение", text)

class DataService:
    @staticmethod
    def auth(login: str, password: str):
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT u.user_id, u.full_name, r.role_name
                FROM users u
                JOIN roles r ON r.role_id = u.role_id
                WHERE u.login = %s AND u.password_plain = %s
                """,
                (login, password),
            )
            row = cur.fetchone()
            return UserInfo(row["user_id"], row["full_name"], row["role_name"]) if row else None
        finally:
            conn.close()

    @staticmethod
    def get_products():
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT
                    p.product_id, p.article, p.name,
                    c.name AS category_name, p.description_text,
                    m.name AS manufacturer_name,
                    s.name AS supplier_name,
                    p.price, p.discount_percent, p.unit_name,
                    p.stock_quantity, p.photo_file
                FROM products p
                JOIN categories c ON c.category_id = p.category_id
                JOIN manufacturers m ON m.manufacturer_id = p.manufacturer_id
                JOIN suppliers s ON s.supplier_id = p.supplier_id
                ORDER BY p.product_id
                """
            )
            return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_supplier_names():
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT name FROM suppliers ORDER BY name")
            return [x[0] for x in cur.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def get_categories():
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT category_id, name FROM categories ORDER BY name")
            return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_manufacturers():
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT manufacturer_id, name FROM manufacturers ORDER BY name")
            return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_product_by_id(product_id: int):
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT p.product_id, p.article, p.name, p.category_id,
                       p.description_text, p.manufacturer_id,
                       s.name AS supplier_name, p.price, p.unit_name,
                       p.stock_quantity, p.discount_percent, p.photo_file
                FROM products p
                JOIN suppliers s ON s.supplier_id = p.supplier_id
                WHERE p.product_id = %s
                """,
                (product_id,)
            )
            return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def ensure_supplier(conn, name: str):
        cur = conn.cursor()
        cur.execute("SELECT supplier_id FROM suppliers WHERE name=%s", (name,))
        row = cur.fetchone()
        if row:
            return row[0]
        cur.execute("INSERT INTO suppliers(name) VALUES(%s)", (name,))
        conn.commit()
        return cur.lastrowid

    @staticmethod
    def save_product(model: dict):
        conn = get_connection()
        try:
            supplier_id = DataService.ensure_supplier(conn, model["supplier_name"])
            cur = conn.cursor()
            if model.get("product_id"):
                cur.execute(
                    """
                    UPDATE products
                    SET article=%s, name=%s, category_id=%s, description_text=%s,
                        manufacturer_id=%s, supplier_id=%s, price=%s, unit_name=%s,
                        stock_quantity=%s, discount_percent=%s, photo_file=%s
                    WHERE product_id=%s
                    """,
                    (model["article"], model["name"], model["category_id"],
                     model["description_text"], model["manufacturer_id"], supplier_id,
                     model["price"], model["unit_name"], model["stock_quantity"],
                     model["discount_percent"], model["photo_file"], model["product_id"])
                )
            else:
                cur.execute(
                    """
                    INSERT INTO products(article, name, category_id, description_text,
                        manufacturer_id, supplier_id, price, unit_name,
                        stock_quantity, discount_percent, photo_file)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """,
                    (model["article"], model["name"], model["category_id"],
                     model["description_text"], model["manufacturer_id"], supplier_id,
                     model["price"], model["unit_name"], model["stock_quantity"],
                     model["discount_percent"], model["photo_file"])
                )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def product_exists_in_orders(product_id: int) -> bool:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM order_items WHERE product_id=%s", (product_id,))
            return cur.fetchone()[0] > 0
        finally:
            conn.close()

    @staticmethod
    def delete_product(product_id: int):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM products WHERE product_id=%s", (product_id,))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def get_orders():
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT o.order_id, o.order_number, o.article_text,
                       os.status_name, pp.address_text,
                       o.order_date, o.delivery_date
                FROM orders o
                JOIN order_statuses os ON os.status_id = o.status_id
                JOIN pickup_points pp ON pp.pickup_point_id = o.pickup_point_id
                ORDER BY o.order_number
                """
            )
            return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_order_statuses():
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT status_id, status_name FROM order_statuses ORDER BY status_name")
            return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_pickup_points():
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT pickup_point_id, address_text FROM pickup_points ORDER BY pickup_point_id")
            return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_order_by_id(order_id: int):
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM orders WHERE order_id=%s", (order_id,))
            return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def get_next_order_number():
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT COALESCE(MAX(order_number), 0) + 1 FROM orders")
            return cur.fetchone()[0]
        finally:
            conn.close()

    @staticmethod
    def get_next_pickup_code():
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT COALESCE(MAX(pickup_code), 900) + 1 FROM orders")
            return cur.fetchone()[0]
        finally:
            conn.close()

    @staticmethod
    def parse_article_pairs(text: str):
        tokens = [x.strip() for x in (text or "").split(",") if x.strip()]
        if len(tokens) < 2 or len(tokens) % 2 != 0:
            raise ValueError("Артикулы задаются парами: артикул, количество.")
        pairs = []
        for i in range(0, len(tokens), 2):
            article = tokens[i]
            try:
                qty = int(tokens[i+1])
            except:
                raise ValueError("Количество должно быть целым числом.")
            if qty <= 0:
                raise ValueError("Количество > 0.")
            pairs.append((article, qty))
        return pairs

    @staticmethod
    def save_order(model: dict):
        conn = get_connection()
        try:
            pairs = DataService.parse_article_pairs(model["article_text"])
            cur = conn.cursor()
            article_ids = {}
            for article, _ in pairs:
                cur.execute("SELECT product_id FROM products WHERE article=%s", (article,))
                row = cur.fetchone()
                if not row:
                    raise ValueError(f"Артикул {article} не найден.")
                article_ids[article] = row[0]

            if model.get("order_id"):
                cur.execute(
                    """
                    UPDATE orders SET article_text=%s, order_date=%s, delivery_date=%s,
                        pickup_point_id=%s, status_id=%s
                    WHERE order_id=%s
                    """,
                    (model["article_text"], model["order_date"], model["delivery_date"],
                     model["pickup_point_id"], model["status_id"], model["order_id"])
                )
                order_id = model["order_id"]
                cur.execute("DELETE FROM order_items WHERE order_id=%s", (order_id,))
            else:
                cur.execute(
                    """
                    INSERT INTO orders(order_number, article_text, order_date, delivery_date,
                        pickup_point_id, client_user_id, pickup_code, status_id)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
                    """,
                    (model["order_number"], model["article_text"], model["order_date"],
                     model["delivery_date"], model["pickup_point_id"], None,
                     model["pickup_code"], model["status_id"])
                )
                order_id = cur.lastrowid

            for article, qty in pairs:
                cur.execute(
                    "INSERT INTO order_items(order_id, product_id, quantity) VALUES(%s,%s,%s)",
                    (order_id, article_ids[article], qty)
                )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def delete_order(order_id: int):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM orders WHERE order_id=%s", (order_id,))
            conn.commit()
        finally:
            conn.close()

# ---------- Диалоги ----------
class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.user_data = None
        self.setWindowTitle("Вход в систему")
        self.setMinimumWidth(430)
        if os.path.exists(ICON_ICO):
            self.setWindowIcon(QIcon(ICON_ICO))

        root = QVBoxLayout(self)
        form = QFormLayout()
        self.login_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow("Логин:", self.login_edit)
        form.addRow("Пароль:", self.password_edit)
        root.addLayout(form)

        buttons = QHBoxLayout()
        btn_login = QPushButton("Войти")
        btn_guest = QPushButton("Войти как гость")
        btn_login.setStyleSheet(f"background:{COLOR_ACCENT};")
        btn_guest.setStyleSheet(f"background:{COLOR_ACCENT};")
        btn_login.clicked.connect(self.login_click)
        btn_guest.clicked.connect(self.guest_click)
        buttons.addWidget(btn_login)
        buttons.addWidget(btn_guest)
        root.addLayout(buttons)

    def login_click(self):
        login = self.login_edit.text().strip()
        password = self.password_edit.text().strip()
        if not login or not password:
            show_warn(self, "Введите логин и пароль.")
            return
        try:
            user = DataService.auth(login, password)
        except Exception as ex:
            show_error(self, f"Ошибка БД:\n{ex}")
            return
        if user is None:
            show_error(self, "Неверный логин или пароль.")
            return
        self.user_data = user
        self.accept()

    def guest_click(self):
        self.user_data = UserInfo(None, "Гость", "Гость")
        self.accept()

class ProductFormDialog(QDialog):
    def __init__(self, product_id=None):
        super().__init__()
        self.product_id = product_id
        self.old_photo_file = ""
        self.selected_photo_path = ""
        self.setWindowTitle("Добавление/редактирование товара")
        self.setMinimumWidth(760)
        if os.path.exists(ICON_ICO):
            self.setWindowIcon(QIcon(ICON_ICO))

        root = QVBoxLayout(self)
        grid = QGridLayout()
        root.addLayout(grid)

        row = 0
        self.id_label = QLabel("ID товара:")
        self.id_edit = QLineEdit()
        self.id_edit.setReadOnly(True)
        grid.addWidget(self.id_label, row, 0)
        grid.addWidget(self.id_edit, row, 1)
        row += 1

        self.article_edit = QLineEdit()
        self.name_edit = QLineEdit()
        self.category_combo = QComboBox()
        self.description_edit = QTextEdit()
        self.description_edit.setFixedHeight(90)
        self.manufacturer_combo = QComboBox()
        self.supplier_edit = QLineEdit()
        self.price_edit = QLineEdit()
        self.unit_edit = QLineEdit()
        self.stock_edit = QLineEdit()
        self.discount_edit = QLineEdit()

        fields = [
            ("Артикул:", self.article_edit),
            ("Наименование товара:", self.name_edit),
            ("Категория товара:", self.category_combo),
            ("Описание товара:", self.description_edit),
            ("Производитель:", self.manufacturer_combo),
            ("Поставщик:", self.supplier_edit),
            ("Цена:", self.price_edit),
            ("Единица измерения:", self.unit_edit),
            ("Количество на складе:", self.stock_edit),
            ("Действующая скидка (%):", self.discount_edit),
        ]
        for title, widget in fields:
            grid.addWidget(QLabel(title), row, 0)
            grid.addWidget(widget, row, 1)
            row += 1

        photo_row = QHBoxLayout()
        self.photo_label = QLabel()
        self.photo_label.setFixedSize(300, 200)
        self.photo_label.setStyleSheet("border:1px solid #546F94;")
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_photo = QPushButton("Выбрать фото")
        btn_photo.clicked.connect(self.choose_photo)
        photo_row.addWidget(self.photo_label)
        photo_row.addWidget(btn_photo)
        root.addLayout(photo_row)

        buttons = QHBoxLayout()
        btn_save = QPushButton("Сохранить")
        btn_back = QPushButton("Назад")
        btn_save.setStyleSheet(f"background:{COLOR_ACCENT};")
        btn_back.setStyleSheet(f"background:{COLOR_BG_SECOND};")
        btn_save.clicked.connect(self.save_click)
        btn_back.clicked.connect(self.reject)
        buttons.addWidget(btn_save)
        buttons.addWidget(btn_back)
        root.addLayout(buttons)

        self.load_lookups()
        if self.product_id:
            self.load_product(self.product_id)
        else:
            self.id_label.hide()
            self.id_edit.hide()
            self.set_preview(PICTURE_PNG)

    def load_lookups(self):
        for x in DataService.get_categories():
            self.category_combo.addItem(x["name"], x["category_id"])
        for x in DataService.get_manufacturers():
            self.manufacturer_combo.addItem(x["name"], x["manufacturer_id"])

    def resolve_photo_path(self, photo_file: str):
        if photo_file:
            fname = os.path.basename(photo_file.strip())
            p = os.path.join(PHOTOS_DIR, fname)
            if os.path.exists(p):
                return p
        return PICTURE_PNG

    def load_product(self, product_id: int):
        row = DataService.get_product_by_id(product_id)
        if not row:
            show_error(self, "Товар не найден.")
            self.reject()
            return
        self.id_edit.setText(str(row["product_id"]))
        self.article_edit.setText(row["article"] or "")
        self.name_edit.setText(row["name"] or "")
        self.description_edit.setPlainText(row["description_text"] or "")
        self.supplier_edit.setText(row["supplier_name"] or "")
        self.price_edit.setText(str(row["price"]))
        self.unit_edit.setText(row["unit_name"] or "")
        self.stock_edit.setText(str(row["stock_quantity"]))
        self.discount_edit.setText(str(row["discount_percent"]))
        idx = self.category_combo.findData(row["category_id"])
        if idx >= 0:
            self.category_combo.setCurrentIndex(idx)
        jdx = self.manufacturer_combo.findData(row["manufacturer_id"])
        if jdx >= 0:
            self.manufacturer_combo.setCurrentIndex(jdx)
        self.old_photo_file = row["photo_file"] or ""
        self.set_preview(self.resolve_photo_path(self.old_photo_file))

    def set_preview(self, path: str):
        pix = QPixmap(path)
        if pix.isNull():
            self.photo_label.setText("Нет фото")
            return
        self.photo_label.setPixmap(pix.scaled(300, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def choose_photo(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выберите фото", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if not path:
            return
        pix = QPixmap(path)
        if pix.isNull():
            show_warn(self, "Не удалось прочитать изображение.")
            return
        if pix.width() > 300 or pix.height() > 200:
            show_warn(self, "Размер фото не должен превышать 300x200 пикселей.")
            return
        self.selected_photo_path = path
        self.set_preview(path)

    def save_click(self):
        article = self.article_edit.text().strip()
        name = self.name_edit.text().strip()
        supplier = self.supplier_edit.text().strip()
        unit = self.unit_edit.text().strip()
        description = self.description_edit.toPlainText().strip()
        if not article or not name or not supplier or not unit:
            show_warn(self, "Заполните обязательные поля: артикул, наименование, поставщик, единица измерения.")
            return
        try:
            price = Decimal(self.price_edit.text().strip().replace(",", "."))
            stock = int(self.stock_edit.text().strip())
            discount = Decimal(self.discount_edit.text().strip().replace(",", "."))
        except:
            show_error(self, "Проверьте формат цены, количества и скидки.")
            return
        if price < 0 or stock < 0 or discount < 0:
            show_error(self, "Цена, количество и скидка не могут быть отрицательными.")
            return
        photo_file = self.old_photo_file
        if self.selected_photo_path:
            os.makedirs(PHOTOS_DIR, exist_ok=True)
            ext = os.path.splitext(self.selected_photo_path)[1].lower() or ".png"
            new_name = f"uploaded_{uuid.uuid4().hex}{ext}"
            target = os.path.join(PHOTOS_DIR, new_name)
            shutil.copy2(self.selected_photo_path, target)
            photo_file = f"resources/photos/{new_name}"
            if self.old_photo_file:
                old_path = os.path.join(PHOTOS_DIR, os.path.basename(self.old_photo_file))
                if os.path.exists(old_path):
                    try:
                        os.remove(old_path)
                    except:
                        pass
        model = {
            "product_id": self.product_id,
            "article": article, "name": name,
            "category_id": self.category_combo.currentData(),
            "description_text": description or None,
            "manufacturer_id": self.manufacturer_combo.currentData(),
            "supplier_name": supplier,
            "price": price, "unit_name": unit,
            "stock_quantity": stock, "discount_percent": discount,
            "photo_file": photo_file or None,
        }
        try:
            DataService.save_product(model)
        except Exception as ex:
            show_error(self, f"Ошибка сохранения:\n{ex}")
            return
        self.accept()

class OrderFormDialog(QDialog):
    def __init__(self, order_id=None):
        super().__init__()
        self.order_id = order_id
        self.setWindowTitle("Добавление/редактирование заказа")
        self.setMinimumWidth(680)
        if os.path.exists(ICON_ICO):
            self.setWindowIcon(QIcon(ICON_ICO))

        root = QVBoxLayout(self)
        form = QFormLayout()
        root.addLayout(form)

        self.order_number_edit = QLineEdit()
        self.order_number_edit.setReadOnly(True)
        self.articles_edit = QLineEdit()
        self.status_combo = QComboBox()
        self.pickup_combo = QComboBox()
        self.order_date_edit = QDateEdit()
        self.order_date_edit.setCalendarPopup(True)
        self.order_date_edit.setDisplayFormat("yyyy-MM-dd")
        self.delivery_date_edit = QDateEdit()
        self.delivery_date_edit.setCalendarPopup(True)
        self.delivery_date_edit.setDisplayFormat("yyyy-MM-dd")

        form.addRow("Номер заказа:", self.order_number_edit)
        form.addRow("Артикул (пары: артикул,кол-во, ...):", self.articles_edit)
        form.addRow("Статус заказа:", self.status_combo)
        form.addRow("Адрес пункта выдачи:", self.pickup_combo)
        form.addRow("Дата заказа:", self.order_date_edit)
        form.addRow("Дата выдачи:", self.delivery_date_edit)

        for x in DataService.get_order_statuses():
            self.status_combo.addItem(x["status_name"], x["status_id"])
        for x in DataService.get_pickup_points():
            self.pickup_combo.addItem(f'{x["pickup_point_id"]}. {x["address_text"]}', x["pickup_point_id"])

        if self.order_id:
            self.load_order(self.order_id)
        else:
            self.order_number_edit.setText(str(DataService.get_next_order_number()))
            self.generated_pickup_code = DataService.get_next_pickup_code()
            today = QDate.currentDate()
            self.order_date_edit.setDate(today)
            self.delivery_date_edit.setDate(today.addDays(1))

        buttons = QHBoxLayout()
        btn_save = QPushButton("Сохранить")
        btn_back = QPushButton("Назад")
        btn_save.setStyleSheet(f"background:{COLOR_ACCENT};")
        btn_back.setStyleSheet(f"background:{COLOR_BG_SECOND};")
        btn_save.clicked.connect(self.save_click)
        btn_back.clicked.connect(self.reject)
        buttons.addWidget(btn_save)
        buttons.addWidget(btn_back)
        root.addLayout(buttons)

    def load_order(self, order_id: int):
        row = DataService.get_order_by_id(order_id)
        if not row:
            show_error(self, "Заказ не найден.")
            self.reject()
            return
        self.order_number_edit.setText(str(row["order_number"]))
        self.articles_edit.setText(row["article_text"] or "")
        self.generated_pickup_code = row["pickup_code"]
        idx = self.status_combo.findData(row["status_id"])
        if idx >= 0:
            self.status_combo.setCurrentIndex(idx)
        jdx = self.pickup_combo.findData(row["pickup_point_id"])
        if jdx >= 0:
            self.pickup_combo.setCurrentIndex(jdx)
        if row["order_date"]:
            dt = row["order_date"]
            self.order_date_edit.setDate(QDate(dt.year, dt.month, dt.day))
        if row["delivery_date"]:
            dt = row["delivery_date"]
            self.delivery_date_edit.setDate(QDate(dt.year, dt.month, dt.day))

    def save_click(self):
        articles = self.articles_edit.text().strip()
        if not articles:
            show_warn(self, "Поле Артикул обязательно.")
            return
        try:
            DataService.parse_article_pairs(articles)
        except Exception as ex:
            show_error(self, str(ex))
            return
        model = {
            "order_id": self.order_id,
            "order_number": int(self.order_number_edit.text()),
            "article_text": articles,
            "status_id": self.status_combo.currentData(),
            "pickup_point_id": self.pickup_combo.currentData(),
            "order_date": self.order_date_edit.date().toString("yyyy-MM-dd"),
            "delivery_date": self.delivery_date_edit.date().toString("yyyy-MM-dd"),
            "pickup_code": self.generated_pickup_code,
        }
        try:
            DataService.save_order(model)
        except Exception as ex:
            show_error(self, f"Ошибка сохранения:\n{ex}")
            return
        self.accept()

class OrdersDialog(QDialog):
    def __init__(self, user_data: UserInfo, parent=None):
        super().__init__(parent)
        self.user_data = user_data
        self.setWindowTitle("Заказы")
        self.resize(1200, 640)
        if os.path.exists(ICON_ICO):
            self.setWindowIcon(QIcon(ICON_ICO))

        root = QVBoxLayout(self)
        top = QHBoxLayout()
        title = QLabel("Список заказов")
        title.setStyleSheet("font-size:24px; font-weight:700;")
        top.addWidget(title)
        top.addStretch()
        self.btn_add = QPushButton("Добавить заказ")
        self.btn_edit = QPushButton("Редактировать заказ")
        self.btn_delete = QPushButton("Удалить заказ")
        btn_back = QPushButton("Назад")
        self.btn_add.clicked.connect(self.add_order)
        self.btn_edit.clicked.connect(self.edit_order)
        self.btn_delete.clicked.connect(self.delete_order)
        btn_back.clicked.connect(self.close)
        top.addWidget(self.btn_add)
        top.addWidget(self.btn_edit)
        top.addWidget(self.btn_delete)
        top.addWidget(btn_back)
        root.addLayout(top)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Номер", "Артикул заказа", "Статус", "Пункт выдачи", "Дата заказа", "Дата выдачи"])
        self.table.doubleClicked.connect(self.double_click_order)
        root.addWidget(self.table)

        is_admin = (self.user_data.role_name == "Администратор")
        self.btn_add.setVisible(is_admin)
        self.btn_edit.setVisible(is_admin)
        self.btn_delete.setVisible(is_admin)
        self.load_orders()

    def load_orders(self):
        rows = DataService.get_orders()
        self.table.setRowCount(len(rows))
        for i, x in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(str(x["order_number"])))
            self.table.setItem(i, 1, QTableWidgetItem(x["article_text"] or ""))
            self.table.setItem(i, 2, QTableWidgetItem(x["status_name"] or ""))
            self.table.setItem(i, 3, QTableWidgetItem(x["address_text"] or ""))
            self.table.setItem(i, 4, QTableWidgetItem(str(x["order_date"] or "")))
            self.table.setItem(i, 5, QTableWidgetItem(str(x["delivery_date"] or "")))
            self.table.item(i, 0).setData(Qt.ItemDataRole.UserRole, x["order_id"])
        self.table.resizeColumnsToContents()

    def current_order_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        item = self.table.item(row, 0)
        return item.data(Qt.ItemDataRole.UserRole) if item else None

    def add_order(self):
        if self.user_data.role_name != "Администратор":
            return
        dlg = OrderFormDialog()
        if dlg.exec():
            self.load_orders()

    def edit_order(self):
        if self.user_data.role_name != "Администратор":
            return
        oid = self.current_order_id()
        if not oid:
            show_warn(self, "Выберите заказ.")
            return
        dlg = OrderFormDialog(oid)
        if dlg.exec():
            self.load_orders()

    def double_click_order(self):
        if self.user_data.role_name == "Администратор":
            self.edit_order()

    def delete_order(self):
        if self.user_data.role_name != "Администратор":
            return
        oid = self.current_order_id()
        if not oid:
            show_warn(self, "Выберите заказ.")
            return
        if QMessageBox.question(self, "Подтверждение", "Удалить заказ?") == QMessageBox.StandardButton.Yes:
            try:
                DataService.delete_order(oid)
                self.load_orders()
            except Exception as ex:
                show_error(self, f"Ошибка удаления: {ex}")

class ProductsWindow(QMainWindow):
    def __init__(self, user_data: UserInfo):
        super().__init__()
        self.user_data = user_data
        self.products = []
        self.product_editor_opened = False

        self.setWindowTitle("МирИгрушек - Список товаров")
        self.resize(1600, 820)
        if os.path.exists(ICON_ICO):
            self.setWindowIcon(QIcon(ICON_ICO))

        root = QWidget()
        self.setCentralWidget(root)
        main = QVBoxLayout(root)

        header = QGridLayout()
        logo = QLabel()
        if os.path.exists(ICON_PNG):
            pix = QPixmap(ICON_PNG).scaled(120, 70, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo.setPixmap(pix)
        title = QLabel("ООО «МирИгрушек» — Список товаров")
        title.setStyleSheet("font-size:28px; font-weight:700;")
        self.role_label = QLabel(f"Роль: {self.user_data.role_name}")
        self.user_label = QLabel(f"Пользователь: {self.user_data.full_name}")
        self.btn_orders = QPushButton("Заказы")
        self.btn_orders.setStyleSheet(f"background:{COLOR_ACCENT};")
        self.btn_orders.clicked.connect(self.open_orders)
        btn_logout = QPushButton("Выход")
        btn_logout.setStyleSheet(f"background:{COLOR_ACCENT};")
        btn_logout.clicked.connect(self.logout)

        right = QVBoxLayout()
        right.addWidget(self.role_label, alignment=Qt.AlignmentFlag.AlignRight)
        right.addWidget(self.user_label, alignment=Qt.AlignmentFlag.AlignRight)
        right.addWidget(self.btn_orders, alignment=Qt.AlignmentFlag.AlignRight)
        right.addWidget(btn_logout, alignment=Qt.AlignmentFlag.AlignRight)

        header.addWidget(logo, 0, 0)
        header.addWidget(title, 0, 1)
        header.addLayout(right, 0, 2)
        header.setColumnStretch(1, 1)
        main.addLayout(header)

        # Фильтры, поиск, сортировка
        self.filter_wrap = QWidget()
        filter_layout = QHBoxLayout(self.filter_wrap)
        filter_layout.addWidget(QLabel("Поиск:"))
        self.search_edit = QLineEdit()
        filter_layout.addWidget(self.search_edit)
        filter_layout.addWidget(QLabel("Поставщик:"))
        self.supplier_combo = QComboBox()
        filter_layout.addWidget(self.supplier_combo)
        filter_layout.addWidget(QLabel("Сортировка:"))
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Без сортировки", "Остаток (по возрастанию)", "Остаток (по убыванию)", "Цена (по возрастанию)", "Цена (по убыванию)"])
        filter_layout.addWidget(self.sort_combo)
        main.addWidget(self.filter_wrap)

        # Кнопки админа
        self.admin_wrap = QWidget()
        admin_layout = QHBoxLayout(self.admin_wrap)
        self.btn_add = QPushButton("Добавить товар")
        self.btn_edit = QPushButton("Редактировать товар")
        self.btn_delete = QPushButton("Удалить товар")
        self.btn_add.setStyleSheet(f"background:{COLOR_ACCENT};")
        self.btn_edit.setStyleSheet(f"background:{COLOR_BG_SECOND};")
        self.btn_delete.setStyleSheet(f"background:{COLOR_BG_SECOND};")
        admin_layout.addWidget(self.btn_add)
        admin_layout.addWidget(self.btn_edit)
        admin_layout.addWidget(self.btn_delete)
        admin_layout.addStretch()
        main.addWidget(self.admin_wrap)

        self.table = QTableWidget()
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels(
            ["Фото", "Артикул", "Наименование", "Категория", "Описание",
             "Производитель", "Поставщик", "Цена", "Цена со скидкой", "Ед.", "Остаток", "Скидка"]
        )
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.doubleClicked.connect(self.row_double_click)
        main.addWidget(self.table)

        self.btn_add.clicked.connect(self.add_product)
        self.btn_edit.clicked.connect(self.edit_product)
        self.btn_delete.clicked.connect(self.delete_product)
        self.search_edit.textChanged.connect(self.apply_filters)
        self.supplier_combo.currentTextChanged.connect(self.apply_filters)
        self.sort_combo.currentTextChanged.connect(self.apply_filters)

        self.apply_role_rules()
        self.load_suppliers()
        self.load_products()

    def is_admin(self):
        return self.user_data.role_name == "Администратор"

    def is_manager_or_admin(self):
        return self.user_data.role_name in ("Менеджер", "Администратор")

    def apply_role_rules(self):
        advanced = self.is_manager_or_admin()
        self.filter_wrap.setVisible(advanced)
        self.admin_wrap.setVisible(self.is_admin())
        self.btn_orders.setVisible(advanced)

    def load_suppliers(self):
        self.supplier_combo.clear()
        self.supplier_combo.addItem("Все поставщики")
        for x in DataService.get_supplier_names():
            self.supplier_combo.addItem(x)

    def load_products(self):
        self.products = DataService.get_products()
        self.apply_filters()

    def photo_pixmap(self, photo_file: str):
        if photo_file:
            p = os.path.join(PHOTOS_DIR, os.path.basename(photo_file))
            if os.path.exists(p):
                pix = QPixmap(p)
                if not pix.isNull():
                    return pix
        return QPixmap(PICTURE_PNG)

    def apply_filters(self):
        data = list(self.products)
        if self.is_manager_or_admin():
            text = self.search_edit.text().strip().lower()
            supplier = self.supplier_combo.currentText()
            sort_mode = self.sort_combo.currentText()
            if supplier and supplier != "Все поставщики":
                data = [x for x in data if (x.get("supplier_name") or "").lower() == supplier.lower()]
            if text:
                def hit(row):
                    fields = [row.get("article"), row.get("name"), row.get("category_name"),
                              row.get("description_text"), row.get("manufacturer_name"),
                              row.get("supplier_name"), row.get("unit_name")]
                    return any(text in str(v or "").lower() for v in fields)
                data = [x for x in data if hit(x)]
            if sort_mode == "Остаток (по возрастанию)":
                data.sort(key=lambda r: int(r.get("stock_quantity") or 0))
            elif sort_mode == "Остаток (по убыванию)":
                data.sort(key=lambda r: int(r.get("stock_quantity") or 0), reverse=True)
            elif sort_mode == "Цена (по возрастанию)":
                data.sort(key=lambda r: float(r.get("price") or 0))
            elif sort_mode == "Цена (по убыванию)":
                data.sort(key=lambda r: float(r.get("price") or 0), reverse=True)
        self.fill_table(data)

    def fill_table(self, rows):
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            pix = self.photo_pixmap(row.get("photo_file") or "")
            img_label = QLabel()
            img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            img_label.setPixmap(pix.scaled(90, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            self.table.setCellWidget(i, 0, img_label)

            price = Decimal(str(row.get("price") or 0))
            discount = Decimal(str(row.get("discount_percent") or 0))
            final_price = (price * (Decimal("100") - discount) / Decimal("100")).quantize(Decimal("0.01"))

            values = [
                row.get("article") or "",
                row.get("name") or "",
                row.get("category_name") or "",
                row.get("description_text") or "",
                row.get("manufacturer_name") or "",
                row.get("supplier_name") or "",
                f"{price:.2f}",
                f"{final_price:.2f}",
                row.get("unit_name") or "",
                str(row.get("stock_quantity") or 0),
                f"{discount:.2f}",
            ]
            for c, v in enumerate(values, start=1):
                item = QTableWidgetItem(v)
                self.table.setItem(i, c, item)

            self.table.item(i, 1).setData(Qt.ItemDataRole.UserRole, row["product_id"])

            price_item = self.table.item(i, 7)
            if discount > 0:
                font = price_item.font()
                font.setStrikeOut(True)
                price_item.setFont(font)
                price_item.setForeground(QColor("red"))

            # Цвет строки
            row_color = QColor(COLOR_WHITE)
            fg_color = QColor("#111827")
            stock = int(row.get("stock_quantity") or 0)
            if stock == 0:
                row_color = QColor(COLOR_ZERO_STOCK)
            elif discount > 17:
                row_color = QColor(COLOR_DISCOUNT_ROW)

            for col in range(1, self.table.columnCount()):
                cell = self.table.item(i, col)
                if cell:
                    cell.setBackground(row_color)
                    cell.setForeground(fg_color)

        self.table.resizeColumnsToContents()
        self.table.setColumnWidth(0, 100)

    def selected_product_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        item = self.table.item(row, 1)
        return item.data(Qt.ItemDataRole.UserRole) if item else None

    def add_product(self):
        if not self.is_admin():
            return
        if self.product_editor_opened:
            show_warn(self, "Окно редактирования уже открыто.")
            return
        self.product_editor_opened = True
        dlg = ProductFormDialog()
        ok = dlg.exec()
        self.product_editor_opened = False
        if ok:
            self.load_suppliers()
            self.load_products()

    def edit_product(self):
        if not self.is_admin():
            return
        pid = self.selected_product_id()
        if not pid:
            show_warn(self, "Выберите товар.")
            return
        if self.product_editor_opened:
            show_warn(self, "Окно редактирования уже открыто.")
            return
        self.product_editor_opened = True
        dlg = ProductFormDialog(pid)
        ok = dlg.exec()
        self.product_editor_opened = False
        if ok:
            self.load_suppliers()
            self.load_products()

    def row_double_click(self):
        if self.is_admin():
            self.edit_product()

    def delete_product(self):
        if not self.is_admin():
            return
        pid = self.selected_product_id()
        if not pid:
            show_warn(self, "Выберите товар.")
            return
        if DataService.product_exists_in_orders(pid):
            show_warn(self, "Товар присутствует в заказе. Удаление невозможно.")
            return
        if QMessageBox.question(self, "Подтверждение", "Удалить товар?") == QMessageBox.StandardButton.Yes:
            try:
                DataService.delete_product(pid)
                self.load_suppliers()
                self.load_products()
            except Exception as ex:
                show_error(self, f"Ошибка удаления: {ex}")

    def open_orders(self):
        if not self.is_manager_or_admin():
            return
        dlg = OrdersDialog(self.user_data, self)
        dlg.exec()

    def logout(self):
        self.close()
        login = LoginDialog()
        if login.exec():
            self.next_window = ProductsWindow(login.user_data)
            self.next_window.show()

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Arial", 11))   # шрифт по руководству стиля
    login = LoginDialog()
    if not login.exec():
        sys.exit(0)
    window = ProductsWindow(login.user_data)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()