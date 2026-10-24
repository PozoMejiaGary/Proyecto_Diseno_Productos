document.addEventListener('DOMContentLoaded', () => {
    const acceso = document.getElementById('acceso');
    const registro = document.getElementById('registro');
    const btnIrRegistro = document.getElementById('btn-login');
    const btnIrLogin = document.getElementById('btn-registro');

    //Cambio al Registro
    btnIrRegistro.addEventListener('click', (e) => {
        e.preventDefault();
        acceso.classList.remove('activo');
        registro.classList.add('activo');
    });

    //Cambio al Login
    btnIrLogin.addEventListener('click', (e) => {
        e.preventDefault();
        registro.classList.remove('activo');
        acceso.classList.add('activo');
    });
});