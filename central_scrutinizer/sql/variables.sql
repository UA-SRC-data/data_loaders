select v.variable as name, v.description as "desc", v.unit, s.source
from   variable v, source s
where  v.source_id=s.source_id
