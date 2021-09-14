from passlib.hash import pbkdf2_sha256

user = pbkdf2_sha256.encrypt('admin')
print(int(4.5))


print(pbkdf2_sha256.verify('admin', '$pbkdf2-sha256$29000$iNH6XwvhvLdWqtWak7L2ng$0pkIIsv0GlOGncRmCDweJyRpZ0aoM8feeDmtIb84lyw'))


# # $pbkdf2-sha256$29000$u7f2njPGOEcoxbj3HmOMsQ$w2Z2iEimuVKi2tO284PKf3/5691uR7rKehYvF71slNg
#
# from functools import wraps
# def logged(func):
#     @wraps(func)
#     def with_logging(*args, **kwargs):
#         print(func.__+ " was called")
#         return func(*args, **kwargs)
#     return with_logging
#
# @logged
# def f(x):
#    """does some math"""
#    return x + x * x
#
# print(f.__name__)  # prints 'f'
# print(f.__doc__)   # prints 'does some math'