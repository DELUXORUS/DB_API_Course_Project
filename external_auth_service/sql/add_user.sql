insert into client(serial_number, who_issued, date_issued, name, birthday, residence_address, date_start_contract, login, password)
values(%s, %s, %s, %s, %s, %s, curdate(), %s, %s)