from ..decision import DecisionAuthority


class EnforcementAuthority:
    @classmethod
    def authorize(cls, request):
        return DecisionAuthority.authorize(request)
    
    @classmethod
    def is_permitted(cls, request):
        return DecisionAuthority.is_permitted(request)