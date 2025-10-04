# Database Helpers

from sqlalchemy import inspect
from datetime import datetime


def object_as_dict(obj):
    """Convert SQLAlchemy model instance to dictionary"""
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def serialize_model(obj, exclude=None, include_relationships=False):
    """
    Serialize SQLAlchemy model to dictionary
    
    Args:
        obj: SQLAlchemy model instance
        exclude: List of fields to exclude
        include_relationships: Whether to include relationship data
    """
    if exclude is None:
        exclude = []
    
    data = {}
    
    # Get all columns
    for column in inspect(obj).mapper.column_attrs:
        if column.key in exclude:
            continue
        
        value = getattr(obj, column.key)
        
        # Handle datetime/date objects
        if isinstance(value, datetime):
            data[column.key] = value.isoformat()
        else:
            data[column.key] = value
    
    # Include relationships if requested
    if include_relationships:
        for relationship in inspect(obj).mapper.relationships:
            if relationship.key in exclude:
                continue
            
            value = getattr(obj, relationship.key)
            
            # Handle collections (one-to-many, many-to-many)
            if hasattr(value, '__iter__'):
                data[relationship.key] = [
                    serialize_model(item, exclude, False) for item in value
                ]
            # Handle single objects (many-to-one)
            elif value is not None:
                data[relationship.key] = serialize_model(value, exclude, False)
    
    return data


def bulk_insert(db, model_class, data_list):
    """
    Bulk insert multiple records
    
    Args:
        db: SQLAlchemy database instance
        model_class: Model class to insert
        data_list: List of dictionaries with model data
    """
    try:
        instances = [model_class(**data) for data in data_list]
        db.session.bulk_save_objects(instances)
        db.session.commit()
        return True, len(instances)
    except Exception as e:
        db.session.rollback()
        return False, str(e)


def get_or_create(db, model_class, defaults=None, **kwargs):
    """
    Get existing record or create new one
    
    Args:
        db: SQLAlchemy database instance
        model_class: Model class
        defaults: Dictionary of default values for new instance
        **kwargs: Filter criteria
    """
    instance = db.session.query(model_class).filter_by(**kwargs).first()
    
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items())
        if defaults:
            params.update(defaults)
        instance = model_class(**params)
        db.session.add(instance)
        db.session.commit()
        return instance, True


def update_model(obj, data, exclude=None):
    """
    Update model instance with data dictionary
    
    Args:
        obj: SQLAlchemy model instance
        data: Dictionary with new values
        exclude: List of fields to exclude from update
    """
    if exclude is None:
        exclude = ['id', 'created_at']
    
    for key, value in data.items():
        if key not in exclude and hasattr(obj, key):
            setattr(obj, key, value)
    
    return obj


def soft_delete(obj, db):
    """
    Soft delete a record by setting is_active to False
    
    Args:
        obj: SQLAlchemy model instance
        db: SQLAlchemy database instance
    """
    if hasattr(obj, 'is_active'):
        obj.is_active = False
        obj.updated_at = datetime.utcnow()
        db.session.commit()
        return True
    return False


def restore_deleted(obj, db):
    """
    Restore a soft-deleted record
    
    Args:
        obj: SQLAlchemy model instance
        db: SQLAlchemy database instance
    """
    if hasattr(obj, 'is_active'):
        obj.is_active = True
        obj.updated_at = datetime.utcnow()
        db.session.commit()
        return True
    return False


def count_records(db, model_class, **filters):
    """
    Count records matching filters
    
    Args:
        db: SQLAlchemy database instance
        model_class: Model class
        **filters: Filter criteria
    """
    query = db.session.query(model_class)
    if filters:
        query = query.filter_by(**filters)
    return query.count()


def exists(db, model_class, **filters):
    """
    Check if record exists
    
    Args:
        db: SQLAlchemy database instance
        model_class: Model class
        **filters: Filter criteria
    """
    return db.session.query(
        db.session.query(model_class).filter_by(**filters).exists()
    ).scalar()


def get_or_404(db, model_class, id):
    """
    Get record by ID or return 404 error
    
    Args:
        db: SQLAlchemy database instance
        model_class: Model class
        id: Record ID
    """
    from flask import abort
    obj = db.session.query(model_class).get(id)
    if obj is None:
        abort(404)
    return obj


def paginate_results(query, page=1, per_page=10):
    """
    Paginate query results
    
    Args:
        query: SQLAlchemy query object
        page: Page number (starting from 1)
        per_page: Items per page
    """
    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return {
        'items': pagination.items,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page,
        'per_page': pagination.per_page,
        'has_prev': pagination.has_prev,
        'has_next': pagination.has_next,
        'prev_num': pagination.prev_num,
        'next_num': pagination.next_num
    }


def search_records(db, model_class, search_term, search_fields):
    """
    Search records in multiple fields
    
    Args:
        db: SQLAlchemy database instance
        model_class: Model class
        search_term: Search term
        search_fields: List of field names to search in
    """
    from sqlalchemy import or_
    
    if not search_term:
        return db.session.query(model_class)
    
    filters = []
    for field in search_fields:
        if hasattr(model_class, field):
            filters.append(
                getattr(model_class, field).ilike(f'%{search_term}%')
            )
    
    if filters:
        return db.session.query(model_class).filter(or_(*filters))
    
    return db.session.query(model_class)
