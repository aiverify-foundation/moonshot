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

# ------------------------------------------------------------------------------
# SQL Queries for Red Teaming
# ------------------------------------------------------------------------------
sql_create_session_metadata_table = """
        CREATE TABLE IF NOT EXISTS session_metadata_table (
        session_id text PRIMARY KEY NOT NULL,
        name text NOT NULL,
        description text NOT NULL,
        endpoints text NOT NULL,
        created_epoch INTEGER NOT NULL,
        created_datetime text NOT NULL,
        context_strategy text,
        prompt_template text,
        chat_ids text
        );
"""

sql_create_session_metadata_record = """
    INSERT INTO session_metadata_table (
    session_id,name,description,endpoints,created_epoch,created_datetime,context_strategy,prompt_template)
    VALUES(?,?,?,?,?,?,?,?)
"""

sql_create_chat_metadata_table = """
        CREATE TABLE IF NOT EXISTS chat_metadata_table (
        chat_id text PRIMARY KEY,
        endpoint text NOT NULL,
        created_epoch INTEGER NOT NULL,
        created_datetime text NOT NULL
        );
"""

sql_create_chat_metadata_record = """
        INSERT INTO chat_metadata_table (
        chat_id,endpoint,created_epoch,created_datetime)
        VALUES(?,?,?,?)
"""

sql_update_session_metadata_chat = """
        UPDATE session_metadata_table SET chat_ids=? WHERE session_id=?
"""

sql_read_session_metadata = """
        SELECT * from session_metadata_table
"""

sql_read_session_chat_metadata = """
        SELECT * from chat_metadata_table
"""

sql_update_context_strategy = """
        UPDATE session_metadata_table SET context_strategy=? WHERE session_id =?
"""

sql_update_prompt_template = """
        UPDATE session_metadata_table SET prompt_template=? WHERE session_id =?
"""
