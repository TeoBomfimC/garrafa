document.addEventListener("DOMContentLoaded", function () {
    const tel = document.querySelector("#id_telefone");
    if (tel) {
        Inputmask("(99) 99999-9999").mask(tel);
    }

    const email = document.querySelector("#id_email");
    if (email) {
        email.addEventListener("input", function () {
            const ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value);
            email.style.borderColor = ok ? "#1e8f41" : "#cc0000";
        });
    }

    const senha1 = document.querySelector("#id_password1");
    const senha2 = document.querySelector("#id_password2");

    if (senha1) {
        senha1.addEventListener("input", function () {
            const forte =
                senha1.value.length >= 8 &&
                /[A-Z]/.test(senha1.value) &&
                /[a-z]/.test(senha1.value) &&
                /[0-9]/.test(senha1.value) &&
                /[^A-Za-z0-9]/.test(senha1.value);

            senha1.style.borderColor = forte ? "#1e8f41" : "#cc0000";
        });
    }

    if (senha2) {
        senha2.addEventListener("input", function () {
            const igual = senha1.value === senha2.value;
            senha2.style.borderColor = igual ? "#1e8f41" : "#cc0000";
        });
    }
});
