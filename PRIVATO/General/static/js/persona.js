const avatar_container = document.getElementById('avatar-container');
const form_avatar = document.getElementById('form_avatar');
const input = document.getElementById("textarea-post")
const contadorChars = document.getElementById("contador-caracteres")
const title = document.getElementById("title") 
const input_like = document.getElementById("url-imagen-like")
const input_like_vacio = document.getElementById("url-imagen-like-vacio")
const boton_seguir = document.getElementById("agregar-btn")


function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}


async function errorHandler(error){
  const div_errores = document.getElementById("div-errores")
  const p_errores = document.getElementById("p-errores")

  if (error){

    div_errores.setAttribute('style', 'display:inline-block')
    p_errores.setAttribute('style', 'display:inline-block')
    p_errores.textContent = error

    await sleep(3000)

    $( "#div-errores" ).fadeOut( "slow", function() {
      div_errores.setAttribute('style', 'display:none')
      p_errores.setAttribute('style', 'display:none')
    });


  }
  else{
    div_errores.setAttribute('style', 'display:none')
    p_errores.setAttribute('style', 'display:none')
  }
}


function rellenarAvatar(lista_colores){
  for (let i = 1; i <= 121; i++) {
      
      const id_box_avatar = `box${i}`;
      const box_avatar = document.getElementById(id_box_avatar) 

      color = 'background-color:' + lista_colores[i - 1] + ';'
      box_avatar.setAttribute("style", color)
      
  }
}


function colorBoton(id, color){
  const boton = document.getElementById(id)
  color = 'background-color:' + color + ';'
  boton.setAttribute("style", color)
}