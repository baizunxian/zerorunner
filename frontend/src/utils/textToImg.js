export const textToImg = (str) => {
  let name = str.substring(0, 1), fsize = 70;
  if (new RegExp("[A-Za-z]+").test(name)) {
    name = name.toUpperCase()
  }
  let fontSize = 62;
  let fontWeight = "bold";
  let canvas = document.createElement("canvas", {display: 'none', id: 'canvas_user_img'});
  canvas.width = 120;
  canvas.height = 120;
  let context = canvas.getContext("2d");
  context.fillStyle = getBG();
  context.fillRect(0, 0, canvas.width, canvas.height);
  context.fillStyle = "#FFF";
  context.font = fontWeight + " " + fsize + "px sans-serif";
  context.textAlign = "center";
  context.textBaseline = "middle";
  context.fillText(name, fontSize, fontSize);
  return canvas.toDataURL("image/png", 1)
}

export const getBG = () => {
  let bgArray = ["#1abc9c", "#2ecc71", "#3498db", "#9b59b6", "#34495e",
    "#16a085", "#27ae60", "#2980b9", "#8e44ad", "#2c3e50", "#f1c40f",
    "#e67e22", "#e74c3c", "#eca0f1", "#95a5a6", "#f39c12", "#d35400",
    "#c0392b", "#bdc3c7", "#7f8c8d"];
  return bgArray[Math.floor(Math.random() * bgArray.length)];
};
