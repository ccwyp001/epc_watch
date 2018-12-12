from ..extensions import db, SLBigInteger


class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(SLBigInteger, primary_key=True)
    brand = db.Column(db.String(100))
    manufacturer = db.Column(db.String(100))
    model = db.Column(db.String(100))
    displacement = db.Column(db.String(100))
    years = db.Column(db.String(100))
    mode = db.Column(db.String(100))

    __table_args__ = (
        db.UniqueConstraint('brand',
                            'manufacturer',
                            'model',
                            'displacement',
                            'years',
                            'mode',
                            name='we_are_special'),
    )

    def __repr__(self):
        return '<Vehicles %r>' % self.id

    def display(self):
        return {'vehicle_id': self.id,
                'displacement': self.displacement,
                'years': self.years,
                'mode': self.mode}

