const avatar_container = document.getElementById('avatar-container');
const form_avatar = document.getElementById('form_avatar');
const contadorChars = document.getElementById("contador-caracteres")
const title = document.getElementById("id_title")
const input = document.getElementById("id_content")
const boton_crear_post = document.getElementById('save-post-btn')


function extraerIdPost(id_comentario) {
  var id_post = id_comentario.slice(id_comentario.lastIndexOf('-') + 1);
  return id_post
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
        console.log(data)
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
      console.log(error)
      errorHandler(error = "Error al subir el post, intentalo de nuevo")

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


function rgbStringToHex(rgbString) {

  let [red, green, blue] = rgbString.match(/\d+/g);

  red = parseInt(red);
  green = parseInt(green);
  blue = parseInt(blue);

  let redHex = red.toString(16).padStart(2, '0');
  let greenHex = green.toString(16).padStart(2, '0');
  let blueHex = blue.toString(16).padStart(2, '0');

  let hexColor = `#${redHex}${greenHex}${blueHex}`;

  return hexColor

}


function countChars(element) {
  chars = element.value
  return [chars.length, chars]
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

    let color_rgb = `(${componenteA},${componenteB},${componenteC})`
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


document.addEventListener('DOMContentLoaded', function () {
  var divEnviar = document.getElementById('avatar-container');
  var formulario = document.getElementById('form-perfil');

  divEnviar.addEventListener('click', function () {
    formulario.submit();
  });

});


boton_crear_post.addEventListener('click', function (event) {
  event.preventDefault()
  crearPost()
});


avatar_container.addEventListener('click', function () {
  form_avatar.submit();
});


function comentarEventsListeners() {
  var botones = document.querySelectorAll('.boton-comentario');

  botones.forEach(function (boton) {
    boton.addEventListener('click', verComentarios);
  });

}


