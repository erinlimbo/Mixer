let sideBar = document.querySelector('#sidebar')
document.querySelector('#openSideBar').addEventListener('click', function(){
  openSide()
})




const openSide = () => {
  if (sideBar.style.width == "100px") {
    sideBar.style.width = "0px"
  } else {
    sideBar.style.width = "100px";
  }
}
