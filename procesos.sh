#!/bin/bash

primer_ag=$1 # Primer argumento

function funcion() {
  { # try
    proceso=$(ps -ef | grep -i $primer_ag.py | grep -iv "screen\|grep\|networkd" | wc -l) # Contador para saber si esta corriendo

    if [ $proceso -eq 1 ]; then # Si el contador del proceso es 1 significa que esta corriendo
      fecha_corriendo=$(ps -ef | grep -i $primer_ag.py | grep -iv "screen\|grep\|networkd" | awk '{print $5}') # Saco desde cuando esta corriendo
      echo "El proceso $primer_ag esta corriendo desde $fecha_corriendo."
    else # El proceso no es 1 significa que no esta corriendo, ya que solo puede estar arrancado una vez
      echo "El proceso $primer_ag no esta corriendo."
    fi
  } || { # catch
    echo "El proceso $primer_ag esta en estado anomalo."
  }
}

funcion
