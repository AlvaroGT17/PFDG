-- Tabla: familias
CREATE TABLE familias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabla: marcas
CREATE TABLE marcas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabla: tipos_iva
CREATE TABLE tipos_iva (
    id SERIAL PRIMARY KEY,
    descripcion VARCHAR(100),
    porcentaje NUMERIC(5,2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabla: formas_pago
CREATE TABLE formas_pago (
    id SERIAL PRIMARY KEY,
    descripcion VARCHAR(100),
    dias INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabla: proveedores
CREATE TABLE proveedores (
    id SERIAL PRIMARY KEY,
    nif VARCHAR(20),
    nombre VARCHAR(150),
    direccion VARCHAR(200),
    localidad VARCHAR(100),
    provincia VARCHAR(100),
    codigo_postal VARCHAR(10),
    telefono VARCHAR(20),
    email VARCHAR(150),
    forma_pago_id INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (forma_pago_id) REFERENCES formas_pago(id) ON DELETE SET NULL
);

-- Tabla: marcas
CREATE TABLE marcas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabla: productos
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    descripcion VARCHAR(255),
    observaciones TEXT,
    precio_coste NUMERIC(10,2),
    precio_venta NUMERIC(10,2),
    stock INTEGER DEFAULT 0,
    stock_minimo INTEGER DEFAULT 0,
    marca_id INTEGER,
    familia_id INTEGER,
    tipo_iva_id INTEGER,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (marca_id) REFERENCES marcas(id) ON DELETE SET NULL,
    FOREIGN KEY (familia_id) REFERENCES familias(id) ON DELETE SET NULL,
    FOREIGN KEY (tipo_iva_id) REFERENCES tipos_iva(id) ON DELETE SET NULL
);

-- Tabla pivot: producto_proveedor
CREATE TABLE producto_proveedor (
    producto_id INTEGER,
    proveedor_id INTEGER,
    PRIMARY KEY (producto_id, proveedor_id),
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE,
    FOREIGN KEY (proveedor_id) REFERENCES proveedores(id) ON DELETE CASCADE
);

-- Tabla pivot: familia_proveedor
CREATE TABLE familia_proveedor (
    familia_id INTEGER,
    proveedor_id INTEGER,
    PRIMARY KEY (familia_id, proveedor_id),
    FOREIGN KEY (familia_id) REFERENCES familias(id) ON DELETE CASCADE,
    FOREIGN KEY (proveedor_id) REFERENCES proveedores(id) ON DELETE CASCADE
);

-- Tabla: compras
CREATE TABLE compras (
    id SERIAL PRIMARY KEY,
    proveedor_id INTEGER,
    fecha TIMESTAMP DEFAULT NOW(),
    importe NUMERIC(10,2),
    iva NUMERIC(10,2),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (proveedor_id) REFERENCES proveedores(id) ON DELETE SET NULL
);

-- Tabla: lineas_compra
CREATE TABLE lineas_compra (
    id SERIAL PRIMARY KEY,
    compra_id INTEGER,
    producto_id INTEGER,
    cantidad INTEGER,
    precio NUMERIC(10,2),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (compra_id) REFERENCES compras(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE SET NULL
);

-- Tabla: tipos_movimientos
CREATE TABLE tipos_movimientos (
    id SERIAL PRIMARY KEY,
    descripcion VARCHAR(100),
    operacion INTEGER, -- (+1 entrada, -1 salida)
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabla: movimientos
CREATE TABLE movimientos (
    id SERIAL PRIMARY KEY,
    tipo_movimiento_id INTEGER,
    producto_id INTEGER,
    fecha TIMESTAMP DEFAULT NOW(),
    cantidad INTEGER,
    precio NUMERIC(10,2),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (tipo_movimiento_id) REFERENCES tipos_movimientos(id) ON DELETE SET NULL,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
);
