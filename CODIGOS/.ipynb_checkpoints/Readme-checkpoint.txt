============= Análisis de datos de precipitación y temperatura =============

[NOMBRE]: Análisis de datos de precipitación y temperatura

[VERSION]: 1.0

[LISTA DE ARCHIVOS]:
- Datos de ejemplo:
  * DATA_ANALISIS/DATOS

- Graficas
  * BOXPLOT.py:  Grafica boxplots para todos los meses deacuerdo a los datos históricos. Precipitación: Total mes, Temperatura: promedio mes
  * BXP_COMPARACION.py:     Grafica boxplots con datos mensuales comparando los datos llenados y los originales
  * CURVAS_DOBLE_MASA.py:     Grafica la curva de doble masa para precipitación con la acumulación mensual
  * GRAFICAR_CORRELACION.py:      Grafica la correlación entre los valores de las estaciones de medición
  * GRAFICAR_DATOS_FALTANTES.py:   Grafica los datos faltantes por estacion
  * MENSUAL_MULTIANUAL.py:     Calcula los valores mensuales medios multianuales
  * PRUEBA_HOMOGENEIDAD.py:    Evalua la homogeneidad de los datos utilizando el test pettitt 

- Preparación de datos
  * DATA_COMPLETA.py:   Completa las fechas faltantes. Asigna Nan a los días sin datos disponibles
  * DATA_LLENADO.py:    Completa datos faltantes con el método IDW
  * CORRECCION_DATA.py: Corrije los datos anomalos resultantes de DATA_COMPLETA.py

- Datos resultantes de la preparación de datos (manejo de datos ejemplo)
  * DATA_ANALISIS/PRE_SALIDAS/DATA_COMPLETA   CSVs con todas las fechas del periodo a evaluar. Las fechas sin datos corresponden a Nan
  * DATA_ANALISIS/PRE_SALIDAS/DATA_LLENADO    CSVs con todas las fechas del periodo a evaluar. Para los datos faltantes se utiliza el método IDW

- Modulo principal
  * MAIN.py  En este módulo se corren todos los códigos

=================================== FIN ========================================