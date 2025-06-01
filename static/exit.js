const pageSite = "/login/";
document.addEventListener('DOMContentLoaded', function() {
    const buttonExit = document.getElementById("button-exit");
    
    if (buttonExit) {
        buttonExit.addEventListener('click', function() {
            if (confirm("Вы уверены, что хотите выйти?")) {
                window.location.href = pageSite;
            }
        });
    }
});
