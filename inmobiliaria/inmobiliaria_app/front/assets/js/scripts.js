$('#cerrar-sesion').click(() => {
    localStorage.clear();
    window.location.href = 'logout';
});

$('#delete-user').click(() => {
    localStorage.clear();
    window.location.href = 'delete_user/';
    // window.location.href = 'logout/';
});
