# -*- coding: utf-8 -*-
#########################################################
import json
import os
import smtplib
import time
from base64 import b64encode, b64decode
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO
from pathlib import Path
from typing import Dict, Any
from zipfile import ZipFile

import requests
from flask import make_response, jsonify

import config
from app.controllers import CertsController, CityController, DepartmentController
from app.exception import InternalServerError, NotFound
from app.models import NotesModel, NotesSendsModel, SendsModel
from app.utils import ResponseData


class NotesController:

    @staticmethod
    def all(data: Dict[str, int]):
        try:
            pageNumber, pageSize = (data["pageNumber"], data["pageSize"])
            db_data = NotesModel.get_data(export=True, pageNumber=pageNumber, pageSize=pageSize)
            if not db_data:
                response = ResponseData.not_found()
                return response
            response = make_response(jsonify(db_data), 200)
            return response
        except KeyError as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(error=str(e))
            return response

    @staticmethod
    def get_by(data: Dict[str, Any]):
        try:
            pageNumber, pageSize = (data["pageNumber"], data["pageSize"])
            db_data = NotesModel.get_by(data=data, export=True, pageNumber=pageNumber, pageSize=pageSize)
            if not db_data:
                response = ResponseData.not_found()
                return response
            response = make_response(jsonify(db_data), 200)
            return response
        except KeyError as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(error=str(e))
            return response

    @staticmethod
    def get_by_id(id: int):
        try:
            if not id and not isinstance(id, int):
                raise ValueError('El id debe ser un entero, y diferente de null')

            response = NotesModel.get_by_id(id=id, export=True)
            if not response:
                response = ResponseData.not_found_by_id(ide=id)
            else:
                response = ResponseData.response_get(data=response)
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(str(e))
            return response

    @staticmethod
    def updateCufe(data: Dict[str, str]):
        try:
            Id = data['Id']
            Cufe = data['Cufe']
            db_data = NotesModel.get_by_id(id=Id, export=True)
            if not db_data:
                response = ResponseData.not_found()
                return response

            db_data["Cufe"] = Cufe
            NotesSendsModel.update_data(db_data)

            response = {
                'cufe': Cufe
            }

            return make_response(response, 200)
        except KeyError as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(error=str(e))
            return response

    @staticmethod
    def pdf(data: Dict[str, str]):
        try:
            Nit = data['Nit']
            SeriePrefix = data['SeriePrefix']
            SerieNumber = data['SerieNumber']
            DocType = data['DocType']
            response = NotesModel.get_by_number(Nit=Nit, SeriePrefix=SeriePrefix, SerieNumber=SerieNumber,
                                                DocType=DocType, export=True)
            if not response:
                response = ResponseData.not_found()
            else:
                response = NotesModel.export_pdf(response)
            return response
        except KeyError as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(error=str(e))
            return response

    @staticmethod
    def xml(data: Dict[str, str]):
        try:
            Nit = data['Nit']
            SeriePrefix = data['SeriePrefix']
            SerieNumber = data['SerieNumber']
            DocType = data['DocType']
            response = NotesModel.get_by_number(Nit=Nit, SeriePrefix=SeriePrefix, SerieNumber=SerieNumber,
                                                DocType=DocType, export=True)
            if not response:
                response = ResponseData.not_found()
            else:
                response = NotesModel.export_xml(response)
            return response
        except KeyError as e:
            print('Error: {er}'.format(er=e))
            response = ResponseData.bad_request(error=str(e))
            return response

    @staticmethod
    def status(data: dict):
        def remove_char(s):
            return s[1: -1]

        datacerts = CertsController.get_by_nit(data["Nit"])
        if not datacerts:
            response = ResponseData.not_found()
            return response
        cert_encode = datacerts["Format"]
        # sending post request and saving response as response object

        datasign = {
            'Id': data["CUFE"],
            "Nit": data["Nit"],
            'keycert': datacerts["Key"],
            'contentcert': cert_encode
        }
        sdatasign = json.dumps(datasign)

        headers = {'content-type': 'application/json'}

        APISIGN_ENDPOINT = os.getenv("APISIGN_ENDPOINT") + "GetStatus/"
        url = APISIGN_ENDPOINT
        response = requests.get(url, data=sdatasign, headers=headers)
        responsebytes = response.content
        responsestr = responsebytes.decode("utf-8")
        strj = responsestr.replace("'", "\"")
        strj = remove_char(strj)
        responsejson = json.loads(strj)
        return responsejson

    @staticmethod
    def new_data(data: dict):
        try:
            def IntToHex(dian_code_int):
                dian_code_hex = '%02x' % dian_code_int
                return dian_code_hex

            def remove_char(s):
                return s[1: -1]

            IssuerParty = data["IssuerParty"]
            DocumentContacts = []
            if "DocumentContacts" in IssuerParty:
                DocumentContacts = IssuerParty["DocumentContacts"]
            Identification = IssuerParty["Identification"]

            AddressIssuer = {}
            if "Address" in IssuerParty:
                AddressIssuer = IssuerParty["Address"]

            datacity = CityController.get_by_code(AddressIssuer["CityCode"])
            datadepartment = DepartmentController.get_by_code(AddressIssuer["DepartmentCode"])

            postalCode = ""
            if "PostalCode" in AddressIssuer:
                postalCode = AddressIssuer["PostalCode"]

            IssuerParty_d = {
                'LegalType': IssuerParty["LegalType"],
                'ContactName': "",
                'ContactTelephone': "",
                'ContactTelefax': "",
                'ContactElectronicMail': IssuerParty["Email"],
                'ContactNote': "",
                'DocumentNumber': Identification["DocumentNumber"],
                'Name': IssuerParty["Name"],
                'CheckDigit': Identification["CheckDigit"],
                'DocumentType': Identification["DocumentType"],
                'CityCode': AddressIssuer["CityCode"],
                'CityName': datacity["name"],
                'PostalZone': postalCode,
                'Department': datadepartment["name"],
                'DepartmentCode': AddressIssuer["DepartmentCode"],
                'AddressLine': "",
                'Country': Identification["CountryCode"],
                'CommercialRegistration': "",
                'ResponsabilityTypes': "",
                'TaxScheme': [
                ]
            }

            if "Name" in DocumentContacts:
                IssuerParty_d["ContactName"] = DocumentContacts["Name"]
            if "Telephone" in DocumentContacts:
                IssuerParty_d["ContactTelephone"] = DocumentContacts["Telephone"]
            if "ContactTelefax" in DocumentContacts:
                IssuerParty_d['ContactTelefax'] = DocumentContacts["Telefax"]
            if "Email" in IssuerParty:
                IssuerParty_d['ContactElectronicMail'] = IssuerParty["Email"]
            if "ContactNote" in DocumentContacts:
                IssuerParty_d['ContactNote'] = DocumentContacts["Note"]
            if "DocumentNumber" in Identification:
                IssuerParty_d['DocumentNumber'] = Identification["DocumentNumber"]
            if "DocumentNumber" in DocumentContacts:
                IssuerParty_d['DocumentNumber'] = DocumentContacts["DocumentNumber"]
            if "Name" in IssuerParty:
                IssuerParty_d['Name'] = IssuerParty["Name"]
            if "CheckDigit" in Identification:
                IssuerParty_d['CheckDigit'] = Identification["CheckDigit"]
            if "DocumentType" in Identification:
                IssuerParty_d['DocumentType'] = Identification["DocumentType"]
            if "Email" in IssuerParty:
                IssuerParty_d['ContactElectronicMail'] = IssuerParty["Email"]
            if "PostalCode" in AddressIssuer:
                IssuerParty_d['PostalZone'] = AddressIssuer["PostalCode"]

            TaxScheme = []

            if "CityCode" in AddressIssuer:
                IssuerParty_d["CityCode"] = AddressIssuer["CityCode"]
            if "CityName" in datacity:
                IssuerParty_d["CityName"] = datacity["name"]
            if "PostalZone" in AddressIssuer:
                IssuerParty_d["PostalZone"] = AddressIssuer["PostalZone"]
            if "DepartmentName" in datadepartment:
                IssuerParty_d["Department"] = datadepartment["name"]
            if "DepartmentCode" in AddressIssuer:
                IssuerParty_d["DepartmentCode"] = AddressIssuer["DepartmentCode"]
            if "AddressLine" in AddressIssuer:
                IssuerParty_d["AddressLine"] = AddressIssuer["AddressLine"]
            if "CountryCode" in Identification:
                IssuerParty_d['Country'] = Identification["CountryCode"]
            if "CommercialRegistration" in IssuerParty:
                IssuerParty_d["CommercialRegistration"] = IssuerParty["CommercialRegistration"]
            if "TaxScheme" in IssuerParty:
                xtaxscheme = {
                    'TaxCategory': IssuerParty["TaxScheme"]
                }
                TaxScheme.append(xtaxscheme)
                IssuerParty_d["TaxScheme"] = TaxScheme
            if "ResponsabilityTypes" in IssuerParty:
                Resp = list()
                Resp = IssuerParty["ResponsabilityTypes"]
                sResp = ";".join(Resp)
                IssuerParty_d["ResponsabilityTypes"] = sResp

            BillingPeriod = data["BillingPeriod"]
            CustomerParty = data["CustomerParty"]
            Lines = data["Lines"]
            TaxSubtotalsC = data["TaxSubTotals"]
            WithholdingTaxSubTotalsC = []
            if "WithholdingTaxSubTotals" in data:
                WithholdingTaxSubTotalsC = data["WithholdingTaxSubTotals"]

            WithholdingTaxTotalsC = []
            if "WithholdingTaxTotals" in data:
                WithholdingTaxTotalsC = data["WithholdingTaxTotals"]

            TaxTotals = data["TaxTotals"]
            TaxTotalsC = data["TaxTotals"]
            Total = data["Total"]

            AddressCustomer = {}
            if "Address" in CustomerParty:
                AddressCustomer = CustomerParty["Address"]

            DocumentContacts0 = []
            if "DocumentContacts" in CustomerParty:
                DocumentContacts0 = CustomerParty["DocumentContacts"]

            IdentificationCustomer = CustomerParty["Identification"]
            datacityC = CityController.get_by_code(AddressCustomer["CityCode"])
            datadepartmentC = DepartmentController.get_by_code(AddressCustomer["DepartmentCode"])
            postalCodeC = ""
            if "PostalCode" in AddressCustomer:
                postalCodeC = AddressCustomer["PostalCode"]
            PaymentExchangeRate = {}
            if "PaymentExchangeRate" in data:
                PaymentExchangeRate = data["PaymentExchangeRate"]

            CustomerParty_d = {
                'LegalType': CustomerParty["LegalType"],
                'ContactName': '',
                'ContactTelephone': '',
                'ContactTelefax': '',
                'ContactElectronicMail': CustomerParty["Email"],
                'ContactNote': '',
                'DocumentNumber': IdentificationCustomer["DocumentNumber"],
                'Name': CustomerParty["Name"],
                'CheckDigit': IdentificationCustomer["CheckDigit"],
                'DocumentType': IdentificationCustomer["DocumentType"],
                'CityCode': '',
                'CityName': datacityC["name"],
                'PostalZone': postalCodeC,
                'Department': datadepartmentC["name"],
                'DepartmentCode': '',
                'AddressLine': '',
                'Country': IdentificationCustomer["CountryCode"],
                'CommercialRegistration': '',
                'ResponsabilityTypes': '',
                'TaxScheme': [
                ]
            }

            if "LegalType" in CustomerParty:
                CustomerParty_d["LegalType"] = CustomerParty["LegalType"]
            if "Email" in CustomerParty:
                CustomerParty_d["ContactElectronicMail"] = CustomerParty["Email"]
            if "DocumentNumber" in IdentificationCustomer:
                CustomerParty_d["DocumentNumber"] = IdentificationCustomer["DocumentNumber"]
            if "Name" in CustomerParty:
                CustomerParty_d["Name"] = CustomerParty["Name"]
            if "CheckDigit" in IdentificationCustomer:
                CustomerParty_d["CheckDigit"] = IdentificationCustomer["CheckDigit"]
            if "DocumentType" in IdentificationCustomer:
                CustomerParty_d["DocumentType"] = IdentificationCustomer["DocumentType"]
            if "CityName" in datacityC:
                CustomerParty_d["CityName"] = datacityC["name"]
            if "Department" in datadepartmentC:
                CustomerParty_d["Department"] = datadepartmentC["name"]
            if "Country" in IdentificationCustomer:
                CustomerParty_d["Country"] = IdentificationCustomer["CountryCode"]

            for DocumentContacts in DocumentContacts0:
                if "Telephone" in DocumentContacts:
                    CustomerParty_d["ContactTelephone"] = DocumentContacts["Telephone"]
                if "ContactTelefax" in DocumentContacts:
                    CustomerParty_d['ContactTelefax'] = DocumentContacts["Telefax"]
                if "ContactNote" in DocumentContacts:
                    CustomerParty_d['ContactNote'] = DocumentContacts["Note"]

            if "CityCode" in AddressCustomer:
                CustomerParty_d["CityCode"] = AddressCustomer["CityCode"]
            if "PostalZone" in AddressCustomer:
                CustomerParty_d["PostalZone"] = AddressCustomer["PostalZone"]
            if "DepartmentCode" in AddressCustomer:
                CustomerParty_d["DepartmentCode"] = AddressCustomer["DepartmentCode"]
            if "AddressLine" in AddressCustomer:
                CustomerParty_d["AddressLine"] = AddressCustomer["AddressLine"]
            if "CommercialRegistration" in CustomerParty:
                CustomerParty_d["CommercialRegistration"] = CustomerParty["CommercialRegistration"]
            if 'LegalType' in CustomerParty["LegalType"]:
                CustomerParty_d["LegalType"] = CustomerParty["LegalType"]

            if "TaxScheme" in CustomerParty:
                TaxScheme = [{
                    'TaxCategory': CustomerParty["TaxScheme"]

                }]
                CustomerParty_d["TaxScheme"] = TaxScheme
            if "ResponsabilityTypes" in CustomerParty:
                Resp = list()
                Resp = CustomerParty["ResponsabilityTypes"]
                sResp = ";".join(Resp)
                CustomerParty_d["ResponsabilityTypes"] = sResp

            withholdingtaxsubtotal_g = []

            withholdingtaxtotal_g = []

            taxsubtotals_g = []

            taxtotals_g = []

            for xtax in TaxSubtotalsC:
                nline_d = {
                    'TaxableAmount': "",
                    'TaxAmount': "",
                    'TaxPercentage': "",
                    'TaxCategory': "",
                    'TributeName': ""
                }
                if "TaxableAmount" in xtax:
                    nline_d["TaxableAmount"] = xtax["TaxableAmount"]
                if "TaxAmount" in xtax:
                    nline_d["TaxAmount"] = xtax["TaxAmount"]
                if "TaxPercentage" in xtax:
                    nline_d["TaxPercentage"] = xtax["TaxPercentage"]
                if "TaxCategory" in xtax:
                    nline_d["TaxCategory"] = xtax["TaxCategory"]
                if "TributeName" in xtax:
                    nline_d["TributeName"] = xtax["TributeName"]
                taxsubtotals_g.append(nline_d)

            for xtax in TaxTotalsC:
                nline_d = {
                    "TaxCategory": "",
                    "TaxAmount": ""
                }
                if "TaxCategory" in xtax:
                    nline_d["TaxCategory"] = xtax["TaxCategory"]
                if "TaxAmount" in xtax:
                    nline_d["TaxAmount"] = xtax["TaxAmount"]
                taxtotals_g.append(nline_d)

            for xwith in WithholdingTaxSubTotalsC:
                nline_d = {
                    "WithholdingTaxCategory": "",
                    "TaxAmount": "",
                    "TaxPercentage": ""
                }
                if "WithholdingTaxCategory" in xwith:
                    nline_d["WithholdingTaxCategory"] = xwith["WithholdingTaxCategory"]
                if "TaxAmount" in xwith:
                    nline_d["TaxAmount"] = xwith["TaxAmount"]
                if "TaxPercentage" in xwith:
                    nline_d["TaxPercentage"] = xwith["TaxPercentage"]
                withholdingtaxsubtotal_g.append(nline_d)

            for xwith in WithholdingTaxTotalsC:
                nline_d = {
                    "WithholdingTaxCategory": xwith["WithholdingTaxCategory"],
                    "TaxAmount": xwith["TaxAmount"]
                }
                withholdingtaxtotal_g.append(nline_d)

            item_d = []

            paymentmeans_d = []
            paymentmeans = data["PaymentMeans"]

            for line in Lines:
                taxsubtotal_d = []
                taxtotal_d = []
                InvoicePeriod = {}
                withholding_taxsubtotal_d = []
                withholding_taxtotal_d = []
                withholdingtaxsubtotal = []
                withholdingtaxtotal = []
                taxsubtotal = line["TaxSubTotals"]
                taxtotal = line["TaxTotals"]
                item = data["Lines"]

                if "WithholdingTaxSubTotals" in line:
                    withholdingtaxsubtotal = line["WithholdingTaxSubTotals"]
                if "WithholdingTaxTotals" in line:
                    withholdingtaxtotal = line["WithholdingTaxTotals"]
                if "InvoicePeriod" in line:
                    InvoicePeriod = line["InvoicePeriod"]

                for xtax in taxsubtotal:
                    nline_d = {
                        "TaxableAmount": "",
                        "TaxCategory": "",
                        "TaxPercentage": "",
                        "TaxAmount": ""
                    }
                    if "TaxableAmount" in xtax:
                        nline_d["TaxableAmount"] = xtax["TaxableAmount"]
                    if "TaxCategory" in xtax:
                        nline_d["TaxCategory"] = xtax["TaxCategory"]
                    if "TaxPercentage" in xtax:
                        nline_d["TaxPercentage"] = xtax["TaxPercentage"]
                    if "TaxAmount" in xtax:
                        nline_d["TaxAmount"] = xtax["TaxAmount"]
                    taxsubtotal_d.append(nline_d)

                for xtax in taxtotal:
                    nline_d = {
                        "TaxCategory": "",
                        "TaxAmount": "",
                        "RoundingAmount": ""
                    }
                    if "TaxCategory" in xtax:
                        nline_d["TaxCategory"] = xtax["TaxCategory"]
                    if "TaxAmount" in xtax:
                        nline_d["TaxAmount"] = xtax["TaxAmount"]
                    if "RoundingAmount" in xtax:
                        nline_d["RoundingAmount"] = xtax["RoundingAmount"]
                    taxtotal_d.append(nline_d)
                xit = line
                # comienzo lineas
                if True:
                    taxsubtotallines = line["TaxSubTotals"]
                    taxtotalslines = line["TaxTotals"]
                    itemlines = xit["Item"]

                    taxtotals_i = []

                    taxsubtotals_i = []
                    if "BaseUnitMeasure" in xtax:
                        nline_d["BaseUnitMeasure"] = xtax["BaseUnitMeasure"]
                    if "PerUnitAmount" in xtax:
                        nline_d["PerUnitAmount"] = xtax["PerUnitAmount"]
                    if "BaseUnitMeasure" in xtax:
                        nline_d["BaseUnitMeasure"] = xtax["BaseUnitMeasure"]

                    for xtax in taxsubtotallines:
                        nline_d = {
                            'TaxableAmount': "",
                            'TaxAmount': "",
                            'BaseUnitMeasure': "",
                            'QuantityUnitOfMeasure': "1",
                            'PerUnitAmount': "",
                            'TaxPercentage': "",
                            'TaxCategory': "",
                            'TributeName': ""
                        }
                        if "TaxableAmount" in xtax:
                            nline_d["TaxableAmount"] = xtax["TaxableAmount"]
                        if "TaxAmount" in xtax:
                            nline_d["TaxAmount"] = xtax["TaxAmount"]
                        if "BaseUnitMeasure" in xtax:
                            nline_d["BaseUnitMeasure"] = xtax["BaseUnitMeasure"]
                        if "QuantityUnitOfMeasure" in xtax:
                            nline_d["QuantityUnitOfMeasure"] = xtax["QuantityUnitOfMeasure"]
                        if "PerUnitAmount" in xtax:
                            nline_d["PerUnitAmount"] = xtax["PerUnitAmount"]
                        if "TaxPercentage" in xtax:
                            nline_d["TaxPercentage"] = xtax["TaxPercentage"]
                        if "TaxCategory" in xtax:
                            nline_d["TaxCategory"] = xtax["TaxCategory"]
                        if "TributeName" in xtax:
                            nline_d["TributeName"] = xtax["TributeName"]
                        taxsubtotals_i.append(nline_d)

                    for xtax in taxtotalslines:
                        nline_d = {
                            'TaxCategory': "",
                            'TaxAmount': ""
                        }
                        if "TaxCategory" in xtax:
                            nline_d["TaxCategory"] = xtax["TaxCategory"]
                        if "TaxAmount" in xtax:
                            nline_d["TaxAmount"] = xtax["TaxAmount"]
                        taxtotals_i.append(nline_d)

                for xwith in withholdingtaxsubtotal:
                    nline_d = {
                        "TaxCategory": "",
                        "TaxPercentage": "",
                        "TaxableAmount": "",
                        "TaxAmount": ""
                    }
                    if "TaxCategory" in xwith:
                        nline_d["TaxCategory"] = xwith["TaxCategory"]
                    if "TaxPercentage" in xwith:
                        nline_d["TaxPercentage"] = xwith["TaxPercentage"]
                    if "TaxableAmount" in xwith:
                        nline_d["TaxableAmount"] = xwith["TaxableAmount"]
                    if "TaxAmount" in xwith:
                        nline_d["TaxAmount"] = xwith["TaxAmount"]
                    withholding_taxsubtotal_d.append(nline_d)

                for xwith in withholdingtaxtotal:
                    nline_d = {
                        "TaxCategory": "",
                        "TaxAmount": "",
                        "TaxableAmount": ""
                    }
                    if "TaxCategory" in xwith:
                        nline_d["TaxCategory"] = xwith["TaxCategory"]
                    if "TaxAmount" in xwith:
                        nline_d["TaxAmount"] = xwith["TaxAmount"]
                    if "TaxableAmount" in xwith:
                        nline_d["TaxableAmount"] = xwith["TaxableAmount"]
                    withholding_taxtotal_d.append(nline_d)

                standardItemIdentifications = [
                    {
                        'IdStandard': itemlines["SellerItemIdentification"],
                        'SchemaId': '999',
                        'SchemaName': '31',
                        'SchemaAgencyId': '1'
                    }
                ]
                if "SellerItemIdentification" in itemlines:
                    standardItemIdentifications[0]["IdStandard"] = itemlines["SellerItemIdentification"]
                if "SchemaId" in itemlines:
                    standardItemIdentifications[0]["SchemaId"] = itemlines["SchemaId"]
                if "SchemaName" in itemlines:
                    standardItemIdentifications[0]["SchemaName"] = itemlines["SchemaName"]
                if "SchemaAgencyId" in itemlines:
                    standardItemIdentifications[0]["SchemaAgencyId"] = itemlines["SchemaAgencyId"]
                nline_d = {
                    'Number': "",
                    'Quantity': "",
                    'BaseQuantity': "",
                    'QuantityUnitOfMeasure': "",
                    'LineExtensionAmount': "",
                    'PriceAmount': "",
                    'CommercialPrice': "",
                    'PriceTypeCode': '01',
                    'InvoicePeriod': InvoicePeriod,
                    'TaxSubTotalLines': taxsubtotals_i,
                    'TaxTotals': taxtotals_i,
                    "WithHoldingTaxSubTotalLines": withholding_taxsubtotal_d,
                    'WithHoldingTaxTotalLines': withholding_taxtotal_d,
                    'Description': "",
                    'PackSizeNumeric': "",
                    'BrandName': "",
                    'ModelName': "",
                    'SellerId': "",
                    'StandardItemIdentifications': standardItemIdentifications
                }
                if "Number" in xit:
                    nline_d["Number"] = xit["Number"]
                if "Quantity" in xit:
                    nline_d["Quantity"] = xit["Quantity"]
                if "UnitsPerPackage" in itemlines:
                    nline_d["BaseQuantity"] = itemlines["UnitsPerPackage"]
                if "QuantityUnitOfMeasure" in xit:
                    nline_d["QuantityUnitOfMeasure"] = xit["QuantityUnitOfMeasure"]
                if "GrossAmount" in xit:
                    nline_d["LineExtensionAmount"] = xit["GrossAmount"]
                if "UnitPrice" in xit:
                    nline_d["PriceAmount"] = xit["UnitPrice"]
                if "CommercialPrice" in xit:
                    nline_d["CommercialPrice"] = xit["CommercialPrice"]
                if "PriceTypeCode" in xit:
                    nline_d["PriceTypeCode"] = xit["PriceTypeCode"]
                if "Description" in itemlines:
                    nline_d["Description"] = itemlines["Description"]
                if "PackSizeNumeric" in itemlines:
                    nline_d["PackSizeNumeric"] = itemlines["UnitsPerPackage"]
                if "BrandName" in itemlines:
                    nline_d["BrandName"] = itemlines["BrandName"]
                if "ModelName" in itemlines:
                    nline_d["ModelName"] = itemlines["ModelName"]
                if "SellerItemIdentification" in itemlines:
                    nline_d["SellerId"] = itemlines["SellerItemIdentification"]
                item_d.append(nline_d)

            Total_d = {
                'LineExtensionAmount': "",
                'TaxExclusiveAmount': "",
                'TaxInclusiveAmount': "",
                'AllowanceTotalAmount': "",
                'ChargeTotalAmount': "",
                'PrePaidAmount': "",
                'PayableAmount': "",
                'TotalIva': '0.00',
                'TotalTaxConsume': '0.00',
                'TotalIca': '0.00'
            }
            if "GrossAmount" in Total:
                Total_d["LineExtensionAmount"] = Total["GrossAmount"]
            if "GrossAmount" in Total:
                Total_d["TaxExclusiveAmount"] = Total["GrossAmount"]
            if "TotalBillableAmount" in Total:
                Total_d["TaxInclusiveAmount"] = Total["TotalBillableAmount"]
            if "AllowanceTotalAmount" in Total:
                Total_d["AllowanceTotalAmount"] = Total["AllowanceTotalAmount"]
            if "ChargesTotalAmount" in Total:
                Total_d["ChargeTotalAmount"] = Total["ChargesTotalAmount"]
            if "PrePaidAmount" in Total:
                Total_d["PrePaidAmount"] = Total["PrePaidTotalAmount"]
            if "PayableAmount" in Total:
                Total_d["PayableAmount"] = Total["PayableAmount"]
            if "TotalIva" in Total:
                Total_d["TotalIva"] = Total["TotalIva"]
            if "TotalIca" in Total:
                Total_d["TotalIca"] = Total["TotalIca"]
            if "TotalTaxConsume" in Total:
                Total_d["TotalTaxConsume"] = Total["TotalTaxConsume"]

            DocumentReferences = []
            if "DocumentReferences" in data:
                DocumentReferences = data["DocumentReferences"]

            OrderReferenceId = ""
            OrderReferenceIssueDte = ""
            CreditNoteId = ""
            CreditNoteIssueDate = ""
            CreditNoteCude = ""
            DebitNoteId = ""
            DebitNoteIssueDate = ""
            DebitNoteCude = ""
            DespatchDocumentReferenceId = ""
            DespatchDocumentIssueDate = ""
            ReceiptDocumentReferenceId = ""
            ReceiptDocumentIssueDate = ""
            AdditionalDocumentReferenceId = ""
            AdditionalDocumentIssueDate = ""
            AdditionalDocumentTypeCode = ""
            AdditionalTypeDescription = ""

            for xref in DocumentReferences:
                if xref["Type"] == "O":
                    if "DocumentReferred" in xref:
                        OrderReferenceId = xref["DocumentReferred"]
                    if "IssueDate" in xref:
                        OrderReferenceIssueDte = xref["IssueDate"]

                if xref["Type"] == "D":
                    if "DocumentReferred" in xref:
                        DespatchDocumentReferenceId = xref["DocumentReferred"]
                    if "IssueDate" in xref:
                        DespatchDocumentIssueDate = xref["IssueDate"]

                if xref["Type"] == "R":
                    if "DocumentReferred" in xref:
                        ReceiptDocumentReferenceId = xref["DocumentReferred"]
                    if "IssueDate" in xref:
                        ReceiptDocumentIssueDate = xref["IssueDate"]

                if xref["Type"] == "A":
                    if "DocumentReferred" in xref:
                        AdditionalDocumentReferenceId = xref["DocumentReferred"]
                    if "IssueDate" in xref:
                        AdditionalDocumentIssueDate = xref["IssueDate"]
                    AdditionalDocumentTypeCode = xref["OtherReferenceTypeId"]

                if xref["Type"] == "NC":
                    if "DocumentReferred" in xref:
                        CreditNoteId = xref["DocumentReferred"]
                    if "IssueDate" in xref:
                        CreditNoteIssueDate = xref["IssueDate"]
                    if "DocumentReferredCUFE" in xref["DocumentReferredCUFE"]:
                        CreditNoteCude = xref["DocumentReferredCUFE"]

                if xref["Type"] == "ND":
                    if "DocumentReferred" in xref:
                        DebitNoteId = xref["DocumentReferred"]
                    if "IssueDate" in xref:
                        DebitNoteIssueDate = xref["IssueDate"]
                    if "DocumentReferredCUFE" in xref["DocumentReferredCUFE"]:
                        DebitNoteCude = xref["DocumentReferredCUFE"]

            NoteDocument = ""
            if "NoteDocument" in data:
                NoteDocument = data["NoteDocument"]

            reason_credit = ''
            if 'ReasonCredit' in data:
                reason_credit = data['ReasonCredit']

            reason_debit = ''
            if 'ReasonDebit' in data:
                reason_debit = data['ReasonDebit']

            pdf = {}
            if "Pdf" in data:
                pdf = data["Pdf"]

            Additional = data["Additional"]

            data = {
                'CUDE': Additional["CUDE"],
                'IssuerNit': Identification["DocumentNumber"],
                'DocType': data["DocType"],
                'SeriePrefix': data["SeriePrefix"],
                'SerieNumber': data["SerieNumber"],
                'InvoiceAuthorization': BillingPeriod["InvoiceAuthorization"],
                'Contingency': Additional["Contingency"],
                'SendEmail': Additional["SendEmail"],
                'StartDate': BillingPeriod["StartDate"],
                'EndDate': BillingPeriod["EndDate"],
                'FromBillingPeriod': BillingPeriod["From"],
                'ToBillingPeriod': BillingPeriod["To"],
                'DianSoftwareId': Additional["DianSoftwareId"],
                'DianPin': Additional["DianPin"],
                'DianTechnicalKey': Additional["DianTechnicalKey"],
                'DianTestSetId': Additional["DianTestSetId"],
                'Reason': '',
                'OrderReferenceId': OrderReferenceId,
                'OrderReferenceIssueDate': OrderReferenceIssueDte,
                'CreditNoteId': CreditNoteId,
                'CreditNoteIssueDate': CreditNoteIssueDate,
                'CreditNoteCude': CreditNoteCude,
                'DebitNoteId': DebitNoteId,
                'DebitNoteIssueDate': DebitNoteIssueDate,
                'DebitNoteCude': DebitNoteCude,
                'DespatchDocumentReferenceId': DespatchDocumentReferenceId,
                'DespatchDocumentIssueDate': DespatchDocumentIssueDate,
                'ReceiptDocumentReferenceId': ReceiptDocumentReferenceId,
                'ReceiptDocumentIssueDate': ReceiptDocumentIssueDate,
                'AdditionalDocumentReferenceId': AdditionalDocumentReferenceId,
                'AdditionalDocumentIssueDate': AdditionalDocumentIssueDate,
                'AdditionalDocumentTypeCode': AdditionalDocumentTypeCode,
                'IssuerParty': IssuerParty_d,
                'ProfileExecutionId': Additional["ProfileExecutionId"],
                'IssueDate': data["IssueDate"],
                'IssueTime': data["IssueTime"],
                'DueDate': data["DueDate"],
                'NoteDocument': NoteDocument,
                'Currency': data["Currency"],
                'OperationType': data["OperationType"],
                'CustomerParty': CustomerParty_d,
                'ActualDeliveryDate': data["DeliveryDate"],
                'ActualDeliveryTime': data["DeliveryTime"],
                'TaxTotals': data["TaxTotals"],
                'WithHoldingTaxSubTotals': withholdingtaxsubtotal_g,
                'WithHoldingTaxTotals': withholdingtaxtotal_g,
                'PaymentMeans': paymentmeans_d,
                'PaymentExchangeRate': PaymentExchangeRate,
                'LineExtensionAmount': Total_d["LineExtensionAmount"],
                'TaxExclusiveAmount': Total_d["TaxExclusiveAmount"],
                'TaxInclusiveAmount': Total_d["TaxInclusiveAmount"],
                'AllowanceTotalAmount': Total_d["AllowanceTotalAmount"],
                'ChargeTotalAmount': Total_d["ChargeTotalAmount"],
                'PrePaidAmount': Total_d["PrePaidAmount"],
                'PayableAmount': Total_d["PayableAmount"],
                'TotalIva': Total_d["TotalIva"],
                'TotalTaxConsume': Total_d["TotalTaxConsume"],
                'TotalIca': Total_d["TotalIca"],
                'TaxSubTotals': taxsubtotals_g,
                'DocumentReferences': DocumentReferences,
                'Lines': item_d,
                'Pdf': pdf
            }

            if reason_credit != '':
                data['ReasonCredit'] = reason_credit

            if reason_debit != '':
                data['ReasonDebit'] = reason_debit

            xml_dian = NotesModel.Create_xml_notes(data)
            xissuer = str.zfill(data["IssuerNit"], 10)
            NumberSend = 1
            ActualYear = time.strftime('%Y')
            # grabar primero y obtener numero de envio
            sends = {
                'IssuerNit': data["IssuerNit"],
                'IssuerName': IssuerParty["Name"],
                'DocType': data["DocType"],
                'Prefix': data["SeriePrefix"],
                'SerieNumber': data["SerieNumber"],
                'YearSend': ActualYear,
                'NumberSend': NumberSend,
            }
            response = NotesSendsModel.new_data(sends)
            dataresponse = response["data"]
            NumberSend = dataresponse["NumberSend"]
            IdSend = dataresponse["Id"]
            xnumbersend = IntToHex(NumberSend)
            snumber = str.zfill(xnumbersend, 8)
            filename = data["DocType"] + xissuer + "000" + snumber

            # verificar si no existe carpeta del cliente y crearla
            path_issuer = config.Config.PATH_DOCS + xissuer + "/"
            import os
            if not Path(path_issuer).is_dir():
                # crear carppeta
                os.mkdir(path_issuer)
            path_issuer = config.Config.PATH_DOCS + xissuer + "/" + "invoice-note/"
            file = path_issuer
            path_issuer = Path(file)
            import os
            if not path_issuer.is_dir():
                # crear carppeta
                os.mkdir(path_issuer)

            save_path_file = str(path_issuer) + "/" + filename + ".xml"

            with open(save_path_file, "w") as f:
                f.write(xml_dian)

            with open(save_path_file, "rb") as f:
                dataxml = f.read()
            dataxml_encode = b64encode(dataxml).decode("utf-8")

            filename_pdf = data["DocType"] + xissuer + "000" + snumber
            filename_json = "js" + xissuer + "000" + snumber
            save_path_file_pdf = str(path_issuer) + "/" + filename_pdf + ".pdf"
            save_path_file_json = str(path_issuer) + "/" + filename_json + ".json"
            with open(save_path_file_json, "w") as f:
                f.write(json.dumps(data))

            pdf = data["Pdf"]
            if len(pdf) != 0:
                bpdf = b64decode(pdf["Pdf"])
                bytesio_o = BytesIO(bpdf)
                with open(save_path_file_pdf, "wb") as f:
                    f.write(bytesio_o.getbuffer())

            # firmarlo
            datacerts = CertsController.get_by_nit(data["IssuerNit"])
            if not datacerts:
                response = {
                    'statusCode': 404,
                    'message': 'No se encontraron certificados para el emisor',
                }
                return make_response(jsonify(response), 404)
            cert_encode = datacerts["Format"]

            # sending post request and saving response as response object

            datasign = {
                'Id': data["DianTestSetId"],
                "Nit": data["IssuerNit"],
                'filename': filename,
                'contentxml': dataxml_encode,
                'keycert': datacerts["Key"],
                'contentcert': cert_encode,
                'DocType': data["DocType"]
            }
            sdatasign = json.dumps(datasign)

            headers = {'content-type': 'application/json'}
            if Additional["ProfileExecutionId"] == "2":
                APISIGN_ENDPOINT = os.getenv("APISIGN_ENDPOINT") + "SendTestSetAsync/"
            else:
                APISIGN_ENDPOINT = os.getenv("APISIGN_ENDPOINT") + "SendBillAsync/"
            url = APISIGN_ENDPOINT
            response = requests.get(url, data=sdatasign, headers=headers)
            responsebytes = response.content
            responsestr = responsebytes.decode("utf-8")
            strj = responsestr.replace("'", "\"")
            strj = remove_char(strj)
            responsejson = json.loads(strj)  # error respuesta dian messages key xmldoc xmlrespuesta
            xmlsign = b64decode(responsejson["xmldoc"]).decode("utf-8")
            respuestadian = responsejson["respuestadian"]
            xmlrespuesta = responsejson["xmlrespuesta"]
            key = responsejson["key"]
            messages = responsejson["messages"]

            if "Regla: 90" in messages:
                find = NotesSendsModel.get_by_number(Nit=data["IssuerNit"], SeriePrefix=data["SeriePrefix"],
                                                     SerieNumber=data["SerieNumber"], DocType=data["DocType"],
                                                     export=True)
                if find:
                    IdSend = find["Id"]

                # respuesta modificada para el consumo del api desde pymes+ v2
                response_api = {
                    'isValid': True,
                    'errors': {
                        'message': messages
                    },
                    'resultCode': 200,
                    'resultData': {
                        'id': IdSend,
                        'content': respuestadian
                    }
                }
                return response_api

            # enviar a la dian

            # llenar tabla sends
            Customer = data["CustomerParty"]

            if data["SendEmail"]:
                sends_ad = {
                    'IssuerNit': data["IssuerNit"],
                    'DocType': "AD",
                    'Prefix': data["SeriePrefix"],
                    'SerieNumber': data["SerieNumber"],
                    'YearSend': ActualYear,
                }
                response2 = NotesSendsModel.new_data(sends_ad)
                dataresponse2 = response2["data"]
                NumberContainer = dataresponse2["NumberSend"]

                sends = {
                    'Id': IdSend,
                    'IssuerNit': data["IssuerNit"],
                    'DocType': data["DocType"],
                    'Prefix': data["SeriePrefix"],
                    'SerieNumber': data["SerieNumber"],
                    'YearSend': ActualYear,
                    'NumberSend': NumberSend,
                    'DianResolution': data["InvoiceAuthorization"],
                    'IdSoftware': data["DianSoftwareId"],
                    'ClientNit': Customer["DocumentNumber"],
                    'ClientName': Customer["Name"],
                    'ClientEmail': CustomerParty["Email"],
                    'DateSend': data["IssueDate"],
                    'HourSend': data["IssueTime"],
                    'DianResponse': respuestadian,
                    'DianResponseErrors': messages,
                    'DianXml': filename + ".xml",
                    'DianXmlAppResponse': xmlrespuesta,
                    'Cufe': data["CUDE"],
                    'TrackIdDian': key,
                    'JsonReceived': "",
                    'Status': '',
                    'Total': Total_d["PayableAmount"]

                }

                xml_ad = NotesModel.Create_xml_ad(data, sends, NumberContainer)
                xnumbersend = IntToHex(NumberContainer)
                snumber = str.zfill(xnumbersend, 8)
                filename_ad = "ad" + xissuer + "000" + snumber
                filename_zip = "z" + xissuer + "000" + snumber

                save_path_file_ad = str(path_issuer) + "/" + filename_ad + ".xml"
                save_path_file_zip = str(path_issuer) + "/" + filename_zip + ".zip"

                with open(save_path_file_ad, "w") as f:
                    f.write(xml_ad)

                # Comprimir archivo
                with ZipFile(save_path_file_zip, mode='w') as file:
                    file.write(save_path_file_ad, arcname=os.path.basename(save_path_file_ad))
                    file.write(save_path_file_pdf, arcname=os.path.basename(save_path_file_pdf))

            # Enviar xml a correo
            messageemail = ""
            if data["SendEmail"]:
                try:
                    # Iniciamos los parámetros del script
                    remitente = os.getenv('EMAIL_DOCS')
                    destinatarios = [CustomerParty["Email"]]
                    if data["DocType"] == "NC":
                        code = "91"
                    else:
                        code = "92"
                    asunto = data["IssuerNit"] + ";" + IssuerParty["Name"] + ";" + \
                             data["SeriePrefix"] + data["SerieNumber"] + ";" + code + ";" + \
                             IssuerParty["Name"] + ";" + "Documentos Electronicos"
                    cuerpo = 'Estimado cliente, se informa recepcion de nota ' + data["SeriePrefix"] + \
                             data["SerieNumber"]
                    ruta_adjunto = save_path_file_zip

                    # Creamos el objeto mensaje
                    mensaje = MIMEMultipart()

                    # Establecemos los atributos del mensaje
                    mensaje['From'] = remitente
                    mensaje['To'] = ", ".join(destinatarios)
                    mensaje['Subject'] = asunto

                    # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
                    mensaje.attach(MIMEText(cuerpo, 'plain'))

                    # Abrimos el archivo que vamos a adjuntar
                    archivo_adjunto = open(ruta_adjunto, 'rb')

                    # Creamos un objeto MIME base
                    adjunto_MIME = MIMEBase('application', 'octet-stream')
                    # Y le cargamos el archivo adjunto
                    adjunto_MIME.set_payload(archivo_adjunto.read())
                    # Codificamos el objeto en BASE64
                    encoders.encode_base64(adjunto_MIME)
                    # Agregamos una cabecera al objeto
                    adjunto_MIME.add_header('Content-Disposition', "attachment; filename= Documento Electrònico")
                    # Y finalmente lo agregamos al mensaje
                    mensaje.attach(adjunto_MIME)

                    # Creamos la conexión con el servidor
                    sesion_smtp = smtplib.SMTP(os.getenv('EMAIL_SMTP_DOCS'), int(os.getenv('EMAIL_PORT_DOCS')))

                    # Ciframos la conexión
                    sesion_smtp.starttls()

                    # Iniciamos sesión en el servidor
                    sesion_smtp.login(os.getenv('EMAIL_DOCS'), os.getenv('EMAIL_KEY_DOCS'))

                    # Convertimos el objeto mensaje a texto
                    texto = mensaje.as_string()

                    # Enviamos el mensaje

                    sesion_smtp.sendmail(remitente, destinatarios, texto)
                except Exception as e:

                    messageemail = e
                else:
                    messageemail = 'Correo enviado'

                    # Cerramos la conexión
                    sesion_smtp.quit()

            if "Procesado" in respuestadian:
                Status = "1"
            else:
                Status = "0"

            sends = {
                'Id': IdSend,
                'IssuerNit': data["IssuerNit"],
                'DocType': data["DocType"],
                'Prefix': data["SeriePrefix"],
                'YearSend': ActualYear,
                'NumberSend': NumberSend,
                'DianResolution': data["InvoiceAuthorization"],
                'IdSoftware': data["DianSoftwareId"],
                'ClientNit': Customer["DocumentNumber"],
                'ClientName': Customer["Name"],
                'ClientEmail': CustomerParty["Email"],
                'DateSend': data["IssueDate"],
                'HourSend': data["IssueTime"],
                'DianResponse': respuestadian,
                'DianResponseErrors': messages,
                'DianXml': filename + ".xml",
                'DianXmlAppResponse': xmlrespuesta,
                'Cufe': data["CUDE"],
                'TrackIdDian': key,
                'JsonReceived': filename_json + ".json",
                'MessageEmail': messageemail,
                'Status': Status,
                'Total': Total_d["PayableAmount"]

            }

            response = NotesSendsModel.update_data(sends)
            responsedata = response["data"]
            if "Procesado" in respuestadian:
                IsValid = True
            else:
                IsValid = False

            # respuesta modificada para el consumo del api desde pymes+ v2
            response_api = {
                'isValid': IsValid,
                'errors': {
                    'message': messages
                },
                'resultCode': 200 if IsValid else 400,
                'resultData': {
                    'id': responsedata['Id'],
                    'content': respuestadian,
                    'CUDE': responsedata['Cufe']
                }
            }
            return response_api

        except Exception as e:
            import os, sys
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('object={0}, lineno={1}'.format(fname, exc_tb.tb_lineno))
            raise InternalServerError(e)

    @staticmethod
    def update_data(data: dict):
        try:
            update_data = NotesModel.get_by_id(id=data['id'], export=False)
            if not update_data:
                return NotFound('Los datos ingresados no pertenecen o no son validos para el registro consultado')
            update_data = NotesModel.import_data(update_data, data=data)
            NotesModel.save(update_data, create=True, commit=True)
            response = {
                'data': NotesModel.export_data(update_data),
                'statusCode': 200,
                'message': 'Registro modificado correctamente'
            }
            return response
        except Exception as e:
            print('Error: {er}'.format(er=e))
            raise

