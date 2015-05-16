#!/bin/bash

export PGPASSWORD="postgres"
echo "Inicio: Actualizacion de estado de Sprint"
psql -c "update sprint_sprint set estado='Finalizado' where fechafin <current_date" -d is2 -U postgres
echo "Fin: Actualizacion de estado de Sprint"

echo "Inicio: Actualizacion de estado de Flujo en la tabla flujoProyecto"
psql -c "update proyecto_flujoproyecto set estado='HalfDone' from sprint_sprint
where proyecto_flujoproyecto.sprint_id = sprint_sprint.id and sprint_sprint.estado='Finalizado' and proyecto_flujoproyecto.estado not ilike 'Done' and proyecto_flujoproyecto.estado not ilike 'Inactivo'" -d is2 -U postgres
echo "Fin: Actualizacion de estado de Flujo en la tabla flujoProyecto"


echo "Inicio: Actualizacion del estado de los US de los sprints que no se finalizaron, estos US deben asignarse al sgte Sprint"
psql -c "update userstory_userstory set estado = 'Incompleto'
where userstory_userstory.estado not ilike 'Validado' and
userstory_userstory.sprint_id in (select proyecto_flujoproyecto.sprint_id
	from proyecto_flujoproyecto
	where estado='HalfDone')" -d is2 -U postgres
echo "Fin: Actualizacion del estado de los US de los sprints que no se finalizaron, estos US deben asignarse al sgte Sprint"