from django.contrib.auth.decorators import login_required, user_passes_test

def organizador_required(view_func):
    return login_required(
        user_passes_test(lambda u: u.perfil in ('organizador', 'admin'))(view_func)
    )

def admin_required(view_func):
    return login_required(
        user_passes_test(lambda u: u.perfil == 'admin')(view_func)
    )
