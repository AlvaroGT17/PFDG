-- Tabla: servicios
CREATE TABLE servicios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio NUMERIC(10,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabla: ordenes_trabajo
CREATE TABLE ordenes_trabajo (
    id SERIAL PRIMARY KEY,
    coche_id INTEGER NOT NULL,
    empleado_id INTEGER NOT NULL,
    fecha TIMESTAMP NOT NULL DEFAULT NOW(),
    descripcion TEXT,
    estado VARCHAR(50) DEFAULT 'pendiente',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (coche_id) REFERENCES coches(id) ON DELETE CASCADE,
    FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE SET NULL
);

-- Tabla pivot: orden_trabajo_servicio
CREATE TABLE orden_trabajo_servicio (
    orden_trabajo_id INTEGER NOT NULL,
    servicio_id INTEGER NOT NULL,
    PRIMARY KEY (orden_trabajo_id, servicio_id),
    FOREIGN KEY (orden_trabajo_id) REFERENCES ordenes_trabajo(id) ON DELETE CASCADE,
    FOREIGN KEY (servicio_id) REFERENCES servicios(id) ON DELETE CASCADE
);
