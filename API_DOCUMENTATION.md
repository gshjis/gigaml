# Документация API

## Схемы данных

### Схемы задач (Task Schemas)

- **TaskSchemaInput**: Используется для создания новой задачи.
  - name: str (обязательное)
  - description: str | None (опциональное)
  - pomodoro_count: int (обязательное)
  - category_id: int (обязательное)

- **TaskSchemaUpdate**: Используется для обновления задачи.
  - name: str | None (опциональное)
  - description: str | None (опциональное)
  - pomodoro_count: int | None (опциональное)
  - category_id: int | None (опциональное)

- **TaskSchemaOutput**: Используется для вывода задачи.
  - task_id: int
  - name: str
  - description: str | None
  - pomodoro_count: int
  - category_id: int
  - owner_id: int
  - created_at: datetime
  - updated_at: datetime

### Схемы пользователей (User Schemas)

- **UserCreate**: Используется для создания нового пользователя.
  - username: str
  - email: EmailStr
  - password: str

- **UserOut**: Используется для вывода пользователя.
  - user_id: int
  - username: str
  - email: EmailStr

### Схемы категорий (Category Schemas)

- **CategorySchemaInput**: Используется для создания новой категории.
  - name: str

- **CategorySchemaOutput**: Используется для вывода категории.
  - category_id: int
  - name: str

## Эндпоинты

### Эндпоинты задач (Tasks Endpoints)

- **GET /api/tasks**
  - Описание: Получает все активные задачи для текущего пользователя.
  - Принимает: Требуется аутентификация (через токен).
  - Возвращает: Список объектов TaskSchemaOutput (код 200 OK).

- **POST /api/tasks**
  - Описание: Создает новую задачу.
  - Принимает: Тело запроса в формате TaskSchemaInput.
  - Возвращает: Объект TaskSchemaOutput созданной задачи (код 201 Created).

- **DELETE /api/tasks/{task_id}**
  - Описание: Удаляет задачу по ID.
  - Принимает: task_id в пути; Требуется аутентификация.
  - Возвращает: Пустой ответ (код 204 No Content).

- **PATCH /api/tasks/{task_id}**
  - Описание: Частично обновляет задачу.
  - Принимает: task_id в пути; Тело запроса в формате TaskSchemaUpdate.
  - Возвращает: Объект TaskSchemaOutput обновленной задачи (код 200 OK).

### Эндпоинты аутентификации (Authentication Endpoints)

- **POST /auth/register**
  - Описание: Регистрирует нового пользователя.
  - Принимает: Тело запроса в формате UserCreate.
  - Возвращает: Объект RegisterResponse с информацией о пользователе и токенами (код 201 Created).

- **POST /auth/login**
  - Описание: Авторизует пользователя.
  - Принимает: Форма с username и password (OAuth2PasswordRequestForm).
  - Возвращает: Объект TokenResponse с access токеном (код 200 OK).

- **POST /auth/refresh**
  - Описание: Обновляет access токен.
  - Принимает: Refresh токен в куках.
  - Возвращает: Новый TokenResponse (код 200 OK).
