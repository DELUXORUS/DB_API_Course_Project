select * from client
            where datediff(current_date, date_start_contract) <= (%s)