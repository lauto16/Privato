const avatar_container = document.getElementById('avatar-container');
const form_avatar = document.getElementById('form_avatar');
const input = document.getElementById("textarea-post")
const contadorChars = document.getElementById("contador-caracteres")
const title = document.getElementById("title") 


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


function cambiar_imagen(id, src1, src2) {
  const img = document.getElementById(id);

  const estaLikeado = img.dataset.likeado === "true";

  if (estaLikeado) {
    img.setAttribute("src", src2);
    img.dataset.likeado = "false"; 
  } 

  else {
    img.setAttribute("src", src1);
    img.dataset.likeado = "true"; 
  }
}


function asignarEventListeners(id_posts){

  for (let i = 0; i < id_posts.length; i++) {

    let id_boton_like = "boton_like-" + id_posts[i].toString();
    let id_imagen_like = "imagen_like-" + id_posts[i].toString();

    const boton_like = document.getElementById(id_boton_like);
    
    boton_like.addEventListener('click', function(){
      cambiar_imagen(id=id_imagen_like, src1=input_like.value, src2=input_like_vacio.value)
    });
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


function countChars(element){
  chars = element.value
  return [chars.length, chars]
}


title.addEventListener('input', function(event) {

  let lista_vars = countChars(title)
  cantidad_chars = lista_vars[0]
  chars = lista_vars[1]

  if (cantidad_chars > 80){
    let sinSobrante = chars.substring(0,80); 
    title.value = sinSobrante
  }

});


input.addEventListener('input', function(event) {

  let lista_vars = countChars(input)
  cantidad_chars = lista_vars[0]
  chars = lista_vars[1]

  if (cantidad_chars <= 950){
    let string_limit_chars = cantidad_chars.toString() + "/950"

    let componenteA = parseInt(cantidad_chars / (950/255))
    let componenteB = parseInt(cantidad_chars / (950/3))
    let componenteC = componenteB
  
    let color_rgb = `(${componenteA},${componenteB},${componenteC})`
    let color_hex = rgbStringToHex(color_rgb) 
    propiedad_color = "color:" + color_hex + ";"
  
    contadorChars.textContent = string_limit_chars
    contadorChars.setAttribute("style", propiedad_color)
  }

  else{
    contadorChars.textContent = "950/950"
    let sinSobrante = chars.substring(0,950); 
    input.value = sinSobrante
  }

});


document.addEventListener('DOMContentLoaded', function() {
  var divEnviar = document.getElementById('avatar-container');
  var formulario = document.getElementById('form-perfil');

  divEnviar.addEventListener('click', function() {
    formulario.submit(); 
  });
});


avatar_container.addEventListener('click', function() {
  form_avatar.submit();
});
