# -*- coding: utf-8 -*-
#########################################################
from app import app
from flask_restx import Api
from app.routes.docs.certs.certs_route import api as ns_certs
from app.routes.docs.invoices.invoices_route import api as ns_invoices
from app.routes.docs.supportdoc.supportdoc_route import api as ns_supportdocs
from app.routes.sends_docs.payrollsends.payrollsends_route import api as ns_payrollsends
from app.routes.docs.notes.notes_route import api as ns_notes
from app.routes.sends_docs.notessends.notessends_route import api as ns_notessends
from app.routes.sends_docs.sends.sends_route import api as ns_sendsinvoices
from app.routes.sends_docs.dssends.dssends_route import api as ns_dssends
from app.routes.sends_docs.dsnotessends.dsnotessends_route import api as ns_dsnotessends
from app.routes.docs.payroll.payroll_route import api as ns_payroll
from app.routes.security.application_route import api as routes_applications
from app.routes.security.auth_route import api as routes_auth

api = Api(
    version='1.0.0',
    title='Electronic documents API',
    description='API for electronic documents',
    prefix='/api/v1'
)

api.add_namespace(routes_auth, path='/oauth')
api.add_namespace(ns_certs, path='/certs')
api.add_namespace(ns_invoices, path='/invoices')
api.add_namespace(ns_supportdocs, path='/supportdocs')
api.add_namespace(ns_payroll, path='/payroll')
api.add_namespace(ns_notes, path='/notes')
api.add_namespace(ns_notessends, path='/notessends')
api.add_namespace(ns_sendsinvoices, path='/sendsinvoices')
api.add_namespace(ns_payrollsends, path='/payrollsends')
api.add_namespace(ns_dssends, path='/dssends')
api.add_namespace(ns_dsnotessends, path='/dsnotessends')
api.add_namespace(routes_applications, path='/applications')

api.init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=5001,
            debug=False)
