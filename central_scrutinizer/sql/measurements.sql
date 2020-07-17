select s.source, v.unit,
       v.variable as variable_name, 
       v.description as variable_desc,
       l.location_name, lt.location_type, m.value,
       m.collected_on, e.medium
from   measurement m, medium e, location l, 
       location_type lt, variable v, source s
where  m.medium_id=e.medium_id
and    m.variable_id=v.variable_id
and    m.location_id=l.location_id
and    l.location_type_id=lt.location_type_id
and    v.source_id=s.source_id
