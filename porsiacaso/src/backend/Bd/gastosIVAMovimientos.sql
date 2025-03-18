-- Tabla: tipos_iva
CREATE TABLE tipos_iva (
    id SERIAL PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL,
    porcentaje NUMERIC(5,2) NOT NULL DEFAULT 21,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabla: tipos_gastos
CREATE TABLE tipos_gastos (
    id SERIAL PRIMARY KEY,
    descripcion VARCHAR(150) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabla: gastos
CREATE TABLE gastos (
    id SERIAL PRIMARY KEY,
    tipo_gasto_id INTEGER NOT NULL,
    fecha TIMESTAMP NOT NULL DEFAULT NOW(),
    descripcion TEXT,
    importe NUMERIC(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (tipo_gasto_id) REFERENCES tipos_gastos(id) ON DELETE CASCADE
);

-- Tabla: tipos_movimientos
CREATE TABLE tipos_movimientos (
    id SERIAL PRIMARY KEY,
    descripcion VARCHAR(150) NOT NULL,
    operacion INTEGER NOT NULL CHECK (operacion IN (-1, 1)),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabla: movimientos
CREATE TABLE movimientos (
    id SERIAL PRIMARY KEY,
    tipo_movimiento_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    fecha TIMESTAMP DEFAULT NOW(),
    cantidad INTEGER NOT NULL,
    precio NUMERIC(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (tipo_movimiento_id) REFERENCES tipos_movimientos(id) ON DELETE SET NULL,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
);
