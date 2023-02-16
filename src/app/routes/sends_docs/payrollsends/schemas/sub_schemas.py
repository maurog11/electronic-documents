from flask_restx import Namespace, fields


api = Namespace("Envios nominas", description="Operaciones relacionadas con Nominas")


FechasPagos = api.model("FechasPagos", {
    'FechaPago': fields.Date(required=True, description="Debe ir la fecha de pago del documento. Considerando zona horaria de Colombia (-5), en formato AAAA-MM-DD")
})

Periodo = api.model("Periodo", {
    'FechaIngreso': fields.Date(required=True, description="Se debe indicar la Fecha de ingreso del trabajador a la empresa, en formato AAAA-MM-DD"),
    'FechaLiquidacionInicio': fields.Date(required=True, description="Se debe indicar la Fecha de Inicio del Periodo de Liquidación del documento, en formato AAAA-MM-DD"),
    'FechaLiquidacionFin': fields.Date(required=True, description="Se debe indicar la Fecha de Fin del Periodo de Liquidación del documento, en formato AAAA-MM-DD"),
    'TiempoLaborado': fields.String(required=True, description="Definido en el numeral 8.4.1 resolucion nomina electronica, debe ser mayor o igual a 1.")
})

NumeroSecuenciaXML = api.model("NumeroSecuenciaXML", {
    'Prefijo': fields.String(required=True, description="Prefijo de la nomina en letras ej. ABC"),
    'Consecutivo': fields.String(required=True, description="Consecutivo de la nomina en numero ej. 123"),
    'Numero': fields.String(required=True, description="No se permiten caracteres adicionales como espacios o guiones. Prefijo + Consecutivo del documento")
    })

GeneracionXML = api.model("LugarGeneracionXML", {
    'Pais': fields.String(required=True, description="Codigo de pais ej. CO= Colombia, US= Estados unidos, mirar los demas en la tabla 5.4.1 Paises resolucion nomina electronica"),
    'DepartamentoEstado': fields.String(required=True, description="Codigo departamento ej. 76= Valle, 66= Risaralda, mirar los demas en la tabla 5.4.2 Departamentos resolucion nomina electronica"),
    'MunicipioCiudad': fields.String(required=True, description="Codigo ciudad ej. 76001= Cali, 66001= Pereira, mirar los demas en la tabla 5.4.3 Municipios resolucion nomina electronica"),
    'Idioma': fields.String(required=True, description="es= español, en= ingles, mirar los demas en la tabla 5.3.1 resolucion nomina electronica")
    })


InfoGeneral = api.model("InformacionGeneral", {
    'FechaGen': fields.String(required=True, description="Debe ir la fecha de emision del documento. Considerando zona horaria de Colombia (-5), en formato AAAA-MM-DD"),
    'HoraGen': fields.String(required=True, description="Debe ir la hora de emision del documento. Considerando zona horaria de Colombia (-5), en formato HH:MM:SSdhh:mm"),
    'PeriodoNomina': fields.String(required=True, description="1= Semanal, 2= Decenal, 3= Catorcenal, 4= Quincenal, 5= Mensual, 6= Otro"),
    'TipoMoneda': fields.String(required=True, description="Para Colombia se debe colocar COP= Peso colombiano, mirar los demas en la tabla 5.3.2 resolucion nomina electronica"),
    'TRM': fields.String(required=True, description="Se debe colocar la tasa de cambio de la moneda utilizada en el documento en el Campo “TipoMoneda” a Pesos Colombianos"),
    'DianTestSetId': fields.String(required=True, description="Se obtiene de la plataforma de la DIAN"),
    'DianSoftwareId': fields.String(required=True, description="Se obtiene de la plataforma de la DIAN"),
    'DianPin': fields.String(required=True, description="Se obtiene de la plataforma de la DIAN"),
    'TipoAmbiente': fields.String(required=True, description="1= Produccion, 2= Pruebas"),
    'CUNE': fields.String(required=True, description="Codigo unico de nomina electronica")

})


InfoGeneralNotas = api.model("InformacionGeneralNotas", {
    'FechaGen': fields.Date(required=True, description="Debe ir la fecha de emision del documento. Considerando zona horaria de Colombia (-5), en formato AAAA-MM-DD"),
    'HoraGen': fields.String(required=True, description="Debe ir la hora de emision del documento. Considerando zona horaria de Colombia (-5), en formato HH:MM:SSdhh:mm"),
    'PeriodoNomina': fields.String(required=True, description="1= Semanal, 2= Decenal, 3= Catorcenal, 4= Quincenal, 5= Mensual, 6= Otro"),
    'TipoMoneda': fields.String(required=True, description="Para Colombia se debe colocar COP= Peso colombiano, mirar los demas en la tabla 5.3.2 resolucion nomina electronica"),
    'TRM': fields.String(required=True, description="Se debe colocar la tasa de cambio de la moneda utilizada en el documento en el Campo “TipoMoneda” a Pesos Colombianos"),
    'DianTestSetId': fields.String(required=True, description="Se obtiene de la plataforma de la DIAN"),
    'DianSoftwareId': fields.String(required=True, description="Se obtiene de la plataforma de la DIAN"),
    'DianPin': fields.String(required=True, description="Se obtiene de la plataforma de la DIAN"),
    'TipoAmbiente': fields.String(required=True, description="1= Produccion, 2= Pruebas"),
    'CUNE': fields.String(required=True, description="Codigo unico de nomina electronica"),
    'TipoNota': fields.String(required=True, description="1= Reemplazar, 2= Eliminar"),
    'FechaGenPredecesor': fields.Date(required=True, description="Debe ir la fecha del documento a Reemplazar, en formato AAAA-MM-DD"),
    'CUNEPredecesor': fields.String(required=True, description="Debe ir el CUNE del documento a Reemplazar"),
    'NumeroDocumentoPredecesor': fields.String(required=True, description="Debe ir el Numero de documento a Reemplazar")

})


Notas = api.model("Notas", {
    'NotaPrueba': fields.String(required=False, description="Información adicional: Texto libre, relativo al documento")
})

Empleador = api.model("Empleador", {
    'NIT': fields.String(required=False, description="Debe ir el NIT del Empleador sin guiones ni DV"),
    'DigitoVerificacion': fields.String(required=False, description="Digito verificacion del empleador"),
    'TipoDocumento': fields.String(required=False, description="13= Cedula de ciudadania, 31= NIT, mirar los demas en la tabla 5.2.1 resolucion nomina electronica"),
    'NumeroDocumento': fields.String(required=False, description="Debe ir el Numero de documento del empleador, sin puntos ni comas ni espacios"),
    'PrimerApellido': fields.String(required=False, description="Debe ir el Primer Apellido del empleador"),
    'SegundoApellido': fields.String(required=False, description="Debe ir el Segundo Apellido del empleador"),
    'PrimerNombre': fields.String(required=False, description="Debe ir el Primer Nombre del empleador"),
    'OtrosNombres': fields.String(required=False, description="Deben ir los Otros Nombres del empleador"),
    'RazonSocial': fields.String(required=False, description="Debe ir el Nombre o Razón Social del empleador"),
    'Pais': fields.String(required=False, description="Debe ir codigo de pais, CO= Colombia, US= Estados unidos, mirar los demas en la tabla 5.4.1 Paises resolucion nomina electronica"),
    'DepartamentoEstado': fields.String(required=True, description="Codigo departamento ej. 76= Valle, 66= Risaralda, mirar los demas en la tabla 5.4.2 Departamentos resolucion nomina electronica"),
    'MunicipioCiudad': fields.String(required=True, description="Codigo ciudad ej. 76001= Cali, 66001= Pereira, mirar los demas en la tabla 5.4.3 Municipios resolucion nomina electronica"),
    'Direccion': fields.String(required=False, description="Debe ir la direccion fisica del empleador")
})

Trabajador = api.model("Trabajador", {
    'TipoTrabajador': fields.String(required=False, description="01= Dependiente, 22= Profesor particular, 51= Tiempo parcial, para los demas mirar la tabla 5.5.3 resolucion nomina electronica"),
    'SubTipoTrabajador': fields.String(required=False, description="00= No aplica, 01= Dependiente pensionado por vejez"),
    'AltoRiesgoPension': fields.String(required=False, description="Se debe colocar True o False"),
    'TipoDocumento': fields.String(required=False, description="13= Cedula de ciudadania, 31= NIT, mirar los demas en la tabla 5.2.1 resolucion nomina electronica"),
    'NumeroDocumento': fields.String(required=False, description="Debe ir el Numero de documento del trabajador, sin puntos ni comas ni espacios"),
    'PrimerApellido': fields.String(required=False, description="Debe ir el Primer Apellido del trabajador"),
    'SegundoApellido': fields.String(required=False, description="Debe ir el Segundo Apellido del trabajador"),
    'PrimerNombre': fields.String(required=False, description="Debe ir el Primer Nombre del trabajador"),
    'OtrosNombres': fields.String(required=False, description="Deben ir los Otros Nombres del trabajador"),
    'LugarTrabajoPais': fields.String(required=False, description="Codigo de pais ej. CO= Colombia, US= Estados unidos, mirar los demas en la tabla 5.4.1 Paises resolucion nomina electronica"),
    'LugarTrabajoDepartamentoEstado': fields.String(required=True, description="Codigo departamento ej. 76= Valle, 66= Risaralda, mirar los demas en la tabla 5.4.2 Departamentos resolucion nomina electronica"),
    'LugarTrabajoMunicipioCiudad': fields.String(required=True, description="Codigo ciudad ej. 76001= Cali, 66001= Pereira, mirar los demas en la tabla 5.4.3 Municipios resolucion nomina electronica"),
    'LugarTrabajoDireccion': fields.String(required=False, description="Debe ir la direccion fisica de trabajo"),
    'SalarioIntegral': fields.String(required=False, description="Se debe colocar true o false"),
    'TipoContrato': fields.String(required=False, description="1= Termino fijo, 2= Indefinido, 3= Obra o labor, 4= Aprendizaje, 5= Practicas o pasantias"),
    'Sueldo': fields.String(required=False, description="Se debe colocar el Sueldo Base que el Trabajdor tiene en la empresa"),
    'CodigoTrabajador': fields.String(required=False, description="Campo Opcional queda a manejo Interno del Empleador."),
    'CorreoElectronico': fields.String(required=False, description="Email del trabajador"),
})

Pago = api.model("Pago", {
    'Forma': fields.String(required=False, description="1= Contado"),
    'Metodo': fields.String(required=False, description="10= Efectivo, 48= Tarjeta Credito, 49= Tarjeta Debito, mirar los demas en la tabla 5.3.3.2 resolucion nomina electronica"),
    'Banco': fields.String(required=False, description="Se debe colocar el nombre de la entidad bancaria que el trabajador tiene para pago de nomina. Si el Metodo de Pago se realiza de forma Bancaria, este campo es obligatorio"),
    'TipoCuenta': fields.String(required=False, description="Ahorros o Corriente"),
    'NumeroCuenta': fields.String(required=False, description="Se debe colocar el número de la cuenta que el trabajador tiene para pago de nomina. Si el Metodo de Pago se realiza de forma Bancaria, este campo es obligatorio"),
})


Basico = api.model("Basico", {
    'DiasTrabajados': fields.String(required=False, description="Cantidad de dias laborados durante el Periodo de Pago"),
    'SueldoTrabajado': fields.String(required=False, description="Valor Base o Sueldo del trabajador según lo estipulado en su contrato. Corresponde al Sueldo Trabajado por los días laborados.")
})


Transporte = api.model("Transporte", {
    'AuxilioTransporte': fields.String(required=False, description="Valor de Auxilio de Transporte que recibe el trabajador por ley, según aplique"),
    'ViaticoManutAlojS': fields.String(required=False, description="Valor de Viaticos, Manutención y Alojamiento de carácter Salarial"),
    'ViaticoManutAlojNS': fields.String(required=False, description="Valor de Viaticos, Manutención y Alojamiento de carácter No Salarial")
})

HEDs = api.model("HEDs", {
    'Cantidad': fields.String(required=False, description="Cantidad horas"),
    'Porcentaje': fields.String(required=False, description="Hora extra diurna= 25.00"),
    'Pago': fields.String(required=False, description="Valor liquidado por hora extra diurna")
})

HENs = api.model("HENs ", {
    'Cantidad': fields.String(required=False, description="Cantidad horas"),
    'Porcentaje': fields.String(required=False, description="Hora extra nocturna= 75.00"),
    'Pago': fields.String(required=False, description="Valor liquidado por hora extra nocturna")
})

HEDDFs = api.model("HEDDFs", {
    'Cantidad': fields.String(required=False, description="Cantidad horas"),
    'Porcentaje': fields.String(required=False, description="Hora extra diurna dominical y festivos= 100.00"),
    'Pago': fields.String(required=False, description="Valor liquidado por hora extra diurna dominical y festivos")
})

HENDFs = api.model("HENDFs", {
    'Cantidad': fields.String(required=False, description="Cantidad horas"),
    'Porcentaje': fields.String(required=False, description="Hora extra nocturna dominical y festivos= 150.00"),
    'Pago': fields.String(required=False, description="Valor liquidado por hora extra nocturna dominical y festivos")
})

HRNs = api.model("HRNs", {
    'Cantidad': fields.String(required=False, description="Cantidad horas"),
    'Porcentaje': fields.String(required=False, description="Hora recargo nocturno= 35.00"),
    'Pago': fields.String(required=False, description="Valor liquidado por hora recargo nocturno")
})

HRDDFs = api.model("HRDDFs", {
    'Cantidad': fields.String(required=False, description="Cantidad horas"),
    'Porcentaje': fields.String(required=False, description="Hora Recargo Diurno Dominical y Festivos= 75.00"),
    'Pago': fields.String(required=False, description="Valor liquidado por Hora Recargo Diurno Dominical y Festivos")
})

HRNDFs = api.model("HRNDFs", {
    'Cantidad': fields.String(required=False, description="Cantidad horas"),
    'Porcentaje': fields.String(required=False, description="Hora Recargo Nocturno Dominical y Festivos= 110.00"),
    'Pago': fields.String(required=False, description="Valor liquidado por Hora Recargo Nocturno Dominical y Festivosa")
})

VacacionesComunes = api.model("VacacionesComunes", {
    'Cantidad': fields.String(required=False, description="Cantidad de dias"),
    'Pago': fields.String(required=False, description="Valor Pagado por Vacaciones Si Disfrutadas"),
    'FechaInicio': fields.Date(required=False, description="En formato AAAA-MM-DD"),
    'FechaFin': fields.Date(required=False, description="En formato AAAA-MM-DD"),
})

VacacionesCompensadas = api.model("VacacionesCompensadas", {
    'Cantidad': fields.String(required=False, description="Cantidad de dias"),
    'Pago': fields.String(required=False, description="Valor Pagado por Vacaciones No Disfrutadas")
})

Primas = api.model("Primas", {
    'Cantidad': fields.String(required=False, description="Cantidad de Dias a los cuales corresponde el pago de la Prima legal"),
    'Pago': fields.String(required=False, description="Valor Pagado por Prima Legal con respecto a Cantidad de Dias"),
    'PagoNS': fields.String(required=False, description="Valor Pagado por Prima No Salarial")
})

Cesantias = api.model("Cesantias", {
    'Pago': fields.String(required=False, description="Valor Pagado por Cesantias"),
    'Porcentaje': fields.String(required=False, description="Porcentaje de Interes de Cesantias"),
    'PagoIntereses': fields.String(required=False, description="Valor Pagado por Intereses de Cesantias")
})

Incapacidades = api.model("Incapacidades", {
    'Cantidad': fields.String(required=False, description="Cantidad de dias"),
    'Tipo': fields.String(required=False, description="1= Comun, 2= Profesional, 3= Laboral"),
    'Pago': fields.String(required=False, description="Valor liquidado segun el tipo de incapacidad"),
    'FechaInicio': fields.Date(required=False, description="En formato AAAA-MM-DD"),
    'FechaFin': fields.Date(required=False, description="En formato AAAA-MM-DD")
})

LicenciaMP = api.model("LicenciaMP", {
    'Cantidad': fields.String(required=False, description="Cantidad de dias"),
    'Pago': fields.String(required=False, description="Valor Pagado por Licencia de Maternidad o Paternidad con respecto a Cantidad de Dias"),
    'FechaInicio': fields.Date(required=False, description="En formato AAAA-MM-DD"),
    'FechaFin': fields.Date(required=False, description="En formato AAAA-MM-DD")
})

LicenciaR = api.model("LicenciaR", {
    'Cantidad': fields.String(required=False, description="Cantidad de dias"),
    'Pago': fields.String(required=False, description="Valor Pagado por Licencia Remunerada con respecto a Cantidad de Dias"),
    'FechaInicio': fields.Date(required=False, description="En formato AAAA-MM-DD"),
    'FechaFin': fields.Date(required=False, description="En formato AAAA-MM-DD")
})

LicenciaNR = api.model("LicenciaNR", {
    'Cantidad': fields.String(required=False, description="Cantidad de dias"),
    'FechaInicio': fields.Date(required=False, description="En formato AAAA-MM-DD"),
    'FechaFin': fields.Date(required=False, description="En formato AAAA-MM-DD")
})

Bonificaciones = api.model("Bonificaciones", {
    'BonificacionS': fields.String(required=False, description="Valor Pagado por Bonificación Salarial"),
    'BonificacionNS': fields.String(required=False, description="Valor Pagado por Bonificación No Salarial")
})

Auxilios = api.model("Auxilios", {
    'AuxilioS': fields.String(required=False, description="Valor Pagado por Auxilios Salariales"),
    'AuxilioNS': fields.String(required=False, description="Valor Pagado por Auxilios No Salariales")
})

OtrosConceptos = api.model("OtrosConceptos", {
    'DescripcionConcepto': fields.String(required=False, description="Debe ir la Descripcion del Concepto"),
    'ConceptoS': fields.String(required=False, description="Valor Pagado por Conceptos Salariales"),
    'ConceptoNS': fields.String(required=False, description="Valor Pagado por Conceptos No Salariales")
})

Compensaciones = api.model("Compensaciones", {
    'CompensacionO': fields.String(required=False, description="Valor Pagado por Compensaciones Ordinarias"),
    'CompensacionE': fields.String(required=False, description="Valor Pagado por Compensaciones Extraordinarias")
})

BonoEPCTVs = api.model("BonoEPCTVs", {
    'PagoS': fields.String(required=False, description="Concepto Salarial"),
    'PagoNS': fields.String(required=False, description="Concepto No Salarial"),
    'PagoAlimentacionS': fields.String(required=False, description="Concepto Salarial"),
    'PagoAlimentacionNS': fields.String(required=False, description="Concepto No Salarial"),
})

Comisiones = api.model("Comisiones", {
    'Comision': fields.String(required=False, description="Valor Pagado por Comision")
})

PagosTerceros = api.model("PagoTerceros", {
    'PagoTercero': fields.String(required=False, description="Valor Pagado por Pago Tercero")
})

Anticipos = api.model("Anticipos", {
    'Anticipo': fields.String(required=False, description="Valor Pagado por Anticipo")
})

Devengados = api.model("Devengados", {
    'Basico': fields.Nested(Basico),
    'Transporte': fields.Nested(Transporte, required=False),
    'HEDs': fields.List(fields.Nested(HEDs)),
    'HENs': fields.List(fields.Nested(HENs)),
    'HEDDFs': fields.List(fields.Nested(HEDDFs)),
    'HENDFs': fields.List(fields.Nested(HENDFs)),
    'HRNs': fields.List(fields.Nested(HRNs)),
    'HRDDFs': fields.List(fields.Nested(HRDDFs)),
    'HRNDFs': fields.List(fields.Nested(HRNDFs)),
    'VacacionesComunes': fields.List(fields.Nested(VacacionesComunes)),
    'VacacionesCompensadas': fields.List(fields.Nested(VacacionesCompensadas)),
    'Primas': fields.Nested(Primas),
    'Cesantias': fields.Nested(Cesantias),
    'Incapacidades': fields.List(fields.Nested(Incapacidades)),
    'LicenciaMP': fields.List(fields.Nested(LicenciaMP)),
    'LicenciaR': fields.List(fields.Nested(LicenciaR)),
    'LicenciaNR': fields.List(fields.Nested(LicenciaNR)),
    'Bonificaciones': fields.List(fields.Nested(Bonificaciones)),
    'Auxilios': fields.List(fields.Nested(Auxilios)),
    'OtrosConceptos': fields.List(fields.Nested(OtrosConceptos)),
    'Compensaciones': fields.List(fields.Nested(Compensaciones)),
    'BonoEPCTVs': fields.List(fields.Nested(BonoEPCTVs)),
    'Comisiones': fields.List(fields.Nested(Comisiones)),
    'PagosTerceros': fields.List(fields.Nested(PagosTerceros)),
    'Anticipos': fields.List(fields.Nested(Anticipos)),
    'Dotacion': fields.String(required=False, description="Valor Pagado por Dotacion"),
    'ApoyoSost': fields.String(required=False, description="Valor Pagado por Apoyo a Sostenimiento"),
    'Teletrabajo': fields.String(required=False, description="Valor Pagado por trabajo en Teletrabajo"),
    'BonifRetiro': fields.String(required=False, description="Valor Pagado por Retiro de la empresa"),
    'Indemnizacion': fields.String(required=False, description="Valor Pagado por Indemnización"),
    'Reintegro': fields.String(required=False, description="Valor Pagado correspondiente a Reintegro por parte del empleador"),
    })

Salud = api.model("Salud", {
    'Porcentaje': fields.String(required=False, description="Se debe colocar el Porcentaje que corresponda"),
    'Deduccion': fields.String(required=False, description="Valor Pagado correspondiente a Salud por parte del trabajador")
})

Pension = api.model("FondoPension", {
    'Porcentaje': fields.String(required=False, description="Se debe colocar el Porcentaje que corresponda"),
    'Deduccion': fields.String(required=False, description="Valor Pagado correspondiente a Pension por parte del trabajador")
})

FondoSP = api.model("FondoSP", {
    'Porcentaje': fields.String(required=False, description="Se debe colocar el Porcentaje que corresponda"),
    'Deduccion': fields.String(required=False, description="Valor Pagado correspondiente a Fondo de Solidaridad Pensional por parte del trabajador"),
    'PorcentajeSub': fields.String(required=False, description="Se debe colocar el Porcentaje que correspondiente al Fondo de Subsistencia correspondiente"),
    'DeduccionSub': fields.String(required=False, description="Valor Pagado correspondiente a Fondo de Subsistencia por parte del trabajador")
})

Sindicatos = api.model("Sindicatos", {
    'Porcentaje': fields.String(required=False, description="Se debe colocar el Porcentaje que corresponda"),
    'Deduccion': fields.String(required=False, description="Valor Pagado correspondiente a Aportes del Sindicato por parte del trabajador")
})

Sanciones = api.model("Sanciones", {
    'Porcentaje': fields.String(required=False, description="Se debe colocar el Porcentaje que corresponda"),
    'Deduccion': fields.String(required=False, description="Valor Pagado correspondiente a Sanciones por parte del trabajador")
})

Libranzas = api.model("Libranzas", {
    'Deduccion': fields.String(required=False, description="Valor Pagado correspondiente a Aportes a Entidades Financieras por parte del trabajador")
})

PagoTerceros = api.model("PagoTerceros", {
    'PagoTercero': fields.String(required=False, description="Valor Pagado por Pago Tercero")
})

Anticipos= api.model("Anticipos", {
    'Anticipo': fields.String(required=False, description="Valor Pagado por Anticipo")
})

OtrasDeducciones = api.model("OtrasDeducciones", {
    'OtraDeduccion': fields.String(required=False, description="Valor Pagado por Otra deduccion")
})

Deducciones = api.model("Deducciones", {
    'Salud': fields.Nested(Salud),
    'Pension': fields.Nested(Pension),
    'FondoSP': fields.Nested(FondoSP),
    'Sindicatos': fields.List(fields.Nested(Sindicatos)),
    'Sanciones': fields.List(fields.Nested(Sanciones)),
    'Libranzas': fields.List(fields.Nested(Libranzas)),
    'PagoTerceros': fields.List(fields.Nested(PagoTerceros)),
    'Anticipos': fields.List(fields.Nested(Anticipos)),
    'OtrasDeducciones': fields.List(fields.Nested(OtrasDeducciones)),
    'PensionVoluntaria': fields.String(required=False, description="Valor Pagado correspondiente al ahorro que hace el trabajador para complementar su pension obligatoria o cumplir metas especificas"),
    'RetencionFuente': fields.String(required=False, description="Valor Pagado correspondiente a Retención en la Fuente por parte del trabajador"),
    'AFC': fields.String(required=False, description="Valor Pagado correspondiente a Ahorro Fomento a la Construccion por parte del trabajador"),
    'Cooperativa': fields.String(required=False, description="Valor Pagado correspondiente a Cooperativas por parte del trabajador"),
    'EmbargoFiscal': fields.String(required=False, description="Valor Pagado correspondiente a Embargos Fiscales por parte del trabajador"),
    'PlanComplementarios': fields.String(required=False, description="Valor Pagado correspondiente a Planes Complementarios por parte del trabajador"),
    'Educacion': fields.String(required=False, description="Valor Pagado correspondiente a Conceptos educativos por parte del trabajador"),
    'ReintegroDeducciones': fields.String(required=False, description="Valor Pagado correspondiente a Reintegro por parte del trabajador"),
    'Deuda': fields.String(required=False, description="Valor Pagado correspondiente a Deuda con la Empresa por parte del trabajador")

})

Pdf = api.model("Pdf", {
    'Pdf': fields.String(required=False, description="Pdf string base64")
})
