-- Tabla: usuarios
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    email_verified_at TIMESTAMP NULL,
    password VARCHAR(255) NOT NULL,
    remember_token VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabla: clientes
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nif VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido1 VARCHAR(100) NOT NULL,
    apellido2 VARCHAR(100),
    email VARCHAR(150),
    telefono VARCHAR(20),
    direccion VARCHAR(200),
    localidad VARCHAR(100),
    provincia VARCHAR(100),
    codigo_postal VARCHAR(10),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabla: empleados
CREATE TABLE empleados (
    id SERIAL PRIMARY KEY,
    nif VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido1 VARCHAR(100) NOT NULL,
    apellido2 VARCHAR(100),
    email VARCHAR(150),
    telefono VARCHAR(20),
    direccion VARCHAR(200),
    localidad VARCHAR(100),
    provincia VARCHAR(100),
    codigo_postal VARCHAR(10),
    fecha_alta DATE NOT NULL,
    fecha_baja DATE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabla: coches
CREATE TABLE coches (
    id SERIAL PRIMARY KEY,
    matricula VARCHAR(15) UNIQUE NOT NULL,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    color VARCHAR(30),
    kms INTEGER DEFAULT 0,
    cliente_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);
