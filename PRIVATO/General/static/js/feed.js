
function rellenarAvatar(lista_colores){
    for (let i = 1; i <= 121; i++) {
        
        const id_box_avatar = `box${i}`;
        const box_avatar = document.getElementById(id_box_avatar) 

        color = 'background-color:' + lista_colores[i - 1] + ';'
        box_avatar.setAttribute("style", color)
        
    }
}


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

document.addEventListener('DOMContentLoaded', function() {
    var divEnviar = document.getElementById('avatar-container');
    var formulario = document.getElementById('form-perfil');
  
    divEnviar.addEventListener('click', function() {
      formulario.submit(); 
    });
  });




const modal = document.getElementById('modal');
const openModal = document.getElementById('noti_btn');
const closeModal = document.getElementsByClassName('close')[0];

openModal.onclick = function() {
  modal.style.display = 'block';
  console.log("se abrio el modal")
}

closeModal.onclick = function() {
  modal.style.display = 'none';
}

window.onclick = function(event) {
  if (event.target === modal) {
    modal.style.display = 'none';
  }
}

document.addEventListener('keydown', function(event) {
  if (event.key === 'Escape') {
    modal.style.display = 'none';
  }
});

