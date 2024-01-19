const avatar_container = document.getElementById('avatar-container');
const form_avatar = document.getElementById('form_avatar');
const input = document.getElementById("textarea-post")
const contadorChars = document.getElementById("contador-caracteres")
const title = document.getElementById("title")
const input_like = document.getElementById("url-imagen-like")
const input_like_vacio = document.getElementById("url-imagen-like-vacio")
const boton_seguir = document.getElementById("agregar-btn")
const modal = document.getElementById('modal-comentarios');
const closeModal = document.getElementById('close-comentarios');


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


function cargarComentarios(data) {

  if (data.esDiccionario == true) {

    var lista_comentarios = data.comentarios

    Object.keys(lista_comentarios).forEach(function (clave) {

      var usuario = lista_comentarios[clave][0];
      var contenido = lista_comentarios[clave][1];
      var fecha = lista_comentarios[clave][2];

      html_comentario = `<div class="comentario">
        <p class="usuario-comentario">
          <strong>` + usuario + `</strong>
        </p>
        <p class="fecha-comentario">` + fecha + `</p>
        <p class="contenido-comentario">` + contenido + `</p>
      </div>`

      $("#container-comentario").prepend(html_comentario);

    });
  }
  else {
    p_no_coments = document.getElementById('no-coments')
    p_no_coments.textContent = "No se encontraron comentarios en el post"
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


function rellenarAvatar(lista_colores) {
  for (let i = 1; i <= 121; i++) {

    const id_box_avatar = `box${i}`;
    const box_avatar = document.getElementById(id_box_avatar)

    color = 'background-color:' + lista_colores[i - 1] + ';'
    box_avatar.setAttribute("style", color)

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