#-------------------------------------------------------------------------------
# Name:        Films.py
# Purpose:
#
# Author:      NPL
#
# Created:     01.11.2021
# Copyright:   (c) 2021
# Licence:     <My>
#-------------------------------------------------------------------------------
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtWidgets
import FormUI
from PyQt5 import QtSql
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem

class UIForm(QtWidgets.QMainWindow, FormUI.Ui_MainWindow):
    
    def __init__(self, path):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.currentChanged.connect(self.changeTab2) # изменение вкладки
        self.addBtn.clicked.connect(self.add_row)  # OK BUTTON
        self.tableWidget.clicked.connect(self.select_row) # SELECT ROW in TABLE
        self.tableWidget.doubleClicked.connect(self.edit_mode) #Изменение строки (2-ой клик)
        self.Ed_find.editingFinished.connect(self.search_title_orig) # Поиск по оригинальному назваию
        self.Ed_find2.editingFinished.connect(self.search_title) # Поиск по названию

        self.comboBox_2.addItems(["Боевик", "Детектив", "Триллер", "Катастрофа", "Комедия", "Ужасы", "Фантастика"])

        self.path = path
        self.con1 = self.create_connection(path)
        self.read_table(self.con1, "SELECT id, num, title_orig, title, year, genre, country, director, actors, desc, prim, tags, img FROM films")
        self.create_films_table = """
        CREATE TABLE IF NOT EXISTS films (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          num TEXT,
          title_orig TEXT NOT NULL,
          title TEXT,
          year INTEGER,
          genre TEXT,
          country TEXT,
          director TEXT,
          actors TEXT,
          desc TEXT,
          prim TEXT,
          tags TEXT,
          img TEXT
        );
        """
        self.current_row = 0
        self.edit_flag = False
        
        # i m a g e -----------------------------------------
        pixmap = QPixmap('data/img0.jpg')
        pixmap_small = pixmap.scaled(400,400, QtCore.Qt.KeepAspectRatio)
        self.label_pix.setScaledContents(True)
        self.label_pix.setPixmap(pixmap_small)

    # ====== S E A R C H ======================================================
    def search(self, key_string, query_string):
        query = QSqlQuery()
        query.prepare(query_string)
        format_key = key_string.lower()  
        query.addBindValue('%'+key_string.title()+'%')
        query.exec_()
        
        self.tableWidget.setRowCount(0)
        while query.next():
            rows = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(rows + 1)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(query.value(0))))
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(query.value(1))))
            self.tableWidget.setItem(rows, 2, QTableWidgetItem(str(query.value(2))))
            self.tableWidget.setItem(rows, 3, QTableWidgetItem(str(query.value(3))))
            self.tableWidget.setItem(rows, 4, QTableWidgetItem(str(query.value(4))))
            self.tableWidget.setItem(rows, 5, QTableWidgetItem(str(query.value(5))))
            self.tableWidget.setItem(rows, 6, QTableWidgetItem(str(query.value(6))))
            self.tableWidget.setItem(rows, 7, QTableWidgetItem(str(query.value(7))))
            self.tableWidget.setItem(rows, 8, QTableWidgetItem(str(query.value(8))))
            self.tableWidget.setItem(rows, 9, QTableWidgetItem(str(query.value(9))))
            self.tableWidget.setItem(rows, 10, QTableWidgetItem(str(query.value(10))))
            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.resizeRowsToContents()
    
    
    def search_title_orig(self):  
        self.search (self.Ed_find.text(), "SELECT id, num, title_orig, title, year, genre, country, director, actors, desc, prim, tags, img FROM films WHERE title_orig LIKE ?")
        
    def search_title(self):
        self.search (self.Ed_find2.text(), "SELECT id, num, title_orig, title, year, genre, country, director, actors, desc, prim, tags, img FROM films WHERE title LIKE ?")

    # - - - - - -  T A B L E   s e c  - - - - - -

    def create_connection(self, path):
        connection = None
        try:
            connection = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            connection.setDatabaseName(path)
            connection.open()
            print("Connection to SQLite DB succesful.")
        except Error as e:
            print("The error occurred:")
            print(e)
        return connection

    def create_table(self, connection, query):
        createTableQuery = QSqlQuery()
        try:
            createTableQuery.exec(query)
            print("Query executed succesfully.")
        except Error as e:
                print("The error occurred:")
                print(e)

    def close_connection(self):
        self.con1.close()
        if self.con1.isOpen() == False:
            print ("Connection closed.")
        
    def read_table(self, connection, query): #Вывод в таблицу QTableWidget
        self.tableWidget.setRowCount(0)
        data = QSqlQuery(query)
        self.tableWidget.setColumnCount(9)
        while data.next():
            rows = self.tableWidget.rowCount()
            self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers) #set read Only
            self.tableWidget.setRowCount(rows + 1)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(data.value(0))))
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(data.value(1))))
            self.tableWidget.setItem(rows, 2, QTableWidgetItem(str(data.value(2))))
            self.tableWidget.setItem(rows, 3, QTableWidgetItem(str(data.value(3))))
            self.tableWidget.setItem(rows, 4, QTableWidgetItem(str(data.value(4))))
            self.tableWidget.setItem(rows, 5, QTableWidgetItem(str(data.value(5))))
            self.tableWidget.setItem(rows, 6, QTableWidgetItem(str(data.value(6))))
            self.tableWidget.setItem(rows, 7, QTableWidgetItem(str(data.value(7))))
            self.tableWidget.setItem(rows, 8, QTableWidgetItem(str(data.value(8))))
            self.tableWidget.setItem(rows, 9, QTableWidgetItem(str(data.value(9))))
            self.tableWidget.setItem(rows, 10, QTableWidgetItem(str(data.value(10))))

        self.tableWidget.resizeColumnsToContents()

    def add_row(self, connection):  # BTTN "OK" ( add row ) WORKS WITH DATABASE
        insertDataQuery = QSqlQuery()
        # EDIT exsist row ============================================================
        if self.edit_flag == True:
            query = QSqlQuery()
            # Year change
            year_ed = self.spinBox_age.value()
            query.prepare('UPDATE films SET year=:year WHERE id=:var')
            query.bindValue(':year', year_ed)
            query.bindValue(':var', self.current_row+1)
            query.exec()

            # Title original change
            title_orig = self.Ed_name.text()
            query.prepare('UPDATE films SET title_orig=:title_orig WHERE id=:var')
            query.bindValue(':title_orig', title_orig)
            query.bindValue(':var', self.current_row+1)
            query.exec()

            # Title change
            title = self.Ed_title.text()
            query.prepare('UPDATE films SET title=:title WHERE id=:var')
            query.bindValue(':title', title)
            query.bindValue(':var', self.current_row+1)
            query.exec()

            # Country change
            country = self.lineEdit_country.text()
            query.prepare('UPDATE films SET country=:country WHERE id=:var')
            query.bindValue(':country', country)
            query.bindValue(':var', self.current_row+1)
            query.exec()

            # Genre change
            genre = self.comboBox_2.currentText()
            query.prepare('UPDATE films SET genre=:genre WHERE id=:var')
            query.bindValue(':genre', genre)
            query.bindValue(':var', self.current_row+1)
            query.exec()
            
            # Director change
            director = self.Ed_director.text()
            query.prepare('UPDATE films SET director=:director WHERE id=:var')
            query.bindValue(':director', director)
            query.bindValue(':var', self.current_row+1)
            query.exec()
            
            # Desc change
            desc = self.Te_desc.toPlainText()
            query.prepare('UPDATE films SET desc=:desc WHERE id=:var')
            query.bindValue(':desc', desc)
            query.bindValue(':var', self.current_row+1)
            query.exec()
            
            # Img change
            img = self.Ed_img.text()
            query.prepare('UPDATE films SET img=:img WHERE id=:var')
            query.bindValue(':img', img)
            query.bindValue(':var', self.current_row+1)
            query.exec()
            
            # Actors change
            actors = self.Ed_actors.text()
            query.prepare('UPDATE films SET actors=:actors WHERE id=:var')
            query.bindValue(':actors', actors)
            query.bindValue(':var', self.current_row+1)
            query.exec()
            
            # ending editing mode and return to tab1
            print ("edit flag")
            self.edit_flag = False
            self.read_table(self.con1, "SELECT id, num, title_orig, title, year, genre, country, director, actors, desc, prim, tags, img FROM films")
            
            # i m a g e -----------------------------------------
            pixmap = QPixmap('data/' + img)
            pixmap_small = pixmap.scaled(400,400, QtCore.Qt.KeepAspectRatio)
            self.label_pix.setScaledContents(True)
            self.label_pix.setPixmap(pixmap_small)
            self.tabWidget.setTabText(1,'Добавить')
            self.tabWidget.setCurrentIndex(0)
        # IF ADDING NEW ROW =========================================================    
        else:
            insertDataQuery.prepare("INSERT INTO films (num, title_orig, title, year, genre, country, director, actors, desc, prim, tags, img) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)")
            num = self.Ed_num.text()
            title_orig = self.Ed_name.text()
            title = self.Ed_title.text()
            year = self.spinBox_age.value()
            genre = self.comboBox_2.currentText()
            country = self.lineEdit_country.text()
            director = self.Ed_director.text()
            actors = self.Ed_actors.text()
            desc = self.Te_desc.toPlainText()
            prim = self.Ed_prim.text()
            tags = self.Ed_tags.text()
            img = self.Ed_img.text() 

            data = [(num, title_orig, title, year, genre, country, director, actors, desc, prim, tags, img)]
            for num, title_orig, title, year, genre, country, director, actors, desc, prim, tags, img in data:
                insertDataQuery.addBindValue(num)
                insertDataQuery.addBindValue(title_orig)
                insertDataQuery.addBindValue(title)
                insertDataQuery.addBindValue(year)
                insertDataQuery.addBindValue(genre)
                insertDataQuery.addBindValue(country)
                insertDataQuery.addBindValue(director)
                insertDataQuery.addBindValue(actors)
                insertDataQuery.addBindValue(desc)
                insertDataQuery.addBindValue(prim)
                insertDataQuery.addBindValue(tags)
                insertDataQuery.addBindValue(img)
                insertDataQuery.exec()
            self.close_connection()
            # Clearing editable widgets for new row
            self.Ed_name.setText('')
            self.Ed_title.setText('')
            self.Ed_num.setText('')
            self.Ed_director.setText('')
            self.Ed_actors.setText('')
            self.Te_desc.setText('')
            self.tabWidget.setCurrentIndex(0)
            

    def changeTab2 (self): # изменение текущей вкладки
        if self.tabWidget.currentIndex() == 1:
            if self.edit_flag == False:
                self.spinBox_id.setValue(self.tableWidget.rowCount()+1)
                self.spinBox_id.setReadOnly(True)
                if self.tableWidget.rowCount() == 0:
                   self.create_table(self.con1, self.create_films_table)
        if self.tabWidget.currentIndex() == 0:
            if self.con1.isOpen() == False: 
                self.create_connection(self.path)
                self.read_table(self.con1, "SELECT id, num, title_orig, title, year, genre, country, director, actors, desc, prim, tags, img FROM films")
            if self.edit_flag == True:
                print("Mode switch to edit_off")
                self.edit_flag = False
                self.tabWidget.setTabText(1,'Добавить')
                # очистка полей
                self.Ed_name.setText('')
                self.Ed_title.setText('')
                self.Ed_num.setText('')
                self.Ed_director.setText('')
                self.Ed_actors.setText('')
                self.Te_desc.setText('')


    def select_row (self):  # Выбор ячейки (строки)
        row = self.tableWidget.currentRow() # Index of Row
        self.current_row = row
        # get info active row    
        key = self.tableWidget.item(row, 2).text() #title_orig is key for search
        query = QSqlQuery()
        query.prepare("SELECT id, title_orig, title, year, genre, country, director, actors, desc, prim, tags, img FROM films WHERE title_orig LIKE ?")
        query.addBindValue(key)
        query.exec()
        # вывод инфы из базы данных в виджеты
        while query.next():
            print("id: ", str(query.value(0)), str(query.value(1)), str(query.value(2))) # <<-- GET ID ACTIVE ELEMENT!!!
            Title = str(query.value(1)) + " - (" + str(query.value(2)) + ")" + ", " + str(query.value(3))
            Desc = str(query.value(8))
            Image = str(query.value(11))

        self.label_title.setText(Title)
        self.label_title.setStyleSheet("""
        font: bold italic;
        background-color: none;
        """)

        self.textEdit.setText(Desc)
        
        pixmap = QPixmap('data/' + Image)
        pixmap_small = pixmap.scaled(400,400, QtCore.Qt.KeepAspectRatio)
        self.label_pix.setScaledContents(True)
        self.label_pix.setPixmap(pixmap_small)
        self.Ed_img.setText(Image)


        # =====================================================================
      # ==========================================================================
      #                         E D I T   T A B
      # ==========================================================================
    def edit_mode (self): # после двойного клика - переходим в режим редактироания
        
        print("Edit mode")
        self.edit_flag = True

        row = self.tableWidget.currentRow() # Index of Row
        self.current_row = row

        print("Row: ", row)
        self.tabWidget.setCurrentIndex(1)
        self.edit_flag = True
        self.tabWidget.setTabText(1,'Редактирование')

        #  вывод года (year)
        query = "SELECT year FROM films"
        data = QSqlQuery(query)
        for i in range (0, self.tableWidget.rowCount()):
            data.next()
            if i==row:            
                Year = data.value(0)
                self.spinBox_age.setValue(Year)
        #  id 
        query = "SELECT id FROM films"
        data = QSqlQuery(query)
        for i in range (0, self.tableWidget.rowCount()):
            data.next()
            if i==row:            
                id_num = data.value(0)
                self.spinBox_id.setValue(id_num)
        #  title original (title_orig)
        query = "SELECT title_orig FROM films"
        data = QSqlQuery(query)
        for i in range (0, self.tableWidget.rowCount()):
            data.next()
            if i==row:            
                title_orig = data.value(0)
                self.Ed_name.setText(title_orig)
        #  title  (title)
        query = "SELECT title FROM films"
        data = QSqlQuery(query)
        for i in range (0, self.tableWidget.rowCount()):
            data.next()
            if i==row:            
                title = data.value(0)
                self.Ed_title.setText(title)
        #  country 
        query = "SELECT country FROM films"
        data = QSqlQuery(query)
        for i in range (0, self.tableWidget.rowCount()):
            data.next()
            if i==row:            
                country = data.value(0)
                self.lineEdit_country.setText(country)
        #  director
        query = "SELECT director FROM films"
        data = QSqlQuery(query)
        for i in range (0, self.tableWidget.rowCount()):
            data.next()
            if i==row:            
                director = data.value(0)
                self.Ed_director.setText(director)     
        #  actors
        query = "SELECT actors FROM films"
        data = QSqlQuery(query)
        for i in range (0, self.tableWidget.rowCount()):
            data.next()
            if i==row:            
                actors = data.value(0)
                self.Ed_actors.setText(actors)
        #  desc
        query = "SELECT desc FROM films"
        data = QSqlQuery(query)
        for i in range (0, self.tableWidget.rowCount()):
            data.next()
            if i==row:            
                desc = data.value(0)
                self.Te_desc.setText(desc)
        #  genre
        query = "SELECT genre FROM films"
        data = QSqlQuery(query)
        for i in range (0, self.tableWidget.rowCount()):
            data.next()
            if i==row:            
                genre = data.value(0)
                self.comboBox_2.setCurrentIndex(self.comboBox_2.findText(genre))     


def main():
    #con1 = create_connection('test.db')
    #create_table(con1, create_users_table)
    #create_row_table(con1, create_user, data)
    #execute_read_query(con1, read_all)    
    
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    app.setStyle('Fusion')

    window = UIForm('movies.db')  # Создаём объект класса UIForm

    #window.read_table(con1, read_all) #вывести в таблицу

    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
    
    window.close_connection()    

if __name__ == '__main__':
    main()
