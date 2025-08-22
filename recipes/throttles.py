# recipes/throttles.py
from rest_framework.throttling import ScopedRateThrottle

class RecipesScopedThrottle(ScopedRateThrottle):
    """
    Use ScopedRateThrottle directly — we keep this class so we can import a named throttle.
    """
    pass
