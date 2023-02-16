from typing import Any, Dict, List
from datetime import datetime


not_validate = [
    'CUFE',
    'CUNE',
    'CUDE',
    'CUDS',
    'DeliveryDate',
    'DeliveryTime',
    'PaymentExchangeRate',
    'PostalCode',
    'BrandName',
    'ModelName',
    'CityName',
    'DepartmentName',
    'TipoNota',
    'Pdfdata',
    'Pdf',
    'SerieExternalKey',
    'Notas',
    'OtherReferenceTypeId',
    'OtherReferenceTypeDescription',
    'CheckDigit',
    'DocumentReferences'
]


def validate(key: str, field: Any) -> Any:
    """La función hace una validación de que los campos no tengan un valor
       incorrecto, verifica que los campos no sean
       ('null', 'None', '', 'string', None) y retorna el primer error
       encontrado de los datos que se le envían.

    Args:
        key (str): Key del campo a validar.
        field (Any): Valor del campo a validar.

    Returns:
        Any: Descripción del error.
    """

    if field is None:
        return f'El campo {key} no es válido: el campo no debe ser nulo'

    if isinstance(field, str) and field in ('null', 'None', ''):
        err = f"El campo {key} no es válido: el campo debe ser diferente de (null, None, vacío)"
        return (
            err,
            field if field != '' else 'vacío'
        )
    elif isinstance(field, list):
        for item in field:
            if isinstance(item, dict):
                res = validate(key, item)
                if res:
                    return res
            elif isinstance(item, str):
                res = validate(key, item)
                if res:
                    return res
    elif isinstance(field, dict):
        errors: List[str] = []
        for k, v in field.items():
            if k not in not_validate:
                res = validate(k, v)
                if res:
                    if isinstance(res, list):
                        [errors.append((f'Error in {key}:' + er[0], er[1])) for er in res]
                    else:
                        errors.append((f'Error in {key}: {res[0]}', res[1]))
        return errors


def validate_json(data: Dict[str, str], to_not_validate: List[str] = None) -> Dict[str, Any]:
    """La función hace una validación de que los campos no tengan un valor
       incorrecto, verifica que los campos no sean
       ('null', 'None', '', 'string', None) y retorna una lista de errores
       encontrados en el json que recibe.

    Args:
        data (Dict[str, str]): json a validar.

    Raises:
        ValueError: Si el json no es válido.
    """

    try:
        if 'Currency' in data and data['Currency'] == 'COP':
            not_validate.append('PaymentExchangeRate')

        if to_not_validate:
            not_validate.extend(to_not_validate)

        status: bool = True
        errors: List[Dict[str, str]] = []
        description_errors: List[Any] = []

        for key, value in data.items():
            if key not in not_validate and value is None:
                errors.append(
                    f'Error: El campo {key} no es válido:\
                        el campo no debe ser nulo.')

            if key not in not_validate and isinstance(value, dict):
                err: List[Dict[str, str]] = []
                for k, v in value.items():
                    if k not in not_validate:
                        res = validate(k, v)
                        if res:
                            if isinstance(res, list):
                                [errors.append((f'Error en {key}:' + er[0], er[1])) for er in res]
                            else:
                                errors.append((f'Error en {key}: {res[0]}', res[1]))
                            status = False
                if err:
                    errors.append(err)
            elif key not in not_validate and isinstance(value, str):
                res = validate(key, value)
                if res:
                    errors.append(res)
                    status = False
            elif key not in not_validate and isinstance(value, bool):
                pass
            elif key not in not_validate and isinstance(value, int):
                errors.append(f'Error: El campo {key} no es válido: debe ser un string.')
            elif key not in not_validate and isinstance(value, list):
                res = validate(key, value)
                if res:
                    if isinstance(res, list):
                        errors.extend(res)
                    else:
                        errors.append((f'Error en {key}: {res[0]}', res[1]))
                    status = False
        if not status:
            del status
            del data

            i: int = 0
            for err in errors:
                i += 1
                description_errors.append({
                    'Code': 'Edocs_404',
                    "Description":"Documento con errores en campos mandatorios.",
                    "ExplanationValues": [err[0]],
                    "Field": err[1],
                })
            del i
            del errors
            raise ValueError
        else:
            return data
    except ValueError:
        response = {
            'message': 'Bad Request',
            "IsValid": False,
            'resultCode': 400,
            'errors': description_errors
        }
        return response
