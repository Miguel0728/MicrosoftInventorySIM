"""
Datos iniciales del inventario.
Se cargan automáticamente si la BD está vacía (local y Render).
"""

INVENTORY_SEED = [
    # (modelo, marca, id_number, asignado_a, costo_total, estado, departamento)
    ('ThinkPad T14 Gen 3',     'Lenovo',      'LNV-0001', 'Juan Pérez',              1350.00, 'Activo',        'IT'),
    ('ThinkPad E15',            'Lenovo',      'LNV-0002', 'María García',             1100.00, 'Activo',        'Dirección'),
    ('ThinkPad L14',            'Lenovo',      'LNV-0003', 'Carlos López',              980.00, 'Inactivo',      'Operaciones'),
    ('ThinkCentre M90q',        'Lenovo',      'LNV-0004', 'Ana Torres',                750.00, 'Activo',        'Finanzas'),
    ('MacBook Pro 14" M3',      'Apple',       'APL-0001', 'Luis Ramírez',             2499.00, 'Activo',        'Dirección'),
    ('MacBook Air M2',          'Apple',       'APL-0002', 'Sofía Méndez',             1299.00, 'Activo',        'Planificación'),
    ('MacBook Pro 16" M3 Pro',  'Apple',       'APL-0003', 'Roberto Sánchez',          3199.00, 'Activo',        'Dirección'),
    ('iPad Pro 12.9"',          'Apple',       'APL-0004', 'Gabriela Ortiz',           1099.00, 'Activo',        'Legal'),
    ('iPhone 15 Pro',           'Apple',       'APL-0005', 'Luis Ramírez',             1099.00, 'Activo',        'Dirección'),
    ('iPhone 14',               'Apple',       'APL-0006', 'Carmen Rivera',             699.00, 'Activo',        'Legal'),
    ('OptiPlex 7090',           'Dell',        'DLL-0001', 'Pedro Martínez',            870.00, 'Activo',        'IT'),
    ('OptiPlex 5090',           'Dell',        'DLL-0002', 'Laura Herrera',             720.00, 'Mantenimiento', 'Operaciones'),
    ('Latitude 5540',           'Dell',        'DLL-0003', 'Miguel Flores',            1150.00, 'Activo',        'Legal'),
    ('Latitude 7440',           'Dell',        'DLL-0004', 'Carmen Rivera',            1450.00, 'Activo',        'Planificación'),
    ('PowerEdge T40',           'Dell',        'DLL-0005', 'IT General',               2100.00, 'Activo',        'IT'),
    ('P2422H Monitor 24"',      'Dell',        'DLL-0006', 'Juan Pérez',                320.00, 'Activo',        'IT'),
    ('P2422H Monitor 24"',      'Dell',        'DLL-0007', 'María García',              320.00, 'Activo',        'Dirección'),
    ('UltraSharp U2722D 27"',   'Dell',        'DLL-0008', 'Carlos López',              580.00, 'Activo',        'IT'),
    ('UltraSharp U2722D 27"',   'Dell',        'DLL-0009', 'Sofía Méndez',              580.00, 'Activo',        'Planificación'),
    ('EliteBook 840 G10',       'HP',          'HP-0001',  'Jorge Vázquez',            1250.00, 'Activo',        'RRHH'),
    ('EliteBook 860 G10',       'HP',          'HP-0002',  'Patricia Castro',          1380.00, 'Activo',        'Finanzas'),
    ('ProBook 450 G10',         'HP',          'HP-0003',  'Fernando Díaz',             890.00, 'Inactivo',      'Operaciones'),
    ('HP LaserJet Pro M404',    'HP',          'HP-0004',  'RRHH General',              450.00, 'Activo',        'RRHH'),
    ('HP DesignJet T650',       'HP',          'HP-0005',  'Planificación General',    2800.00, 'Activo',        'Planificación'),
    ('Galaxy Book3 Pro',        'Samsung',     'SAM-0001', 'Valeria Morales',          1499.00, 'Activo',        'Ventas'),
    ('Galaxy Tab S9',           'Samsung',     'SAM-0002', 'Ricardo Luna',              799.00, 'Mantenimiento', 'Legal'),
    ('Galaxy S24 Ultra',        'Samsung',     'SAM-0003', 'Natalia Jiménez',           999.00, 'Activo',        'Dirección'),
    ('Galaxy S24',              'Samsung',     'SAM-0004', 'Andrés Vargas',             799.00, 'Activo',        'Ventas'),
    ('Surface Pro 10',          'Microsoft',   'MSF-0001', 'Elena Castillo',           1599.00, 'Activo',        'Planificación'),
    ('Surface Laptop 6',        'Microsoft',   'MSF-0002', 'Héctor Reyes',             1399.00, 'Activo',        'IT'),
    ('Switch Cisco SG350-28',   'Cisco',       'CSC-0001', 'IT General',               1800.00, 'Activo',        'IT'),
    ('Router Cisco RV340',      'Cisco',       'CSC-0002', 'IT General',                450.00, 'Activo',        'IT'),
    ('UPS CyberPower 1500VA',   'CyberPower',  'CYB-0001', 'IT General',                220.00, 'Activo',        'IT'),
    ('Webcam Logitech C925e',   'Logitech',    'LGT-0001', 'Pedro Martínez',            180.00, 'Activo',        'IT'),
    ('Teclado MX Keys',         'Logitech',    'LGT-0002', 'Roberto Sánchez',           120.00, 'Baja',          'Dirección'),
]
