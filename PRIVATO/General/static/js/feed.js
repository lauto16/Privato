const modalComentarios = document.getElementById("modal-comentarios");
const closeModalComentarios = document.getElementById("close-comentarios");
const modal = document.getElementById('modal');
const openModal = document.getElementById('noti_btn');
const closeModal = document.getElementById('close-notis')
const boton_cancelar_cerrar_sesion = document.getElementById('boton-cancelar-cerrar-sesion')
const boton_cerrar_sesion = document.getElementById('salir-nav-der')
const modal_cerrar_sesion = document.getElementById('modal-cerrar-sesion')
const enviarPerfil = document.getElementById('avatar-imagen');
const form_perfil = document.getElementById('form-perfil');
const boton_enviar_comentario = document.getElementById("boton-enviar-comentario")




async function blurBackground(action) {
  container = document.getElementById('container')

  if (action == "blur") {
    for (let i = 0; i < 100; i++) {
      await sleep(0.05)
      property_blur = 'filter: blur(' + parseInt(i / 10).toString() + 'px);'
      container.setAttribute('style', property_blur);

    }
  }

  else if (action == "unblur") {
    container.setAttribute('style', 'filter: blur("0px")')
  }
}


function verComentarios(event) {

  event.preventDefault()

  var id_comentario = (event.target.id.toString())

  var id_post = id_comentario.slice((id_comentario.lastIndexOf('-')) + 1);

  var form = new FormData(document.getElementById('form-comentarios'))

  form.append("id_post", id_post);

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

        cargarComentarios(data)

        blurBackground(action = "blur")

        if (modalComentarios.style.display == 'block') {
          modalComentarios.style.display = 'none'
        }

        else {
          modalComentarios.style.display = 'block'
          blurBackground(action = "unblur")
        }

      }
    })
    .catch(error => {
      console.log(error)
    });

}


function enviarComentario(event) {

  event.preventDefault()

  var form = new FormData(document.getElementById('form-enviar-comentario'))

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

        agregarComentario(data)

      }
    })
    .catch(error => {
      console.log(error)
      blurBackground(action = "unblur")
      modalComentarios.style.display = 'none'
      errorHandler(error = "No se pudo enviar el comentario")
    });

}


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

closeModalComentarios.onclick = function () {
  modalComentarios.style.display = 'none';
  blurBackground(action = "unblur")
}

function modalCerrarSesion(event) {
  event.preventDefault()
  modal_cerrar_sesion.style.display = "block"
}


function cerrarModal(event) {
  event.preventDefault()
  modal_cerrar_sesion.style.display = 'none';
}


enviarPerfil.addEventListener('click', function () {
  form_perfil.submit();
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


function comentarEventsListeners() {
  var botones = document.querySelectorAll('.boton-comentario');

  botones.forEach(function (boton) {
    boton.addEventListener('click', verComentarios);
  });

}


boton_enviar_comentario.addEventListener('click', enviarComentario)


boton_cancelar_cerrar_sesion.addEventListener('click', cerrarModal)


boton_cerrar_sesion.addEventListener('click', modalCerrarSesion)


document.addEventListener('keydown', function (event) {
  if (event.key === 'Escape') {
    modalComentarios.style.display = 'none';
    blurBackground(action = "unblur")
    $("#container-comentario").innerHTML = ""
  }
});

