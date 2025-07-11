# swagger_docs.py
import yaml

register_doc = yaml.safe_load("""
---
tags:
  - Authentication
summary: Registro de nuevo usuario
description: |
  Crea una cuenta nueva enviando un JSON con los campos username, email y password.
  Retorna un mensaje de éxito o un error si los datos son inválidos.
consumes:
  - application/json
produces:
  - application/json
parameters:
  - in: body
    name: user
    required: true
    schema:
      type: object
      properties:
        username:
          type: string
        email: 
          type: string
        password:
          type: string
responses:
  "200":
    description: Usuario registrado exitosamente
  "400":
    description: Datos inválidos o faltantes
  "500":
    description: Error interno del servidor
""")


login_doc = yaml.safe_load("""
---
tags:
  - Authentication
summary: Inicio de sesión de usuario
description: |
  Permite que un usuario registrado inicie sesión proporcionando su correo y contraseña.
  Si las credenciales son válidas, devuelve un token JWT y la información del usuario.
consumes:
  - application/json
produces:
  - application/json
parameters:
  - in: body
    name: credentials
    description: Credenciales del usuario
    required: true
    schema:
      type: object
      properties:
        email:
          type: string
          example: usuario@email.com
        password:
          type: string
          example: my_secure_password
responses:
  "200":
    description: Usuario logueado exitosamente
    examples:
      application/json:
        access_token: "jwt_token_aqui"
        refresh_token: "jwt_refresh_token"
        user_id: 1
        email: usuario@email.com
        message: Login successful
  "400":
    description: Datos faltantes
  "401":
    description: Credenciales inválidas
  "404":
    description: Usuario no encontrado
  "500":
    description: Error interno del servidor
""")

get_tasks_doc = yaml.safe_load("""
---
tags:
  - Tareas
summary: Obtener tareas del usuario autenticado
description: |
  Devuelve todas las tareas del usuario autenticado. 
  Requiere token JWT en el encabezado Authorization.
security:
  - BearerAuth: []
produces:
  - application/json
responses:
  "200":
    description: Lista de tareas del usuario
    examples:
      application/json:
        - id: 1
          title: Comprar pan
          completed: false
        - id: 2
          title: Estudiar Flask
          completed: true
  "401":
    description: Token JWT inválido o no proporcionado
  "500":
    description: Error interno del servidor
""")

create_task_doc = yaml.safe_load("""
---
tags:
  - Tareas
summary: Crear una nueva tarea
description: |
  Crea una nueva tarea para el usuario autenticado. Requiere un título y una descripción.
  Debe enviarse un token JWT en el encabezado Authorization.
security:
  - BearerAuth: []
consumes:
  - application/json
produces:
  - application/json
parameters:
  - in: body
    name: tarea
    required: true
    description: Datos de la tarea a crear
    schema:
      type: object
      required:
        - title
        - description
      properties:
        title:
          type: string
          example: Estudiar
        description:
          type: string
          example: Repasar los apuntes del módulo 2
responses:
  "201":
    description: Tarea creada exitosamente
    examples:
      application/json:
        id: 3
        title: Estudiar
        description: Repasar los apuntes del módulo 2
        completed: false
  "400":
    description: Faltan campos requeridos (title o description)
  "401":
    description: No autorizado (token JWT inválido o no proporcionado)
  "500":
    description: Error interno del servidor
""")
get_task_doc = yaml.safe_load("""
---
tags:
  - Tareas
summary: Obtener una tarea por ID
description: | 
 Devuelve una tarea específica perteneciente al usuario autenticado.
  Requiere autenticación JWT y que la tarea exista y pertenezca al usuario.
security:
  - BearerAuth: []
produces:
    - application/json
parameters:
  - name: id
    in: path
    type: integer
    required: true
    description: ID de la tarea a obtener
responses:
  "200":
    description: Tarea encontrada
    examples:
      application/json:
        id: 1
        title: Comprar pan
        description: Ir al supermercado a comprar pan
        completed: false
    "401":
    description: Token JWT inválido o no proporcionado
  "404":
    description: Tarea no encontrada o no pertenece al usuario
  "500":
    description: Error interno del servidor
                              
 """)
update_task_doc = yaml.safe_load("""
---
tags:
  - Tareas
summary: Actualizar una tarea existente
description: |
  Permite modificar el título y/o la descripción de una tarea del usuario autenticado.
  Requiere autenticación JWT y que la tarea exista.
security: 
    - BearerAuth: []
consumes:
  - application/json
produces:
  - application/json
parameters:
    - name: id
      in: path
      type: integer
      required: true
      description: ID de la tarea a actualizar
    - in: body
      name: tarea 
      required: true
      description: Datos de la tarea a actualizar
      schema:
          type: object
          properties:
            title:
              type: string
              example: Actualizar título
            description:
              type: string
              example: Actualizar descripción de la tarea
responses:
  "200":
    description: Tarea actualizada exitosamente
    examples:
      application/json:
        id: 1
        title: Actualizar título
        description: Actualizar descripción de la tarea
        completed: false
  "401":
    description: No autorizado (token JWT inválido o no proporcionado)
  "404":
    description: Tarea no encontrada o no pertenece al usuario
  "500":
    description: Error interno del servidor
                                                            
""")
delete_task_doc = yaml.safe_load("""
---
tags:
  - Tareas
summary: Eliminar una tarea
description: |
  Elimina una tarea específica del usuario autenticado.
  Requiere autenticación JWT y que la tarea exista.
security:
  - BearerAuth: []
produces:
  - application/json
parameters:
  - name: id
    in: path
    required: true
    type: integer
    description: ID de la tarea a eliminar
responses:
  "200":
    description: Tarea eliminada exitosamente
    examples:
      application/json:
        message: Tarea eliminada
  "401":
    description: No autorizado (token JWT inválido o ausente)
  "404":
    description: Tarea no encontrada
  "500":
    description: Error interno del servidor
""")

mark_task_done_doc = yaml.safe_load("""
---
tags:
  - Tareas
summary: Marcar tarea como completada
description: |
  Marca una tarea como hecha (done = true) y registra la fecha de finalización.
  Requiere autenticación JWT.
security:
  - BearerAuth: []
produces:
  - application/json
parameters:
  - name: id
    in: path
    required: true
    type: integer
    description: ID de la tarea a marcar como completada
responses:
  "200":
    description: Tarea marcada como completada
    examples:
      application/json:
        id: 5
        title: Terminar proyecto
        description: Subirlo a GitHub
        done: true
        completed: "2025-07-11T10:34:00"
  "400":
    description: Tarea no encontrada
  "401":
    description: Token JWT no válido o ausente
  "500":
    description: Error interno del servidor
""")

