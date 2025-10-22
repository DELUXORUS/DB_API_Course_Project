select max(cost_favor) from favor
    where LOCATE(%s, name_favor) = 1
