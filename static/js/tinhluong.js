const modalBtn = $('.close-btn')
const modal = $('.modal')
const modalContainer = $('.modal-container')
const modalOpenBtns = $$('.employee-show-info')

function showModal () {
    modal.classList.add('open')
}

function hideModal () {
    modal.classList.remove('open')
}

for(const modalOpenBtn of modalOpenBtns) {
    modalOpenBtn.addEventListener('click', showModal)
    const employeeId = modalOpenBtn.id
    modalOpenBtn.addEventListener('click', function(){
        const einfor_string = document.getElementById("einfor_strformat_"+employeeId).textContent
        
        // console.log(einfor_string)
        const infors = einfor_string.split('@')
        
        document.getElementById("emodal_name").textContent = infors[0]
        document.getElementById("emodal_birthday").textContent = infors[1]
        document.getElementById("emodal_phone").textContent = infors[2]
        document.getElementById("emodal_workday").textContent = infors[3]
        document.getElementById("emodal_salary").textContent = infors[4]
        document.getElementById("emodal_avatar").style.background = `url(/media/${infors[5]})  top center / cover no-repeat`
        // console.log(document.getElementById("emodal_avatar").style.background)
    })
}

modalBtn.addEventListener('click', hideModal)
modal.addEventListener('click',hideModal)

modalContainer.addEventListener('click', function(event){
    event.stopPropagation()
})