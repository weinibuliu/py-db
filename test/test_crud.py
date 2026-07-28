"""
对 user_rft / class / class_record 三张表的 CRU 操作进行单测覆盖。

C — Create  (create_user / create_class / create_class_record)
R — Read    (get_user / get_class / get_class_record)
U — Update  (update_user / update_class / update_class_record)

未涉及 Delete，因为项目采用逻辑删除策略，不对外提供 DELETE 接口。
"""

import pytest

from src import db
from src.db import AlreadyExistsError, NotFoundError
from src.db._db import (
    # Create
    create_user,
    create_class,
    create_class_record,
    CreateUser,
    CreateClass,
    CreateClassRecord,
    # Update models
    UpdateUser,
    UpdateClass,
    UpdateClassRecord,
    # Read
    get_user,
    # get_user_by_id,
    get_user_by_uid,
    get_class,
    get_class_by_id,
    get_class_record,
    # Update
    update_user,
    update_class,
    update_class_record,
    # Enums
    Role,
    Gender,
    UserStatus,
    ClassStatus,
    ClassRecordStatus,
)

pytestmark = pytest.mark.usefixtures("setup_test_db")

# ============================================================
#  User (user_rft)  —  CRU
# ============================================================


class TestCreateUser:
    """create_user"""

    def test_create_ok(self):
        """创建一个新用户，应成功完成。"""
        result = create_user(
            usr=CreateUser(
                uid="2024001001",
                password="12345678",
                name="张三",
                role=Role.Student,
                gender=Gender.Male,
                college="信息学院",
                grade="2024",
                class_="软件2401",
                major="软件工程",
            )
        )
        assert result is None

    def test_create_minimal_fields(self):
        """仅传必填字段创建用户，可选字段留空"""
        result = create_user(
            usr=CreateUser(
                uid="t001000000",
                password="password1",
                name="李四",
                role=Role.Teacher,
                gender=Gender.Female,
                college="",
            )
        )
        assert result is None

    def test_create_duplicate_uid(self):
        """重复 uid 创建应抛出 AlreadyExistsError。"""
        create_user(
            usr=CreateUser(
                uid="dup0010000",
                password="password1",
                name="王五",
                role=Role.Student,
                gender=Gender.Male,
                college="",
            )
        )
        with pytest.raises(AlreadyExistsError):
            create_user(
                usr=CreateUser(
                    uid="dup0010000",
                    password="another12",
                    name="赵六",
                    role=Role.Teacher,
                    gender=Gender.Female,
                    college="",
                )
            )


class TestReadUser:
    """get_user"""

    def test_get_by_uid_found(self):
        """按 uid 查询存在的用户，应返回 User 对象"""
        create_user(
            usr=CreateUser(
                uid="r001000000",
                password="password1",
                name="读测试",
                role=Role.Student,
                gender=Gender.Male,
                college="计算机学院",
            )
        )
        user = get_user_by_uid(uid="r001000000")
        assert user is not None
        assert user.uid == "r001000000"  # type: ignore[union-attr]
        assert user.name == "读测试"  # type: ignore[union-attr]
        assert user.role == Role.Student  # type: ignore[union-attr]
        assert user.gender == Gender.Male  # type: ignore[union-attr]
        assert user.college == "计算机学院"  # type: ignore[union-attr]
        assert user.status == UserStatus.OK  # type: ignore[union-attr]

    def test_get_by_uid_not_found(self):
        """按 uid 查询不存在的用户，应返回 None"""
        user = get_user_by_uid(uid="nonexistent")
        assert user is None

    def test_get_by_name_multiple(self):
        """按 name 查询，返回同名用户列表"""
        create_user(
            usr=CreateUser(
                uid="n010000000",
                password="password1",
                name="同名",
                role=Role.Student,
                gender=Gender.Male,
                college="",
            )
        )
        create_user(
            usr=CreateUser(
                uid="n020000000",
                password="password2",
                name="同名",
                role=Role.Student,
                gender=Gender.Female,
                college="",
            )
        )
        users = get_user(name="同名")
        assert isinstance(users, list)
        assert len(users) == 2

    def test_get_by_name_none(self):
        """按 name 查询无匹配，返回空列表"""
        users = get_user(name="不存在的名字")
        assert isinstance(users, list)
        assert len(users) == 0

    def test_get_by_status(self):
        """按 status 查询，仅返回匹配状态的用户"""
        create_user(
            usr=CreateUser(
                uid="s010000000",
                password="password1",
                name="正常",
                role=Role.Student,
                gender=Gender.Male,
                college="",
            )
        )
        create_user(
            usr=CreateUser(
                uid="s020000000",
                password="password2",
                name="禁用",
                role=Role.Teacher,
                gender=Gender.Female,
                college="",
            )
        )
        # 将 s020000000 禁用
        update_user(uid="s020000000", data=UpdateUser(status=UserStatus.Banned))

        ok_users = get_user(status=UserStatus.OK)
        banned_users = get_user(status=UserStatus.Banned)

        assert len(ok_users) == 1
        assert ok_users[0].uid == "s010000000"
        assert len(banned_users) == 1
        assert banned_users[0].uid == "s020000000"

    def test_get_by_role(self):
        """按 role 查询，仅返回匹配角色的用户"""
        create_user(
            usr=CreateUser(
                uid="role_stu01",
                password="password1",
                name="学生A",
                role=Role.Student,
                gender=Gender.Male,
                college="",
            )
        )
        create_user(
            usr=CreateUser(
                uid="role_tea01",
                password="password2",
                name="教师A",
                role=Role.Teacher,
                gender=Gender.Female,
                college="",
            )
        )
        create_user(
            usr=CreateUser(
                uid="role_stu02",
                password="password3",
                name="学生B",
                role=Role.Student,
                gender=Gender.Male,
                college="",
            )
        )

        students = get_user(role=Role.Student)
        teachers = get_user(role=Role.Teacher)

        assert isinstance(students, list)
        assert len(students) == 2
        assert all(r.role == Role.Student for r in students)

        assert isinstance(teachers, list)
        assert len(teachers) == 1
        assert teachers[0].uid == "role_tea01"
        assert teachers[0].role == Role.Teacher

    def test_read_after_create_all_fields_match(self):
        """创建后读取，所有字段应与创建时一致"""
        create_user(
            usr=CreateUser(
                uid="full001000",
                password="secret_12",
                name="完整测试",
                role=Role.Student,
                gender=Gender.Female,
                college="理学院",
                grade="2023",
                class_="数学2301",
                major="应用数学",
            )
        )
        user = get_user_by_uid(uid="full001000")
        assert user is not None
        u = user  # type: ignore[union-attr]
        assert u.password == "secret_12"
        assert u.grade == "2023"
        assert u.class_ == "数学2301"
        assert u.major == "应用数学"


class TestUpdateUser:
    """update_user"""

    def test_update_all_fields(self):
        """更新用户所有可更新字段"""
        create_user(
            usr=CreateUser(
                uid="upd0010000",
                password="old_passw",
                name="旧名",
                role=Role.Student,
                gender=Gender.Male,
                college="旧学院",
            )
        )
        result = update_user(
            uid="upd0010000",
            data=UpdateUser(
                password="new_passw",
                name="新名",
                role=Role.Teacher,
                gender=Gender.Female,
                college="新学院",
                grade="2025",
                class_="新班级",
                major="新专业",
                reason="测试原因",
            ),
        )
        assert result is None

        user = get_user_by_uid(uid="upd0010000")
        assert user is not None
        u = user  # type: ignore[union-attr]
        assert u.password == "new_passw"
        assert u.name == "新名"
        assert u.role == Role.Teacher
        assert u.gender == Gender.Female
        assert u.college == "新学院"
        assert u.grade == "2025"
        assert u.class_ == "新班级"
        assert u.major == "新专业"
        assert u.reason == "测试原因"

    def test_update_partial_fields(self):
        """仅更新部分字段，其余字段不变"""
        create_user(
            usr=CreateUser(
                uid="upd0020000",
                password="password1",
                name="部分更新",
                role=Role.Student,
                gender=Gender.Male,
                college="原学院",
            )
        )
        result = update_user(uid="upd0020000", data=UpdateUser(name="新名字"))
        assert result is None

        user = get_user_by_uid(uid="upd0020000")
        assert user is not None
        u = user  # type: ignore[union-attr]
        assert u.name == "新名字"
        # 未传的字段保持原值
        assert u.college == "原学院"
        assert u.role == Role.Student

    def test_update_status_to_banned(self):
        """将用户状态更新为 Banned"""
        create_user(
            usr=CreateUser(
                uid="upd0030000",
                password="password1",
                name="待禁用",
                role=Role.Student,
                gender=Gender.Male,
                college="",
            )
        )
        result = update_user(
            uid="upd0030000",
            data=UpdateUser(status=UserStatus.Banned, reason="违规"),
        )
        assert result is None

        user = get_user_by_uid(uid="upd0030000")
        assert user is not None
        assert user.status == UserStatus.Banned

    def test_update_not_found(self):
        """更新不存在的用户应抛出 NotFoundError。"""
        with pytest.raises(NotFoundError):
            update_user(uid="no_such_user", data=UpdateUser(name="新名字"))


# ============================================================
#  Class (class)  —  CRU
# ============================================================


class TestCreateClass:
    """create_class"""

    def test_create_ok(self):
        """创建一个班级应成功完成。"""
        result = create_class(
            cls=CreateClass(name="蓝桥1班", course="2026年蓝桥杯培训")
        )
        assert result is None

    def test_create_with_status(self):
        """以指定状态创建班级"""
        result = create_class(
            cls=CreateClass(name="已结束班", course="旧课程", status=ClassStatus.Ended)
        )
        assert result is None


class TestReadClass:
    """get_class"""

    def test_get_by_id_found(self):
        """按 id 查询存在的班级"""
        create_class(cls=CreateClass(name="测试班", course="测试课程"))
        # 自增 id 从 1 开始
        cls = get_class_by_id(id=1)
        assert cls is not None
        assert cls.name == "测试班"  # type: ignore[union-attr]
        assert cls.course == "测试课程"  # type: ignore[union-attr]
        assert cls.status == ClassStatus.OK  # type: ignore[union-attr]
        assert cls.private is False  # type: ignore[union-attr]

    def test_get_by_id_not_found(self):
        """按 id 查询不存在的班级，应返回 None"""
        cls = get_class_by_id(id=9999)
        assert cls is None

    def test_get_by_name(self):
        """按 name / course 查询班级列表"""
        create_class(cls=CreateClass(name="A班", course="C语言"))
        create_class(cls=CreateClass(name="B班", course="C语言"))
        create_class(cls=CreateClass(name="C班", course="Python"))

        result = get_class(name="A班")
        assert isinstance(result, list)
        assert len(result) == 1

        result = get_class(course="C语言")
        assert isinstance(result, list)
        assert len(result) == 2

    def test_get_by_name_empty(self):
        """按 name 查询无匹配的 course，返回空列表"""
        result = get_class(name="任意", course="不存在的课程")
        assert isinstance(result, list)
        assert len(result) == 0

    def test_get_by_status(self):
        """按 status 查询班级列表"""
        create_class(cls=CreateClass(name="进行中", status=ClassStatus.OK))
        create_class(cls=CreateClass(name="已结束", status=ClassStatus.Ended))

        ok = get_class(status=ClassStatus.OK)
        ended = get_class(status=ClassStatus.Ended)

        assert len(ok) == 1
        assert ok[0].name == "进行中"
        assert len(ended) == 1
        assert ended[0].name == "已结束"

    def test_get_by_id_private(self):
        """按 id 查询私有班级"""
        create_class(cls=CreateClass(name="私有班", private=True))
        cls = get_class_by_id(id=1)
        assert cls is not None
        assert cls.private == True
        assert cls.name == "私有班"  # type: ignore[union-attr]


class TestUpdateClass:
    """update_class"""

    def test_update_all_fields(self):
        """更新班级所有可更新字段"""
        create_class(cls=CreateClass(name="旧班名", course="旧课程"))
        result = update_class(
            id=1,
            data=UpdateClass(
                name="新班名",
                course="新课程",
                status=ClassStatus.Ended,
                private=True,
            ),
        )
        assert result is None

        cls = get_class_by_id(id=1)
        assert cls is not None
        assert cls.status == ClassStatus.Ended
        assert cls.private == True

        c = cls  # type: ignore[union-attr]
        assert c.name == "新班名"
        assert c.course == "新课程"
        assert c.status == ClassStatus.Ended
        assert c.private is True

    def test_update_partial(self):
        """仅更新班级名称"""
        create_class(cls=CreateClass(name="原名"))
        result = update_class(id=1, data=UpdateClass(name="改名"))
        assert result is None

        cls = get_class_by_id(id=1)
        assert cls is not None
        assert cls.name == "改名"  # type: ignore[union-attr]
        assert cls.course is None  # type: ignore[union-attr]  # 未改

    def test_update_not_found(self):
        """更新不存在的班级应抛出 NotFoundError。"""
        with pytest.raises(NotFoundError):
            update_class(id=9999, data=UpdateClass(name="新名"))


# ============================================================
#  ClassRecord (class_record)  —  CRU
# ============================================================


class TestCreateClassRecord:
    """create_class_record"""

    def test_create_ok(self):
        """创建一条班级记录（需先有班级）"""
        create_class(cls=CreateClass(name="测试班"))
        result = create_class_record(
            record=CreateClassRecord(uid="u001000000", role=Role.Student, class_id=1)
        )
        assert result is None

    def test_create_multiple_records_same_user(self):
        """同一用户可属于多个班级"""
        create_class(cls=CreateClass(name="A班"))
        create_class(cls=CreateClass(name="B班"))
        r1 = create_class_record(
            record=CreateClassRecord(uid="u001000000", role=Role.Student, class_id=1)
        )
        r2 = create_class_record(
            record=CreateClassRecord(uid="u001000000", role=Role.Student, class_id=2)
        )
        assert r1 is None
        assert r2 is None

    def test_create_duplicate(self):
        """重复 (uid, class_id) 组合应抛出 AlreadyExistsError。"""
        create_class(cls=CreateClass(name="测试班"))
        create_class_record(
            record=CreateClassRecord(uid="u001000000", role=Role.Student, class_id=1)
        )
        with pytest.raises(AlreadyExistsError):
            create_class_record(
                record=CreateClassRecord(
                    uid="u001000000", role=Role.Student, class_id=1
                )
            )

    def test_create_teacher_record(self):
        """教师也可被关联到班级"""
        create_class(cls=CreateClass(name="教师班"))
        result = create_class_record(
            record=CreateClassRecord(uid="t001000000", role=Role.Teacher, class_id=1)
        )
        assert result is None


class TestReadClassRecord:
    """get_class_record"""

    def test_get_by_uid(self):
        """按 uid 查询某用户的所有班级记录"""
        create_class(cls=CreateClass(name="A班"))
        create_class(cls=CreateClass(name="B班"))
        create_class_record(
            record=CreateClassRecord(uid="u001000000", role=Role.Student, class_id=1)
        )
        create_class_record(
            record=CreateClassRecord(uid="u001000000", role=Role.Student, class_id=2)
        )
        create_class_record(
            record=CreateClassRecord(uid="u002000000", role=Role.Student, class_id=1)
        )

        records = get_class_record(uid="u001000000")
        assert len(records) == 2
        assert all(r.uid == "u001000000" for r in records)

    def test_get_by_uid_empty(self):
        """按 uid 查询无记录的用户，返回空列表"""
        records = get_class_record(uid="nobody")
        assert isinstance(records, list)
        assert len(records) == 0

    def test_get_by_role(self):
        """按 role 查询"""
        create_class(cls=CreateClass(name="班"))
        create_class_record(
            record=CreateClassRecord(uid="t001000000", role=Role.Teacher, class_id=1)
        )
        create_class_record(
            record=CreateClassRecord(uid="s001000000", role=Role.Student, class_id=1)
        )
        create_class_record(
            record=CreateClassRecord(uid="s002000000", role=Role.Student, class_id=1)
        )

        teachers = get_class_record(role=Role.Teacher)
        students = get_class_record(role=Role.Student)

        assert len(teachers) == 1
        assert teachers[0].uid == "t001000000"
        assert len(students) == 2

    def test_get_by_class_id(self):
        """按 class_id 查询班级内所有成员"""
        create_class(cls=CreateClass(name="A班"))
        create_class(cls=CreateClass(name="B班"))
        create_class_record(
            record=CreateClassRecord(uid="s001000000", role=Role.Student, class_id=1)
        )
        create_class_record(
            record=CreateClassRecord(uid="s002000000", role=Role.Student, class_id=1)
        )
        create_class_record(
            record=CreateClassRecord(uid="s003000000", role=Role.Student, class_id=2)
        )

        class1 = get_class_record(class_id=1)
        class2 = get_class_record(class_id=2)

        assert len(class1) == 2
        assert len(class2) == 1

    def test_get_by_status(self):
        """按 status 过滤记录"""
        create_class(cls=CreateClass(name="班"))
        create_class_record(
            record=CreateClassRecord(
                uid="ok00000000",
                role=Role.Student,
                class_id=1,
                status=ClassRecordStatus.OK,
            )
        )
        create_class_record(
            record=CreateClassRecord(
                uid="del0000000",
                role=Role.Student,
                class_id=1,
                status=ClassRecordStatus.Deleted,
            )
        )

        ok = get_class_record(status=ClassRecordStatus.OK)
        deleted = get_class_record(status=ClassRecordStatus.Deleted)

        assert len(ok) == 1
        assert ok[0].uid == "ok00000000"
        assert len(deleted) == 1
        assert deleted[0].uid == "del0000000"


class TestUpdateClassRecord:
    """update_class_record"""

    def test_update_all_fields(self):
        """更新 class_record 所有可更新字段"""
        create_class(cls=CreateClass(name="A班"))
        create_class(cls=CreateClass(name="B班"))
        create_class_record(
            record=CreateClassRecord(uid="u001000000", role=Role.Student, class_id=1)
        )

        result = update_class_record(
            id=1,
            data=UpdateClassRecord(
                uid="u002000000",
                role=Role.Teacher,
                class_id=2,
                status=ClassRecordStatus.Deleted,
            ),
        )
        assert result is None

        records = get_class_record(status=ClassRecordStatus.Deleted)
        assert len(records) == 1
        r = records[0]
        assert r.uid == "u002000000"
        assert r.role == Role.Teacher
        assert r.class_id == 2

    def test_update_partial(self):
        """仅更新部分字段"""
        create_class(cls=CreateClass(name="A班"))
        create_class_record(
            record=CreateClassRecord(uid="u001000000", role=Role.Student, class_id=1)
        )

        result = update_class_record(id=1, data=UpdateClassRecord(role=Role.Teacher))
        assert result is None

        records = get_class_record(uid="u001000000")
        assert len(records) == 1
        assert records[0].role == Role.Teacher
        assert records[0].class_id == 1  # 未变

    def test_update_not_found(self):
        """更新不存在的记录应抛出 NotFoundError。"""
        with pytest.raises(NotFoundError):
            update_class_record(
                id=9999, data=UpdateClassRecord(status=ClassRecordStatus.Deleted)
            )


class TestExternalSession:
    def test_create_read_update_with_shared_session(self):
        with db.get_session() as ss:
            create_result = create_user(
                usr=CreateUser(
                    uid="tx00100000",
                    password="password1",
                    name="事务测试",
                    role=Role.Student,
                    gender=Gender.Male,
                    college="信息学院",
                ),
                ss=ss,
            )
            update_result = update_user(
                uid="tx00100000", data=UpdateUser(name="事务内更新"), ss=ss
            )
            user = get_user_by_uid(uid="tx00100000", ss=ss)

            assert create_result is None
            assert update_result is None
            assert user is not None
            assert user.name == "事务内更新"  # type: ignore[union-attr]

            ss.commit()

        user = get_user_by_uid(uid="tx00100000")
        assert user is not None
        assert user.name == "事务内更新"  # type: ignore[union-attr]

    def test_external_session_rollback_discards_changes(self):
        with db.get_session() as ss:
            result = create_user(
                usr=CreateUser(
                    uid="rback00001",
                    password="password1",
                    name="回滚测试",
                    role=Role.Student,
                    gender=Gender.Female,
                    college="信息学院",
                ),
                ss=ss,
            )
            assert result is None
            assert get_user_by_uid(uid="rback00001", ss=ss) is not None

            ss.rollback()

        assert get_user_by_uid(uid="rback00001") is None
