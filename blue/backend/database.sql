CREATE DATABASE IF NOT EXISTS figurazone;
USE figurazone;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    email VARCHAR(200) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol ENUM('admin', 'cliente', 'operador') NOT NULL DEFAULT 'cliente',
    activo TINYINT(1) NOT NULL DEFAULT 1
);

CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    imagen_url VARCHAR(500) NULL
);

CREATE TABLE perfiles_compra (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    email VARCHAR(200) NOT NULL UNIQUE,
    telefono VARCHAR(20) NOT NULL,
    direccion VARCHAR(300) NOT NULL
);

CREATE TABLE ordenes_compra (
    id INT AUTO_INCREMENT PRIMARY KEY,
    perfil_id INT NOT NULL,
    estado VARCHAR(50) NOT NULL DEFAULT 'pendiente',
    total DECIMAL(10, 2) NOT NULL,
    fecha DATETIME NOT NULL,
    FOREIGN KEY (perfil_id) REFERENCES perfiles_compra(id)
);

CREATE TABLE items_orden (
    id INT AUTO_INCREMENT PRIMARY KEY,
    orden_id INT NOT NULL,
    producto_id INT NOT NULL,
    nombre_producto VARCHAR(200) NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    cantidad INT NOT NULL,
    FOREIGN KEY (orden_id) REFERENCES ordenes_compra(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- Productos de ejemplo
INSERT INTO productos (nombre, descripcion, precio, stock) VALUES
('Spider-Man Classic', 'Figura articulada de Spider-Man escala 1:12', 599.99, 15),
('Goku Ultra Instinct', 'Figura Dragon Ball Super con efectos de aura', 899.99, 8),
('Batman Dark Knight', 'Figura premium de Batman con capa de tela', 749.99, 10),
('Naruto Sage Mode', 'Figura Naruto en modo sabio con base', 699.99, 12);

-- Tablas del sistema de chat
CREATE TABLE sesiones_chat (
    id VARCHAR(36) PRIMARY KEY,
    usuario_id INT NULL,
    estado ENUM('activa', 'cerrada', 'escalada') NOT NULL DEFAULT 'activa',
    fecha_inicio DATETIME NOT NULL,
    fecha_fin DATETIME NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
);

CREATE TABLE mensajes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sesion_id VARCHAR(36) NOT NULL,
    contenido TEXT NOT NULL,
    origen ENUM('cliente', 'asistente', 'operador') NOT NULL,
    fecha DATETIME NOT NULL,
    es_automatico TINYINT(1) NOT NULL DEFAULT 0,
    FOREIGN KEY (sesion_id) REFERENCES sesiones_chat(id)
);

CREATE TABLE preguntas_frecuentes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    palabras_clave VARCHAR(500) NOT NULL,
    respuesta TEXT NOT NULL,
    activa TINYINT(1) NOT NULL DEFAULT 1
);

-- FAQs de ejemplo para el e-commerce de figuras
INSERT INTO preguntas_frecuentes (palabras_clave, respuesta) VALUES
('pago metodo tarjeta transferencia paypal', 'Aceptamos tarjeta de crédito/débito, transferencia bancaria y PayPal. Todos los pagos son procesados de forma segura.'),
('envio tiempo entrega dias', 'El tiempo de entrega es de 3 a 7 días hábiles en el interior del país. Envíos express disponibles en 24-48 horas con costo adicional.'),
('orden estado pedido seguimiento', 'Puedes consultar el estado de tu orden en la sección Mis Órdenes con tu número de pedido. Te enviamos actualizaciones por email.'),
('devolucion cambio garantia', 'Aceptamos devoluciones dentro de los 15 días posteriores a la entrega, siempre que el producto esté en su empaque original sin usar.'),
('horario atencion soporte contacto', 'Nuestro equipo de soporte atiende de Lunes a Viernes de 9am a 6pm y Sábados de 10am a 2pm (hora de México).'),
('cancelar orden pedido', 'Puedes cancelar tu orden siempre que esté en estado pendiente o confirmada. Una vez enviada ya no es posible cancelarla.'),
('stock disponible producto agotado', 'Si un producto aparece sin stock puedes escribirnos para recibir una notificación cuando esté disponible nuevamente.'),
('precio descuento promocion', 'Tenemos promociones semanales en nuestra tienda. Síguenos en redes sociales para enterarte de descuentos exclusivos.');
