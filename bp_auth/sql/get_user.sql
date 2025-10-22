select id, role from (
select in_id as id, login, password, role from internal_user
union
select ex_id as id, login, password, role from external_user
) as result
    where login = (%s) and password = (%s)