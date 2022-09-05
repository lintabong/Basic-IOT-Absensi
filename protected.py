from flask import session, redirect, url_for, request
import functools


def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)

    return secure_function
