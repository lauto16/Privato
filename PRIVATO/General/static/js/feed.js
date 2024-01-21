const modal = document.getElementById('modal');
const openModal = document.getElementById('noti_btn');
const closeModal = document.getElementsByClassName('close')[0];
const boton_cancelar_cerrar_sesion = document.getElementById('boton-cancelar-cerrar-sesion')
const boton_cerrar_sesion = document.getElementById('salir-nav-der')
const modal_cerrar_sesion = document.getElementById('modal-cerrar-sesion')


function rellenarAvatar(lista_colores) {
  for (let i = 1; i <= 121; i++) {

    const id_box_avatar = `box${i}`;
    const box_avatar = document.getElementById(id_box_avatar)

    var color = 'background-color:' + lista_colores[i - 1] + ';'
    box_avatar.setAttribute("style", color)

  }
}


function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}


async function errorHandler(error) {
  const div_errores = document.getElementById("div-errores")
  const p_errores = document.getElementById("p-errores")

  if (error) {

    div_errores.setAttribute('style', 'display:inline-block')
    p_errores.setAttribute('style', 'display:inline-block')
    p_errores.textContent = error

    await sleep(3000)

    $("#div-errores").fadeOut("slow", function () {
      div_errores.setAttribute('style', 'display:none')
      p_errores.setAttribute('style', 'display:none')
    });


  }
  else {
    div_errores.setAttribute('style', 'display:none')
    p_errores.setAttribute('style', 'display:none')
  }




}


function getCookie(name) {

  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


function borrarNotificacion(id_noti) {
  var id_noti_completo = 'form_noti-' + id_noti.toString()
  noti = document.getElementById(id_noti_completo)
  noti.remove()

  var notificaciones_activas = document.querySelectorAll('.container-noti');
  if (notificaciones_activas.length == 0) {
    document.getElementById('no-notis').textContent = "No hay notificaciones recientes"

  }


}


function aceptarNotificacion(event) {

  event.preventDefault()

  var id_boton_noti = (event.target.id.toString())

  var id_noti = id_boton_noti.slice((id_boton_noti.lastIndexOf('-')) + 1);

  var id_form = 'form_noti-' + id_noti

  var form = new FormData(document.getElementById(id_form))

  form.append("id_noti", id_noti);
  form.append('action_noti', 'aceptar_noti');

  fetch('./', {

    method: "POST",
    body: form,
    headers: {
      "X-CSRFToken": getCookie('csrftoken'),
    },
  })

    .then(response => response.json())
    .then(data => {

      if (data) {
        if (data.success) {
          borrarNotificacion(id_noti = data.id_noti)
        }
        else {
          errorHandler("Se ha producido un error al aceptar la solicitud")
        }
      }
    })
    .catch(error => {
      errorHandler("Se ha producido un error")
    });

}


function denegarNotificacion(event) {

  event.preventDefault()

  var id_boton_noti = (event.target.id.toString())

  var id_noti = id_boton_noti.slice((id_boton_noti.lastIndexOf('-')) + 1);

  var id_form = 'form_noti-' + id_noti

  var form = new FormData(document.getElementById(id_form))

  form.append("id_noti", id_noti);
  form.append('action_noti', 'denegar_noti');

  fetch('./', {

    method: "POST",
    body: form,
    headers: {
      "X-CSRFToken": getCookie('csrftoken'),
    },
  })

    .then(response => response.json())
    .then(data => {

      if (data) {
        if (data.success) {
          borrarNotificacion(id_noti = data.id_noti)
        }
        else {
          errorHandler("Se ha producido un error al denegar la solicitud")
        }
      }
    })
    .catch(error => {
      errorHandler("Se ha producido un error")
    });

}


function notificacionesAddEvent() {
  var aceptar = document.querySelectorAll('.aceptar-noti');
  var denegar = document.querySelectorAll('.denegar-noti');

  aceptar.forEach(function (boton_aceptar) {
    boton_aceptar.addEventListener('click', aceptarNotificacion);
  });

  denegar.forEach(function (boton_denegar) {
    boton_denegar.addEventListener('click', denegarNotificacion);
  });

}


function modalCerrarSesion(event) {
  event.preventDefault()
  modal_cerrar_sesion.style.display = "block"
}


function cerrarModal(event) {
  event.preventDefault()
  modal_cerrar_sesion.style.display = 'none';
}


document.addEventListener('DOMContentLoaded', function () {
  var divEnviar = document.getElementById('avatar-container');
  var formulario = document.getElementById('form-perfil');

  divEnviar.addEventListener('click', function () {
    formulario.submit();
  });
});


openModal.onclick = function () {
  modal.style.display = 'block';
}


closeModal.onclick = function () {
  modal.style.display = 'none';
  modal_cerrar_sesion.style.display = 'none';
}


window.onclick = function (event) {
  if (event.target === modal) {
    modal.style.display = 'none';
  }
}


document.addEventListener('keydown', function (event) {
  if (event.key === 'Escape') {
    modal.style.display = 'none';
  }
});


boton_cancelar_cerrar_sesion.addEventListener('click', cerrarModal)


boton_cerrar_sesion.addEventListener('click', modalCerrarSesion)