with filtered_clients as (
    select id_favor from client_favor
		where serial_number = (%s) and date_disconnect is null
)
select fc.id_favor, name_favor, cost_favor from favor
join filtered_clients as fc on favor.id_favor = fc.id_favor