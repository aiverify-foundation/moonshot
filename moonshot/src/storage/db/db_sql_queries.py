# ------------------------------------------------------------------------------
# SQL Queries for Benchmark Metadata Information
# ------------------------------------------------------------------------------
sql_create_metadata_table = """
        CREATE TABLE IF NOT EXISTS metadata_table (
        id text PRIMARY_KEY,
        name text NOT NULL,
        type text NOT NULL,
        start_time INTEGER NOT NULL,
        end_time INTEGER NOT NULL,
        duration INTEGER NOT NULL,
        database_file text NOT NULL,
        error_messages text NOT NULL,
        results_file text NOT NULL,
        recipes text,
        cookbooks text,
        endpoints text NOT NULL,
        num_of_prompts INTEGER NOT NULL,
        results text NOT NULL,
        status text NOT NULL
        );
"""

sql_create_metadata_records = """
        INSERT INTO metadata_table (
        name,type,start_time,end_time,duration,database_file,error_messages,results_file,recipes,cookbooks,endpoints,
        num_of_prompts,results,status,id)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
"""

sql_read_metadata_records = """
        SELECT * from metadata_table WHERE id=?
"""

sql_update_metadata_records = """
        UPDATE metadata_table SET name=?,type=?,start_time=?,end_time=?,duration=?,database_file=?,error_messages=?,
        results_file=?,recipes=?,cookbooks=?,endpoints=?,num_of_prompts=?,results=?,status=? WHERE id=?
"""

# ------------------------------------------------------------------------------
# SQL Queries for Benchmark Cache Information
# ------------------------------------------------------------------------------
sql_create_cache_table = """
        CREATE TABLE IF NOT EXISTS cache_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conn_id text NOT NULL,
        rec_id text NOT NULL,
        ds_id text NOT NULL,
        pt_id text NOT NULL,
        prompt_index INTEGER NOT NULL,
        prompt text NOT NULL,
        target text NOT NULL,
        predicted_results text NOT NULL,
        duration text NOT NULL
        );
"""

sql_create_cache_records = """
        INSERT INTO cache_table(conn_id,rec_id,ds_id,pt_id,prompt_index,prompt,target,predicted_results,duration)
        VALUES(?,?,?,?,?,?,?,?,?)
"""

sql_read_cache_records = """
        SELECT * from cache_table WHERE rec_id=? AND conn_id=? AND pt_id=? AND prompt=?
"""
