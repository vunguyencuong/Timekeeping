const employeeContainerItems = $$('.employee-container-item')
const containerContents = $$('.employee-container-content-wrapped')

employeeContainerItems.forEach(function(employeeContainerItem, index){
    const containerContent = containerContents[index]
    employeeContainerItem.onclick = function(){
        $('.employee-container-item.active').classList.remove('active')
        $('.employee-container-content-wrapped.active').classList.remove('active')
        this.classList.add('active')
        containerContent.classList.add('active')
    }
})

// dong mo modal
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
 
        const infors = einfor_string.split('@')
        
        document.getElementById("emodal_name").textContent = infors[0]
        document.getElementById("emodal_gender").textContent = infors[1]
        document.getElementById("emodal_birthday").textContent = infors[2]
        document.getElementById("emodal_homeTown").textContent = infors[3]
        document.getElementById("emodal_phone").textContent = infors[4]
        document.getElementById("emodal_education").textContent = infors[5]
        document.getElementById("emodal_avatar").style.background = `url(/media/${infors[6]})  top center / cover no-repeat`
        // console.log(`url(${infors[6]})  top center / cover no-repeat;`)
    })
    
}

modalBtn.addEventListener('click', hideModal)
modal.addEventListener('click',hideModal)

modalContainer.addEventListener('click', function(event){
    event.stopPropagation()
})

const deleteBtns = $$('.employee-delete')
for(const deleteBtn of deleteBtns) {
    deleteBtn.onclick =  async function(){
        
        const card= document.getElementById("employee_infor_"+deleteBtn.id);
        card.remove();
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        let res = await fetch(`/employee/?employeeId=${deleteBtn.id}`, {
            method: "DELETE",
            headers: {'X-CSRFToken': csrfToken,'Content-Type': 'application/json'}
            })
        }
}