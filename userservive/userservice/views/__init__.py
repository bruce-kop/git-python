from .users import users
from .verifycode import verifycode
from .auth import auth
from .logout import user_logout
blueprints = [verifycode, users, auth, user_logout]