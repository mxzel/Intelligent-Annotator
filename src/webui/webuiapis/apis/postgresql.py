

#conn = psycopg2.connect(database="testdb", user="postgres", password="pass123", host="127.0.0.1", port="5432")

#print "Opened database successfully"

import psycopg2

conn = psycopg2.connect(database="Intelligent-Annotator", user="postgres", password="pass123", host="127.0.0.1", port="5432")
print "Opened database successfully"

cur = conn.cursor()
cur.execute('''CREATE TABLE public."Dataset"
(
    did integer NOT NULL,
    dataset_name "char" NOT NULL,
    uid integer NOT NULL,
    creat_timestamp timestamp without time zone NOT NULL,
    CONSTRAINT "Dataset_pkey" PRIMARY KEY (did)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."Dataset"
    OWNER to postgres;
COMMENT ON TABLE public."Dataset"
    IS '数据集表';''')
print "Table Dataset created successfully"

cur.execute('''CREATE TABLE public."LabeledData"
(
    lid integer NOT NULL,
    dataset_did integer NOT NULL,
    text "char" NOT NULL,
    label "char",
    "timestamp" time without time zone,
    CONSTRAINT "LabeledData_pkey" PRIMARY KEY (lid)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."LabeledData"
    OWNER to postgres;
COMMENT ON TABLE public."LabeledData"
    IS '标注后的数据';''')
print "Table LabeledData created successfully"

cur.execute('''CREATE TABLE public."RowData"
(
    rid integer NOT NULL,
    text "char" NOT NULL,
    dataset_did integer NOT NULL,
    labeled boolean NOT NULL,
    CONSTRAINT "RowData_pkey" PRIMARY KEY (rid)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."RowData"
    OWNER to postgres;
COMMENT ON TABLE public."RowData"
    IS '未标注数据';''')
print "Table RowData created successfully"

cur.execute('''CREATE TABLE public."User"
(
    name "char"[] NOT NULL,
    uid integer NOT NULL,
    CONSTRAINT "User_pkey" PRIMARY KEY (uid)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."User"
    OWNER to postgres;
COMMENT ON TABLE public."User"
    IS '用户表';''')
print "Table user created successfully"

cur.execute('''CREATE TABLE public.train_status
(
    uid integer NOT NULL,
    dataset_did integer NOT NULL,
    model_name "char" NOT NULL,
    is_full_train boolean NOT NULL,
    status integer NOT NULL,
    start_timestamp time without time zone NOT NULL,
    end_timestamp time without time zone NOT NULL,
    CONSTRAINT train_status_pkey PRIMARY KEY (dataset_did)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.train_status
    OWNER to postgres;
COMMENT ON TABLE public.train_status
    IS '训练状态';''')
print "Table train_satus created successfully"

conn.commit()
conn.close()