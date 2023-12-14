# Create metadata tables
sql_create_run_metadata_table = """
        CREATE TABLE IF NOT EXISTS run_metadata_table (
        id text PRIMARY_KEY,
        type text NOT NULL,
        arguments text NOT NULL,
        start_time INTEGER NOT NULL,
        end_time INTEGER NOT NULL,
        duration INTEGER NOT NULL,
        db_file text NOT NULL,
        filepath text NOT NULL,
        recipes text,
        cookbooks text,
        endpoints text NOT NULL,
        num_of_prompts INTEGER NOT NULL,
        results text NOT NULL
        );
"""

sql_create_chat_metadata_table = """
        CREATE TABLE IF NOT EXISTS chat_metadata_table (
        id text PRIMARY KEY,
        endpoint text NOT NULL,
        created_epoch INTEGER NOT NULL,
        created_datetime text NOT NULL,
        context_strategy int,
        prompt_template text
        );
"""

# Create cache and chat history tables
sql_create_cache_table = """
        CREATE TABLE IF NOT EXISTS cache_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        endpoint text NOT NULL,
        recipe text NOT NULL,
        prompt_template text NOT NULL,
        prompt text NOT NULL,
        target text NOT NULL,
        predicted_result text NOT NULL,
        duration text NOT NULL
        );
"""

sql_create_chat_history_table = """
        CREATE TABLE IF NOT EXISTS chat_history_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        connection_id text NOT NULL,
        context_strategy int,
        prompt_template text,
        prompt text NOT NULL,
        prepared_prompt text NOT NULL,
        predicted_result text NOT NULL,
        duration text NOT NULL
        );
"""

# Run metadata records
sql_create_run_metadata_records = """
        INSERT INTO run_metadata_table (
        id,type,arguments,start_time,end_time,duration,db_file,filepath,recipes,cookbooks,endpoints,
        num_of_prompts,results)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
"""

sql_update_run_metadata_records = """
        UPDATE run_metadata_table SET end_time=?,duration=?,results=? WHERE id=?
"""

sql_read_run_metadata_records = """
        SELECT * from run_metadata_table WHERE id=?
"""

# Chat metadata records
sql_create_chat_metadata_records = """
        INSERT INTO chat_metadata_table (
        id,endpoint,created_epoch,created_datetime,context_strategy,prompt_template)
        VALUES(?,?,?,?,?,?)
"""

sql_update_chat_metadata_records = """
        UPDATE chat_metadata_table SET context_strategy=?, prompt_template=? WHERE id=?
"""

sql_read_chat_metadata_records = """
        SELECT * from chat_metadata_table WHERE id=?
"""

# Cache records
sql_create_cache_records = """
        INSERT INTO cache_table(endpoint,recipe,prompt_template,prompt,target,predicted_result,
        duration)VALUES(?,?,?,?,?,?,?)
"""

sql_read_cache_records = """
        SELECT * from cache_table WHERE recipe=? AND endpoint=?
"""

# Chat history records
sql_create_chat_history_records = """
        INSERT INTO chat_history_table(connection_id,context_strategy,prompt_template,prompt,
        prepared_prompt,predicted_result,duration)VALUES(?,?,?,?,?,?,?)
"""

sql_read_chat_history_records = """
        SELECT * from chat_history_table order by id desc limit ?
"""
