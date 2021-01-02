//select element fro the dom open, close and sidebarnav div

let closeBtn = document.querySelector('.fa-times');
let openBtn = document.querySelector('.fa-bars');
let sideBarMenu = document.querySelector('#sideBarNav')


// Add event listener to open icon
openBtn.addEventListener('click', ()=>{
sideBarMenu.style.width ="250px";
})

// Add event listener to close icon
closeBtn.addEventListener('click', ()=>{
  sideBarMenu.style.width ="0";
})