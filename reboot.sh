#!/bin/bash

primer_ag=$1 # Primer argumento

function funcion() {
  { # try
    ./stop.sh "$primer_ag"
    ./start.sh "$primer_ag"
    echo ''
    sleep 10 # Paramos 10 segundos para esperar el arranque del proceso

    proceso=$(ps -ef | grep -i $primer_ag.py | grep -iv "screen\|grep\|networkd" | wc -l) # Contador para saber si esta corriendo

    if [ $proceso -eq 1 ]; then # Si el contador del proceso es 1 significa que se ha reiniciado
      echo "Se ha reiniciado $primer_ag correctamente."
    else # El contador de procesos no es 3 significa que no esta corriendo
      echo "No se ha reiniciado $primer_ag correctamente."
    fi
  } || { # catch
    echo "Error al reiniciar el proceso $primer_ag."
  }
}

funcion
