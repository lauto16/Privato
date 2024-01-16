const colorPickerInput = document.getElementById('favcolor');
colorPickerInput.value = "#038554"


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


function rellenarTodo(color){

  for (let i = 1; i <= 121; i++) {
    const boxId = `box${i}`;
    const boxElement = document.getElementById(boxId);
    style_color = 'background-color:' + color + ";"
    boxElement.setAttribute('style', style_color)

  }
}


function recoverColors(){

  valores_colores = []

  for (let i = 1; i <= 121; i++) {
    const gridBoxId = `box${i}`;
    const gridBox = document.getElementById(gridBoxId);
    valor_color = gridBox.style.backgroundColor;
    valor_color = rgbStringToHex(valor_color)
    valores_colores.push(valor_color)
  }
  return valores_colores
}


const boton_rellenar = document.getElementById("boton-rellenar")
boton_rellenar.addEventListener('click', function(){
  rellenarTodo(colorPickerInput.value)
});


const crear_avatar = document.getElementById("crear-avatar")
crear_avatar.addEventListener('click', function() {
  
  colors = recoverColors()
  
  for (let i = 0; i <= 120; i++) {

    const input_id = 'color_' + i.toString();
    const input = document.getElementById(input_id);
    input.value = colors[i];

  }
});


let selectedColor = colorPickerInput.value + ";"
colorPickerInput.addEventListener('input', function() {
  selectedColor = colorPickerInput.value;
  colorPickerInput.setAttribute('value', selectedColor);
});


for (let i = 1; i <= 121; i++) {
    const boxId = `box${i}`;
    const boxElement = document.getElementById(boxId);
  
    if (boxElement) {

      boxElement.addEventListener('click', function() {
        let color = "background-color:" + selectedColor
        boxElement.setAttribute("style", color)
      });

      boxElement.addEventListener('contextmenu', function(event) {
        event.preventDefault();
        let color = "background-color: #e9e7e7;"
        boxElement.setAttribute("style", color)

      });
  }
}