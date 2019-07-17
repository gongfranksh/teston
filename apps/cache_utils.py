from werkzeug.contrib.cache import SimpleCache

from apps.model1 import User

cache = SimpleCache()
def getUserById(userId):
    key = "user:"+str(userId)
    rv = cache.get(key)
    if rv is None:
        user = User.query.filter_by(id=userId).first()
        if user:
            rv = user
            cache.set(key, rv, timeout=5 * 60)
        return rv
    else:
        print("===============hit on==============="+str(userId))
        return  rv