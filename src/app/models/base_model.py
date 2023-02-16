# -*- coding: utf-8 -*-
#########################################################
from datetime import datetime

from app import db
from app.exception import InternalServerError


class BaseModel(db.Model):
    __abstract__ = True

    Id = db.Column(db.Integer, primary_key=True, nullable=False)
    CreateDate = db.Column(db.DateTime, default=db.func.now(), comment='Fecha de creación')
    UpdateDate = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), comment='Fecha de Modificación')

    def delete(self, commit: bool = False):
        try:
            db.session.delete(self)
            if commit:
                db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            raise InternalServerError(e)

    def save(self, create: bool = False, commit: bool = False):
        try:
            if create:
                self.CreateDate = datetime.now()
            self.UpdateDate = datetime.now()
            db.session.add(self)
            db.session.flush()
            if commit:
                db.session.commit()
            return self
        except Exception as e:
            print(e)
            db.session.rollback()
            raise InternalServerError(e)
