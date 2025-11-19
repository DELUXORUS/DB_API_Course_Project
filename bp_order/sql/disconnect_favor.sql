update client_favor
set date_disconnect = curdate()
where id_favor = (%s) and date_disconnect is null
