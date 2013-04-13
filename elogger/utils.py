
def xstr(obj):
    return str(obj) if obj else ''

def xtrim(obj):
    if not obj:
        return obj
    if isinstance(obj, basestring):
        return obj.strip()
    return obj