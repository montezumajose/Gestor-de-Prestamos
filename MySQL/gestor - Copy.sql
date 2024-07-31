create database gestordeprestamos;

use gestordeprestamos;

create table deudores(
	 id int auto_increment primary key,
     nombre varchar(100) not null,
     apellido varchar(100) not null,
     cedula varchar(100) not null,
     fecha_inicio varchar(13) not null,
     prestamo double not null,
     cuota double not null,
     forma_pagar varchar(15) not null
);

create table abonos(
     deudor_id int not null,
     abono_capital double,
     abono_interes double,
     fecha_abono varchar(13),
     total_capital_debe double,
     total_interes_debe double,
     total_debe double,
     foreign key (deudor_id) references deudores(id)
);

create table administradores(
	id int auto_increment primary key,
    nombre varchar(15),
    apellido varchar(20),
    cedula varchar (15),
    contrasenia varchar(15)
);

-- si necesita cambiar la password del usuario root
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('__cambiar__');

-- crear usuario alterno para hacer el backup
CREATE USER 'backup'@'localhost' IDENTIFIED BY '';

-- Otorgar permisos de backup
GRANT SELECT, SHOW DATABASES, LOCK TABLES, RELOAD ON *.* TO 'nuevo_usuario'@'localhost';

-- Aplicar los cambios
FLUSH PRIVILEGES;

-- asignar unos permisos de procesos a backup
GRANT PROCESS, SUPER ON *.* TO 'backup'@'localhost';

-- se necesita mysqldump para hacer el backup / instalarlo correctamente