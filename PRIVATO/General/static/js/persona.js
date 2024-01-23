const input = document.getElementById("textarea-post")
const contadorChars = document.getElementById("contador-caracteres")
const title = document.getElementById("title")
const boton_seguir = document.getElementById("agregar-btn")
const modal = document.getElementById("modal-comentarios");
const closeModal = document.getElementById("close-comentarios");
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

        if (modal.style.display == 'block') {
          modal.style.display = 'none'
        }

        else {
          modal.style.display = 'block'
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
      blurBackground(action = "unblur")
      modal.style.display = 'none'
      errorHandler(error = "No se pudo enviar el comentario")
    });

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

        if (modal.style.display == 'block') {
          modal.style.display = 'none'
        }

        else {
          modal.style.display = 'block'
          blurBackground(action = "unblur")
        }

      }
    })
    .catch(error => {
      console.log(error)
    });

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


function colorBoton(id, color) {
  const boton = document.getElementById(id)
  color = 'background-color:' + color + ';'
  boton.setAttribute("style", color)
}


function comentarEventsListeners() {
  var botones = document.querySelectorAll('.boton-comentario');

  botones.forEach(function (boton) {
    boton.addEventListener('click', verComentarios);
  });

}


boton_enviar_comentario.addEventListener('click', enviarComentario)


closeModal.onclick = function () {
  modal.style.display = 'none';
  blurBackground(action = "unblur")
}


window.onclick = function (event) {
  if (event.target === modal) {
    modal.style.display = 'none';
    blurBackground(action = "unblur")
  }
}


document.addEventListener('keydown', function (event) {
  if (event.key === 'Escape') {
    modal.style.display = 'none';
    blurBackground(action = "unblur")
  }
});
