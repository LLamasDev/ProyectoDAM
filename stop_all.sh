#!/bin/bash

function funcion() {
  { # try
    /bot/ProyectoDAM/stop.sh 'resultadosfutbol'
    echo ''
    /bot/ProyectoDAM/stop.sh 'supercell'
    echo ''
    /bot/ProyectoDAM/stop.sh 'clashroyale'
    echo''
    /bot/ProyectoDAM/stop.sh 'clashofclans'
    echo''
    sleep 10 # Paramos 10 segundos para esperar la parada del proceso

    proceso=$(ps -ef | grep -i "resultadosfutbol\|supercell\|clashroyale\|clashofclans" | grep -iv "screen\|grep\|networkd" | wc -l) # Contador para saber si esta corriendo

    if [ $proceso -eq 0 ]; then # Si el contador del proceso es 0 significa que no estan corriendo los procesos
      echo 'Parado todos los procesos correctamente.'
    else # El contador de procesos no es 0 significa que no han parado todos los procesos
      echo "No se ha parado todos los procesos correctamente."
    fi
  } || { # catch
    echo 'Error al arrancar los procesos.'
  }
}

funcion
