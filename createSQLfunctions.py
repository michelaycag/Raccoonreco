import psycopg2

def initDB():
    try:
        con = psycopg2.connect(
            host="postgres",
            port=5432,
            database='postgres',
            user='postgres',
            password='OpenCV'
        )
    except:
        print('connection failed!')
        con = None

    cur = con.cursor()

    cur.execute("""
    CREATE OR REPLACE FUNCTION public.vec_sub(arr1 double precision[], arr2 double precision[])
    RETURNS double precision[]
    LANGUAGE sql
    STRICT
    AS $function$	
    SELECT array_agg (result)
        FROM (SELECT (tuple.val1 - tuple.val2) * (tuple.val1 - tuple.val2)
            AS result
            FROM (SELECT UNNEST ($1) AS val1
                , UNNEST ($2) AS val2
                , generate_subscripts ($1, 1) AS ix) tuple
        ORDER BY ix) inn;
        
        $function$

    """)
    cur.execute('''
    CREATE OR REPLACE FUNCTION public.euclidian(arr1 double precision[], arr2 double precision[])
    RETURNS double precision
    LANGUAGE sql
    AS $function$
    select sqrt (SUM (tab.v)) as euclidian from (SELECT
        UNNEST (vec_sub (arr1, arr2)) as v) as tab;
        $function$

    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS public.partners
    (
        id serial NOT NULL,
        name character varying(100) NOT NULL,
        partnerId integer NOT NULL UNIQUE,
        document character varying(100) NOT NULL,
        authorized boolean NOT NULL,
        contactNumber character varying(100) NOT NULL,
        PRIMARY KEY (id)
    );
    '''
                )

    cur.execute('''
    CREATE TABLE IF NOT EXISTS public.users
    (
        id serial NOT NULL,
        name character varying(100) NOT NULL,
        email character varying(100) NOT NULL UNIQUE,
        password TEXT NOT NULL,
        rol character varying(100) NOT NULL,
        PRIMARY KEY (id)
    );
    '''
                )

    cur.execute('''
    CREATE TABLE IF NOT EXISTS public.face_table
    (
        id serial NOT NULL,
        name character varying(100) NOT NULL,
        face_embedding double precision[] NOT NULL,
        partnerId integer NOT NULL,
        CONSTRAINT fk_partner_id FOREIGN KEY(partnerId) REFERENCES partners (id) ON DELETE CASCADE,
        PRIMARY KEY (id)
    );
    '''
                )

    con.commit()
