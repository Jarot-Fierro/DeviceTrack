$(document).ready(function () {
        $('.toggle-status-btn').on('click', function (e) {
            e.preventDefault(); // Detenemos la navegación por ahora

            const url = $(this).attr('href'); // Obtenemos la URL a donde queremos ir

            swal({
                title: "¿Estás seguro?",
                text: "Se cambiará el estado de esta marca",
                type: "warning",
                buttons: {
                    cancel: {
                        visible: true,
                        text: "No, cancelar",
                        className: "btn btn-danger",
                    },
                    confirm: {
                        text: "Sí, continuar",
                        className: "btn btn-success",
                    },
                },
            }).then((confirmed) => {
                if (confirmed) {
                    window.location.href = url; // Redirige si confirma
                } else {
                    swal("Acción cancelada", "No hubieron cambios", {
                        icon: "info",
                        buttons: { confirm: { className: "btn btn-primary" } }
                    });
                }
            });
        });
    });