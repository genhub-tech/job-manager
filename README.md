# Job Manager

Este es un sistema de gestión de trabajos que permite añadir, consultar y ejecutar trabajos en cola con soporte para prioridades.

## Archivos

- `job_manager.py`: Script principal para gestionar los trabajos.
- `run_jobs.sh`: Script para ejecutar `job_manager.py run` en segundo plano.
- `job_queue.txt`: Archivo que almacena la lista de trabajos en cola.

## Uso

### Añadir un Trabajo

```
python3 job_manager.py add "<comando>" [prioridad]
```

### Consultar el Estado de un Trabajo

```
python3 job_manager.py status <ID_trabajo>
```

### Ejecutar los Trabajos en Cola

```
./run_jobs.sh
```

