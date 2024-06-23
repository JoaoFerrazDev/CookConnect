from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    db.app = app
    db.init_app(app)


class Encomenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilizadorId = db.Column(db.Integer)
    aberta = db.Column(db.Boolean, default=False)
    linhas_encomenda = db.relationship('EncomendaLinha', backref='linhaEncomenda')

    def serializar(self):
        return {
            'utilizadorId': self.utilizadorId,
            'aberta': self.aberta,
            'linhas_encomenda': [x.serializar() for x in self.linhas_encomenda]
        }


class EncomendaLinha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encomendaId = db.Column(db.Integer, db.ForeignKey('encomenda.id'))
    artigoId = db.Column(db.Integer)
    quantidade = db.Column(db.Float)

    def __init__(self, artigoId, quantidade):
        self.artigoId = artigoId
        self.quantidade = quantidade

    def serializar(self):
        return {
            'artigo': self.artigoId,
            'quantidade': self.quantidade
        }