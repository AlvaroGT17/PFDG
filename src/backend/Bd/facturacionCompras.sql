-- Tabla: facturas
CREATE TABLE facturas (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    fecha TIMESTAMP DEFAULT NOW(),
    importe NUMERIC(10,2) NOT NULL DEFAULT 0,
    iva NUMERIC(5,2) NOT NULL DEFAULT 21,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);

-- Tabla: lineas_factura
CREATE TABLE lineas_factura (
    id SERIAL PRIMARY KEY,
    factura_id INTEGER NOT NULL,
    orden_trabajo_id INTEGER,
    descripcion VARCHAR(255),
    cantidad INTEGER NOT NULL DEFAULT 1,
    precio NUMERIC(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (factura_id) REFERENCES facturas(id) ON DELETE CASCADE,
    FOREIGN KEY (orden_trabajo_id) REFERENCES ordenes_trabajo(id) ON DELETE SET NULL
);

-- Tabla: compras
CREATE TABLE compras (
    id SERIAL PRIMARY KEY,
    proveedor_id INTEGER NOT NULL,
    fecha TIMESTAMP DEFAULT NOW(),
    importe NUMERIC(10,2) NOT NULL DEFAULT 0,
    iva NUMERIC(5,2) NOT NULL DEFAULT 21,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (proveedor_id) REFERENCES proveedores(id) ON DELETE CASCADE
);

-- Tabla: lineas_compra
CREATE TABLE lineas_compra (
    id SERIAL PRIMARY KEY,
    compra_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio NUMERIC(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (compra_id) REFERENCES compras(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE SET NULL
);
