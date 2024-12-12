from .base_model import PydanticBaseModel

class PagedQuery(PydanticBaseModel):
    """
    Base query class for paged requests
    """
    
    page: int = 1
    """Page number to request"""
    
    page_size: int = 10
    """Number of items per page"""

    order_by: str | None = None
    """Order by field"""

    filter: str | None = None
    """Filter term"""
