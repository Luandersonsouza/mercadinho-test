from tkinter import *
from tkinter import ttk
import sqlite3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser

window = Tk()
class reports():
	def print_product(self):
		webbrowser.open("products.pdf")


	def generate_product_report(self):
		self.c = canvas.Canvas("products.pdf")

		self.code_report = self.code_entry.get()
		self.name_report = self.name_entry.get()
		self.value_report = self.value_entry.get()
		self.city_report = self.city_entry.get()
		self.c.setFont("Helvetica-Bold", 24)
		self.c.drawString(200, 790, 'Product File')
		self.c.setFont("Helvetica-Bold", 18)
		self.c.drawString(50, 700,'Code : ')
		self.c.drawString(50, 670,'Name : ')
		self.c.drawString(50, 630,'Value : ')
		self.c.drawString(50, 600,'Expiration : ')
		self.c.setFont("Helvetica", 18)
		self.c.drawString(150, 700, self.code_report)
		self.c.drawString(150, 670, self.name_report)
		self.c.drawString(150, 630, self.value_report)
		self.c.drawString(150, 600, self.city_report)
		self.c.rect(20,550,550,200, fill = False, stroke = True)
		self.c.showPage()
		self.c.save()
		self.print_customers()

class functions():
	def clear_frame_1(self):
		self.code_entry.delete(0, END)
		self.name_entry.delete(0, END)
		self.value_entry.delete(0, END)
		self.expiration_entry.delete(0,END)


	def db_connection(self):
		self.conn = sqlite3.connect("products.db")
		self.cursor = self.conn.cursor();print("connecting to database")


	def db_disconnection(self):
		self.conn.close();print("disconnecting from database")


	def create_tables_db(self):
		self.db_connection() 
		self.cursor.execute("""
			CREATE TABLE IF NOT EXISTS products( 
				code INTEGER PRIMARY KEY,
				name_products CHAR(40) NOT NULL,
				value INTEGER(20),
				expiration CHAR(40)
			);
		                    """)
		self.conn.commit(); print("Created database")
		self.db_disconnection()


	def variables(self):
		self.code = self.code_entry.get()
		self.name = self.name_entry.get()
		self.value = self.value_entry.get()
		self.expiration = self.expiration_entry.get()


	def add_product(self):
		self.variables()
		self.db_connection()
		self.cursor.execute(""" INSERT INTO 
								products (name_products, value, expiration)
								VALUES (?,?,?)""", 
								(self.name, self.value, self.expiration))
		self.conn.commit()
		self.db_disconnection()
		self.select()
		self.clear_frame_1()


	def select(self):
		self.listaCli.delete(*self.listaCli.get_children())
		self.db_connection()
		list_a = self.cursor.execute("""	SELECT code, name_products, value, expiration 
											FROM products
											ORDER BY name_products ASC; 
									""")
		for i in list_a:
			self.listaCli.insert("", END, values=i)
		self.db_disconnection()


	def on_double_click(self, event):
		self.clear_frame_1()
		self.listaCli.selection()
		for n in self.listaCli.selection():
			col1,col2,col3,col4 = self.listaCli.item(n, 'values')
			self.code_entry.insert(END, col1)
			self.name_entry.insert(END, col2)
			self.value_entry.insert(END, col3)
			self.expiration_entry.insert(END, col4)


	def delete_product(self):
		self.variables()
		self.db_connection()
		self.cursor.execute("""DELETE FROM products WHERE code = ?  """, (self.code))
		self.conn.commit()
		self.db_disconnection()
		self.clear_frame_1()
		self.select()


	def change_products(self):
		self.variables()
		self.db_connection()
		self.cursor.execute(""" UPDATE products SET name_products = ?, value = ?, expiration = ?
							WHERE code = ?""", (self.name, self.value, self.expiration, self.code))
		self.conn.commit()
		self.db_disconnection()
		self.select()
		self.clear_frame_1()


	def search_product (self):
		self.db_connection()
		self.listaCli.delete(*self.listaCli.get_children())
		self.name_entry.insert(END, '%')
		name = self.name_entry.get()
		self.cursor.execute(""" SELECT code, name_products, value, expiration
								FROM products 
								WHERE name_products LIKE '%s' ORDER BY name_products ASC
							""" %name)
		search_name_product = self.cursor.fetchall()
		for i in search_name_product:
			self.listaCli.insert("", END, values =i)
		self.clear_frame_1()
		self.db_disconnection()

class aplication(functions, reports):
	def __init__(self):
		self.window = window
		self.screen()
		self.frames_in_screen()
		self.widgets_Frame_1()
		self.widgets_Frame_2()
		self.create_tables_db()
		self.select()
		self.menu()
		window.mainloop()


	def screen(self):
		self.window.title("Kmercado")
		self.window.configure(background= '#6495ED')
		self.window.geometry("700x500")
		self.window.resizable(True, True)
		self.window.maxsize(width = 900, height= 700)
		self.window.minsize(width = 500, height= 400)


	def frames_in_screen(self):
		self.frame_1= Frame(self.window, bd=4, bg='#B0C4DE', highlightbackground='#D3D3D3', highlightthickness=3)
		self.frame_1.place(relx = 0.02, rely=0.02, relwidth = 0.96, relheight = 0.46)
		self.frame_2= Frame(self.window, bd=4, bg='#B0C4DE', highlightbackground='#D3D3D3', highlightthickness=3)
		self.frame_2.place(relx = 0.02, rely=0.5, relwidth = 0.96, relheight = 0.46)


	def widgets_Frame_1(self):
		#creating the clear button
		self.button_clear = Button(self.frame_1, text="Clear", bd = 2, bg = '#107db2',
									 fg = 'white', activebackground = '#108ecb', activeforeground = 'white',
									 font = ('verdana', 8, 'bold'),command = self.clear_frame_1)
		self.button_clear.place(relx= 0.2, rely= 0.15,relwidth=0.1, relheight=0.15)
		
        #creanting the search button
		self.button_search = Button(self.frame_1, text="Search",bd = 2, bg = '#107db2',
									 fg = 'white', activebackground = '#108ecb', activeforeground = 'white',
									 font = ('verdana', 8, 'bold'), command = self.search_product)
		self.button_search.place(relx= 0.3, rely= 0.15,relwidth=0.1, relheight=0.15)
		
        #creating the new button
		self.button_new = Button(self.frame_1, text="New",bd = 2, bg = '#107db2',
									 fg = 'white', activebackground = '#108ecb', activeforeground = 'white',
									 font = ('verdana', 8, 'bold'), command= self.add_product)
		self.button_new.place(relx= 0.6, rely= 0.15,relwidth=0.1, relheight=0.15)
		
        #creating the change button
		self.button_change = Button(self.frame_1, text="Change", bd = 2, bg = '#107db2',
									 fg = 'white', activebackground = '#108ecb', activeforeground = 'white',
									 font = ('verdana', 8, 'bold'), command = self.change_products)
		self.button_change.place(relx= 0.7, rely= 0.15,relwidth=0.1, relheight=0.15)
		
        #creating the delete button
		self.button_delete = Button(self.frame_1, text="Delete", bd = 2, bg = '#107db2',
									 fg = 'white', activebackground = '#108ecb', activeforeground = 'white', 
									 font = ('verdana', 8, 'bold'), command = self.delete_product)
		self.button_delete.place(relx= 0.8, rely= 0.15,relwidth=0.1, relheight=0.15)
		
        #label code
		self.label_code= Label(self.frame_1, text="Code", bg = '#B0C4DE')
		self.label_code.place(relx=0.05, rely=0.05)
		self.code_entry= Entry(self.frame_1)
		self.code_entry.place(relx=0.05, rely= 0.16, relwidth=0.08)
		
        #label name 
		self.label_name= Label(self.frame_1, text="Name", bg = '#B0C4DE')
		self.label_name.place(relx=0.05, rely=0.35)
		self.name_entry= Entry(self.frame_1)
		self.name_entry.place(relx=0.05, rely= 0.45, relwidth=0.85)
		
        #label televalue
		self.label_value= Label(self.frame_1, text="Value", bg = '#B0C4DE')
		self.label_value.place(relx=0.05, rely=0.6)
		self.value_entry= Entry(self.frame_1)
		self.value_entry.place(relx=0.05, rely= 0.7, relwidth=0.4)
		
        #label description
		self.label_expiration= Label(self.frame_1, text="Expiration", bg = '#B0C4DE')
		self.label_expiration.place(relx=0.5, rely=0.6)
		self.expiration_entry= Entry(self.frame_1)
		self.expiration_entry.place(relx=0.5, rely= 0.7, relwidth=0.4)


	def widgets_Frame_2(self):
		self.listaCli = ttk.Treeview(self.frame_2, height = 3, colum =("col1","col2", "col3", "col4"))
		self.listaCli.heading("#0", text = "")
		self.listaCli.heading("#1", text = "Code")
		self.listaCli.heading("#2", text = "Name")
		self.listaCli.heading("#3", text = "value")
		self.listaCli.heading("#4", text = "expiration")
		self.listaCli.column('#0', width=1)
		self.listaCli.column('#1', width=50)
		self.listaCli.column('#2', width=200)
		self.listaCli.column('#3', width=125)
		self.listaCli.column('#4', width=125)
		self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)
		self.scroll_lista = Scrollbar(self.frame_2, orient='vertical')
		self.listaCli.configure(yscroll=self.scroll_lista.set)
		self.scroll_lista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight= 0.85)
		self.listaCli.bind("<Double-1>", self.on_double_click)


	def menu (self):
		menu_bar = Menu(self.window)
		self.window.config(menu = menu_bar)
		file_menu = Menu(menu_bar)
		file_menu_2 = Menu(menu_bar)
		def quit(): self.window.destroy()
		menu_bar.add_cascade(label = "Options", menu = file_menu)
		menu_bar.add_cascade(label = "Reports", menu = file_menu_2)
		file_menu.add_command(label = "Quit", command = quit)
		file_menu.add_command(label = "Clear frame", command = self.clear_frame_1)
		file_menu_2.add_command(label = "Product File", command = self.generate_product_report)

aplication()
