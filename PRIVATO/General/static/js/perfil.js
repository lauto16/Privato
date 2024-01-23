const form_avatar = document.getElementById('form_avatar');
const contadorChars = document.getElementById("contador-caracteres")
const title = document.getElementById("id_title")
const input = document.getElementById("id_content")
const boton_crear_post = document.getElementById('save-post-btn')
const modal = document.getElementById('modal-comentarios');
const closeModal = document.getElementById('close-comentarios');
const boton_enviar_comentario = document.getElementById("boton-enviar-comentario")
const enviarAvatar = document.getElementById('avatar-imagen');


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
      errorHandler(error = "No se pudo enviar el comentario")
    });

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


function crearPost() {

  var form = new FormData(document.getElementById('form-post'))

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
        title.value = ""
        input.value = ""
        contadorChars.textContent = "0/950"
        agregarNuevoPost(data)
      }
    })

    .catch(error => {
      errorHandler(error = "Error al subir el post, intentalo de nuevo")

    });

}


function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}


async function cerrarPost(id) {
  id = id.slice(1)
  post = document.getElementById(id)
  for (let i = post.offsetWidth; i > 0; i--) {
    await sleep(0.01)
    size_width = (i).toString() + 'px'
    post.style.width = size_width

  }
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


function rgbStringToHex(rgbString) {

  let [red, green, blue] = rgbString.match(/\d+/g);

  red = parseInt(red);
  green = parseInt(green);
  blue = parseInt(blue);

  let redHex = red.toString(16).padStart(2, '0');
  let greenHex = green.toString(16).padStart(2, '0');
  let blueHex = blue.toString(16).padStart(2, '0');

  let hexColor = `#${redHex}${greenHex}${blueHex} `;

  return hexColor

}


function countChars(element) {
  chars = element.value
  return [chars.length, chars]
}


function eliminarPost(event) {

  event.preventDefault()

  var id_boton_eliminar = (event.target.id.toString())

  var id_post = id_boton_eliminar.slice((id_boton_eliminar.lastIndexOf('-')) + 1);

  var form = new FormData(document.getElementById('form-eliminar-post'))

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

        eliminarHTMLPost(data)

      }
    })
    .catch(error => {
      console.log(error)
    });
}


function comentarEventsListeners() {
  var botones = document.querySelectorAll('.boton-comentario');

  botones.forEach(function (boton) {
    boton.addEventListener('click', verComentarios);

  });

}


function eliminarPostsEventsListeners() {
  var botones_eliminar = document.querySelectorAll('.boton-eliminar-post');

  botones_eliminar.forEach(function (boton) {

    boton.addEventListener('click', eliminarPost);

  });
}


title.addEventListener('input', function (event) {

  let lista_vars = countChars(title)
  cantidad_chars = lista_vars[0]
  chars = lista_vars[1]

  if (cantidad_chars > 80) {
    let sinSobrante = chars.substring(0, 80);
    title.value = sinSobrante
  }

});


input.addEventListener('input', function (event) {

  let lista_vars = countChars(input)
  cantidad_chars = lista_vars[0]
  chars = lista_vars[1]

  if (cantidad_chars <= 950) {
    let string_limit_chars = cantidad_chars.toString() + "/950"

    let componenteA = parseInt(cantidad_chars / (950 / 255))
    let componenteB = parseInt(cantidad_chars / (950 / 3))
    let componenteC = componenteB

    let color_rgb = `(${componenteA}, ${componenteB}, ${componenteC})`
    let color_hex = rgbStringToHex(color_rgb)
    propiedad_color = "color:" + color_hex + ";"

    contadorChars.textContent = string_limit_chars
    contadorChars.setAttribute("style", propiedad_color)
  }

  else {
    contadorChars.textContent = "950/950"
    let sinSobrante = chars.substring(0, 950);
    input.value = sinSobrante
  }

});


boton_crear_post.addEventListener('click', function (event) {
  event.preventDefault()
  crearPost()
});


enviarAvatar.addEventListener('click', function () {
  form_avatar.submit();
});


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
    $("#container-comentario").innerHTML = ""
  }
});

