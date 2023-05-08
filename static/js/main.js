const menuToggle = document.querySelector('.menuToggle')
const navigation = document.querySelector('.navigation')
const menuToggleIcon = document.querySelector('.menuToggle-icon')
const colMenu = document.querySelector('.col-menu')
const colContainer = document.querySelector('.col-container')
const container = document.querySelector('.container')

menuToggle.onclick = function() {
    navigation.classList.toggle('open')
    if (navigation.classList.contains('open')) {
        menuToggleIcon.classList.replace('ti-menu','ti-close')
        colMenu.classList.replace('col-6','col-15')
        colContainer.classList.replace('col-94','col-85')
        container.style.left = "286px"
    }
    else {
        menuToggleIcon.classList.replace('ti-close','ti-menu')
        colMenu.classList.replace('col-15','col-6')
        colContainer.classList.replace('col-85','col-94')
        container.style.left = "114px"
    }
}

const $ = document.querySelector.bind(document)
const $$ = document.querySelectorAll.bind(document)

const menuItems = $$('.menuList-item')

// function resetActivate(){
//     menuItems.forEach((menuItem,index) => {
//         $('.menuList-item.active').classList.remove('active')
//     })
// }

menuItems.forEach((menuItem,index) => {
    menuItem.onclick = function () {
        $('.menuList-item.active').classList.remove('active')
        // resetActivate()
        this.classList.add('active')
    }
})