from flask_restx import Namespace, fields


api = Namespace("Eventos", description="Operaciones relacionadas con eventos")

PersonModel = api.model(
    "PersonModel", {
        'documentNumber': fields.String(required=True, description="Numero de documento"),
        'checkDigitPerson': fields.String(required=True, description="Digito de verificacion"),
        'documentTypePerson': fields.String(required=True, description="Tipo de documento 13 =CC, 31 =NIT"),
        'firstNamePerson': fields.String(required=True, description="Nombre"),
        'lastNamePerson':  fields.String(required=True, description="Apellido"),
        'jobTitle': fields.String(required=True, description="Cargo en la empresa"),
        'organizationDepartment': fields.String(required=True, description="Departamento de la empresa"),

        })

EventsModelAcuse = api.model(
    "EventsAcuse", {
         'issueDate': fields.Date(required=True, description="Debe ir la fecha de emision del documento. Considerando zona horaria de Colombia (-5), en formato AAAA-MM-DD"),
         'issueTime': fields.String(required=True, description="Debe ir la hora de emision del documento. Considerando zona horaria de Colombia (-5), en formato HH:MM:SSdhh:mm"),
         'registrationNameSenderParty': fields.String(required=True, description="Debe ir el nombre del emisor del evento"),
         'checkDigitSenderParty': fields.String(required=False, description="Debe ir el digito de verificacion del emisor del evento, solo si el tipo de documento es NIT"),
         'docTypeSenderParty': fields.String(required=True, description="Debe ir el tipo de documento del emisor del evento 31= Nit, 13= Cedula"),
         'nitSenderParty': fields.String(required=True, description="Debe ir el documento del emisor del evento"),
         'legalTypeSenderParty': fields.String(required=True, description="Debe ir el tipo de organizacion del emisor del evento 1= Persona Juridica, 2= Persona Natural"),
         'taxSchemeNameSenderParty': fields.String(required=True, description="Debe ir el nombre del regimen fiscal del emisor del evento IVA,INC,IVA e INC ó No aplica"),
         'taxSchemeCodeSenderParty': fields.String(required=True, description="Debe ir el codgio del regimen fiscal del emisor del evento 01, 02"),
         'taxSchemeNameReceiverParty': fields.String(required=True, description="Debe ir el nombre del regimen fiscal del receptor del evento IVA,INC,IVA e INC ó No aplica"),
         'taxSchemeCodeReceiverParty': fields.String(required=True, description="Debe ir el codgio del regimen fiscal del receptor del evento 01, 02"),
         'dianPin': fields.String(required=True, description="Debe ir el numero de pin del emisor del evento"),
         'dianSofwareID': fields.String(required=True, description="Debe ir el numero de identificacion del software del emisor del evento"),
         'registrationNameReceiverParty': fields.String(required=True, description="Debe ir el nombre del receptor del evento"),
         'checkDigitReceiverParty': fields.String(required=False, description="Debe ir el digito de verificacion del receptor del evento, solo si el tipo de documento es NIT"),
         'docTypeReceiverParty': fields.String(required=True, description="Debe ir el tipo de documento del receptor del evento 31= Nit, 13= Cedula"),
         'nitReceiverParty': fields.String(required=True, description="Debe ir el documento del receptor del evento"),
         'legalTypeReceiverParty': fields.String(required=True, description="Debe ir el tipo de organizacion del receptor del evento 1= Persona Juridica, 2= Persona Natural"),
         'electronicMailReceiverParty': fields.String(required=True, description="Debe ir el correo electronico del receptor del evento"),
         'documentReference': fields.String(required=True, description="Debe ir el numero de factura que se va a referenciar, incluyendo el prefijo"),
         'CUFE': fields.String(required=True, description="Debe el numero de CUFE de la factura"),
         'documentTypeCode': fields.String(required=True, description="Debe ir el codigo del tipo de documento 01= Factura, 02= Factura de exportacion"),
         'person': fields.Nested(PersonModel, required=True, description="Debe ir la informacion de la persona que emite el evento")
      })

EventsModelClaim = api.model(
    "EventsClaim", {
         'issueDate': fields.Date(required=True, description="Debe ir la fecha de emision del documento. Considerando zona horaria de Colombia (-5), en formato AAAA-MM-DD"),
         'issueTime': fields.String(required=True, description="Debe ir la hora de emision del documento. Considerando zona horaria de Colombia (-5), en formato HH:MM:SSdhh:mm"),
         'registrationNameSenderParty': fields.String(required=True, description="Debe ir el nombre del emisor del evento"),
         'checkDigitSenderParty': fields.String(required=False, description="Debe ir el digito de verificacion del emisor del evento, solo si el tipo de documento es NIT"),
         'docTypeSenderParty': fields.String(required=True, description="Debe ir el tipo de documento del emisor del evento 31= Nit, 13= Cedula"),
         'legalTypeSenderParty': fields.String(required=True, description="Debe ir el tipo de organizacion del emisor del evento 1= Persona Juridica, 2= Persona Natural"),
         'taxSchemeNameSenderParty': fields.String(required=True, description="Debe ir el nombre del regimen fiscal del emisor del evento IVA,INC,IVA e INC ó No aplica"),
         'taxSchemeCodeSenderParty': fields.String(required=True, description="Debe ir el codgio del regimen fiscal del emisor del evento 01, 02"),
         'taxSchemeNameReceiverParty': fields.String(required=True, description="Debe ir el nombre del regimen fiscal del receptor del evento IVA,INC,IVA e INC ó No aplica"),
         'taxSchemeCodeReceiverParty': fields.String(required=True, description="Debe ir el codgio del regimen fiscal del receptor del evento 01, 02"),
         'dianPin': fields.String(required=True, description="Debe ir el numero de pin del emisor del evento"),
         'dianSofwareID': fields.String(required=True, description="Debe ir el numero de identificacion del software del emisor del evento"),
         'claimCode': fields.String(required=True, description="Codigo del reclamo 01= Documento con inconsistencias, 02= Mercancia no entregada totalmente,"
                                                               "03= Mercancia no entregada parcialmente, 04= Servicio no prestado"),
         'registrationNameReceiverParty': fields.String(required=True, description="Debe ir el nombre del receptor del evento"),
         'checkDigitReceiverParty': fields.String(required=False, description="Debe ir el digito de verificacion del receptor del evento, solo si el tipo de documento es NIT"),
         'docTypeReceiverParty': fields.String(required=True, description="Debe ir el tipo de documento del receptor del evento 31= Nit, 13= Cedula"),
         'nitReceiverParty': fields.String(required=True, description="Debe ir el documento del receptor del evento"),
         'legalTypeReceiverParty': fields.String(required=True, description="Debe ir el tipo de organizacion del receptor del evento 1= Persona Juridica, 2= Persona Natural"),
         'electronicMailReceiverParty': fields.String(required=True, description="Debe ir el correo electronico del receptor del evento"),
         'documentReference': fields.String(required=True, description="Debe ir el numero de factura que se va a referenciar, incluyendo el prefijo"),
         'CUFE': fields.String(required=True, description="Debe el numero de CUFE de la factura"),
         'documentTypeCode': fields.String(required=True, description="Debe ir el codigo del tipo de documento 01= Factura, 02= Factura de exportacion")
      })

EventsModelReceipt = api.model(
    "EventsReceipt", {
         'issueDate': fields.Date(required=True, description="Debe ir la fecha de emision del documento. Considerando zona horaria de Colombia (-5), en formato AAAA-MM-DD"),
         'issueTime': fields.String(required=True, description="Debe ir la hora de emision del documento. Considerando zona horaria de Colombia (-5), en formato HH:MM:SSdhh:mm"),
         'registrationNameSenderParty': fields.String(required=True, description="Debe ir el nombre del emisor del evento"),
         'checkDigitSenderParty': fields.String(required=False, description="Debe ir el digito de verificacion del emisor del evento, solo si el tipo de documento es NIT"),
         'docTypeSenderParty': fields.String(required=True, description="Debe ir el tipo de documento del emisor del evento 31= Nit, 13= Cedula"),
         'nitSenderParty': fields.String(required=True, description="Debe ir el documento del emisor del evento"),
         'legalTypeSenderParty': fields.String(required=True, description="Debe ir el tipo de organizacion del emisor del evento 1= Persona Juridica, 2= Persona Natural"),
         'taxSchemeNameSenderParty': fields.String(required=True, description="Debe ir el nombre del regimen fiscal del emisor del evento IVA,INC,IVA e INC ó No aplica"),
         'taxSchemeCodeSenderParty': fields.String(required=True, description="Debe ir el codgio del regimen fiscal del emisor del evento 01, 02"),
         'taxSchemeNameReceiverParty': fields.String(required=True, description="Debe ir el nombre del regimen fiscal del receptor del evento IVA,INC,IVA e INC ó No aplica"),
         'taxSchemeCodeReceiverParty': fields.String(required=True, description="Debe ir el codgio del regimen fiscal del receptor del evento 01, 02"),
         'dianPin': fields.String(required=True, description="Debe ir el numero de pin del emisor del evento"),
         'dianSofwareID': fields.String(required=True, description="Debe ir el numero de identificacion del software del emisor del evento"),
         'registrationNameReceiverParty': fields.String(required=True, description="Debe ir el nombre del receptor del evento"),
         'checkDigitReceiverParty': fields.String(required=False, description="Debe ir el digito de verificacion del receptor del evento, solo si el tipo de documento es NIT"),
         'docTypeReceiverParty': fields.String(required=True, description="Debe ir el tipo de documento del receptor del evento 31= Nit, 13= Cedula"),
         'nitReceiverParty': fields.String(required=True, description="Debe ir el documento del receptor del evento"),
         'legalTypeReceiverParty': fields.String(required=True, description="Debe ir el tipo de organizacion del receptor del evento 1= Persona Juridica, 2= Persona Natural"),
         'electronicMailReceiverParty': fields.String(required=True, description="Debe ir el correo electronico del receptor del evento"),
         'documentReference': fields.String(required=True, description="Debe ir el numero de factura que se va a referenciar, incluyendo el prefijo"),
         'CUFE': fields.String(required=True, description="Debe el numero de CUFE de la factura"),
         'documentTypeCode': fields.String(required=True, description="Debe ir el codigo del tipo de documento 01= Factura, 02= Factura de exportacion"),
         'person': fields.Nested(PersonModel, required=True, description="Debe ir la informacion de la persona que emite el evento")
      })

EventsModelAccept = api.model(
    "EventsAccept", {
         'issueDate': fields.Date(required=True, description="Debe ir la fecha de emision del documento. Considerando zona horaria de Colombia (-5), en formato AAAA-MM-DD"),
         'issueTime': fields.String(required=True, description="Debe ir la hora de emision del documento. Considerando zona horaria de Colombia (-5), en formato HH:MM:SSdhh:mm"),
         'registrationNameSenderParty': fields.String(required=True, description="Debe ir el nombre del emisor del evento"),
         'checkDigitSenderParty': fields.String(required=False, description="Debe ir el digito de verificacion del emisor del evento, solo si el tipo de documento es NIT"),
         'docTypeSenderParty': fields.String(required=True, description="Debe ir el tipo de documento del emisor del evento 31= Nit, 13= Cedula"),
         'nitSenderParty': fields.String(required=True, description="Debe ir el documento del emisor del evento"),
         'legalTypeSenderParty': fields.String(required=True, description="Debe ir el tipo de organizacion del emisor del evento 1= Persona Juridica, 2= Persona Natural"),
         'taxSchemeNameSenderParty': fields.String(required=True, description="Debe ir el nombre del regimen fiscal del emisor del evento IVA,INC,IVA e INC ó No aplica"),
         'taxSchemeCodeSenderParty': fields.String(required=True, description="Debe ir el codgio del regimen fiscal del emisor del evento 01, 02"),
         'taxSchemeNameReceiverParty': fields.String(required=True, description="Debe ir el nombre del regimen fiscal del receptor del evento IVA,INC,IVA e INC ó No aplica"),
         'taxSchemeCodeReceiverParty': fields.String(required=True, description="Debe ir el codgio del regimen fiscal del receptor del evento 01, 02"),
         'dianPin': fields.String(required=True, description="Debe ir el numero de pin del emisor del evento"),
         'dianSofwareID': fields.String(required=True, description="Debe ir el numero de identificacion del software del emisor del evento"),
         'registrationNameReceiverParty': fields.String(required=True, description="Debe ir el nombre del receptor del evento"),
         'checkDigitReceiverParty': fields.String(required=False, description="Debe ir el digito de verificacion del receptor del evento, solo si el tipo de documento es NIT"),
         'docTypeReceiverParty': fields.String(required=True, description="Debe ir el tipo de documento del receptor del evento 31= Nit, 13= Cedula"),
         'nitReceiverParty': fields.String(required=True, description="Debe ir el documento del receptor del evento"),
         'legalTypeReceiverParty': fields.String(required=True, description="Debe ir el tipo de organizacion del receptor del evento 1= Persona Juridica, 2= Persona Natural"),
         'electronicMailReceiverParty': fields.String(required=True, description="Debe ir el correo electronico del receptor del evento"),
         'documentReference': fields.String(required=True, description="Debe ir el numero de factura que se va a referenciar, incluyendo el prefijo"),
         'CUFE': fields.String(required=True, description="Debe el numero de CUFE de la factura"),
         'documentTypeCode': fields.String(required=True, description="Debe ir el codigo del tipo de documento 01= Factura, 02= Factura de exportacion")
      })

EventsModelTacitAccept = api.model(
    "EventsTacitAccept", {
         'issueDate': fields.Date(required=True, description="Debe ir la fecha de emision del documento. Considerando zona horaria de Colombia (-5), en formato AAAA-MM-DD"),
         'issueTime': fields.String(required=True, description="Debe ir la hora de emision del documento. Considerando zona horaria de Colombia (-5), en formato HH:MM:SSdhh:mm"),
         'registrationNameSenderParty': fields.String(required=True, description="Debe ir el nombre del emisor del evento"),
         'checkDigitSenderParty': fields.String(required=False, description="Debe ir el digito de verificacion del emisor del evento, solo si el tipo de documento es NIT"),
         'docTypeSenderParty': fields.String(required=True, description="Debe ir el tipo de documento del emisor del evento 31= Nit, 13= Cedula"),
         'nitSenderParty': fields.String(required=True, description="Debe ir el documento del emisor del evento"),
         'legalTypeSenderParty': fields.String(required=True, description="Debe ir el tipo de organizacion del emisor del evento 1= Persona Juridica, 2= Persona Natural"),
         'taxSchemeNameSenderParty': fields.String(required=True, description="Debe ir el nombre del regimen fiscal del emisor del evento IVA,INC,IVA e INC ó No aplica"),
         'taxSchemeCodeSenderParty': fields.String(required=True, description="Debe ir el codgio del regimen fiscal del emisor del evento 01, 02"),
         'taxSchemeNameReceiverParty': fields.String(required=True, description="Debe ir el nombre del regimen fiscal del receptor del evento IVA,INC,IVA e INC ó No aplica"),
         'taxSchemeCodeReceiverParty': fields.String(required=True, description="Debe ir el codgio del regimen fiscal del receptor del evento 01, 02"),
         'dianPin': fields.String(required=True, description="Debe ir el numero de pin del emisor del evento"),
         'dianSofwareID': fields.String(required=True, description="Debe ir el numero de identificacion del software del emisor del evento"),
         'registrationNameReceiverParty': fields.String(required=True, description="Debe ir el nombre del receptor del evento"),
         'checkDigitReceiverParty': fields.String(required=False, description="Debe ir el digito de verificacion del receptor del evento, solo si el tipo de documento es NIT"),
         'docTypeReceiverParty': fields.String(required=True, description="Debe ir el tipo de documento del receptor del evento 31= Nit, 13= Cedula"),
         'nitReceiverParty': fields.String(required=True, description="Debe ir el documento del receptor del evento"),
         'legalTypeReceiverParty': fields.String(required=True, description="Debe ir el tipo de organizacion del receptor del evento 1= Persona Juridica, 2= Persona Natural"),
         'electronicMailReceiverParty': fields.String(required=True, description="Debe ir el correo electronico del receptor del evento"),
         'documentReference': fields.String(required=True, description="Debe ir el numero de factura que se va a referenciar, incluyendo el prefijo"),
         'CUFE': fields.String(required=True, description="Debe el numero de CUFE de la factura"),
         'documentTypeCode': fields.String(required=True, description="Debe ir el codigo del tipo de documento 01= Factura, 02= Factura de exportacion"),
         'note': fields.String(required=True, description="Debe ir la nota del evento")
      })

EventsFilterModel = api.model(
    "EventsFilterModel", {
        "issuerNit": fields.String(required=True, description="Nit de emisor"),
        "startClientNit": fields.String(required=False, description="Rango inicial del nit del cliente"),
        "endClientNit": fields.String(required=False, description="Rango final del nit del cliente"),
        "startDate": fields.Date(required=False, description="Fecha inicial a consultar en formato AAAA-MM-DD"),
        "endDate": fields.Date(required=False, description="Fecha final a consultar en formato AAAA-MM-DD"),
        "startNumber": fields.String(required=False, description="Rango inicial del documento incluido el prefijo"),
        "endNumber": fields.String(required=False, description="Rango final del documento incluido el prefijo"),
        "eventType": fields.String(required=False, description="Tipo de evento a consultar, 030= Acuse de recibo, 031= Rechazo, 033= Aceptacion"),
        "status": fields.String(required=True, description="Estado del documento 1= enviado a la DIAN, 0= rechazado por la DIAN"),
        "pageSize": fields.Integer(required=True, description="Tamaño de la pagina"),
        "pageNumber": fields.Integer(required=True, description="Numero de la pagina")
    }
)

allEventsModel = api.model(
    "allEvents", {
        "pageSize": fields.Integer(required=True, description="Tamaño de la pagina"),
        "pageNumber": fields.Integer(required=True, description="Numero de la pagina")
    }
)

EventsFilterNumberModel = api.model(
    "EventsFilterNumberModel", {
        "nit": fields.String(required=True, description="Nit de emisor"),
        "docType": fields.String(required=False, description="Tipo de documento FV=factura DS=documento soporte"),
        "seriePrefix": fields.String(required=False, description="prefijo del documento"),
        "serieNumber": fields.String(required=False, description="numero del documento")

    }
)

statusEventModel = api.model(
    'Status', {
        'Nit': fields.String(required=True, description="Nit del emisor"),
        'CUDE': fields.String(required=True, description="CUDE a consultar")
    }
)
