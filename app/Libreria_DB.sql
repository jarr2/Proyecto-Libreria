create database LibOnline;
use LibOnline;
#DROP DATABASE libonline;
create table Usuarios(
id_usuario INT auto_increment,
id_direccion INT NOT NULL,
id_login INT NOT NULL,
nombre VARCHAR(30) NOT NULL,
apellidos VARCHAR(30) NOT NULL,
numero_telefonico VARCHAR(10) NOT NULL,
PRIMARY KEY(id_usuario)
);

create table Logins(
id_login INT auto_increment,
correo VARCHAR(256) NOT NULL,
contrasena VARCHAR(256) NOT NULL,
privilegio VARCHAR(15) NOT NULL,
UNIQUE KEY (correo),
PRIMARY KEY (id_login)
);

create table Direcciones(
id_direccion INT auto_increment,
calle VARCHAR(25) NOT NULL,
estado VARCHAR(20) NOT NULL,
municipio VARCHAR(25) NOT NULL,
colonia VARCHAR(25) NOT NULL,
cp NUMERIC(5) NOT NULL,
num_interior NUMERIC(4),
num_exterior NUMERIC(4) NOT NULL,
PRIMARY KEY (id_direccion)
);



create table Envios(
id_envio INT auto_increment,
id_compra INT NOT NULL,
id_usuario INT NOT NULL,
fecha_entrega DATETIME NOT NULL,
estatus VARCHAR(20) NOT NULL,
PRIMARY KEY (id_envio)
);

create table Libros(
id_libro VARCHAR(12) NOT NULL,
nombre VARCHAR(40) NOT NULL,
editorial VARCHAR(40) NOT NULL,
autor VARCHAR(40) NOT NULL,
stock NUMERIC(6) NOT NULL,
estatus VARCHAR(20) NOT NULL,
precio NUMERIC(5) NOT NULL,
img_ruta VARCHAR(100) NOT NULL,
PRIMARY KEY (id_libro)
);

create table Compras (
id_compra INT auto_increment,
id_usuario INT NOT NULL,
id_libro VARCHAR(12) NOT NULL,
estatus VARCHAR(20) NOT NULL,
fecha_pedido DATE NOT NULL,
total NUMERIC(6) NOT NULL,
PRIMARY KEY (id_compra),
FOREIGN KEY (id_libro) REFERENCES Libros(id_libro)
);

create table Ranking(
id_ranking INT auto_increment,
id_usuario INT NOT NULL,
id_libro VARCHAR(12) NOT NULL,
ranking INT(1) NOT NULL,
cantidad_calificaciones INT(6) NOT NULL,
suma_calificaciones INT(6) NOT NULL,
PRIMARY KEY (id_ranking),
FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario),
FOREIGN KEY (id_libro) REFERENCES Libros(id_libro)
);



ALTER TABLE Usuarios ADD FOREIGN KEY (id_direccion) REFERENCES Direcciones(id_direccion);
ALTER TABLE Usuarios ADD FOREIGN KEY (id_login) REFERENCES Logins(id_login);
ALTER TABLE Envios ADD FOREIGN KEY (id_compra) REFERENCES Compras(id_compra);
ALTER TABLE Compras ADD FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario);
/*ALTER TABLE Compras ADD FOREIGN KEY (id_libro) REFERENCES Libros(id_libro);*/
ALTER TABLE Envios ADD FOREIGN KEY (id_usuario) REFERENCES Compras(id_usuario);


insert into logins(correo,contrasena, privilegio) values ("20223tn111@utez.edu.mx","b'$2b$12$Bj2s7PI42QkpqlbJtkAH/eR12/Tvs.IJYWlf6eU14Tf/G0FsL0FL2'",'user');
insert into logins(correo,contrasena, privilegio) values ("messi@utez.edu.mx","b'$2b$12$Bj2s7PI42QkpqlbJtkAH/eR12/Tvs.IJYWlf6eU14Tf/G0FsL0FL2'",'admin');
/*
contraseña de ambos encriptados con bcrypt (1234) :
b'$2b$12$Bj2s7PI42QkpqlbJtkAH/eR12/Tvs.IJYWlf6eU14Tf/G0FsL0FL2'
*/


insert into direcciones(calle,estado,municipio,colonia,cp,num_exterior,num_interior) values ("Av siempre viva","Morelos","Jiutepec","La Campestre","62553","6","0");
insert into direcciones(calle,estado,municipio,colonia,cp,num_exterior,num_interior) values ("7","6","5","4","3","2","1");

insert into usuarios(id_direccion, id_login,nombre,apellidos,numero_telefonico) values (1,1,"Cristobal Eduardo","Serrano Bahena", 7772689242);
insert into usuarios(id_direccion, id_login,nombre,apellidos,numero_telefonico) values (2,2,"Lionel Andrés","Messi", 7772689243);

insert into Libros(id_libro, nombre, editorial, autor, stock, estatus, precio,img_ruta) values ("1","Hellblazer De Garth Ennis Vol.01","DC","Garth Ennis",2,"Disponible",499,"static/img/Hellblazer De Garth Ennis Vol.01.jpg");
insert into Libros(id_libro, nombre, editorial, autor, stock, estatus, precio,img_ruta) values ("2","Batman: Enigmista","DC","McCarthy Castillo Ramos",1,"Disponible",329,"static/img/Batman Enigmista.png");
insert into Libros(id_libro, nombre, editorial, autor, stock, estatus, precio, img_ruta) values ("3","Daredevil Vol.01","Marvel","Saladin Ahmed",2,"Nuevo",169,"static/img/Daredevil Vol.01.png");
insert into Libros(id_libro, nombre, editorial, autor, stock, estatus, precio, img_ruta) values ("4","Wolverine Vol.9","Marvel","Percy Lavalle",2,"Nuevo",149,"static/img/Wolverine Vol.9.png");
insert into Libros(id_libro, nombre, editorial, autor, stock, estatus, precio, img_ruta) values ("5","The Amazing Spider-Man #25","Marvel","Wells",2,"Nuevo",79,"static/img/The Amazing Spider-Man 25.png");
insert into Libros(id_libro, nombre, editorial, autor, stock, estatus, precio, img_ruta) values ("6","Flash Vol.02","DC","Perez Dogson",2,"Nuevo",209,"static/img/Flash Vol.02.png");
DELIMITER $$
CREATE PROCEDURE VerificarUsuario(
	in chamo VARCHAR(256),
    in chamo2 VARCHAR(256)
)
BEGIN
    SELECT distinct * FROM Logins WHERE (correo = chamo AND contrasena=chamo2);
END$$
DELIMITER ;


#drop database libonline;

call VerificarUsuario("messi@utez.edu.mx","b'$2b$12$Bj2s7PI42QkpqlbJtkAH/eR12/Tvs.IJYWlf6eU14Tf/G0FsL0FL2'");

/*
show tables;
insert into Logins (correo,contrasena,privilegio) values ('20223tn999@utez.edu.mx','Cisco123','cliente');
select * from Logins;
insert into clientes
  values ('Marcos Luis','marcosluis@gmail.com',aes_encrypt('5390700823285988','xyz123'));
drop database libonline;
drop table Compras;
*/
select * from Ranking;

DELIMITER $$
CREATE PROCEDURE VerificarDireccionyUsuario(
	in chivas INT,
    in necaxa INT
)
BEGIN
	SELECT 
        u.nombre, 
        u.apellidos, 
        u.numero_telefonico, 
        d.calle, 
        d.estado, 
        d.municipio, 
        d.colonia, 
        d.cp, 
        d.num_exterior, 
        d.num_interior
    FROM 
        Direcciones d
    JOIN 
        Usuarios u ON u.id_direccion = d.id_direccion
	WHERE 
        d.id_direccion = chivas
        AND u.id_usuario = necaxa;
END $$
DELIMITER ;

call VerificarDireccionyUsuario(1,1);

DELIMITER $$
CREATE PROCEDURE ActualizarDireccionyUsuario(
	in idUsuario INT,
    in nombre VARCHAR(30),
    in apellido VARCHAR(30),
    in numTelefono NUMERIC(10),
    in calle VARCHAR(25),
    in numInterior NUMERIC(4),
    in numExterior NUMERIC(4),
    in municipio VARCHAR(25),
    in colonia VARCHAR(25),
    in estado VARCHAR(20),
    in cp NUMERIC(5)
)
BEGIN
    -- Actualiza la tabla usuarios
    UPDATE usuarios
    SET nombre = nombre,
        apellidos = apellido,
        numero_telefonico = numTelefono
    WHERE id_usuario = idUsuario;

    -- Actualiza la tabla direccion
    UPDATE direcciones
    SET calle = calle,
        estado = estado,
        municipio = municipio,
        colonia = colonia,
        cp = cp,
        num_interior = numInterior,
        num_exterior = numExterior
    WHERE id_direccion = idUsuario;
END$$    
DELIMITER ;

