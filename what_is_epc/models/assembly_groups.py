from ..extensions import db, SLBigInteger


class AssemblyGroups(db.Model):
    __tablename__ = 'assembly_groups'

    id = db.Column(db.String(50), primary_key=True)
    outer_teething_wheel = db.Column(db.String(100))
    inner_teething_wheel = db.Column(db.String(100))
    length = db.Column(db.String(100))
    abs = db.Column(db.String(100))
    material_number = db.Column(db.String(100))

    def __repr__(self):
        return '<AssemblyGroups %r>' % self.id

    def display(self):
        return {"outer_teething_wheel": self.outer_teething_wheel,
                "inner_teething_wheel": self.inner_teething_wheel,
                "length": self.length,
                "abs": self.abs,
                "material_number": self.material_number}


class VehicleAssemblyGroups(db.Model):
    __tablename__ = 'vehicle_assembly_groups'

    id = db.Column(SLBigInteger, primary_key=True)
    vehicle_id = db.Column(SLBigInteger, db.ForeignKey('vehicles.id', ondelete='CASCADE'),
                           nullable=False)
    vehicle = db.relationship('Vehicles',
                              backref=db.backref('va_groups', cascade="delete", lazy='dynamic'))

    assembly_group_id = db.Column(db.String(50),
                                  db.ForeignKey('assembly_groups.id', ondelete='CASCADE'),
                                  nullable=False)
    assembly_group = db.relationship('AssemblyGroups',
                                     backref=db.backref('va_groups', cascade="delete",
                                                        lazy='dynamic'))
    side = db.Column(db.String(50))

    oe_numbers = db.Column(db.String(50))

    other_numbers = db.Column(db.String(50))

    __table_args__ = (
        db.UniqueConstraint('vehicle_id',
                            'assembly_group_id',
                            'side',
                            name='we_are_special'),
    )

    def __repr__(self):
        return '<VehicleAssemblyGroups %r>' % self.id

    def display(self):
        return {'assembly_id': self.assembly_group_id,
                'side': self.side}
