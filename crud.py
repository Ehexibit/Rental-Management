from sqlalchemy.orm import Session
from model import Tenant, Biller, BillRecord  # Replace 'your_module' with the actual module where Tenant is defined

#CRUD OPERATION FOR TENANT START HERE
def create_tenant(db: Session, unique_id: int, name: str, lastname: str, email: str, duedate: str, paiddate: str):
    new_tenant = Tenant(
        unique_id=unique_id,
        name=name,
        lastname=lastname,
        email=email,
        duedate=duedate,
        paiddate=paiddate
    )
    db.add(new_tenant)
    db.commit()

def get_tenant_by_id(db: Session, tenant_id: int):
    return db.query(Tenant).filter(Tenant.id == tenant_id).first()

def get_tenant_by_unique_id(db: Session, tenant_id: int):
    return db.query(Tenant).filter(Tenant.unique_id == tenant_id).first()

def update_tenant(db: Session, tenant_id: int, name: str, lastname: str, email: str, duedate: str, paiddate: str):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if tenant:
        tenant.name = name
        tenant.lastname = lastname
        tenant.email = email
        tenant.duedate = duedate
        tenant.paiddate = paiddate
        db.commit()

def delete_tenant(db: Session, tenant_id: int):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if tenant:
        db.delete(tenant)
        db.commit()




#CRUD OPERATION FOR BILLER START HERE