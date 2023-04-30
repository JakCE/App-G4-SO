from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL connection
app.config['MYSQL_HOST'] = '18.204.213.81'
app.config['MYSQL_USER'] = 'support'
app.config['MYSQL_PASSWORD'] = 'grupo4password'
app.config['MYSQL_DB'] = 'project_G4'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

#MAIN principal
@app.route('/')
def Index():
    return render_template('dashboard.html')
    
#CRUD PRODUCTO
@app.route('/add_form/producto')
def add_form_producto():
    opc="producto"
    cur1 = mysql.connection.cursor()
    cur1.execute('SELECT * FROM Categoria')
    data1=cur1.fetchall()

    return render_template('add_form.html',opc=opc, Categoria=data1)

@app.route('/productos')
def productos_part():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Producto')
    data=cur.fetchall()

    return render_template('productos.html', Producto = data)

@app.route('/add_producto', methods=['POST'])
def add_producto():
    if request.method == 'POST': #Define método de envío
        #id_prod = request.form['id']
        descripcion = request.form['descripcion'] # request.form recoge datos de formulario
        precio = request.form['precio']
        marca = request.form['marca']
        stock = request.form['stock']
        id_cat = int(request.form['categoria'])
        
        cur = mysql.connection.cursor() #genera conexion DB SQL
        cur.execute('INSERT INTO Producto (descripcion, precio, marca, stock, id_categoria) VALUES (%s, %s, %s, %s, %s)', 
        (descripcion, precio, marca, stock, id_cat)) # ejecuta comando SLQ datos recogidos del form
        mysql.connection.commit() # Guarda cambios en DB
        #flash('Contact Added Succesfully')
        return redirect(url_for('productos_part')) #Redirecciona a pagina Index
    
@app.route('/edit_producto/<id>')
def get_producto(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Producto WHERE id_producto = %s', (id))
    data = cur.fetchall()
    #----
    cur1 = mysql.connection.cursor()
    cur1.execute('SELECT * FROM Categoria')
    data1 = cur1.fetchall()
    #----
    opc="producto"
    return render_template('edit_form.html', producto = data[0],opc=opc,Categoria=data1)

@app.route('/update_producto/<id>', methods = ['POST'])
def update_producto(id):
    if request.method == 'POST':
        descripcion = request.form['descripcion'] # request.form recoge datos de formulario
        precio = request.form['precio']
        marca = request.form['marca']
        stock = request.form['stock']
        cat = request.form['categoria']
        #----
        cur1 = mysql.connection.cursor()
        cur1.execute('SELECT id_categoria FROM Categoria WHERE nombre = %s', (cat))
        data1 = cur1.fetchall()
        id_cat=data1
        #----
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE Producto
        SET descripcion = %s,
            precio = %s,
            marca = %s,
            stock = %s,
            id_categoria = %s
        WHERE id_producto = %s
        """, (descripcion,precio,marca,stock,id_cat,id ))
        mysql.connection.commit()
        flash('Contact updated successfully')
        return redirect(url_for('productos_part'))

@app.route('/delete_producto/<string:id>')
def delete_producto(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Producto WHERE id_producto = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('productos_part'))

#CRUD VENTA
@app.route('/add_form/ventas')
def add_form_ventas():
    opc="ventas"
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Cliente')
    data=cur.fetchall()

    cur1 = mysql.connection.cursor()
    cur1.execute('SELECT * FROM Producto')
    data1=cur1.fetchall()
    return render_template('add_form.html',opc=opc, Cliente=data,Producto=data1)

@app.route('/ventas')
def ventas_part():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Venta')
    data=cur.fetchall()
    return render_template('ventas.html', Ventas = data)

@app.route('/add_venta', methods=['POST'])
def add_venta():
    if request.method == 'POST': #Define método de envío
        #id_venta = request.form['id_ven']
        id_prod = request.form['id_prod'] # request.form recoge datos de formulario
        id_cli = request.form['id_cli']
        talla = request.form['talla']
        color = request.form['color']
        cantidad = int(request.form['cantidad'])
        fecha = request.form['fecha']
        monto = float(request.form['monto'])
        cur = mysql.connection.cursor() #genera conexion DB SQL
        cur.execute('INSERT INTO Venta (id_producto, id_cliente, talla, color, cantidad, fecha, monto) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
        (id_prod, id_cli, talla, color, cantidad, fecha, monto)) # ejecuta comando SLQ datos recogidos del form
        mysql.connection.commit() # Guarda cambios en DB
        #flash('Contact Added Succesfully')
        return redirect(url_for('ventas_part')) #Redirecciona a pagina Index

@app.route('/edit_venta/<id>')
def get_venta(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Venta WHERE id_venta = %s', (id))
    print(id)
    data = cur.fetchall()
    print(data[0])
    opc="ventas"
    return render_template('edit_form.html', venta = data[0],opc=opc)

@app.route('/update_venta/<id>', methods = ['POST'])
def update_venta(id):
    if request.method == 'POST':
        id_prod = request.form['id_prod'] # request.form recoge datos de formulario
        id_cli = request.form['id_cli']
        talla = request.form['talla']
        color = request.form['color']
        cantidad = int(request.form['cantidad'])
        fecha = request.form['fecha']
        monto = float(request.form['monto'])
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE Venta
        SET id_producto = %s,
            id_cliente = %s,
            talla = %s,
            color = %s,
            cantidad = %s,
            fecha = %s,
            monto = %s
        WHERE id_venta = %s
        """, (id_prod,id_cli,talla,color,cantidad,fecha,monto,id ))
        mysql.connection.commit()
        flash('Contact updated successfully')
        return redirect(url_for('ventas_part'))

@app.route('/delete_venta/<string:id>')
def delete_venta(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Venta WHERE id_venta = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('ventas_part'))

#CLIENTE CRUD
@app.route('/add_form/cliente')
def add_form_cliente():
    opc="cliente"
    return render_template('add_form.html',opc=opc)

@app.route('/clientes')
def clientes_part():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Cliente')
    data=cur.fetchall()
    return render_template('clientes.html', Cliente = data)

@app.route('/add_cliente', methods=['POST'])
def add_cliente():
    if request.method == 'POST': #Define método de envío
        #id = request.form['id']
        nombres = request.form['nombres'] # request.form recoge datos de formulario
        apellidos = request.form['apellidos']
        celular = request.form['celular']
        email = request.form['email']
        direccion = request.form['direccion']
        print(direccion)
        cur = mysql.connection.cursor() #genera conexion DB SQL
        cur.execute('INSERT INTO Cliente (nombres, apellidos, n_celular, email, direccion) VALUES (%s, %s, %s, %s, %s)', 
        (nombres, apellidos, celular, email, direccion)) # ejecuta comando SLQ datos recogidos del form
        mysql.connection.commit() # Guarda cambios en DB
        #flash('Contact Added Succesfully')
        return redirect(url_for('clientes_part')) #Redirecciona a pagina Index

@app.route('/edit_cliente/<id>')
def get_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Cliente WHERE id_cliente = %s', (id))
    print(id)
    data = cur.fetchall()
    print(data[0])
    opc="cliente"
    return render_template('edit_form.html', cliente = data[0],opc=opc)

@app.route('/update_cliente/<id>', methods = ['POST'])
def update_cliente(id):
    if request.method == 'POST':
        nombres = request.form['nombres'] # request.form recoge datos de formulario
        apellidos = request.form['apellidos']
        celular = request.form['celular']
        email = request.form['email']
        direccion = request.form['direccion']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE Cliente
        SET nombres = %s,
            apellidos = %s,
            n_celular = %s,
            email = %s,
            direccion = %s
        WHERE id_cliente = %s
        """, (nombres,apellidos,celular,email,direccion,id ))
        mysql.connection.commit()
        flash('Contact updated successfully')
        return redirect(url_for('clientes_part'))

@app.route('/delete_cliente/<string:id>')
def delete_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Cliente WHERE id_cliente = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('clientes_part'))

#CATEGORIA CRUD
@app.route('/add_form/categoria')
def add_form_categoria():
    opc="categoria"
    return render_template('add_form.html',opc=opc)

@app.route('/categorias')
def categorias_part():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Categoria')
    data=cur.fetchall()
    return render_template('categorias.html', Categoria = data)

@app.route('/add_categoria', methods=['POST'])
def add_categoria():
    if request.method == 'POST': #Define método de envío
        #id_cat = request.form['id']
        nombre = request.form['nombre'] # request.form recoge datos de formulario
        descripcion = request.form['descripcion']
        cur = mysql.connection.cursor() #genera conexion DB SQL
        cur.execute('INSERT INTO Categoria (nombre, descripcion) VALUES (%s, %s)', 
        (nombre, descripcion)) # ejecuta comando SLQ datos recogidos del form
        mysql.connection.commit() # Guarda cambios en DB
        #flash('Contact Added Succesfully')
        return redirect(url_for('categorias_part')) #Redirecciona a pagina Index

@app.route('/edit_categoria/<id>')
def get_categoria(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Categoria WHERE id_categoria = %s', (id))
    data = cur.fetchall()
    print(data[0])
    opc="categoria"
    return render_template('edit_form.html', categoria = data[0],opc=opc)

@app.route('/update_categoria/<id>', methods = ['POST'])
def update_categoria(id):
    if request.method == 'POST':
        nombre = request.form['nombre'] # request.form recoge datos de formulario
        descripcion = request.form['descripcion']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE Categoria
        SET nombre = %s,
            descripcion = %s
        WHERE id_categoria = %s
        """, (nombre,descripcion,id))
        mysql.connection.commit()
        flash('Contact updated successfully')
        return redirect(url_for('categorias_part'))

@app.route('/delete_categoria/<string:id>')
def delete_categoria(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Categoria WHERE id_categoria = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('categorias_part'))

####
@app.route('/tienda')
def tienda_part():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Producto')
    data=cur.fetchall()

    return render_template('tienda.html', Producto = data)
####

if __name__ == '__main__':
    app.run(port = 5000, debug = True)