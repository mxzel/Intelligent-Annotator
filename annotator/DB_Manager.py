from abc import abstractmethod
import psycopg2


class DB_Manager(object):
    table_name = None

    def __init__(self, dbname="django-annotator", user="django-annotator", password="django-annotator"):
        self._dbname = dbname
        self._user = user
        self._password = password
        self._conn = None
        self._cur = None

    def _connect(self):
        """
        连接数据库
        :return: None
        """
        para = "dbname=" + self._dbname \
               + " user=" + self._user \
               + " password=" + self._password
        print(para)
        self._conn = psycopg2.connect(para)
        self._cur = self._conn.cursor()

    def _close_connection(self):
        """
        关闭数据库连接
        :return: None
        """
        self._cur.close()
        self._conn.close()

    def commit(self):
        """
        commit
        :return: None
        """
        return self._conn.commit()

    def rollback(self):
        return self._conn.rollback()

    def _execute(self, *args, **kwargs):
        """
        执行操作
        :param args:
        :param kwargs:
        :return: None
        """
        self._cur.execute(*args, **kwargs)
        try:
            ret = self._cur.fetchone()
        except psycopg2.ProgrammingError:
            ret = None
        return ret

    def fetchone(self):
        """
        获取查询结果中的一条记录
        :return: 查询结果中的一条记录
        """
        return self._cur.fetchone()

    def fetchall(self):
        """
        获取查询结果中的所有记录
        :return: 查询结果中的所有记录
        """
        return self._cur.fetchall()

    @abstractmethod
    def create(self):
        """
        创建数据表
        :return: None
        """
        pass

    @abstractmethod
    def insert(self):
        """
        向数据表中插入记录
        :return: None
        """
        pass

    def delete(self, condition=''):
        """
        删除满足条件的记录
        :param condition: 删除条件
        :return: None
        """
        self._connect()
        sql = "delect from " + self.table_name
        sql = sql + " where " + condition + ";" if not condition == '' else sql + ";"
        self._execute(sql)
        self.commit()
        self._close_connection()

    def update(self, ret, condition):
        """
        更新数据库记录
        :param ret: 更新结果
        :param condition: 更新条件
        :return: None
        """
        self._connect()
        sql = "update " + self.table_name + " set " + ret + " where " + condition + ";"
        self._execute(sql)
        self.commit()
        self._close_connection()

    def select(self, columns='*', condition='', num=-1, additional_tables=''):
        """
        选择满足条件的记录
        :param columns: 要选择的列
        :param condition: 选择条件
        :param num: 返回数量
        :param additional_tables: 额外的表
        :return: 一定数量的选择结果
        """
        self._connect()
        if additional_tables == '':
            sql = "select " + columns + " from " + self.table_name
        else:
            sql = "SELECT " + columns + " FROM " + self.table_name + ", " + additional_tables
        sql = sql + " WHERE " + condition + ";" if not condition == '' else sql + ";"
        ret = self._execute(sql)
        ret = [] if ret is None else [ret]
        self.commit()
        ret.extend(self.fetchall())
        self._execute(sql)
        self.commit()

        self._close_connection()
        print(11141)
        #num = ret.__len__() if num > ret.__len__() else num
        print(num)
        return ret #if num == -1 else ret[:num]

    def drop(self):
        """
        删除数据表
        :return: None
        """
        self._connect()
        sql = 'DROP TABLE IF EXISTS ' + self.table_name + ';'
        self._cur.execute(sql)
        self.commit()
        self._close_connection()


class Labeled_DB_Manager(DB_Manager):
    table_name = "labeled_data"

    labeled_id = "labeled_id"
    unlabeled_id = "unlabeled_id"
    file_id = "file_id"
    data_content = "data_content"
    labeled_time = "labeled_time"
    labeled_content = "labeled_content"
    predicted_relation = "predicted_relation"
    predicted_e1 = "predicted_e1"
    predicted_e2 = "predicted_e2"
    labeled_relation = "labeled_relation"
    labeled_e1 = "labeled_e1"
    labeled_e2 = "labeled_e2"
    additional_info = "additional_info"

    def create(self):
        """
        创建已标注数据表
        :return: None
        """
        self._connect()
        sql = "CREATE TABLE " + self.table_name + " ( \
                        labeled_id serial PRIMARY KEY, \
                        unlabeled_id int NOT NULL, \
                        file_id int REFERENCES file_info(file_id), \
                        data_content text NOT NULL, \
                        labeled_time timestamp, \
                        labeled_content text, \
                        predicted_relation text, \
                        predicted_e1 text, \
                        predicted_e2 text, \
                        labeled_relation text, \
                        labeled_e1 text, \
                        labeled_e2 text, \
                        additional_info text \
                );"
        self._cur.execute(sql)
        self.commit()
        self._close_connection()

    def insert(self, unlabeled_id=-1, data_content='', file_id='',
               labeled_time='', labeled_content='',
               predicted_relation='', predicted_e1='', predicted_e2='',
               labeled_relation='', labeled_e1='', labeled_e2='',
               additional_info=''):
        """
        向已标注数据表中插入记录
        :param unlabeled_id: 数据的 id
        :param data_content: 数据内容
        :param file_id: 文件 id
        :param labeled_time: 标注时间
        :param labeled_content: 标注后的数据内容
        :param predicted_relation: 预测关系
        :param predicted_e1: 预测实体1
        :param predicted_e2: 预测实体2
        :param labeled_relation: 标注关系
        :param labeled_e1: 标注实体1
        :param labeled_e2: 标注实体2
        :param additional_info: 对关系预测有帮助的附加信息
        :return: None
        """
        self._connect()
        sql = "INSERT INTO " + self.table_name + " ( \
                         unlabeled_id, data_content, file_id, labeled_time, \
                         labeled_content, predicted_relation, predicted_e1, predicted_e2,\
                         labeled_relation, labeled_e1, labeled_e2, additional_info) \
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
                         RETURNING labeled_id;"
        ret = self._execute(sql, (unlabeled_id, data_content, file_id, labeled_time,
                                  labeled_content, predicted_relation, predicted_e1, predicted_e2,
                                  labeled_relation, labeled_e1, labeled_e2, additional_info))
        self.commit()
        self._close_connection()
        return ret


class Unlabeled_DB_Manager(DB_Manager):
    table_name = "unlabeled_data"

    unlabeled_id = "unlabeled_id"
    file_id = "file_id"
    data_content = "data_content"
    upload_time = "upload_time"

    def create(self):
        """
        创建未标注数据表
        :return: None
        """
        self._connect()
        sql = "CREATE TABLE " + self.table_name + " ( \
                        unlabeled_id serial PRIMARY KEY, \
                        file_id integer REFERENCES file_info (file_id), \
                        data_content text NOT NULL, \
                        upload_time timestamp);"
        self._execute(sql)
        self.commit()
        self._close_connection()

    def insert(self, file_id='', data_content='', upload_time=''):
        """
        向未标注数据表中插入记录
        :param file_id: 文件 id
        :param data_content: 数据内容
        :param upload_time: 上传时间
        :return: None
        """
        self._connect()
        sql = "INSERT INTO " + self.table_name + " ( \
                        file_id, data_content, upload_time) \
                        VALUES (%s, %s, %s) returning unlabeled_id;"
        ret = self._execute(sql, (file_id, data_content, upload_time))
        self.commit()
        self._close_connection()
        return ret


class File_info_DB_Manager(DB_Manager):
    table_name = "file_info"

    file_id = "file_id"
    file_name = "file_name"
    project_id = "project_id"

    def create(self):
        """
        创建文件信息表
        :return: None
        """
        self._connect()
        sql = "CREATE TABLE " + self.table_name + " ( \
                        file_id serial PRIMARY KEY, \
                        file_name text, \
                        project_id integer REFERENCES project_info (project_id));"
        self._execute(sql)
        self.commit()
        self._close_connection()

    def insert(self, project_id='', file_name=''):
        """
        向文件信息表中插入记录
        :param project_id: 项目 id
        :param file_name: 文件名字
        :return: None
        """
        self._connect()
        sql = "INSERT INTO " + self.table_name + " ( \
                        project_id, file_name) \
                        VALUES (%s, %s) RETURNING file_id;"
        ret = self._execute(sql, (project_id, file_name))
        self.commit()
        self._close_connection()
        return ret


class Project_info_DB_Manager(DB_Manager):
    table_name = "project_info"

    project_id = "project_id"
    project_name = "project_name"

    def create(self):
        """
        创建项目信息表
        :return: None
        """
        self._connect()
        sql = "CREATE TABLE " + self.table_name + " ( \
                        project_id serial PRIMARY KEY, \
                        project_name text NOT NULL);"
        self._execute(sql)
        self.commit()
        self._close_connection()

    def insert(self, project_name=''):
        """
        向项目信息表中插入记录
        :param project_name: 项目 名字
        :return: None
        """
        self._connect()
        sql = "INSERT INTO " + self.table_name + " ( \
                        project_name) \
                        VALUES (%s) \
                        RETURNING project_id;"
        # print(sql)
        ret = self._execute(sql, (project_name,))
        self.commit()
        self._close_connection()
        return ret


def test_file_info_db():
    db = File_info_DB_Manager()

    try:
        db.drop()
    except psycopg2.InternalError:
        pass

    try:
        db.create()
    except psycopg2.ProgrammingError:
        print('数据库已存在')
    else:
        print('数据库创建成功')


def test_project_info_db():
    """
    项目信息数据库 测试
    :return: None
    """
    db = Labeled_DB_Manager()
    # db.drop()
    db = Unlabeled_DB_Manager()
    # db.drop()
    db = Project_info_DB_Manager()

    try:
        db.drop()
    except psycopg2.InternalError:
        pass

    # 创建数据表
    # db.create()
    try:
        db.create()
    except psycopg2.ProgrammingError:
        print('数据库已存在')
    else:
        print('数据库创建成功')

    # 删除数据表中的所有记录
    db.delete()
    db.insert(project_name='shit')

    # 向数据表中添加两条记录
    ret = db.insert(project_name="name")
    print(ret)
    records = db.select()
    print(records)
    assert False
    ret = db.insert(project_name="name")
    print(ret)
    records = db.select()
    print(records)
    ret = db.insert(project_name="test")
    print(ret)
    records = db.select()
    print(records)

    # 更新数据记录
    db.update(ret="project_name='file'", condition="project_name='name'")
    records = db.select(condition="project_name='file'")
    print(records)

    # 删除某条记录
    db.delete(condition="project_id='2' AND project_name='file'")
    records = db.select()
    print(records)


def test_unlabeled_db():
    """
    未标注数据库 测试
    :return: None
    """
    db = Unlabeled_DB_Manager()

    db.drop()

    # 创建数据表
    db.create()
    """
    try:
        db.create()
    except psycopg2.ProgrammingError:
        print('数据库已存在')
    else:
        print('数据库创建成功')
    """

    # 删除数据表中的所有记录
    db.delete()

    # 向数据表中添加两条记录
    db.insert(project_id='4', data_content='content', upload_time='2015-08-08')
    db.insert(project_id='4', data_content='特朗普', upload_time='2016-06-07')
    records = db.select()
    print(records)

    # 更新数据记录
    db.update(ret="data_content='test'", condition="data_content='content'")
    records = db.select(condition="data_content='test'")
    print(records)

    # 删除某条记录
    db.delete(condition="data_content='特朗普'")
    records = db.select(condition="data_content='特朗普'")
    print(records)


def test_labeled_db():
    """
    已标注数据库 测试
    :return: None
    """
    db = Labeled_DB_Manager()

    db.drop()

    # 创建数据表
    try:
        db.create()
    except psycopg2.ProgrammingError:
        print('数据库已存在')
    else:
        print('数据库创建成功')

    # 删除数据表中的所有记录
    db.delete()

    # 向数据表中添加两条记录
    db.insert(unlabeled_id=1, data_content="特朗普是奥巴马的儿子", project_id='4',
              labeled_time="2016-01-01", entity1="奥巴马",
              entity2="特朗普", predicted_relation="儿子", labeled_relation="爸爸")
    db.insert(unlabeled_id=2, data_content="金正恩又名金三胖", project_id='4',
              labeled_time="2014-06-06", entity1="金正恩",
              entity2="金三胖", predicted_relation="又名", labeled_relation="又名")
    records = db.select()
    print(records)

    # 更新数据表记录
    db.update(ret="labeled_time='1970-01-01', entity1='不是奥巴马'", condition="unlabeled_id=1")
    records = db.select()
    print(records)

    # 删除数据表记录
    db.delete(condition="entity1='奥巴马' OR entity1='金正恩'")
    records = db.select()
    print(records)


if __name__ == '__main__':
    # test_project_info_db()
    # test_file_info_db()
    print()
    db = Labeled_DB_Manager()
    db.select()
    # print()
    # print()
    # test_unlabeled_db()
    # print()
    test_labeled_db()
