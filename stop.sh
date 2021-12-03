#!/bin/bash

primer_ag=$1 # Primer argumento

function funcion() {
  { # try
    proceso=$(ps -ef | grep -i $primer_ag.py | grep -iv "screen\|grep\|networkd" | wc -l) # Contador para saber si esta corriendo

    if [ $proceso -eq 1 ]; then # Si el contador del proceso es 1 significa que esta corriendo
      pid=$(ps -ef | grep -i $primer_ag.py | grep -iv "screen\|grep\|networkd" | awk '{print $2}') # Saco el pid del proceso
      matar_pid=$(kill -9 $pid) # Mato el pid
      screen_id=$(screen -ls | grep -i $primer_ag | cut -d'.' -f1) # Saco el id del screen
      matar_screen=$(screen -XS $screen_id quit) # Mato el screen del proceso
      confirmacion=$(ps -ef | grep -i $primer_ag.py | grep -iv "screen\|grep\|networkd" | wc -l) # Verifico que esté parado

      if [ $confirmacion -eq 0 ]; then # Si el contador del proceso es 0 significa que se paró correctamente
        echo "El proceso $primer_ag se ha parado correctamente."
      else # No se paro el proceso correctamente
        echo "No se pudo parar el proceso $primer_ag."
      fi
    else # El proceso no es 1 significa que no esta corriendo, ya que solo puede estar arrancado una vez
      echo "El proceso $primer_ag no esta corriendo, saliendo de la parada."
    fi
  } || { # catch
    echo "Error al parar el proceso $primer_ag."
  }
}

funcion
