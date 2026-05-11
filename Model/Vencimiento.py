from database import db

class Vencimiento(db.Model):
    __tablename__ = "Vencimientos"

    Id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100), nullable=False)
    FechaVencimiento = db.Column(db.Date, nullable=False)
    Avisado = db.Column(db.Boolean, default=False)

    IdUsuario = db.Column(
        db.Integer,
        db.ForeignKey("Usuario.Id"),
        nullable=False
    )

    __table_args__ = (
    db.UniqueConstraint('Nombre', 'IdUsuario', name='uq_vencimiento_usuario'),
    )