select in_id as id, r.role, db_config from internal_user as iu
    join role as r on r.role = iu.role
        where login = (%s) and password = (%s)