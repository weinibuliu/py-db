# 数据表文档

## 公共枚举与基类

### Role（角色）

| 值  | 名称    | 说明   |
| --- | ------- | ------ |
| 0   | Student | 学生   |
| 1   | Teacher | 教师   |
| 2   | Admin   | 管理员 |

### Gender（性别）

| 值  | 名称   | 说明 |
| --- | ------ | ---- |
| 0   | Male   | 男   |
| 1   | Female | 女   |

### MyBaseModel（公共字段）

所有数据表模型均继承此基类，包含以下公共字段：

| 字段       | 类型 | 约束                 | 说明           |
| ---------- | ---- | -------------------- | -------------- |
| id         | int  | PK, 自增             | 主键           |
| created_at | int  | 非空                 | 创建时间戳     |
| edited_at  | int  | 非空, 更新时自动刷新 | 最后编辑时间戳 |
| created_by | str? | 可空                 | 创建者 uid     |

---

## 数据表

### 1. user_rft（用户表）

对应模型：`User`（继承 `BaseUser` → `MyBaseModel`，`table=True`）

| 字段                   | 类型      | 约束     | 默认值                 | 说明                               |
| ---------------------- | --------- | -------- | ---------------------- | ---------------------------------- |
| **继承自 MyBaseModel** |           |          |                        |                                    |
| id                     | int       | PK, 自增 | —                      | 主键                               |
| created_at             | int       | 非空     | 当前时间戳             | 创建时间                           |
| edited_at              | int       | 非空     | 当前时间戳（自动更新） | 最后编辑时间                       |
| created_by             | str(255)? | 可空     | null                   | 创建者 uid                         |
| **User 字段**          |           |          |                        |                                    |
| uid                    | str(255)  | 非空     | —                      | 用户唯一标识（10 位学号/工号）     |
| password               | str(255)  | 非空     | —                      | 密码（加密存储）                   |
| status                 | int       | 非空     | 0 (OK)                 | 用户状态（见 `UserStatus`）        |
| name                   | str(255)  | 非空     | —                      | 姓名                               |
| role                   | int       | 非空     | —                      | 角色（见 `Role`）                  |
| gender                 | int       | 非空     | —                      | 性别（见 `Gender`）                |
| college                | str(255)  | 非空     | —                      | 学院                               |
| reason                 | str(255)? | 可空     | null                   | 状态说明（如封禁原因）             |
| grade                  | str(255)? | 可空     | null                   | 年级（仅学生）                     |
| class                  | str(255)? | 可空     | null                   | 班级（仅学生，数据库列名 `class`） |
| major                  | str(255)? | 可空     | null                   | 专业（仅学生）                     |

#### 关联模型

**CreateUser**（创建用户请求，继承 `pydantic.BaseModel`）

| 字段     | 类型   | 约束      | 默认值     | 说明 |
| -------- | ------ | --------- | ---------- | ---- |
| uid      | str    | 长度 10   | —          | uid  |
| password | str    | 长度 8-18 | —          | 密码 |
| name     | str    | 长度 ≥ 2  | —          | 姓名 |
| role     | Role   | —         | Student(0) | 角色 |
| gender   | Gender | 必填      | —          | 性别 |
| college  | str    | 必填      | —          | 学院 |
| grade    | str?   | 可空      | null       | 年级 |
| class\_  | str?   | 可空      | null       | 班级 |
| major    | str?   | 可空      | null       | 专业 |

**UpdateUser**（更新用户请求，继承 `MyBaseModel`）：所有字段均为可选（`Optional`），包含除 `uid` 外的全部 `User` 字段。

**UserPublic**（用户公开信息，`table=False`，不映射数据表）

| 字段    | 类型      | 约束 | 说明         |
| ------- | --------- | ---- | ------------ |
| uid     | str(255)  | 非空 | 用户唯一标识 |
| name    | str(255)  | 非空 | 姓名         |
| role    | int       | 非空 | 角色         |
| gender  | int       | 非空 | 性别         |
| college | str(255)  | 非空 | 学院         |
| grade   | str(255)? | 可空 | 年级         |
| class   | str(255)? | 可空 | 班级         |
| major   | str(255)? | 可空 | 专业         |

---

### 2. class（班级表）

对应模型：`Class`（继承 `BaseClass` → `MyBaseModel`，`table=True`）

| 字段                   | 类型      | 约束     | 默认值                 | 说明                         |
| ---------------------- | --------- | -------- | ---------------------- | ---------------------------- |
| **继承自 MyBaseModel** |           |          |                        |                              |
| id                     | int       | PK, 自增 | —                      | 主键                         |
| created_at             | int       | 非空     | 当前时间戳             | 创建时间                     |
| edited_at              | int       | 非空     | 当前时间戳（自动更新） | 最后编辑时间                 |
| created_by             | str(255)? | 可空     | null                   | 创建者 uid                   |
| **Class 字段**         |           |          |                        |                              |
| status                 | int       | 非空     | 0 (OK)                 | 班级状态（见 `ClassStatus`） |
| name                   | str(255)  | 非空     | —                      | 班级名称                     |
| course                 | str(255)? | 可空     | null                   | 课程名                       |
| private                | bool      | 非空     | false                  | 是否为私有班级               |

#### ClassStatus（班级状态）

| 值  | 名称    | 说明     |
| --- | ------- | -------- |
| 0   | OK      | 正常     |
| 1   | Created | 已创建   |
| 2   | Ended   | 已结束   |
| 100 | Deleted | 逻辑删除 |

#### 关联模型

**CreateClass**（创建班级请求，继承 `MyBaseModel`）

| 字段    | 类型        | 约束 | 默认值 | 说明     |
| ------- | ----------- | ---- | ------ | -------- |
| name    | str         | 必填 | —      | 班级名称 |
| course  | str?        | 可空 | null   | 课程名   |
| status  | ClassStatus | —    | OK(0)  | 班级状态 |
| private | bool        | —    | false  | 是否私有 |

**UpdateClass**（更新班级请求，继承 `MyBaseModel`）：所有字段均为可选（`Optional`），包含 `status`、`name`、`course`、`private`。

---

### 3. class_record（班级记录表）

对应模型：`ClassRecord`（继承 `BaseClassRecord` → `MyBaseModel`，`table=True`）

记录用户与班级的关联关系（用户加入班级的记录）。

| 字段                   | 类型      | 约束     | 默认值                 | 说明                               |
| ---------------------- | --------- | -------- | ---------------------- | ---------------------------------- |
| **继承自 MyBaseModel** |           |          |                        |                                    |
| id                     | int       | PK, 自增 | —                      | 主键                               |
| created_at             | int       | 非空     | 当前时间戳             | 创建时间                           |
| edited_at              | int       | 非空     | 当前时间戳（自动更新） | 最后编辑时间                       |
| created_by             | str(255)? | 可空     | null                   | 创建者 uid                         |
| **ClassRecord 字段**   |           |          |                        |                                    |
| status                 | int       | 非空     | 0 (OK)                 | 记录状态（见 `ClassRecordStatus`） |
| uid                    | str(255)  | 非空     | —                      | 用户 uid                           |
| role                   | int       | 非空     | —                      | 用户在班级中的角色（见 `Role`）    |
| class_id               | int       | 非空     | —                      | 关联的班级 id（→ `class.id`）      |

#### ClassRecordStatus（班级记录状态）

| 值  | 名称    | 说明     |
| --- | ------- | -------- |
| 0   | OK      | 正常     |
| 100 | Deleted | 逻辑删除 |

#### 关联模型

**CreateClassRecord**（创建班级记录请求，继承 `MyBaseModel`）

| 字段     | 类型              | 约束 | 默认值 | 说明     |
| -------- | ----------------- | ---- | ------ | -------- |
| uid      | str               | 必填 | —      | 用户 uid |
| role     | Role              | 必填 | —      | 角色     |
| class_id | int               | 必填 | —      | 班级 id  |
| status   | ClassRecordStatus | —    | OK(0)  | 记录状态 |

**UpdateClassRecord**（更新班级记录请求，继承 `MyBaseModel`）：所有字段均为可选（`Optional`），包含 `status`、`uid`、`role`、`class_id`。

---

## ER 关系

```
┌──────────────┐          ┌─────────────────┐
│   user_rft   │          │      class      │
├──────────────┤          ├─────────────────┤
│ id (PK)      │          │ id (PK)         │
│ uid (UNIQUE) │──┐       │ name            │
│ password     │  │       │ course?         │
│ status       │  │       │ status          │
│ name         │  │    ┌──│ private         │
│ role         │  │    │  │ created_by?     │
│ gender       │  │    │  │ created_at      │
│ college      │  │    │  │ edited_at       │
│ reason?      │  │    │  └─────────────────┘
│ grade?       │  │    │
│ class?       │  │    │
│ major?       │  │    │
│ created_by?  │  │    │
│ created_at   │  │    │
│ edited_at    │  │    │
└──────────────┘  │    │
                  │    │
       ┌──────────┼────┼──────────────────┐
       │      class_record                │
       ├──────────────────────────────────┤
       │ id (PK)                          │
       │ uid ────→ user_rft.uid           │
       │ class_id ──→ class.id            │
       │ role                             │
       │ status                           │
       │ created_by?                      │
       │ created_at                       │
       │ edited_at                        │
       └──────────────────────────────────┘
```

- `class_record.uid` → `user_rft.uid`：班级记录关联用户
- `class_record.class_id` → `class.id`：班级记录关联班级

---

## 通用约定

1. **逻辑删除**：`status = 100`（`Deleted`）表示逻辑删除，不物理删除记录。
2. **时间戳**：`created_at` / `edited_at` 均为 Unix 时间戳（秒），`edited_at` 在每次更新时自动刷新。
3. **审计字段**：`created_by` 记录创建者的 uid，用于审计追溯。
4. **命名注意**：`class_` 在 Python 模型中使用下划线后缀避免关键字冲突，数据库实际列名为 `class`（通过 `sa_column_kwargs={"name": "class"}` 映射）。
